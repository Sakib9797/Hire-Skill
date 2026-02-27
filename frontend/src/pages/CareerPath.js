import React, { useState, useEffect, useRef, useMemo } from 'react';
import Navbar from '../components/Navbar';
import salaryService from '../services/salaryService';
import '../styles/CareerPath.css';

const CATEGORY_COLORS = {
  'Software Development': '#4f46e5',
  'Data Science':         '#0891b2',
  'AI/ML':               '#7c3aed',
  'Infrastructure':      '#059669',
  'Mobile Development':  '#d97706',
  'Cloud Computing':     '#0369a1',
  'Data Engineering':    '#06b6d4',
  'Security':            '#dc2626',
  'Design':              '#db2777',
  'Product Management':  '#65a30d',
  'Quality Assurance':   '#9333ea',
  'Blockchain':          '#f97316',
  'Business':            '#6b7280',
};

const GROWTH_COLORS = { 'Very High': '#10b981', 'High': '#3b82f6', 'Medium': '#f59e0b', 'Low': '#ef4444' };
const GROWTH_ICONS  = { 'Very High': '🚀', 'High': '📈', 'Medium': '⚡', 'Low': '📉' };
const CAT_ICONS = {
  'Software Development': '💻', 'Data Science': '📊', 'AI/ML': '🤖',
  'Infrastructure': '🏗️', 'Mobile Development': '📱', 'Cloud Computing': '☁️',
  'Data Engineering': '🔧', 'Security': '🔒', 'Design': '🎨',
  'Product Management': '📋', 'Quality Assurance': '✅', 'Blockchain': '⛓️',
  'Business': '💼',
};

// ── SVG Graph Component ──────────────────────────────────────────────────────
const CareerGraph = ({ nodes, edges, highlightPath, onNodeClick, activeNode, hoveredNode, onNodeHover, isDark }) => {
  const W = 960, H = 720, CX = W / 2, CY = H / 2, R = 280, NR = 28;

  const positions = useMemo(() => {
    const pos = {};
    nodes.forEach((n, i) => {
      const angle = (i / nodes.length) * 2 * Math.PI - Math.PI / 2;
      pos[n.id] = { x: CX + R * Math.cos(angle), y: CY + R * Math.sin(angle) };
    });
    return pos;
  }, [nodes]);

  const pathSet = useMemo(() => {
    const s = new Set();
    for (let i = 0; i < highlightPath.length - 1; i++) {
      s.add(`${highlightPath[i]}→${highlightPath[i+1]}`);
      s.add(`${highlightPath[i+1]}→${highlightPath[i]}`);
    }
    return s;
  }, [highlightPath]);

  const activeNeighbors = useMemo(() => {
    const s = new Set();
    if (activeNode) edges.forEach(e => {
      if (e.source === activeNode) s.add(e.target);
      if (e.target === activeNode) s.add(e.source);
    });
    return s;
  }, [activeNode, edges]);

  const hoveredNeighbors = useMemo(() => {
    const s = new Set();
    if (hoveredNode) edges.forEach(e => {
      if (e.source === hoveredNode) s.add(e.target);
      if (e.target === hoveredNode) s.add(e.source);
    });
    return s;
  }, [hoveredNode, edges]);

  const edgePath = (s, t) => {
    const mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2;
    const dx = t.x - s.x, dy = t.y - s.y;
    const nx = -dy * 0.15, ny = dx * 0.15;
    return `M ${s.x} ${s.y} Q ${mx+nx} ${my+ny} ${t.x} ${t.y}`;
  };

  const isPathEdge = e => pathSet.has(`${e.source}→${e.target}`) || pathSet.has(`${e.target}→${e.source}`);
  const textFill    = isDark ? '#e2e8f0' : '#1e293b';
  const strokeColor = isDark ? '#1e293b' : '#ffffff';
  const bgFill      = isDark ? '#1e293b' : '#f8fafc';
  const bgStroke    = isDark ? '#334155' : '#e2e8f0';
  const dimEdge     = isDark ? '#334155' : '#cbd5e1';

  const edgeVisible = e => {
    if (highlightPath.length > 1) return isPathEdge(e);
    if (activeNode) return e.source === activeNode || e.target === activeNode;
    if (hoveredNode) return e.source === hoveredNode || e.target === hoveredNode;
    return e.weight >= 28;
  };

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="career-svg">
      <defs>
        <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="4" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" floodOpacity="0.2"/>
        </filter>
        <linearGradient id="pathGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%"   stopColor="#7c3aed"/>
          <stop offset="100%" stopColor="#4f46e5"/>
        </linearGradient>
      </defs>

      {/* Center hub */}
      <circle cx={CX} cy={CY} r={50} fill={bgFill} stroke={bgStroke} strokeWidth="1.5"/>
      <text x={CX} y={CY - 8}  textAnchor="middle" fontSize="22">🗺️</text>
      <text x={CX} y={CY + 10} textAnchor="middle" fontSize="10" fill={isDark ? '#94a3b8' : '#64748b'} fontWeight="600">Career</text>
      <text x={CX} y={CY + 24} textAnchor="middle" fontSize="10" fill={isDark ? '#94a3b8' : '#64748b'} fontWeight="600">Graph</text>

      {/* Edges */}
      {edges.map((e, i) => {
        const s = positions[e.source], t = positions[e.target];
        if (!s || !t || !edgeVisible(e)) return null;
        const isPath   = isPathEdge(e);
        const isActive = e.source === activeNode || e.target === activeNode;
        const isHover  = e.source === hoveredNode || e.target === hoveredNode;
        const mx = (s.x + t.x) / 2 + (-(t.y - s.y) * 0.15);
        const my = (s.y + t.y) / 2 + ((t.x - s.x) * 0.15);
        return (
          <g key={i}>
            <path d={edgePath(s, t)} fill="none"
              stroke={isPath ? 'url(#pathGrad)' : isActive ? '#6366f1' : isHover ? '#8b5cf6' : dimEdge}
              strokeWidth={isPath ? 3.5 : isActive || isHover ? 2.5 : Math.max(1, e.weight / 20)}
              strokeOpacity={isPath ? 1 : isActive || isHover ? 0.85 : 0.4}
              strokeDasharray={isPath ? '8 3' : 'none'}
              style={isPath ? { animation: 'dashMove 1.2s linear infinite' } : {}}
            />
            {(isActive || isHover || isPath) && (
              <g>
                <circle cx={mx} cy={my} r={12} fill={bgFill} strokeWidth="0.5" stroke={bgStroke}/>
                <text x={mx} y={my + 4} textAnchor="middle" fontSize="9" fill={isPath ? '#7c3aed' : '#6366f1'} fontWeight="700">{e.weight}%</text>
              </g>
            )}
          </g>
        );
      })}

      {/* Nodes */}
      {nodes.map((n) => {
        const pos      = positions[n.id];
        if (!pos) return null;
        const color    = CATEGORY_COLORS[n.category] || '#6b7280';
        const isActive = activeNode === n.id;
        const isHover  = hoveredNode === n.id;
        const isInPath = highlightPath.includes(n.id);
        const pathIdx  = highlightPath.indexOf(n.id);
        const isDim    = (activeNode && !isActive && !activeNeighbors.has(n.id)) ||
                         (!activeNode && hoveredNode && !isHover && !hoveredNeighbors.has(n.id));
        const scale    = (isActive || isHover) ? 1.18 : isInPath ? 1.1 : 1;

        return (
          // Outer <g> handles position only — no CSS transition here to avoid jitter
          <g key={n.id}
            transform={`translate(${pos.x} ${pos.y})`}
            style={{ cursor: 'pointer' }}
            onClick={() => onNodeClick(n)}
            onMouseEnter={() => onNodeHover(n.id)}
            onMouseLeave={() => onNodeHover(null)}>

            {/* Inner <g> handles scale + opacity — transformOrigin 0 0 = local centre */}
            <g style={{
              opacity: isDim ? 0.18 : 1,
              transform: `scale(${scale})`,
              transformOrigin: '0 0',
              transition: 'opacity 0.22s ease, transform 0.2s ease',
            }}>

              {/* Glow ring on hover/active/path */}
              {(isActive || isHover || isInPath) && (
                <circle cx={0} cy={0} r={NR + 11}
                  fill={color} fillOpacity="0.13"
                  stroke={color} strokeWidth="1.5" strokeOpacity="0.5"
                  filter="url(#glow)"
                />
              )}

              {/* Main circle */}
              <circle cx={0} cy={0} r={NR}
                fill={color}
                stroke={isActive ? 'white' : isInPath ? '#fde68a' : strokeColor}
                strokeWidth={isActive ? 3.5 : isInPath ? 2.5 : 1.5}
                filter={isActive || isHover ? 'url(#shadow)' : 'none'}
              />

              {/* Step badge */}
              {isInPath && pathIdx > 0 && (
                <>
                  <circle cx={NR - 4} cy={-NR + 4} r={9} fill="#fde68a"/>
                  <text x={NR - 4} y={-NR + 8} textAnchor="middle" fontSize="9" fill="#92400e" fontWeight="800">{pathIdx}</text>
                </>
              )}

              {/* Category icon in node */}
              <text x={0} y={8} textAnchor="middle" fontSize="17" style={{ userSelect: 'none' }}>
                {CAT_ICONS[n.category] || '●'}
              </text>

              {/* Node label */}
              <text className="cp-node-label" x={0} y={NR + 16}
                textAnchor="middle" fontSize="9.5"
                fill={textFill}
                fontWeight={isActive || isInPath ? '700' : '500'}
                style={{ userSelect: 'none' }}>
                {n.label.length > 17 ? n.label.slice(0, 15) + '…' : n.label}
              </text>
            </g>
          </g>
        );
      })}
    </svg>
  );
};

// ── Floating Tooltip ──────────────────────────────────────────────────────────
const NodeTooltip = ({ node }) => {
  if (!node) return null;
  const color = CATEGORY_COLORS[node.category] || '#6b7280';
  return (
    <div className="cp-tooltip" style={{ borderLeftColor: color }}>
      <div className="cp-tooltip-title">{CAT_ICONS[node.category] || '●'} {node.label}</div>
      <div className="cp-tooltip-meta">
        <span style={{ color }}>⬡ {node.category}</span>
        <span>💰 {node.salary}</span>
        <span style={{ color: GROWTH_COLORS[node.growth] }}>
          {GROWTH_ICONS[node.growth]} {node.growth}
        </span>
      </div>
      {(node.skills || []).length > 0 && (
        <div className="cp-tooltip-skills">
          {node.skills.slice(0, 4).map(s => <span key={s} className="cp-tt-chip">{s}</span>)}
        </div>
      )}
      <div className="cp-tooltip-hint">Click to explore →</div>
    </div>
  );
};

// ── Stats Bar ─────────────────────────────────────────────────────────────────
const StatsBar = ({ nodes, edges, filteredCount }) => {
  const cats      = new Set(nodes.map(n => n.category)).size;
  const avgOverlap = edges.length
    ? Math.round(edges.reduce((s, e) => s + e.weight, 0) / edges.length) : 0;
  return (
    <div className="cp-stats">
      <div className="cp-stat"><span className="cp-stat-num">{filteredCount}</span><span className="cp-stat-lbl">Roles</span></div>
      <div className="cp-stat-div"/>
      <div className="cp-stat"><span className="cp-stat-num">{edges.length}</span><span className="cp-stat-lbl">Connections</span></div>
      <div className="cp-stat-div"/>
      <div className="cp-stat"><span className="cp-stat-num">{avgOverlap}%</span><span className="cp-stat-lbl">Avg Overlap</span></div>
      <div className="cp-stat-div"/>
      <div className="cp-stat"><span className="cp-stat-num">{cats}</span><span className="cp-stat-lbl">Categories</span></div>
    </div>
  );
};

// ── Main Page ────────────────────────────────────────────────────────────────
const CareerPath = () => {
  const [graph, setGraph]               = useState({ nodes: [], edges: [] });
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState('');
  const [activeNode, setActiveNode]     = useState(null);
  const [hoveredNode, setHoveredNode]   = useState(null);
  const [hoveredObj, setHoveredObj]     = useState(null);
  const [nodeDetail, setNodeDetail]     = useState(null);
  const [fromRole, setFromRole]         = useState('');
  const [toRole, setToRole]             = useState('');
  const [pathLoading, setPathLoading]   = useState(false);
  const [highlightPath, setHighlightPath] = useState([]);
  const [pathEdges, setPathEdges]       = useState([]);
  const [filterCategory, setFilterCategory] = useState('All');
  const [searchQuery, setSearchQuery]   = useState('');
  const [isDark, setIsDark]             = useState(false);

  // Track dark mode via MutationObserver
  useEffect(() => {
    const check = () => setIsDark(document.documentElement.getAttribute('data-theme') === 'dark');
    check();
    const obs = new MutationObserver(check);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => obs.disconnect();
  }, []);

  useEffect(() => {
    salaryService.getCareerPathGraph()
      .then(res => { const d = res.data || res; setGraph({ nodes: d.nodes || [], edges: d.edges || [] }); })
      .catch(() => setError('Failed to load career graph.'))
      .finally(() => setLoading(false));
  }, []);

  const allCategories = useMemo(() => ['All', ...new Set(graph.nodes.map(n => n.category))], [graph.nodes]);

  const handleNodeClick = (node) => {
    if (activeNode === node.id) { setActiveNode(null); setNodeDetail(null); }
    else { setActiveNode(node.id); setNodeDetail(node); }
  };

  const handleNodeHover = (nodeId) => {
    setHoveredNode(nodeId);
    setHoveredObj(nodeId ? (graph.nodes.find(n => n.id === nodeId) || null) : null);
  };

  const findPath = async () => {
    if (!fromRole || !toRole || fromRole === toRole) return;
    setPathLoading(true); setHighlightPath([]); setPathEdges([]);
    try {
      const res = await salaryService.getCareerPathGraph(fromRole, toRole);
      const d = res.data || res;
      const p = d.path || [];
      setHighlightPath(p);
      setGraph({ nodes: d.nodes || [], edges: d.edges || [] });
      const pe = (d.edges || []).filter(e => {
        for (let i = 0; i < p.length - 1; i++) {
          if ((e.source === p[i] && e.target === p[i+1]) || (e.target === p[i] && e.source === p[i+1])) return true;
        }
        return false;
      });
      setPathEdges(pe);
    } catch {}
    finally { setPathLoading(false); }
  };

  const clearPath = () => { setHighlightPath([]); setPathEdges([]); setFromRole(''); setToRole(''); };

  const filteredNodes = useMemo(() => {
    let nodes = filterCategory === 'All' ? graph.nodes : graph.nodes.filter(n => n.category === filterCategory);
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      nodes = nodes.filter(n => n.label.toLowerCase().includes(q) || n.category.toLowerCase().includes(q));
    }
    return nodes;
  }, [graph.nodes, filterCategory, searchQuery]);

  const filteredEdges = useMemo(() => graph.edges.filter(e =>
    filteredNodes.find(n => n.id === e.source) && filteredNodes.find(n => n.id === e.target)
  ), [graph.edges, filteredNodes]);

  const connectedTo = useMemo(() => nodeDetail ? graph.edges
    .filter(e => e.source === nodeDetail.id || e.target === nodeDetail.id)
    .sort((a, b) => b.weight - a.weight).slice(0, 6)
    .map(e => ({ role: e.source === nodeDetail.id ? e.target : e.source, weight: e.weight })) : [],
  [nodeDetail, graph.edges]);

  return (
    <>
      <Navbar />
      <div className="career-path-page">

        {/* Header */}
        <div className="cp-header">
          <h1>🗺️ Career Path Visualization</h1>
          <p>Interactive career graph — explore role transitions based on real skill overlap. Hover nodes to preview, click to explore, or find shortest paths between any two roles.</p>
        </div>

        {/* Stats bar */}
        {!loading && !error && (
          <StatsBar nodes={graph.nodes} edges={graph.edges} filteredCount={filteredNodes.length} />
        )}

        {/* Controls */}
        <div className="cp-controls card">
          <div className="control-group">
            <label>🔍 Search Role</label>
            <input className="cp-search" type="text" placeholder="e.g. Data Scientist…"
              value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
          </div>

          <div className="control-group">
            <label>⬡ Filter Category</label>
            <select value={filterCategory} onChange={e => { setFilterCategory(e.target.value); clearPath(); setSearchQuery(''); }}>
              {allCategories.map(c => <option key={c}>{c}</option>)}
            </select>
          </div>

          <div className="control-group path-finder">
            <label>🧭 Find Transition Path</label>
            <div className="path-row">
              <select value={fromRole} onChange={e => setFromRole(e.target.value)}>
                <option value="">From role…</option>
                {graph.nodes.map(n => <option key={n.id} value={n.id}>{n.id}</option>)}
              </select>
              <span className="arrow-sep">→</span>
              <select value={toRole} onChange={e => setToRole(e.target.value)}>
                <option value="">To role…</option>
                {graph.nodes.map(n => <option key={n.id} value={n.id}>{n.id}</option>)}
              </select>
              <button className="btn-path" onClick={findPath} disabled={!fromRole || !toRole || pathLoading || fromRole === toRole}>
                {pathLoading ? <span className="spinner-sm" /> : '⚡ Find'}
              </button>
              {highlightPath.length > 0 && <button className="btn-clear" onClick={clearPath}>✕ Clear</button>}
            </div>
          </div>
        </div>

        {/* Path banner */}
        {highlightPath.length > 0 && (
          <div className="path-banner">
            <strong>🧭 Path found:</strong>
            {highlightPath.map((role, i) => (
              <React.Fragment key={role}>
                <span className="path-node">{role}</span>
                {i < highlightPath.length - 1 && <span className="path-sep"> → </span>}
              </React.Fragment>
            ))}
            <span className="path-steps">({highlightPath.length - 1} step{highlightPath.length !== 2 ? 's' : ''})</span>
          </div>
        )}

        {/* Main grid */}
        <div className="cp-main">

          {/* Graph */}
          <div className="graph-container card" style={{ position: 'relative' }}>
            {loading ? (
              <div className="graph-loading"><div className="spinner" /><p>Building career graph…</p></div>
            ) : error ? (
              <div className="alert-error">{error}</div>
            ) : (
              <>
                <CareerGraph
                  nodes={filteredNodes}
                  edges={filteredEdges}
                  highlightPath={highlightPath}
                  onNodeClick={handleNodeClick}
                  activeNode={activeNode}
                  hoveredNode={hoveredNode}
                  onNodeHover={handleNodeHover}
                  isDark={isDark}
                />
                {/* Floating tooltip — shown on hover when no node is actively selected */}
                {hoveredObj && !activeNode && (
                  <div className="cp-tooltip-wrap">
                    <NodeTooltip node={hoveredObj} />
                  </div>
                )}
              </>
            )}
            <div className="graph-hint">Hover to preview · Click to explore · Path finder plans your transition</div>
          </div>

          {/* Detail panel */}
          {nodeDetail && (
            <div className="node-detail card animate-in">
              <div className="nd-header" style={{ borderColor: CATEGORY_COLORS[nodeDetail.category] || '#6b7280' }}>
                <span className="nd-category" style={{ background: CATEGORY_COLORS[nodeDetail.category] || '#6b7280' }}>
                  {CAT_ICONS[nodeDetail.category] || '●'} {nodeDetail.category}
                </span>
                <h3>{nodeDetail.label}</h3>
                <div className="nd-meta">
                  <span className="nd-meta-chip">💰 {nodeDetail.salary}</span>
                  <span className="nd-meta-chip" style={{ color: GROWTH_COLORS[nodeDetail.growth] }}>
                    {GROWTH_ICONS[nodeDetail.growth]} {nodeDetail.growth} growth
                  </span>
                </div>
              </div>

              {/* Quick-set path buttons */}
              <div className="nd-actions">
                <button className="nd-action-btn" onClick={() => setFromRole(nodeDetail.id)}>📍 Set as From</button>
                <button className="nd-action-btn" onClick={() => setToRole(nodeDetail.id)}>🎯 Set as To</button>
              </div>

              <div className="nd-skills">
                <strong>Top Skills</strong>
                <div className="skill-chips">
                  {(nodeDetail.skills || []).map(s => <span key={s} className="chip">{s}</span>)}
                </div>
              </div>

              {connectedTo.length > 0 && (
                <div className="nd-connections">
                  <strong>Closest Transitions</strong>
                  {connectedTo.map(c => (
                    <div key={c.role} className="connection-row"
                      onClick={() => { const n = graph.nodes.find(x => x.id === c.role); if (n) handleNodeClick(n); }}
                      title={`Click to explore ${c.role}`}>
                      <span className="conn-role">{c.role}</span>
                      <div className="conn-bar-wrap">
                        <div className="conn-bar-track">
                          <div className="conn-bar" style={{ width: `${c.weight}%` }} />
                        </div>
                        <span className="conn-pct">{c.weight}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {pathEdges.length > 0 && highlightPath.includes(nodeDetail.id) && (
                <div className="nd-path-skills">
                  <strong>🔗 Skills bridging the path</strong>
                  <div className="skill-chips">
                    {[...new Set(pathEdges.flatMap(e => e.shared_skills || []))].slice(0, 8)
                      .map(s => <span key={s} className="chip chip-path">{s}</span>)}
                  </div>
                </div>
              )}

              <button className="btn-secondary" onClick={() => { setActiveNode(null); setNodeDetail(null); }}>
                ✕ Close
              </button>
            </div>
          )}
        </div>

        {/* Clickable legend */}
        <div className="cp-legend card">
          <div className="cp-legend-header">
            <h3>Category Legend</h3>
            <span className="cp-legend-hint">Click to filter · Click again to reset</span>
          </div>
          <div className="legend-grid">
            {Object.entries(CATEGORY_COLORS).map(([cat, clr]) => {
              const active = filterCategory === cat;
              return (
                <div key={cat}
                  className={`legend-item${active ? ' legend-item-active' : ''}`}
                  style={active ? { outline: `2px solid ${clr}`, outlineOffset: '3px' } : {}}
                  onClick={() => { setFilterCategory(active ? 'All' : cat); clearPath(); setSearchQuery(''); }}>
                  <span className="legend-dot" style={{ background: clr }} />
                  <span>{CAT_ICONS[cat] || ''} {cat}</span>
                  <span className="legend-count">{graph.nodes.filter(n => n.category === cat).length}</span>
                </div>
              );
            })}
          </div>
        </div>

      </div>
    </>
  );
};

export default CareerPath;

