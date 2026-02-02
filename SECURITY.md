# Security Guidelines for HireSkill

## 🔐 Protecting Sensitive Data

This document outlines security best practices for the HireSkill project to prevent accidental exposure of API keys, passwords, and other sensitive data.

---

## ⚠️ CRITICAL: Before Pushing to GitHub

### Files That MUST NOT Be Committed

1. **`backend/.env`** - Contains real API keys and database passwords
2. **`frontend/.env`** - May contain sensitive configuration
3. **Any file ending in `.env.local`, `.env.production`, etc.**
4. **Log files** that might contain sensitive data
5. **Database dump files** (`.sql`, `.dump`, `.backup`)

### Files That ARE Safe to Commit

1. **`backend/.env.example`** - Template with placeholders (NO real secrets)
2. **Configuration files** without hardcoded credentials
3. **Documentation** (after verifying no secrets)

---

## 🛡️ What I've Done For You

### ✅ Removed Secrets From:

- `backend/.env.example` - Now uses placeholder: `gsk_YOUR_GROQ_API_KEY_HERE`
- `GROQ_API_SETUP.md` - All API keys replaced with placeholders
- `GROQ_INTEGRATION_COMPLETE.md` - API key removed
- `MODULE_3_DOCUMENTATION_INDEX.md` - API key removed

### ✅ Already Protected by .gitignore:

```
.env                    # Root env files
backend/.env            # Backend environment
frontend/.env.local     # Frontend local env
*.log                   # Log files
backend/__pycache__/    # Python cache
frontend/node_modules/  # Node modules
```

---

## 🚨 ACTION REQUIRED: Your Security Checklist

### Step 1: Secure Your Groq API Key (URGENT)
⚠️ **Your API key was exposed in documentation files. Anyone could have seen it.**

1. **Revoke the old key immediately:**
   - Go to https://console.groq.com
   - Delete the existing API key: `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`
   - Create a new API key

2. **Update your local `.env` file:**
   ```bash
   # backend/.env
   LLM_API_KEY=gsk_YOUR_NEW_API_KEY_HERE
   ```

### Step 2: Secure Your Database Password

1. **Change your PostgreSQL password** (if you used the real one anywhere):
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_strong_password';
   ```

2. **Update your local `.env` file:**
   ```bash
   # backend/.env
   DATABASE_URL=postgresql://postgres:new_password@localhost:5432/hireskill_db
   ```

### Step 3: Verify Before Pushing

Run these commands in your terminal:

```bash
# 1. Check what files are staged for commit
git status

# 2. Check if .env files are being tracked (should show nothing)
git ls-files | grep "\.env"

# 3. Review all changes before committing
git diff --cached

# 4. Search for any remaining API keys in your code
grep -r "gsk_" . --include="*.py" --include="*.md" --include="*.txt" 2>/dev/null
```

### Step 4: Clean Your Git History (If Already Pushed)

**If you've already pushed with secrets, you MUST clean your history:**

```bash
# Install git-filter-repo (one time)
pip install git-filter-repo

# Remove sensitive files from entire history
git filter-repo --force --path backend/.env --path frontend/.env --invert-paths

# Or use BFG Repo-Cleaner for large repos
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
```

**⚠️ Warning:** Force pushing rewritten history affects all collaborators!

---

## 🔍 Regular Security Checks

### Before Every Commit, Ask Yourself:

- [ ] Did I check `git status` to see what's being committed?
- [ ] Are there any `.env` files in the staged changes?
- [ ] Did I search for API keys or passwords in new files?
- [ ] Are log files or database dumps included?

### Quick Security Scan Command:

```bash
# Create this alias in your ~/.bashrc or ~/.zshrc
alias security-check='
  echo "🔍 Checking for secrets..." && \
  git diff --cached --name-only | xargs grep -l "gsk_\|password\|secret" 2>/dev/null && \
  echo "⚠️  Found potential secrets! Review before committing."
'

# Run before every commit
security-check
```

---

## 📝 Best Practices

### 1. Never Hardcode Secrets

❌ **DON'T:**
```python
# In your Python code
API_KEY = "gsk_actual_key_here"
```

✅ **DO:**
```python
# In your Python code
import os
API_KEY = os.getenv('LLM_API_KEY')
```

### 2. Use Environment Variables

```bash
# backend/.env (NOT committed)
LLM_API_KEY=gsk_actual_key_here
DATABASE_URL=postgresql://postgres:password@localhost/db
```

```bash
# backend/.env.example (Committed as template)
LLM_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/db
```

### 3. Use Strong Passwords

- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- No dictionary words
- Use a password manager

### 4. Rotate Keys Regularly

- API keys: Every 3-6 months
- Database passwords: Every 6-12 months
- Immediately if you suspect exposure

---

## 🆘 What To Do If Secrets Are Exposed

1. **Don't panic** - Act quickly but methodically

2. **Immediately revoke the exposed secret:**
   - API keys: Delete from provider dashboard
   - Database passwords: Change immediately
   - JWT secrets: Regenerate and restart services

3. **Check for unauthorized usage:**
   - Review API usage logs
   - Check database access logs
   - Monitor for suspicious activity

4. **Clean Git history** (see Step 4 above)

5. **Update all dependent systems:**
   - Update `.env` files on all machines
   - Update deployment configurations
   - Notify team members if working in a team

6. **Learn from the incident:**
   - Add pre-commit hooks
   - Implement secret scanning
   - Better documentation

---

## 🔧 Recommended Tools

### Pre-Commit Hooks

Install `pre-commit` to automatically check for secrets:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install hooks
pre-commit install
```

### Secret Scanning Tools

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [GitGuardian](https://www.gitguardian.com/)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [detect-secrets](https://github.com/Yelp/detect-secrets)

---

## 📚 Additional Resources

- [GitHub Docs: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP: Secrets Management](https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication)
- [GitHub .gitignore templates](https://github.com/github/gitignore)

---

## ❓ Questions?

If you're unsure about anything:
1. Ask before committing
2. Double-check with `git diff`
3. When in doubt, don't commit it!

**Remember: It's easier to prevent secret exposure than to clean it up later!**
