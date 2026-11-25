# v63: การ์ด project — หลอดความคืบหน้าแบบ HP (ล็อก 🔒 แก้ผ่าน ✏️ แก้ %) + milestone จุดในหลอด ป้ายสลับบน/ล่าง
#      + "✓ task done" ผูกเข้าจุดเองตามวันที่เสร็จ · หน้า ✏️ แก้ % = slider + timeline เต็ม (กล่อง 6 บรรทัด เลื่อนดู)
#  ข้อมูล: จุด % จาก Process ("dd/mm/yy ความคืบหน้า N%" ที่แอปเขียนอยู่แล้ว) · งานเสร็จจากแท็บ Tasks (เสร็จเมื่อ)
# รันในโฟลเดอร์ที่มี Code.v62.gs : python patch63.py  → ได้ Code.v63.gs
import json,re
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v62.gs',encoding='utf8').read()
assert ck(B)==(593650,3228),('base ไม่ใช่ v62',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v62';","var APP_VER = 'v63';")
C=rep(C,"""      pct: o.v[10] === '' || o.v[10] == null ? null : Math.max(0, Math.min(100, Math.round(Number(o.v[10]) || 0))) };
    if (isParked(r)""","""      pct: o.v[10] === '' || o.v[10] == null ? null : Math.max(0, Math.min(100, Math.round(Number(o.v[10]) || 0))),
      created: isDate(o.v[9]) ? o.v[9] : null };
    if (isParked(r)""")
C=rep(C,"""  var doneN = {}; tasks.forEach(function (t) { if (t.status === 'เสร็จ' && t.projectId) doneN[t.projectId] = (doneN[t.projectId] || 0) + 1; });""",
"""  var doneN = {}, doneBy = {}; tasks.forEach(function (t) { if (t.status === 'เสร็จ' && t.projectId) { doneN[t.projectId] = (doneN[t.projectId] || 0) + 1; if (t.doneAt) (doneBy[t.projectId] = doneBy[t.projectId] || []).push({ t: String(t.title || ''), d: ymd(t.doneAt) }); } });""")
C=rep(C,"""      plan: String(r.plan || '').trim(), pct: r.pct, done: doneN[r.id] || 0,""",
"""      plan: String(r.plan || '').trim(), pct: r.pct, done: doneN[r.id] || 0,
      ms: pjMilestones(r.process), start: r.created ? ymd(r.created) : '', last: r.last ? ymd(r.last) : '', // v63: timeline
      dn: (doneBy[r.id] || []).sort(function (a, b) { return a.d < b.d ? -1 : a.d > b.d ? 1 : 0; }).slice(-60),""")
C=C.rstrip('\n')+'\n'+r"""
/* ============================================================
 *  v63: timeline ของ project — อ่านบรรทัดใน Process (ล่าสุดอยู่บนสุด) เป็นรายการเก่า→ใหม่
 *  "25/11/69 ความคืบหน้า 20%" → { d: '2026-11-25', pct: 20 } · บรรทัดอื่นที่มีวันที่ → { d, x: ข้อความ }
 *  ปีในชีทเป็น พ.ศ. 2 หลัก (≥60) หรือ ค.ศ. 2 หลัก (บันทึกเก่า) หรือ 4 หลัก
 * ============================================================ */
function pjMilestones(proc) {
  var out = [];
  String(proc || '').split('\n').forEach(function (l) {
    var m = /^\s*(\d{1,2})\/(\d{1,2})\/(\d{2,4})\s+(.+?)\s*$/.exec(l); if (!m) return;
    var y = +m[3]; if (m[3].length <= 2) y = y >= 60 ? 2500 + y - 543 : 2000 + y; else if (y > 2400) y -= 543;
    var mo = +m[2], da = +m[1]; if (mo < 1 || mo > 12 || da < 1 || da > 31) return;
    var d = y + '-' + (mo < 10 ? '0' : '') + mo + '-' + (da < 10 ? '0' : '') + da, rest = m[4];
    var pm = /^ความคืบหน้า\s*(\d{1,3})\s*%$/.exec(rest);
    if (pm) out.push({ d: d, pct: Math.min(100, +pm[1]) });
    else if (!/^📌|^▶️|เสร็จ 100%/.test(rest)) out.push({ d: d, x: rest.slice(0, 120) });
  });
  return out.reverse().slice(-40);
}
"""
# ---------------- แอป ----------------
H=rep(H,".blk h4{",""".pbh{display:flex;justify-content:space-between;align-items:center}
.pbh button{border:1px solid var(--line);background:#fff;border-radius:16px;height:32px;padding:0 12px;font-size:13px;font-weight:600;color:var(--pj)}
.pbu,.pbd{position:relative}
.pbt{position:relative;height:34px;background:#E6EAF0;border-radius:17px;box-shadow:inset 0 1px 2px rgba(0,0,0,.08)}
.pbf{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(180deg,#3C8A5C,#2E6B47);border-radius:17px 0 0 17px;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;color:#fff;font-weight:700;font-size:16px;overflow:hidden}
.pbf.full{border-radius:17px}
.pbf::after{content:'';position:absolute;left:8px;right:8px;top:3px;height:8px;border-radius:4px;background:rgba(255,255,255,.18)}
.pbo{position:absolute;top:0;bottom:0;display:flex;align-items:center;font-size:16px;font-weight:700;color:var(--pj)}
.pbr{position:absolute;right:12px;top:0;bottom:0;display:flex;align-items:center;font-size:13px;color:var(--mute);font-weight:600}
.pbm{position:absolute;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:var(--pj);border:2px solid #fff;z-index:2;top:-5px}
.pbm.b{top:auto;bottom:-5px}
.pbl{position:absolute;font-size:11px;line-height:15px;color:var(--mute);padding-left:6px;border-left:1px solid #A8D8BA;overflow:hidden}
.pbu .pbl{bottom:0;padding-bottom:5px}.pbd .pbl{top:0;padding-top:5px}
.pbl.r{border-left:0;border-right:1px solid #A8D8BA;padding:0 6px 0 0;text-align:right;transform:translateX(-100%)}
.pbu .pbl.r{padding-bottom:5px}.pbd .pbl.r{padding-top:5px}
.pbl span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pbl b{color:var(--pj)}.pbl i{font-style:normal;color:#33503F}
.pbe{border:2px solid var(--pj)!important;box-shadow:0 0 0 3px var(--pj-head)}
.ptl{max-height:150px;overflow-y:auto;border:1px solid var(--line);border-radius:10px;padding:6px 10px 6px 26px;background:#FCFDFC;-webkit-overflow-scrolling:touch}
.ptl .ln{position:relative;font-size:13px;line-height:24px;min-height:24px;display:flex;gap:8px;align-items:baseline}
.ptl .ln::before{content:'';position:absolute;left:-17px;top:0;bottom:0;border-left:2px solid var(--pj-head)}
.ptl .ln.m::after{content:'';position:absolute;left:-21px;top:7px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--pj)}
.ptl .ln.m.now::after{background:var(--pj)}.ptl .ln.m.s::after{border-color:var(--pause)}
.ptl .ln b{color:var(--pj)}.ptl .ln .d{color:var(--mute);font-size:12px;white-space:nowrap}
.ptl .ln.t{font-size:12px;color:#33503F;padding-left:8px}.ptl .ln.t .tt{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ptl .ln.n{color:var(--mute)}
.blk h4{""")
H=rep(H,"  S.sheet = id; S.steps = null; S.pe = null;","  S.sheet = id; S.steps = null; S.pe = null; S.pfe = false;")
a=H.index("  // ความคืบหน้า\n  h += '<div class=\"blk\"><h4>ความคืบหน้า</h4>")
b=H.index("  h += logB;",a)
H=H[:a]+r"""  // v63: ความคืบหน้า — หลอด HP ล็อกไว้ · ✏️ แก้ % = slider + timeline เต็ม
  h += S.pfe ? viewPEdit(p, pf) : viewPBar(p);
"""+H[b:]
PB_JS=r"""
/* ---------- v63: หลอดความคืบหน้า + milestone ---------- */
function pjPts(p) { // จุด: [เริ่ม 0%] + จุด % (เก่า→ใหม่) · งานเสร็จ/บันทึกผูกเข้าจุดแรกที่วันที่ ≥ วันที่เสร็จ (เกินจุดล่าสุด → จุดล่าสุด)
  var cur = p.pct == null ? 0 : +p.pct, ms = p.ms || [], raw = [];
  ms.forEach(function (m) { if (m.pct != null && m.pct > 0) raw.push({ pct: +m.pct, d: m.d, tk: [], nt: [] }); });
  if (cur > 0 && (!raw.length || raw[raw.length - 1].pct !== cur)) raw.push({ pct: cur, d: p.last || todayStr(), tk: [], nt: [] });
  var pts = [], lim = 101;
  for (var i = raw.length - 1; i >= 0; i--) if (raw[i].pct < lim) { pts.unshift(raw[i]); lim = raw[i].pct; } // % ลดลงทีหลัง → ตัดจุดเก่าที่สูงกว่าทิ้ง
  var first = (ms[0] && ms[0].d) || ((p.dn || [])[0] || {}).d || '';
  var st = { pct: 0, d: p.start || first, tk: [], nt: [], s: true };
  if (st.d && pts.length && st.d > pts[0].d) st.d = pts[0].d;
  var all = [st].concat(pts);
  var put = function (d, fn) { var t = null; for (var k = 0; k < all.length; k++) if (all[k].d >= d) { t = all[k]; break; } fn(t || all[all.length - 1]); };
  (p.dn || []).forEach(function (x) { put(x.d, function (t) { t.tk.push(x); }); });
  ms.forEach(function (m) { if (m.x) put(m.d, function (t) { t.nt.push(m); }); });
  return all;
}
function viewPBar(p) {
  var cur = p.pct == null ? 0 : +p.pct, all = pjPts(p), show = all.length > 5 ? [all[0]].concat(all.slice(-4)) : all;
  var labs = show.slice().reverse().map(function (pt, k) { return { pt: pt, up: k % 2 === 0 }; }); // ใหม่สุดอยู่บน สลับลง
  var side = function (up) { return labs.filter(function (l) { return l.up === up; }).sort(function (a, b) { return a.pt.pct - b.pt.pct; }); };
  var lines = function (pt, wide) {
    var r = pt.s ? ['<span><b>เริ่ม</b></span>'].concat(pt.d ? ['<span>' + esc(beDMY(pt.d)) + '</span>'] : []) : ['<span><b>' + pt.pct + '%</b>' + (pt.d ? ' · ' + esc(beDMY(pt.d)) : '') + '</span>'];
    var tk = pt.tk.slice().reverse();
    tk.slice(0, 2).forEach(function (t, i) { r.push('<span><i>✓ ' + esc(t.t) + '</i>' + (i === 1 && tk.length > 2 ? ' +' + (tk.length - 2) : '') + '</span>'); });
    return r;
  };
  var hU = 0, hD = 0, out = { u: '', d: '' }, dots = '';
  [true, false].forEach(function (up) {
    var L = side(up);
    L.forEach(function (l, i) {
      var nx = L[i + 1], x = l.pt.pct, right = false, mw;
      if (!nx && 100 - x < 28 && x > 30) { right = true; mw = Math.min(42, x - (L[i - 1] ? L[i - 1].pt.pct : 0) - 1); }
      else mw = (nx ? nx.pt.pct : 100) - x - 1;
      l.right = right; l.mw = mw;
    });
    // ถ้าป้ายสุดท้ายชิดขวา ป้ายก่อนหน้าต้องหยุดก่อนขอบซ้ายของมัน
    var last = L[L.length - 1];
    if (last && last.right && L.length > 1) { var pv = L[L.length - 2]; pv.mw = Math.max(6, last.pt.pct - last.mw - pv.pt.pct - 1); }
    L.forEach(function (l) {
      var ls = lines(l.pt, l.mw > 18), h = ls.length * 15 + 6;
      if (up) hU = Math.max(hU, h); else hD = Math.max(hD, h);
      out[up ? 'u' : 'd'] += '<div class="pbl' + (l.right ? ' r' : '') + '" style="left:' + Math.max(l.pt.pct, 0) + '%;max-width:' + Math.max(l.mw, 6) + '%">' + ls.join('') + '</div>';
      if (!l.pt.s && l.pt.pct < 100) dots += '<span class="pbm' + (up ? '' : ' b') + '" style="left:' + l.pt.pct + '%"></span>';
    });
  });
  all.forEach(function (pt) { if (!pt.s && pt.pct < 100 && show.indexOf(pt) < 0) dots += '<span class="pbm" style="left:' + pt.pct + '%;opacity:.6"></span>'; });
  var fill = cur > 0 ? '<div class="pbf' + (cur >= 100 ? ' full' : '') + '" style="width:' + cur + '%">' + (cur >= 14 ? cur + '%' : '') + '</div>' : '';
  var outTxt = cur < 14 ? '<span class="pbo" style="left:calc(' + cur + '% + 10px)">' + cur + '%</span>' : '';
  var left = 100 - cur >= 22 ? '<span class="pbr">เหลืออีก ' + (100 - cur) + '%</span>' : '';
  return '<div class="blk"><div class="pbh"><h4>ความคืบหน้า 🔒</h4><button data-act="pfedit" data-id="' + esc(p.id) + '" aria-label="ปลดล็อกเพื่อแก้ความคืบหน้า">✏️ แก้ %</button></div>' +
    '<div class="pbu" style="height:' + hU + 'px">' + out.u + '</div>' +
    '<div class="pbt" role="img" aria-label="ความคืบหน้า ' + cur + '%">' + fill + outTxt + left + dots + '</div>' +
    '<div class="pbd" style="height:' + hD + 'px">' + out.d + '</div>' +
    (p.plan ? '<div style="border-top:1px solid var(--soft);padding-top:8px;margin-top:2px"><div style="font-size:12px;color:var(--mute);font-weight:600">เหลืออะไรบ้าง / ทำต่อครั้งหน้า</div><div style="font-size:14px;white-space:pre-line">' + esc(p.plan) + '</div></div>' : '') +
    '<button data-act="carry" data-id="' + esc(p.id) + '" style="height:40px;border-radius:10px;border:1px solid var(--pj);background:#fff;color:var(--pj);font-weight:600">📌 ทดไปพรุ่งนี้</button></div>';
}
function pjTimeline(p) {
  var all = pjPts(p), h = '';
  var wd = function (s) { var q = String(s || '').split('-'); return q.length < 3 ? '' : WD_TH[new Date(+q[0], +q[1] - 1, +q[2]).getDay()] + ' '; };
  all.slice().reverse().forEach(function (pt, i) {
    h += '<div class="ln m' + (i === 0 && !pt.s ? ' now' : '') + (pt.s ? ' s' : '') + '">' + (pt.s ? '<b style="color:var(--mute)">เริ่ม</b>' : '<b>' + pt.pct + '%</b>') +
      ' <span class="d">' + (pt.d ? wd(pt.d) + beDMY(pt.d) : '') + (i === 0 && !pt.s ? ' · ล่าสุด' : '') + '</span></div>';
    pt.tk.slice().reverse().forEach(function (t) { h += '<div class="ln t"><span class="tt">✓ ' + esc(t.t) + '</span><span class="d">' + esc(beDMY(t.d)) + '</span></div>'; });
    pt.nt.slice().reverse().forEach(function (n) { h += '<div class="ln t n"><span class="tt">↳ ' + esc(n.x) + '</span></div>'; });
  });
  return all.length > 1 || all[0].tk.length || all[0].nt.length ? h : '<div class="ln n" style="color:var(--mute);font-size:12px">ยังไม่มีประวัติ — บันทึก % ครั้งแรกจะเป็นจุดแรก</div>';
}
function viewPEdit(p, pf) {
  var o = p.pct == null ? 0 : +p.pct, d = pf.pct - o;
  return '<div class="blk pbe"><div class="pbh"><h4>แก้ความคืบหน้า</h4><span style="font-size:12px;color:var(--mute)">เดิม ' + o + '%</span></div>' +
    '<div class="pbh"><b id="pf-pctv" style="font-size:26px;color:var(--pj)">' + pf.pct + '%</b><span id="pf-left" style="font-size:12px;color:var(--pj);font-weight:600">' + pfDiff(d) + '</span></div>' +
    '<label class="sr" for="pf-pct">เลื่อนความคืบหน้า</label><input id="pf-pct" data-pf="pct" type="range" min="0" max="100" step="5" value="' + pf.pct + '">' +
    '<label>เส้นทางที่ผ่านมา</label><div class="ptl">' + pjTimeline(p) + '</div>' +
    '<label for="pf-plan">เหลืออะไรบ้าง / ทำต่อครั้งหน้า</label><textarea id="pf-plan" data-pf="plan" placeholder="เช่น ตัดต่อคลิป 2 ตอนที่เหลือ">' + esc(pf.plan) + '</textarea>' +
    '<div class="two"><button id="pf-save" data-act="psave" data-id="' + esc(p.id) + '" style="border:0;background:var(--pj);color:#fff">' + pfSaveTxt(pf.pct, o) + '</button>' +
    '<button data-act="pfcancel" style="border:1px solid var(--line);background:#fff;color:var(--mute)">ยกเลิก</button></div></div>';
}
function pfDiff(d) { return d > 0 ? '+' + d + '% 🎯' : d < 0 ? d + '%' : ''; }
function pfSaveTxt(v, o) { return +v === 100 ? '🎉 บันทึก · เสร็จแล้ว' : +v !== +o ? 'บันทึก → ปักหมุด ' + v + '%' : 'บันทึก'; }
"""
H=rep(H,"function viewSheet() {",PB_JS.strip('\n')+"\nfunction viewSheet() {")
H=rep(H,"""  if (act === 'pedit') {""","""  if (act === 'pfedit') { var pz = findP(id); if (!pz) return; S.pfe = true; S.pf.pct = pz.pct == null ? 0 : pz.pct; S.pf.plan = pz.plan || ''; return render(); }
  if (act === 'pfcancel') { S.pfe = false; return render(); }
  if (act === 'pedit') {""")
H=rep(H,"""    if (pct === 100) return finishP(pp, plan);
    toast('📈 ' + pp.title + ' ' + pct + '%');
    return api('progress', { pid: id, pct: pct, plan: plan }, function () { pp.pct = pct; pp.plan = plan; if (plan) pp.next = plan; });""",
"""    if (pct === 100) return finishP(pp, plan);
    toast('📈 ' + pp.title + ' ' + pct + '%'); S.pfe = false;
    return api('progress', { pid: id, pct: pct, plan: plan }, function () { if (+pp.pct !== pct) { pp.ms = (pp.ms || []).concat([{ d: todayStr(), pct: pct }]); pp.last = todayStr(); } pp.pct = pct; pp.plan = plan; if (plan) pp.next = plan; });""")
H=rep(H,"""    if (q === 'pct') { $('pf-pctv').textContent = el.value + '%'; $('pf-left').textContent = 'เหลืออีก ' + (100 - el.value) + '%'; }""",
"""    if (q === 'pct') { var po = findP(S.sheet), o0 = po && po.pct != null ? +po.pct : 0; $('pf-pctv').textContent = el.value + '%'; $('pf-left').textContent = pfDiff(el.value - o0); if ($('pf-save')) $('pf-save').textContent = pfSaveTxt(el.value, o0); }""")
H=rep(H,"  if (act === 'close') { if (ev.target !== el) return; S.sheet = null; S.pe = null; return render(); }","  if (act === 'close') { if (ev.target !== el) return; S.sheet = null; S.pe = null; S.pfe = false; return render(); }")
out=C+'/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
open('Code.v63.gs','w',encoding='utf8',newline='\n').write(out)
print('OK Code.v63.gs',ck(out))
