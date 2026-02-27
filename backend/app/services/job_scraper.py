"""
Real-Time Job Scraping Service
================================
Fetches live job postings from multiple free & freemium APIs.

Sources (in priority order):
  1. JSearch via RapidAPI  - aggregates LinkedIn, Indeed, Glassdoor   (200 req/mo free)
  2. Adzuna                - 16 countries, millions of jobs            (1000 req/mo free)
  3. RemoteOK              - remote tech jobs                          (completely free)
  4. The Muse              - curated tech company jobs                 (completely free)

Anti-ban measures built-in:
  Per-domain minimum delay between requests + random jitter
  Rotating User-Agent pool (5 real browser UAs)
  Requests Retry adapter: auto-retry on 429/5xx with exponential back-off
  In-memory TTL cache (1 hour) to drastically reduce live API calls
  Parallel fetching capped at 2 concurrent workers
  Per-request timeout (10-15 s)
  Graceful degradation: one source failing will not kill the rest

Configuration (add to backend/.env):
  ADZUNA_APP_ID=your_adzuna_app_id
  ADZUNA_APP_KEY=your_adzuna_app_key
  RAPIDAPI_KEY=your_rapidapi_key
"""

import os
import time
import random
import hashlib
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# Per-domain throttle tracking
_last_request_at: Dict[str, float] = {}
_DOMAIN_DELAY: Dict[str, float] = {
    # Free / no-key sources
    "remoteok.com":             3.0,   # RSS-style endpoint, be gentle
    "themuse.com":              2.0,
    "remotive.com":             2.5,   # free API
    "www.arbeitnow.com":        2.0,   # European jobs, free
    "jobicy.com":               2.5,   # free remote-jobs API
    "weworkremotely.com":       3.5,   # RSS feed
    # Key-required sources
    "api.adzuna.com":           1.5,   # multi-country; delay shared across all countries
    "jsearch.p.rapidapi.com":   1.5,
    "www.reed.co.uk":           2.0,   # UK jobs
    "findwork.dev":             1.5,   # developer jobs worldwide
}
_DEFAULT_DELAY = 2.0

# In-memory results cache (1 hour TTL)
_cache: Dict[str, Tuple[List[Dict], float]] = {}
CACHE_TTL_SECONDS = 3600

# Rotating User-Agent pool
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

# --- Internal helpers ---------------------------------------------------------

def _make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=2,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({
        "User-Agent":      random.choice(_USER_AGENTS),
        "Accept":          "application/json, text/html;q=0.9, */*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection":      "keep-alive",
    })
    return session


def _throttle(domain: str) -> None:
    min_delay = _DOMAIN_DELAY.get(domain, _DEFAULT_DELAY)
    elapsed = time.monotonic() - _last_request_at.get(domain, 0.0)
    if elapsed < min_delay:
        time.sleep(min_delay - elapsed + random.uniform(0.2, 0.8))
    _last_request_at[domain] = time.monotonic()


def _cache_key(source: str, query: str, location: str) -> str:
    raw = f"{source}:{query.lower().strip()}:{location.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()


def _from_cache(key: str) -> Optional[List[Dict]]:
    if key in _cache:
        jobs, ts = _cache[key]
        if time.time() - ts < CACHE_TTL_SECONDS:
            return jobs
    return None


def _to_cache(key: str, jobs: List[Dict]) -> None:
    _cache[key] = (jobs, time.time())


def _job_id(title: str, company: str, source: str) -> str:
    raw = f"{title.lower().strip()}:{company.lower().strip()}:{source}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def _parse_date(val) -> datetime:
    if not val:
        return datetime.utcnow()
    try:
        if isinstance(val, (int, float)):
            return datetime.utcfromtimestamp(float(val))
        if isinstance(val, str):
            # RFC 2822 (RSS pubDate: "Mon, 24 Feb 2026 00:00:00 +0000")
            try:
                return parsedate_to_datetime(val).replace(tzinfo=None)
            except Exception:
                pass
            for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(val, fmt)
                except ValueError:
                    continue
    except Exception:
        pass
    return datetime.utcnow()


def _guess_level(title: str) -> str:
    t = title.lower()
    if any(w in t for w in ("staff", "principal", "director", "vp ", "head of", "chief")):
        return "Lead"
    if any(w in t for w in ("senior", "sr.", "sr ", "lead", " iii", " iv")):
        return "Senior"
    if any(w in t for w in ("junior", "jr.", "jr ", "associate", "entry", "intern")):
        return "Entry"
    return "Mid"


def _map_employment_type(emp_type: str) -> str:
    return {
        "FULLTIME": "Full-time", "PARTTIME": "Part-time",
        "CONTRACTOR": "Contract", "INTERN": "Internship", "TEMPORARY": "Contract",
    }.get((emp_type or "").upper(), "Full-time")


def _muse_level(short_name: str) -> str:
    return {"entry": "Entry", "mid": "Mid", "senior": "Senior", "management": "Lead"}.get(
        (short_name or "").lower(), "Mid")


def _source_from_url(url: str) -> str:
    u = (url or "").lower()
    for name, kw in [("LinkedIn","linkedin"),("Indeed","indeed"),("Glassdoor","glassdoor"),
                     ("ZipRecruiter","ziprecruiter"),("Monster","monster"),
                     ("Lever","lever"),("Greenhouse","greenhouse"),("Workday","workday")]:
        if kw in u:
            return name
    return "JSearch"


_SKILL_TOKENS = [
    "python","java","javascript","typescript","golang","rust","c++","c#",
    "react","vue","angular","node.js","next.js","django","flask","fastapi",
    "spring","rails","aws","azure","gcp","terraform","kubernetes","docker","linux",
    "sql","postgresql","mysql","mongodb","redis","elasticsearch",
    "machine learning","deep learning","nlp","tensorflow","pytorch","spark",
    "airflow","kafka","git","ci/cd","agile","scrum","jira","figma",
]


def _extract_skills(text: str) -> List[str]:
    if not text:
        return []
    t = text.lower()
    return [s.title() for s in _SKILL_TOKENS if s in t][:8]


# --- Source fetchers ----------------------------------------------------------

def _fetch_remoteok(query: str, limit: int = 30) -> List[Dict]:
    """RemoteOK public API. Completely free, no key needed."""
    domain = "remoteok.com"
    ck = _cache_key("remoteok", query, "remote")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        resp = session.get("https://remoteok.com/api", timeout=12)
        if resp.status_code != 200:
            logger.warning("RemoteOK HTTP %s", resp.status_code)
            return []

        data = resp.json()
        jobs_raw = [j for j in data if isinstance(j, dict) and j.get("position")]

        if query:
            q = query.lower()
            jobs_raw = [j for j in jobs_raw
                        if q in j.get("position","").lower()
                        or q in j.get("company","").lower()
                        or any(q in tag.lower() for tag in j.get("tags",[]))]

        jobs = []
        for j in jobs_raw[:limit]:
            jobs.append({
                "id":               _job_id(j.get("position",""), j.get("company",""), "RemoteOK"),
                "title":            j.get("position", "Unknown Position"),
                "company":          j.get("company", "Unknown Company"),
                "location":         j.get("location") or "Remote",
                "work_type":        "Remote",
                "job_type":         "Full-time",
                "experience_level": _guess_level(j.get("position","")),
                "description":      j.get("description", ""),
                "skills_required":  (j.get("tags") or [])[:10],
                "salary":           j.get("salary",""),
                "salary_min":       None,
                "salary_max":       None,
                "source":           "RemoteOK",
                "source_url":       j.get("url") or "https://remoteok.com",
                "company_logo":     j.get("company_logo") or j.get("logo",""),
                "posted_date":      _parse_date(j.get("date")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("RemoteOK: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("RemoteOK error: %s", exc)
        return []


def _fetch_themuse(query: str, limit: int = 30) -> List[Dict]:
    """The Muse public API. Completely free, no key needed."""
    domain = "themuse.com"
    ck = _cache_key("themuse", query, "")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        params: Dict = {"page": 0, "count": min(limit, 20)}
        if query:
            params["category"] = query

        resp = session.get("https://www.themuse.com/api/public/jobs", params=params, timeout=12)
        if resp.status_code != 200:
            logger.warning("TheMuse HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("results", []):
            locs      = j.get("locations", [])
            location  = locs[0].get("name","Flexible") if locs else "Flexible"
            levels    = j.get("levels", [])
            level_str = levels[0].get("short_name","") if levels else ""
            cats      = [c.get("name","") for c in j.get("categories",[])]
            company   = j.get("company", {})
            logo_refs = company.get("refs",{}).get("logo_image",{})
            logo_url  = logo_refs.get("130x130") or logo_refs.get("480x480","")

            jobs.append({
                "id":               _job_id(j.get("name",""), company.get("name",""), "TheMuse"),
                "title":            j.get("name", "Unknown Position"),
                "company":          company.get("name", "Unknown Company"),
                "location":         location,
                "work_type":        "Remote" if "remote" in location.lower() else "On-site",
                "job_type":         "Full-time",
                "experience_level": _muse_level(level_str),
                "description":      (j.get("contents") or "")[:2000],
                "skills_required":  cats[:6],
                "salary":           "",
                "salary_min":       None,
                "salary_max":       None,
                "source":           "The Muse",
                "source_url":       j.get("refs",{}).get("landing_page","https://www.themuse.com/jobs"),
                "company_logo":     logo_url,
                "posted_date":      _parse_date(j.get("publication_date")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("TheMuse: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("TheMuse error: %s", exc)
        return []


def _fetch_adzuna(query: str, location: str = "", limit: int = 30) -> List[Dict]:
    """
    Adzuna API. 1,000 free requests/month.
    Requires ADZUNA_APP_ID and ADZUNA_APP_KEY in .env.
    """
    app_id  = os.environ.get("ADZUNA_APP_ID","")
    app_key = os.environ.get("ADZUNA_APP_KEY","")
    if not app_id or not app_key:
        return []

    domain = "api.adzuna.com"
    ck = _cache_key("adzuna", query, location)
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        params: Dict = {
            "app_id": app_id, "app_key": app_key,
            "results_per_page": min(limit, 50),
            "what": query or "software engineer",
            "content-type": "application/json",
        }
        if location:
            params["where"] = location

        resp = session.get("https://api.adzuna.com/v1/api/jobs/us/search/1",
                           params=params, timeout=14)
        if resp.status_code != 200:
            logger.warning("Adzuna HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("results", []):
            comp    = j.get("company",{}).get("display_name","Unknown")
            loc     = j.get("location",{}).get("display_name","")
            sal_min = j.get("salary_min")
            sal_max = j.get("salary_max")
            cat     = (j.get("category") or {}).get("label","")

            jobs.append({
                "id":               _job_id(j.get("title",""), comp, "Adzuna"),
                "title":            j.get("title","Unknown"),
                "company":          comp,
                "location":         loc,
                "work_type":        "Remote" if "remote" in (loc+j.get("title","")).lower() else "On-site",
                "job_type":         "Full-time",
                "experience_level": _guess_level(j.get("title","")),
                "description":      j.get("description",""),
                "skills_required":  [cat] if cat else [],
                "salary":           "",
                "salary_min":       int(sal_min) if sal_min else None,
                "salary_max":       int(sal_max) if sal_max else None,
                "source":           "Adzuna",
                "source_url":       j.get("redirect_url","https://www.adzuna.com"),
                "company_logo":     "",
                "posted_date":      _parse_date(j.get("created")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("Adzuna: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("Adzuna error: %s", exc)
        return []


def _fetch_jsearch(query: str, location: str = "", limit: int = 30) -> List[Dict]:
    """
    JSearch via RapidAPI. Aggregates LinkedIn, Indeed, Glassdoor.
    Free: 200 req/month. Requires RAPIDAPI_KEY in .env.
    """
    api_key = os.environ.get("RAPIDAPI_KEY","")
    if not api_key:
        return []

    domain = "jsearch.p.rapidapi.com"
    ck = _cache_key("jsearch", query, location)
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        q = (query or "software engineer") + (f" in {location}" if location else "")
        resp = session.get(
            "https://jsearch.p.rapidapi.com/search",
            headers={"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"},
            params={"query": q, "page": "1", "num_pages": "2", "date_posted": "all"},
            timeout=18,
        )
        if resp.status_code == 429:
            logger.warning("JSearch 429 - monthly quota likely reached")
            return []
        if resp.status_code != 200:
            logger.warning("JSearch HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("data", [])[:limit]:
            city    = j.get("job_city","")
            state   = j.get("job_state","")
            country = j.get("job_country","")
            loc     = ", ".join(p for p in [city, state, country] if p) or "Not specified"
            employer   = j.get("employer_name","Unknown")
            apply_link = j.get("job_apply_link") or j.get("job_google_link","")
            source_name = _source_from_url(apply_link)
            highlights  = j.get("job_highlights") or {}
            sal_min = j.get("job_min_salary")
            sal_max = j.get("job_max_salary")

            jobs.append({
                "id":               _job_id(j.get("job_title",""), employer, source_name),
                "title":            j.get("job_title","Unknown"),
                "company":          employer,
                "location":         loc,
                "work_type":        "Remote" if j.get("job_is_remote") else "On-site",
                "job_type":         _map_employment_type(j.get("job_employment_type","")),
                "experience_level": _guess_level(j.get("job_title","")),
                "description":      (j.get("job_description") or "")[:2000],
                "skills_required":  j.get("job_required_skills") or _extract_skills(j.get("job_description","")),
                "salary":           "",
                "salary_min":       int(sal_min) if sal_min else None,
                "salary_max":       int(sal_max) if sal_max else None,
                "source":           source_name,
                "source_url":       apply_link,
                "company_logo":     j.get("employer_logo",""),
                "posted_date":      _parse_date(j.get("job_posted_at_datetime_utc")),
                "is_active":        True,
                "requirements":     highlights.get("Qualifications",[])[:6],
                "responsibilities": highlights.get("Responsibilities",[])[:6],
                "benefits":         highlights.get("Benefits",[])[:6],
            })

        _to_cache(ck, jobs)
        logger.info("JSearch: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("JSearch error: %s", exc)
        return []


def _fetch_remotive(query: str, limit: int = 30) -> List[Dict]:
    """
    Remotive public API. Completely free, no key needed.
    Global remote tech jobs — USA, EU, UK, Australia, Asia.
    """
    domain = "remotive.com"
    ck = _cache_key("remotive", query, "remote")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        params: Dict = {"limit": min(limit, 100)}
        if query:
            params["search"] = query
        q_lower = (query or "").lower()
        if any(w in q_lower for w in ("software", "developer", "engineer", "backend", "frontend")):
            params["category"] = "software-dev"
        elif "data" in q_lower:
            params["category"] = "data"
        elif "design" in q_lower:
            params["category"] = "design"
        elif "devops" in q_lower or "infra" in q_lower:
            params["category"] = "devops-sysadmin"

        resp = session.get("https://remotive.com/api/remote-jobs", params=params, timeout=14)
        if resp.status_code != 200:
            logger.warning("Remotive HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("jobs", [])[:limit]:
            location = j.get("candidate_required_location") or "Remote - Worldwide"
            jobs.append({
                "id":               _job_id(j.get("title", ""), j.get("company_name", ""), "Remotive"),
                "title":            j.get("title", "Unknown Position"),
                "company":          j.get("company_name", "Unknown Company"),
                "location":         location,
                "work_type":        "Remote",
                "job_type":         "Full-time",
                "experience_level": _guess_level(j.get("title", "")),
                "description":      (j.get("description") or "")[:2000],
                "skills_required":  (j.get("tags") or _extract_skills(j.get("description", "")))[:8],
                "salary":           j.get("salary", ""),
                "salary_min":       None,
                "salary_max":       None,
                "source":           "Remotive",
                "source_url":       j.get("url", "https://remotive.com"),
                "company_logo":     j.get("company_logo_url", ""),
                "posted_date":      _parse_date(j.get("publication_date")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("Remotive: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("Remotive error: %s", exc)
        return []


def _fetch_arbeitnow(query: str, limit: int = 30) -> List[Dict]:
    """
    Arbeitnow API. Completely free, no key needed.
    European + international tech jobs: Germany, UK, Netherlands, remote.
    """
    domain = "www.arbeitnow.com"
    ck = _cache_key("arbeitnow", query, "")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        resp = session.get("https://www.arbeitnow.com/api/job-board-api", timeout=14)
        if resp.status_code != 200:
            logger.warning("Arbeitnow HTTP %s", resp.status_code)
            return []

        data = resp.json().get("data", [])
        if query:
            q = query.lower()
            data = [j for j in data
                    if q in j.get("title", "").lower()
                    or any(q in t.lower() for t in j.get("tags", []))
                    or q in (j.get("description", "") or "").lower()[:500]]

        jobs = []
        for j in data[:limit]:
            loc = j.get("location", "Europe")
            if j.get("remote"):
                loc = f"Remote ({loc})" if loc else "Remote"
            jobs.append({
                "id":               _job_id(j.get("title", ""), j.get("company_name", ""), "Arbeitnow"),
                "title":            j.get("title", "Unknown Position"),
                "company":          j.get("company_name", "Unknown Company"),
                "location":         loc,
                "work_type":        "Remote" if j.get("remote") else "On-site",
                "job_type":         "Full-time",
                "experience_level": _guess_level(j.get("title", "")),
                "description":      (j.get("description") or "")[:2000],
                "skills_required":  (j.get("tags") or [])[:8],
                "salary":           "",
                "salary_min":       None,
                "salary_max":       None,
                "source":           "Arbeitnow",
                "source_url":       j.get("url", "https://www.arbeitnow.com"),
                "company_logo":     j.get("company_logo", ""),
                "posted_date":      _parse_date(j.get("created_at")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("Arbeitnow: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("Arbeitnow error: %s", exc)
        return []


def _fetch_jobicy(query: str, limit: int = 30) -> List[Dict]:
    """
    Jobicy public API v2. Completely free, no key needed.
    Global remote tech jobs with geo-tagging (US, UK, EU, Asia, etc.).
    """
    domain = "jobicy.com"
    ck = _cache_key("jobicy", query, "remote")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        params: Dict = {"count": min(limit, 50)}
        if query:
            params["tag"] = query.lower().replace(" ", "-")

        resp = session.get("https://jobicy.com/api/v2/remote-jobs", params=params, timeout=14)
        if resp.status_code != 200:
            logger.warning("Jobicy HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("jobs", [])[:limit]:
            industry = j.get("jobIndustry") or []
            if isinstance(industry, str):
                industry = [industry]
            jobs.append({
                "id":               _job_id(j.get("jobTitle", ""), j.get("companyName", ""), "Jobicy"),
                "title":            j.get("jobTitle", "Unknown Position"),
                "company":          j.get("companyName", "Unknown Company"),
                "location":         j.get("jobGeo") or "Remote - Worldwide",
                "work_type":        "Remote",
                "job_type":         j.get("jobType", "Full-time"),
                "experience_level": _guess_level(j.get("jobTitle", "")),
                "description":      (j.get("jobDescription") or "")[:2000],
                "skills_required":  industry[:6],
                "salary":           j.get("jobSalary", ""),
                "salary_min":       None,
                "salary_max":       None,
                "source":           "Jobicy",
                "source_url":       j.get("url", "https://jobicy.com"),
                "company_logo":     j.get("companyLogo", ""),
                "posted_date":      _parse_date(j.get("pubDate")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("Jobicy: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("Jobicy error: %s", exc)
        return []


def _fetch_weworkremotely(query: str, limit: int = 20) -> List[Dict]:
    """
    We Work Remotely RSS feed. Completely free, no key needed.
    International remote developer jobs — worldwide applicants welcome.
    """
    domain = "weworkremotely.com"
    ck = _cache_key("weworkremotely", query, "remote")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        resp = session.get(
            "https://weworkremotely.com/categories/remote-programming-jobs.rss",
            timeout=14,
        )
        if resp.status_code != 200:
            logger.warning("WeWorkRemotely HTTP %s", resp.status_code)
            return []

        root = ET.fromstring(resp.text)
        channel = root.find("channel")
        if channel is None:
            return []

        items = channel.findall("item")
        if query:
            q = query.lower()
            items = [i for i in items
                     if q in (i.findtext("title") or "").lower()
                     or q in (i.findtext("description") or "").lower()]

        jobs = []
        for item in items[:limit]:
            title_raw = (item.findtext("title") or "").strip()
            # WWR format often: "Company: Job Title"
            parts = title_raw.split(":", 1)
            if len(parts) == 2:
                company = parts[0].strip()
                title   = parts[1].strip()
            else:
                company = "Unknown Company"
                title   = title_raw
            # Remove trailing location hint in parens
            import re as _re
            title = _re.sub(r"\s*\(.*?\)\s*$", "", title).strip() or title_raw

            # WWR uses a custom namespace for region
            region = None
            for child in item:
                if child.tag.endswith("region"):
                    region = child.text
                    break
            location = region or "Remote - Worldwide"

            jobs.append({
                "id":               _job_id(title, company, "WeWorkRemotely"),
                "title":            title,
                "company":          company,
                "location":         location,
                "work_type":        "Remote",
                "job_type":         "Full-time",
                "experience_level": _guess_level(title),
                "description":      (item.findtext("description") or "")[:2000],
                "skills_required":  _extract_skills(item.findtext("description") or ""),
                "salary":           "",
                "salary_min":       None,
                "salary_max":       None,
                "source":           "WeWorkRemotely",
                "source_url":       item.findtext("link") or "https://weworkremotely.com",
                "company_logo":     "",
                "posted_date":      _parse_date(item.findtext("pubDate")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("WeWorkRemotely: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("WeWorkRemotely error: %s", exc)
        return []


def _fetch_reed(query: str, location: str = "", limit: int = 25) -> List[Dict]:
    """
    Reed.co.uk API. Free tier with registration (~1000 req/month).
    UK-specific jobs. Sign up at https://www.reed.co.uk/developers/jobseeker
    Requires REED_API_KEY in .env.
    """
    api_key = os.environ.get("REED_API_KEY", "")
    if not api_key:
        return []

    domain = "www.reed.co.uk"
    ck = _cache_key("reed", query, location)
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        params: Dict = {
            "keywords":       query or "software engineer",
            "resultsToTake":  min(limit, 100),
        }
        if location:
            params["locationName"] = location

        # Reed uses HTTP Basic Auth: API key as username, blank password
        resp = session.get(
            "https://www.reed.co.uk/api/1.0/search",
            params=params,
            auth=(api_key, ""),
            timeout=14,
        )
        if resp.status_code != 200:
            logger.warning("Reed HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("results", [])[:limit]:
            sal_min = j.get("minimumSalary")
            sal_max = j.get("maximumSalary")
            sal_str = ""
            if sal_min and sal_max:
                sal_str = f"£{sal_min:,.0f} – £{sal_max:,.0f}"

            jobs.append({
                "id":               _job_id(j.get("jobTitle", ""), j.get("employerName", ""), "Reed"),
                "title":            j.get("jobTitle", "Unknown Position"),
                "company":          j.get("employerName", "Unknown Company"),
                "location":         j.get("locationName", "UK"),
                "work_type":        "Remote" if "remote" in (j.get("jobTitle", "") + j.get("locationName", "")).lower() else "On-site",
                "job_type":         "Full-time",
                "experience_level": _guess_level(j.get("jobTitle", "")),
                "description":      (j.get("jobDescription") or "")[:2000],
                "skills_required":  _extract_skills(j.get("jobDescription") or ""),
                "salary":           sal_str,
                "salary_min":       int(sal_min) if sal_min else None,
                "salary_max":       int(sal_max) if sal_max else None,
                "source":           "Reed (UK)",
                "source_url":       j.get("jobUrl", "https://www.reed.co.uk"),
                "company_logo":     "",
                "posted_date":      _parse_date(j.get("date")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("Reed: %d UK jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("Reed error: %s", exc)
        return []


def _fetch_findwork(query: str, limit: int = 30) -> List[Dict]:
    """
    FindWork.dev API. Free with API key.
    Developer-focused jobs: US, UK, EU, Canada, Australia + Remote.
    Sign up at https://findwork.dev to get a free key.
    Requires FINDWORK_API_KEY in .env.
    """
    api_key = os.environ.get("FINDWORK_API_KEY", "")
    if not api_key:
        return []

    domain = "findwork.dev"
    ck = _cache_key("findwork", query, "")
    cached = _from_cache(ck)
    if cached is not None:
        return cached[:limit]

    _throttle(domain)
    session = _make_session()
    try:
        params: Dict = {"search": query or "software engineer", "ordering": "-date"}
        resp = session.get(
            "https://findwork.dev/api/jobs/",
            headers={"Authorization": f"Token {api_key}"},
            params=params,
            timeout=14,
        )
        if resp.status_code != 200:
            logger.warning("FindWork HTTP %s", resp.status_code)
            return []

        jobs = []
        for j in resp.json().get("results", [])[:limit]:
            remote = j.get("remote", False)
            loc    = j.get("location", "") or ("Remote" if remote else "Not specified")
            jobs.append({
                "id":               _job_id(j.get("role", ""), j.get("company_name", ""), "FindWork"),
                "title":            j.get("role", "Unknown Position"),
                "company":          j.get("company_name", "Unknown Company"),
                "location":         "Remote" if remote else loc,
                "work_type":        "Remote" if remote else "On-site",
                "job_type":         "Full-time",
                "experience_level": _guess_level(j.get("role", "")),
                "description":      (j.get("text") or "")[:2000],
                "skills_required":  list(j.get("keywords") or [])[:8],
                "salary":           "",
                "salary_min":       None,
                "salary_max":       None,
                "source":           "FindWork",
                "source_url":       j.get("url", "https://findwork.dev"),
                "company_logo":     j.get("company_logo", ""),
                "posted_date":      _parse_date(j.get("date_posted")),
                "is_active":        True,
                "requirements":     [],
                "responsibilities": [],
                "benefits":         [],
            })

        _to_cache(ck, jobs)
        logger.info("FindWork: %d jobs (query=%r)", len(jobs), query)
        return jobs
    except Exception as exc:
        logger.error("FindWork error: %s", exc)
        return []


def _fetch_adzuna_countries(query: str, limit_per_country: int = 12) -> List[Dict]:
    """
    Adzuna multi-country fetcher.
    Covers: UK (gb), Australia (au), Canada (ca), India (in),
            Singapore (sg), Germany (de), Netherlands (nl).
    Uses the same ADZUNA_APP_ID + ADZUNA_APP_KEY.
    Countries are queried sequentially with per-domain throttle between
    each to avoid rate-limit bans across the shared API key.
    """
    app_id  = os.environ.get("ADZUNA_APP_ID", "")
    app_key = os.environ.get("ADZUNA_APP_KEY", "")
    if not app_id or not app_key:
        return []

    # (code, label, tld-hint)
    COUNTRIES = [
        ("gb", "UK",          "co.uk"),
        ("au", "Australia",   "com.au"),
        ("ca", "Canada",      "ca"),
        ("in", "India",       "in"),
        ("sg", "Singapore",   "com.sg"),
        ("de", "Germany",     "de"),
        ("nl", "Netherlands", "nl"),
    ]
    domain    = "api.adzuna.com"
    all_jobs: List[Dict] = []
    seen:     set = set()
    session   = _make_session()

    for code, label, _tld in COUNTRIES:
        ck = _cache_key(f"adzuna_{code}", query, "")
        cached = _from_cache(ck)
        if cached is not None:
            for j in cached[:limit_per_country]:
                if j["id"] not in seen:
                    seen.add(j["id"])
                    all_jobs.append(j)
            continue

        _throttle(domain)   # enforces min delay between every country call
        try:
            params: Dict = {
                "app_id":          app_id,
                "app_key":         app_key,
                "results_per_page": min(limit_per_country, 50),
                "what":            query or "software engineer",
                "content-type":    "application/json",
            }
            url  = f"https://api.adzuna.com/v1/api/jobs/{code}/search/1"
            resp = session.get(url, params=params, timeout=15)

            if resp.status_code == 404:
                continue                         # country not supported by Adzuna
            if resp.status_code != 200:
                logger.warning("Adzuna %s HTTP %s", label, resp.status_code)
                continue

            jobs = []
            for j in resp.json().get("results", []):
                comp    = j.get("company", {}).get("display_name", "Unknown")
                loc_raw = j.get("location", {}).get("display_name", label)
                # Append country label if it's not already in the string
                area_parts = j.get("location", {}).get("area", [])
                loc = loc_raw if any(label.lower() in p.lower() for p in area_parts) \
                      else f"{loc_raw}, {label}"
                sal_min = j.get("salary_min")
                sal_max = j.get("salary_max")
                cat     = (j.get("category") or {}).get("label", "")
                jid     = _job_id(j.get("title", ""), comp, f"Adzuna_{code}")

                jobs.append({
                    "id":               jid,
                    "title":            j.get("title", "Unknown"),
                    "company":          comp,
                    "location":         loc,
                    "work_type":        "Remote" if "remote" in (loc + j.get("title", "")).lower() else "On-site",
                    "job_type":         "Full-time",
                    "experience_level": _guess_level(j.get("title", "")),
                    "description":      (j.get("description") or "")[:2000],
                    "skills_required":  [cat] if cat else [],
                    "salary":           "",
                    "salary_min":       int(sal_min) if sal_min else None,
                    "salary_max":       int(sal_max) if sal_max else None,
                    "source":           f"Adzuna ({label})",
                    "source_url":       j.get("redirect_url", f"https://www.adzuna.{_tld}"),
                    "company_logo":     "",
                    "posted_date":      _parse_date(j.get("created")),
                    "is_active":        True,
                    "requirements":     [],
                    "responsibilities": [],
                    "benefits":         [],
                })

            _to_cache(ck, jobs)
            logger.info("Adzuna %s: %d jobs", label, len(jobs))

            for j in jobs:
                if j["id"] not in seen:
                    seen.add(j["id"])
                    all_jobs.append(j)

        except Exception as exc:
            logger.error("Adzuna %s error: %s", label, exc)
            continue

    return all_jobs


# --- Public API ---------------------------------------------------------------

class JobScraper:
    """
    Multi-source real-time job scraper with anti-ban protection.
    Free sources (RemoteOK, The Muse) work out of the box.
    Adzuna and JSearch activate automatically when keys are in .env.
    """

    @staticmethod
    def fetch_jobs(query: str = "", location: str = "",
                   limit_per_source: int = 25) -> List[Dict]:
        """
        Fetch live jobs from all configured sources.

        Anti-ban strategy:
          - Free no-key sources (6) run in parallel with max 3 workers.
          - Key-required sources (5) run in a separate pool with max 2 workers.
          - Every source has its own per-domain throttle + random jitter.
          - 1-hour in-memory TTL cache drastically reduces live calls.
          - Adzuna multi-country fetches sequentially with per-domain delay.
          - Duplicate jobs (same id hash) are discarded across all sources.

        Sources by region:
          Free  : RemoteOK (global remote), TheMuse (US/global),
                  Remotive (global remote), Arbeitnow (EU + remote),
                  Jobicy (global remote), WeWorkRemotely (global remote)
          Keyed : JSearch/RapidAPI (US, global via LinkedIn/Indeed),
                  Adzuna US, Adzuna multi-country (UK/AU/CA/IN/SG/DE/NL),
                  Reed.co.uk (UK), FindWork.dev (US/UK/EU/AU/Remote)
        """
        lps = limit_per_source

        # Group 1 — completely free, parallel (3 workers)
        free_fetchers = [
            (_fetch_remoteok,       (query, lps)),
            (_fetch_themuse,        (query, lps)),
            (_fetch_remotive,       (query, lps)),
            (_fetch_arbeitnow,      (query, lps)),
            (_fetch_jobicy,         (query, lps)),
            (_fetch_weworkremotely, (query, min(lps, 20))),
        ]

        # Group 2 — key-required, parallel (2 workers, lower quota pressure)
        key_fetchers = [
            (_fetch_jsearch,          (query, location, lps)),
            (_fetch_adzuna,           (query, location, lps)),
            (_fetch_adzuna_countries, (query, 12)),
            (_fetch_reed,             (query, location or "", min(lps, 25))),
            (_fetch_findwork,         (query, lps)),
        ]

        all_jobs: List[Dict] = []
        seen_ids: set = set()

        def _collect(future_map: dict) -> None:
            try:
                futures_iter = as_completed(future_map, timeout=45)
            except Exception:
                futures_iter = iter(future_map.keys())
            try:
                for future in futures_iter:
                    name = future_map[future]
                    try:
                        for job in future.result(timeout=35):
                            if job["id"] not in seen_ids:
                                seen_ids.add(job["id"])
                                all_jobs.append(job)
                    except Exception as exc:
                        logger.warning("%s failed: %s", name, exc)
            except Exception as tex:
                logger.warning("Source pool timed out, using partial results: %s", tex)

        with ThreadPoolExecutor(max_workers=3) as pool:
            _collect({pool.submit(fn, *args): fn.__name__ for fn, args in free_fetchers})

        with ThreadPoolExecutor(max_workers=2) as pool:
            _collect({pool.submit(fn, *args): fn.__name__ for fn, args in key_fetchers})

        all_jobs.sort(key=lambda j: j.get("posted_date") or datetime.min, reverse=True)
        logger.info("Total unique jobs fetched: %d", len(all_jobs))
        return all_jobs

    @staticmethod
    def search_jobs(query: str = "", location: str = "", role_type: str = "",
                    experience_level: str = "", work_type: str = "",
                    limit: int = 50) -> List[Dict]:
        """Fetch then filter jobs."""
        q = " ".join(filter(None, [query, role_type]))
        jobs = JobScraper.fetch_jobs(query=q, location=location, limit_per_source=40)

        if experience_level:
            jobs = [j for j in jobs if j.get("experience_level") == experience_level]
        if work_type:
            jobs = [j for j in jobs if (j.get("work_type") or "").lower() == work_type.lower()]

        return jobs[:limit]

    @staticmethod
    def generate_mock_jobs(count: int = 50, role_filter: Optional[str] = None) -> List[Dict]:
        """Backward-compat shim: now delegates to real live fetch."""
        return JobScraper.fetch_jobs(
            query=role_filter or "", limit_per_source=max(count // 4, 15)
        )[:count]