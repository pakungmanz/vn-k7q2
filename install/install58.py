# v58: แท็บฉลอง → หน้าฉลอง & เหรียญ (กาง/พับ) ประจำวัน / สัปดาห์ / เดือน · 🥇 project จบ · 🥈 งานเสร็จ
#      · คลังเหรียญทั้งหมด · สถิติตั้งแต่เริ่มจด + กราฟแท่ง (SVG วาดเฉพาะตอนกางสถิติ ไม่ทำให้แอปช้า)
# รันในโฟลเดอร์ที่มี Code.v57.gs : python patch58.py
import json,re,os
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v57.gs',encoding='utf8').read()
assert ck(B)==(465149,1690),('base ไม่ใช่ v57',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v57';","var APP_VER = 'v58';")
C=rep(C,"status: o.v[5], doneAt: isDate(o.v[6]) ? o.v[6] : null, calendar: o.v[9]",
        "status: o.v[5], doneAt: isDate(o.v[6]) ? o.v[6] : null, created: isDate(o.v[1]) ? o.v[1] : null, calendar: o.v[9]")
C=rep(C,"  return { date: TH_DAYS_FULL[","  var adat = archiveData();\n  return { date: TH_DAYS_FULL[")
C=rep(C,"    archive: archiveData(), today: today,","    archive: adat, cel: celebData(tasks, adat, pj), today: today,")
C=rep(C,"function weekDone() { return archiveData().done.filter(function (r) { return r.week; }); }","""function weekDone() { return archiveData().done.filter(function (r) { return r.week; }); }
/* v58: ฉลอง & เหรียญ — นับงานเสร็จรายวันตั้งแต่เริ่มจด (เบา: วันละ 1 ตัวเลข) + รายชื่องานเสร็จย้อนหลัง CEL_DAYS วัน
 *  project ที่จบใช้ archive.done (มีวันที่ at อยู่แล้ว) · 🥇 = 1 project จบ · 🥈 = 1 งานเสร็จ */
var CEL_DAYS = 100;
function celebData(tasks, adat, pj) {
  var first = '', t = {}, list = [], from = ymd(new Date(Date.now() - CEL_DAYS * 86400000)), names = {};
  (adat.done || []).forEach(function (r) { names[String(r.id)] = r.title; if (r.at && (!first || r.at < first)) first = r.at; });
  Object.keys(pj || {}).forEach(function (k) { names[k] = pj[k].title; });
  tasks.forEach(function (x) {
    var c = x.created ? ymd(x.created) : '';
    if (c && (!first || c < first)) first = c;
    if (x.status !== 'เสร็จ') return;
    var w = x.doneAt || x.due || x.created; if (!w) return;
    var d = ymd(w); t[d] = (t[d] || 0) + 1;
    if (d >= from) list.push({ id: x.id, t: x.title, d: d, p: x.projectId ? names[String(x.projectId)] || '' : '', k: w.getTime() });
  });
  list.sort(function (a, b) { return b.k - a.k; });
  return { first: first, from: from, t: t, list: list.map(function (x) { return { id: x.id, t: x.t, d: x.d, p: x.p }; }) };
}""")
# วันที่ project จบ = วันที่บันทึก "เสร็จ 100%" ใน Process (ไม่เลื่อนตามบันทึกที่มาทีหลัง) · ไม่มีบรรทัดนี้ = Last progress เหมือนเดิม
C=rep(C,"""      .map(function (r) { return { id: r.id, title: r.title, rm: rmName(r), at: r.last ? ymd(r.last) : '', week: !!r.last && r.last.getTime() >= wk }; });""",
"""      .map(function (r) { var fd = st === ST_DONE ? finishDate(r) : r.last; return { id: r.id, title: r.title, rm: rmName(r), at: fd ? ymd(fd) : '', week: !!fd && ymd(fd) >= ymd(new Date(wk)) }; })
      .sort(function (a, b) { return a.at < b.at ? 1 : a.at > b.at ? -1 : 0; });""")
C=rep(C,"function weekDone() { return archiveData()","""/** v58: วันที่บันทึกความคืบหน้าเป็น 100% ล่าสุด (บรรทัด "dd/mm/yy เสร็จ 100%" ใน Process ปี พ.ศ.) */
function finishDate(r) {
  var m = /(\\d{2})\\/(\\d{2})\\/(\\d{2}) เสร็จ 100%/.exec(String(r.process || ''));
  return m ? new Date(2500 + +m[3] - 543, +m[2] - 1, +m[1]) : r.last;
}
function weekDone() { return archiveData()""")
# ---------------- หน้าแอป ----------------
H=rep(H,"#party{","""/* v58: ฉลอง & เหรียญ */
.celsec{border:1px solid var(--line);border-radius:14px;background:#fff;overflow:hidden}
.celh{width:100%;display:flex;align-items:center;gap:10px;padding:14px 16px;border:0;background:#fff;font:inherit;text-align:left;cursor:pointer;min-height:52px}
.celh .t{flex:1;font-weight:700;font-size:15px;color:var(--ink)}
.celh .n{font-size:13px;color:var(--mute);white-space:nowrap}
.celh .cv{color:var(--mute);transition:transform .2s}
.celh[aria-expanded="true"] .cv{transform:rotate(90deg)}
.celb{padding:0 16px 14px;display:flex;flex-direction:column;gap:8px}
.celnav{display:flex;align-items:center;justify-content:space-between;gap:8px}
.celnav button{width:40px;height:36px;border-radius:10px;border:1px solid var(--line);background:#fff;font-size:16px;color:var(--ink)}
.celnav button:disabled{opacity:.3}
.celnav b{font-size:14px;text-align:center;flex:1}
.celi{display:flex;gap:8px;align-items:flex-start;font-size:14px;padding:6px 0;border-bottom:1px solid var(--soft)}
.celi:last-child{border-bottom:0}
.celi .p{font-size:12px;color:var(--mute)}
.celsub{font-size:13px;font-weight:700;margin:6px 0 0}
.medals{font-size:20px;letter-spacing:1px;line-height:1.3;word-break:break-all}
.medals small{font-size:13px;color:var(--mute);letter-spacing:0}
.celtot{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.celtot div{border-radius:12px;padding:12px;text-align:center}
.celtot b{display:block;font-size:26px}
.celtot span{font-size:12px}
.celst{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;font-size:13px}
.celst b{display:block;font-size:16px;color:var(--ink)}
.celst span{color:var(--mute)}
.seg2{display:flex;gap:4px;background:var(--soft);border-radius:10px;padding:3px}
.seg2 button{flex:1;height:34px;border:0;border-radius:8px;background:transparent;font:inherit;font-size:13px;font-weight:600;color:var(--mute)}
.seg2 button.on{background:#fff;color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.celg svg{display:block;width:100%;height:auto}
.celg .bar{cursor:pointer}
#party{""")
H=rep(H,"""  var wk = weekDone();
  if (wk.length) h += '<button class="cele" data-act="party"><span class="boing">🎉</span><span class="col"><span class="t">ฉลองประจำสัปดาห์!</span><span class="s">7 วันนี้ทำเสร็จ ' + wk.length + ' project — แตะเพื่อฉลอง</span></span><span class="boing" style="animation-delay:.4s">🥳</span></button>';""",
"""  var wk = weekDone(), cs = celTot(); // v58: แท็บฉลอง → หน้าฉลอง & เหรียญ (โชว์ตลอด)
  h += '<button class="cele" data-act="cel"><span class="boing">🏅</span><span class="col"><span class="t">ฉลอง & เหรียญ</span><span class="s">วันนี้เสร็จ ' + celDay(todayStr()).length + ' งาน · สะสม 🥇 ' + cs.g + ' 🥈 ' + cs.s + (wk.length ? ' · 🎉 7 วันนี้จบ ' + wk.length + ' project' : '') + '</span></span><span aria-hidden="true" style="font-size:22px;color:#8A6A00">›</span></button>';""")
H=rep(H,"(S.arch ? viewArch() : '')","(S.arch ? viewArch() : '') + (S.cel ? viewCel() : '')")
H=rep(H,"  if (act === 'party') { S.arch = false; render(); return party(); }","""  if (act === 'party') { S.arch = false; S.cel = false; render(); return party(); }
  if (act === 'cel') { S.cel = true; S.sheet = null; if (!S.celO) S.celO = { d: true }; return render(); } // v58
  if (act === 'celx') { if (ev.target !== el) return; S.cel = false; return render(); }
  if (act === 'celsec') { S.celO[v] = !S.celO[v]; return render(); }
  if (act === 'celnav') { var cn = v.split(':'); S.celOff[cn[0]] = Math.min(0, (S.celOff[cn[0]] || 0) + +cn[1]); return render(); }
  if (act === 'celg') { var cg = v.split(':'); S.celG[cg[0]] = cg[1]; S.celBar = null; return render(); }
  if (act === 'celbar') { S.celBar = +v; return render(); }""")
# งานเสร็จจากแอป → เหรียญเงินขึ้นทันที (ข้อมูลจริงมาทับตอนเซิร์ฟเวอร์ตอบ)
H=rep(H,"api('toggle', { id: tt.id }, function () { tt.done = true; });","api('toggle', { id: tt.id }, function () { tt.done = true; celMark(tt); });")
H=rep(H,"""      allDayTasks().forEach(function (t) { if (String(t.id) === id) t.done = !t.done; });
      D.projects.forEach(function (p) { (p.tasks || []).forEach(function (t) { if (String(t.id) === id) t.done = !t.done; }); });""",
"""      var cm = null;
      allDayTasks().forEach(function (t) { if (String(t.id) === id) { t.done = !t.done; cm = t; } });
      D.projects.forEach(function (p) { (p.tasks || []).forEach(function (t) { if (String(t.id) === id) t.done = !t.done; }); });
      if (cm) celMark(cm);""")
H=rep(H,"var CF = ['#FFC21A',",r"""/* ---------- v58: ฉลอง & เหรียญ ---------- */
var TH_MON = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
S.celOff = { d: 0, w: 0, m: 0 }; S.celG = { r: 'm', k: 's' };
function cel() { if (!D.cel) D.cel = { first: '', from: '', t: {}, list: [] }; return D.cel; }
function celMark(t) {
  var c = cel(), d = todayStr();
  c.list = c.list.filter(function (x) { return String(x.id) !== String(t.id); });
  if (t.done) { c.list.unshift({ id: t.id, t: t.title, d: d, p: String(t.project || '').replace(/ \([^)]*\)$/, '') }); c.t[d] = (c.t[d] || 0) + 1; }
  else if (c.t[d]) c.t[d]--;
}
function ymdD(s) { var p = String(s).split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
function celDay(d) { return cel().list.filter(function (x) { return x.d === d; }); }
function celTot() { var s = 0, t = cel().t; for (var k in t) s += t[k]; return { g: arch().done.length, s: s }; }
function celSum(a, b) { var s = 0, t = cel().t; for (var k in t) if (k >= a && k <= b) s += t[k]; return s; }
function celGold(a, b) { return arch().done.filter(function (x) { return x.at && x.at >= a && x.at <= b; }); }
function celRange(k, off) {
  var n = new Date(), s, e;
  if (k === 'd') { s = e = new Date(n.getFullYear(), n.getMonth(), n.getDate() + off); }
  else if (k === 'w') { s = new Date(n.getFullYear(), n.getMonth(), n.getDate() - (n.getDay() + 6) % 7 + 7 * off); e = new Date(s.getFullYear(), s.getMonth(), s.getDate() + 6); }
  else { s = new Date(n.getFullYear(), n.getMonth() + off, 1); e = new Date(s.getFullYear(), s.getMonth() + 1, 0); }
  return { a: ymdL(s), b: ymdL(e) };
}
function monLabel(s) { var d = ymdD(s); return TH_MON[d.getMonth()] + ' ' + String(d.getFullYear() + 543).slice(-2); }
function medalRow(n, ic) { if (!n) return ''; return '<div class="medals">' + new Array(Math.min(n, 30) + 1).join(ic) + (n > 30 ? ' <small>+' + (n - 30) + '</small>' : '') + '</div>'; }
function celList(it, ic) {
  return it.map(function (x) { return '<div class="celi"><span>' + ic + '</span><span>' + esc(x.t || x.title) + (x.p || x.rm ? '<div class="p">' + esc(x.p || x.rm) + (x.at ? ' · ' + esc(beDMY(x.at)) : '') + '</div>' : '') + '</span></div>'; }).join('');
}
function celSec(k, icon, title, n, body) {
  var o = !!S.celO[k];
  return '<div class="celsec"><button class="celh" data-act="celsec" data-v="' + k + '" aria-expanded="' + o + '"><span style="font-size:20px">' + icon + '</span><span class="t">' + title + '</span><span class="n">' + n + '</span><span class="cv">›</span></button>' + (o ? '<div class="celb">' + body() + '</div>' : '') + '</div>';
}
function celPeriod(k) {
  var off = S.celOff[k] || 0, r = celRange(k, off), c = cel(), first = c.first || todayStr();
  var lab = k === 'd' ? (off === 0 ? 'วันนี้' : off === -1 ? 'เมื่อวาน' : '') + ' ' + beDMY(r.a) : k === 'w' ? (off === 0 ? 'สัปดาห์นี้ ' : '') + beDMY(r.a) + ' – ' + beDMY(r.b) : (off === 0 ? 'เดือนนี้ ' : '') + monLabel(r.a);
  var nav = '<div class="celnav"><button data-act="celnav" data-v="' + k + ':-1" aria-label="ก่อนหน้า"' + (r.a <= first ? ' disabled' : '') + '>‹</button><b>' + esc(lab.trim()) + '</b><button data-act="celnav" data-v="' + k + ':1" aria-label="ถัดไป"' + (off >= 0 ? ' disabled' : '') + '>›</button></div>';
  var tasks = cel().list.filter(function (x) { return x.d >= r.a && x.d <= r.b; }), ns = celSum(r.a, r.b), old = c.from && r.a < c.from;
  var tl = tasks.length ? celList(tasks, '🥈') : '<div class="empty" style="padding:6px 0">' + (ns ? '' : 'ยังไม่มีงานที่เสร็จ') + '</div>';
  if (old && ns > tasks.length) tl += '<div style="font-size:12px;color:var(--mute)">รายชื่องานเก็บย้อนหลัง ' + Math.round((Date.now() - ymdD(c.from)) / 864e5) + ' วัน — ช่วงนี้เสร็จทั้งหมด ' + ns + ' งาน</div>';
  if (k === 'd') return nav + medalRow(ns, '🥈') + tl;
  var gold = celGold(r.a, r.b), wk = weekDone();
  return nav + (k === 'w' && off === 0 && wk.length ? '<button class="cele" data-act="party" style="padding:10px 14px"><span class="boing">🎉</span><span class="col"><span class="t">เปิดฉลอง!</span><span class="s">7 วันนี้จบ ' + wk.length + ' project</span></span></button>' : '') +
    '<div class="celsub" style="color:#8A6A00">🥇 Project ที่จบ (' + gold.length + ')</div>' + medalRow(gold.length, '🥇') + (gold.length ? celList(gold, '🥇') : '<div class="empty" style="padding:6px 0">ยังไม่มี project ที่จบ</div>') +
    '<div class="celsub" style="color:#5B6474">🥈 งานที่เสร็จ (' + ns + ')</div>' + medalRow(ns, '🥈') + tl;
}
/* ช่องกราฟ: เดือน = ทุกเดือนตั้งแต่เริ่มจด (สูงสุด 24) · สัปดาห์ = 12 สัปดาห์ · วัน = 30 วัน */
function celBuckets(rg) {
  var out = [], first = cel().first || todayStr(), i, r;
  if (rg === 'm') { var f = ymdD(first), n = new Date(), nm = (n.getFullYear() - f.getFullYear()) * 12 + n.getMonth() - f.getMonth(); for (i = -Math.min(nm, 23); i <= 0; i++) { r = celRange('m', i); out.push({ a: r.a, b: r.b, l: TH_MON[ymdD(r.a).getMonth()], f: monLabel(r.a) }); } }
  else if (rg === 'w') { for (i = -11; i <= 0; i++) { r = celRange('w', i); out.push({ a: r.a, b: r.b, l: beDMY(r.a).slice(0, 5), f: beDMY(r.a) + ' – ' + beDMY(r.b) }); } }
  else { for (i = -29; i <= 0; i++) { r = celRange('d', i); out.push({ a: r.a, b: r.b, l: String(+r.a.slice(8)), f: beDMY(r.a) }); } }
  return out;
}
function celChart() {
  var g = S.celG, B = celBuckets(g.r), gold = g.k === 'g', col = gold ? '#C9971C' : '#8C96A8', unit = gold ? 'project' : 'งาน';
  B.forEach(function (x) { x.v = gold ? celGold(x.a, x.b).length : celSum(x.a, x.b); });
  var max = Math.max(1, Math.max.apply(null, B.map(function (x) { return x.v; }))), W = 320, Ht = 150, top = 14, bot = 22, ph = Ht - top - bot, bw = W / B.length, gap = Math.max(2, bw * 0.25);
  var step = B.length > 24 ? 5 : B.length > 12 ? 2 : 1, sel = S.celBar != null && B[S.celBar] ? S.celBar : B.length - 1, s = '';
  s += '<line x1="0" x2="' + W + '" y1="' + (top + ph) + '" y2="' + (top + ph) + '" stroke="#C9D0DC" stroke-width="1"/>';
  s += '<text x="0" y="10" font-size="10" fill="#566174">สูงสุด ' + max + '</text>';
  B.forEach(function (x, i) {
    var h = x.v ? Math.max(3, x.v / max * ph) : 0, X = i * bw + gap / 2, w = bw - gap;
    s += '<g class="bar" data-act="celbar" data-v="' + i + '"><title>' + esc(x.f) + ': ' + x.v + ' ' + unit + '</title><rect x="' + (i * bw) + '" y="0" width="' + bw + '" height="' + Ht + '" fill="transparent"/>' +
      (h ? '<rect x="' + X.toFixed(1) + '" y="' + (top + ph - h).toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" rx="' + Math.min(4, w / 2).toFixed(1) + '" fill="' + col + '" opacity="' + (i === sel ? 1 : 0.55) + '"/>' : '') + '</g>';
    if (i % step === (B.length - 1) % step) s += '<text x="' + (i * bw + bw / 2).toFixed(1) + '" y="' + (Ht - 6) + '" font-size="10" text-anchor="middle" fill="' + (i === sel ? '#141B2B' : '#566174') + '">' + esc(x.l) + '</text>';
  });
  var seg = function (key, opts) { return '<div class="seg2" role="group">' + opts.map(function (o) { return '<button data-act="celg" data-v="' + key + ':' + o[0] + '" class="' + (g[key] === o[0] ? 'on' : '') + '">' + o[1] + '</button>'; }).join('') + '</div>'; };
  return seg('r', [['m', 'รายเดือน'], ['w', 'รายสัปดาห์'], ['d', 'รายวัน']]) + seg('k', [['s', '🥈 งานเสร็จ'], ['g', '🥇 Project จบ']]) +
    '<div style="font-size:14px"><b>' + esc(B[sel].f) + '</b> · ' + B[sel].v + ' ' + unit + '</div>' +
    '<div class="celg"><svg viewBox="0 0 ' + W + ' ' + Ht + '" role="img" aria-label="กราฟ' + unit + 'ที่เสร็จ ' + esc(B[0].f) + ' ถึง ' + esc(B[B.length - 1].f) + '">' + s + '</svg></div>';
}
function celStats() {
  var c = cel(), t = c.t, tot = celTot(), first = c.first || todayStr(), nd = Math.max(1, Math.round((ymdD(todayStr()) - ymdD(first)) / 864e5) + 1);
  var bestD = '', bestDn = 0, mon = {}, k;
  for (k in t) { if (t[k] > bestDn) { bestDn = t[k]; bestD = k; } mon[k.slice(0, 7)] = (mon[k.slice(0, 7)] || 0) + t[k]; }
  var bestM = '', bestMn = 0; for (k in mon) if (mon[k] > bestMn) { bestMn = mon[k]; bestM = k; }
  var cur = 0, d = new Date(); if (!t[ymdL(d)]) d.setDate(d.getDate() - 1); while (t[ymdL(d)]) { cur++; d.setDate(d.getDate() - 1); }
  var longest = 0, run = 0, prev = null; Object.keys(t).filter(function (x) { return t[x] > 0; }).sort().forEach(function (x) { var dx = ymdD(x); run = prev && Math.round((dx - prev) / 864e5) === 1 ? run + 1 : 1; prev = dx; if (run > longest) longest = run; });
  var cell = function (a, b) { return '<div><b>' + a + '</b><span>' + b + '</span></div>'; };
  return '<div class="celst">' + cell(esc(beDMY(first)), 'เริ่มจดงาน (' + nd + ' วัน)') + cell((tot.s / nd * 7).toFixed(1), 'งานเสร็จเฉลี่ย / สัปดาห์') +
    cell(tot.s, 'งานเสร็จทั้งหมด 🥈') + cell(tot.g, 'project จบทั้งหมด 🥇') +
    cell(bestD ? bestDn + ' งาน' : '-', 'วันที่ทำได้มากสุด' + (bestD ? ' ' + esc(beDMY(bestD)) : '')) + cell(bestM ? bestMn + ' งาน' : '-', 'เดือนที่ดีที่สุด' + (bestM ? ' ' + esc(monLabel(bestM + '-01')) : '')) +
    cell(cur + ' วัน', 'ทำงานเสร็จติดกันตอนนี้') + cell(longest + ' วัน', 'ติดกันนานสุด') + '</div>' + celChart();
}
function celVault() {
  var tot = celTot(), c = cel(), mon = {}, k;
  for (k in c.t) { var m = k.slice(0, 7); (mon[m] = mon[m] || { s: 0, g: 0 }).s += c.t[k]; }
  arch().done.forEach(function (x) { if (!x.at) return; var m = x.at.slice(0, 7); (mon[m] = mon[m] || { s: 0, g: 0 }).g++; });
  var rows = Object.keys(mon).sort().reverse().map(function (m) { var o = mon[m]; return '<div class="celi" style="align-items:center"><span style="width:62px;flex-shrink:0;font-weight:600">' + esc(monLabel(m + '-01')) + '</span><span style="flex:1;font-size:13px">🥇 ' + o.g + ' · 🥈 ' + o.s + '</span></div>'; }).join('');
  return '<div class="celtot"><div style="background:#FFF4CC;color:#6B5200"><b>🥇 ' + tot.g + '</b><span>เหรียญทอง · project ที่จบ</span></div><div style="background:#EEF1F6;color:#3F4756"><b>🥈 ' + tot.s + '</b><span>เหรียญเงิน · งานที่เสร็จ</span></div></div>' +
    medalRow(tot.g, '🥇') + '<div class="celsub">แยกรายเดือน</div>' + (rows || '<div class="empty">ยังไม่มีเหรียญ</div>') +
    (tot.g ? '<div class="celsub" style="color:#8A6A00">🥇 ทุก project ที่จบ</div>' + celList(arch().done, '🥇') : '');
}
function viewCel() {
  var dr = celRange('d', 0), wr = celRange('w', 0), mr = celRange('m', 0), tot = celTot();
  return '<div class="sheet" data-act="celx"><div class="box" role="dialog" aria-label="ฉลอง & เหรียญ" style="background:#FAF7EE"><div class="shx" style="background:#FAF7EE"><h3>🏅 ฉลอง & เหรียญ</h3><button data-act="celx" aria-label="ปิด">✕</button></div>' +
    celSec('d', '📅', 'ประจำวัน', '🥈 ' + celSum(dr.a, dr.b), function () { return celPeriod('d'); }) +
    celSec('w', '🗓', 'ประจำสัปดาห์', '🥇 ' + celGold(wr.a, wr.b).length + ' 🥈 ' + celSum(wr.a, wr.b), function () { return celPeriod('w'); }) +
    celSec('m', '📆', 'ประจำเดือน', '🥇 ' + celGold(mr.a, mr.b).length + ' 🥈 ' + celSum(mr.a, mr.b), function () { return celPeriod('m'); }) +
    celSec('v', '🏆', 'คลังเหรียญทั้งหมด', '🥇 ' + tot.g + ' 🥈 ' + tot.s, celVault) +
    celSec('s', '📊', 'สถิติ & กราฟ', 'ตั้งแต่ ' + beDMY(cel().first || todayStr()), celStats) +
    '<button data-act="celx" style="height:44px;border:0;background:var(--soft);border-radius:10px;font-weight:600;margin-top:4px">ปิด</button></div></div>';
}
var CF = ['#FFC21A',""")
OUT=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
L,S=ck(OUT)
open('Code.v58.gs','w',encoding='utf8',newline='').write(OUT)
if os.environ.get('VEE_DEV'):
    open('app.v58.html','w',encoding='utf8',newline='').write(H); open('Code.gs','w',encoding='utf8',newline='').write(OUT)
print('OK Code.v58.gs length',L,'checksum',S)
