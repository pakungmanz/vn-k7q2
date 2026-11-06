# v54: แมววีบอกเมื่อยังไม่ได้บันทึก · บันทึกความคืบหน้าในการ์ด · แยก project/ไอเดีย · ย้าย ⇄ · ลบ (ยืนยันก่อน)
# รันในโฟลเดอร์ vee-note-v20 ที่มี Code.v53.gs (= v53b) + app.html + assets/cat.png : python patch54.py
import json,re,base64
CATB64='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'
import os
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
BASE=None
for fn in ['Code.v53b.gs','Code.v53.gs']:
    if os.path.exists(fn) and ck(open(fn,encoding='utf8').read())==(437589,8710): BASE=fn; break
assert BASE,'ไม่พบไฟล์ v53b (checksum 437589/8710)'
print('base',BASE)
B=open(BASE,encoding='utf8').read()
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v53b';","var APP_VER = 'v54';")
C=rep(C,": (old === ST_IDEA && note ? ST_ACTIVE : old);",": old; // v54: จดความคืบหน้าบนไอเดีย ไม่ทำให้ไอเดียกลายเป็น project เอง")
C=rep(C,"function setProjectStatus(id, st) { return updateProject(id, '', null, st); }\n","""function setProjectStatus(id, st) { return updateProject(id, '', null, st); }
/** v54: ไอเดียกับ project แยกกัน — เริ่มทำไอเดีย = สร้าง project ใหม่ (สำเนาชื่อ/รายละเอียด/หมวด) ไอเดียต้นทางยังอยู่ · คืน project ใหม่ (สถานะยังเป็นไอเดีย ให้คนเรียกตั้งเป็นกำลังทำเอง) */
var SPAWN_NOTE = '▶️ เริ่มเป็น project แล้ว';
function spawnProject(id) {
  var o = findRow('roadmap', id);
  if (!o) return null;
  var nid = newId('R'), now = new Date(), sh = sheet('roadmap');
  sh.appendRow([nid, o.v[1], o.v[2], o.v[3], '', '', '', ST_IDEA, now, now]);
  sh.getRange(o.row, 5).setValue(dmy(now) + ' ' + SPAWN_NOTE + (o.v[4] ? '\\n' + o.v[4] : ''));
  return projectById(nid);
}
""")
C=rep(C,"          if (pjOf && pjOf.status === ST_DONE) pjOf = null;\n","          if (pjOf && pjOf.status === ST_DONE) pjOf = null;\n          if (pjOf && pjOf.status === ST_IDEA) pjOf = spawnProject(pjOf.id) || pjOf; // v54: จดงานให้ไอเดีย = สร้าง project ใหม่ ไอเดียยังอยู่\n")
C=rep(C,"  var u = setProjectStatus(r.id, ST_ACTIVE);\n  var head = '▶️ เริ่มทำ: '","  if (r.status === ST_IDEA) r = spawnProject(r.id) || r; // v54\n  var u = setProjectStatus(r.id, ST_ACTIVE);\n  var head = '▶️ เริ่มทำ: '")
C=rep(C,"    else { setProjectStatus(a.id, ST_ACTIVE); msg = '▶️ เริ่มทำ ' + p.title; }","    else { var fromIdea = p.status === ST_IDEA; if (fromIdea) p = spawnProject(p.id) || p; setProjectStatus(p.id, ST_ACTIVE); msg = '▶️ เริ่มทำ ' + p.title + (fromIdea ? ' (ไอเดียต้นทางยังอยู่)' : ''); }")
C=rep(C,"      if (pp.status !== ST_ACTIVE) setProjectStatus(pp.id, ST_ACTIVE);","      if (pp.status === ST_IDEA) pp = spawnProject(pp.id) || pp;\n      if (pp.status !== ST_ACTIVE) setProjectStatus(pp.id, ST_ACTIVE);")
C=rep(C,"  } else if (action === 'archive') {","""  } else if (action === 'toproject') { // v54: AI ลงผิด → ย้ายไอเดียไปเป็น project (ช่องเต็ม = พัก)
    var tpj = projectById(a.id);
    if (!tpj) { msg = 'ไม่พบไอเดียนี้'; warn = true; }
    else { var tfull = activeProjects().length >= MAX_ACTIVE; setProjectStatus(a.id, tfull ? ST_PAUSE : ST_ACTIVE); msg = '↪ ย้ายไป Projects: ' + tpj.title + (tfull ? ' (ทำอยู่ครบ ' + MAX_ACTIVE + ' เลยอยู่ในกลุ่มพัก)' : ''); }
  } else if (action === 'pdelete') { // v54: ลบ project/ไอเดีย ถาวร + ยกเลิกงานที่ยังไม่เสร็จของมัน
    var dpr = findRow('roadmap', a.id);
    if (!dpr) { msg = 'ไม่พบรายการนี้'; warn = true; }
    else {
      var dcn = 0;
      readRows('tasks').forEach(function (o) { if (String(o.v[11]) === String(a.id) && (o.v[5] === 'ค้าง' || o.v[5] === ST_PAUSE) && cancelItem('task', o.v[0])) dcn++; });
      var dtitle = dpr.v[2]; dpr = findRow('roadmap', a.id);
      if (dpr) sheet('roadmap').deleteRow(dpr.row);
      msg = '🗑 ลบแล้ว: ' + dtitle + (dcn ? ' · ยกเลิกงานที่ค้าง ' + dcn + ' งาน' : '');
    }
  } else if (action === 'rawtask') { // v54: แมวถามกลับ → กด "จดเป็นงานเลย"
    var rtt = String(a.text || '').trim().slice(0, 200);
    if (!rtt) { msg = 'ไม่มีข้อความ'; warn = true; }
    else { var rtk = addTask(rtt, ymd(new Date()), null, {}); msg = '📝 จดเป็นงานวันนี้: ' + rtk.title + ' · 📆 ' + rtk.calendar; }
  } else if (action === 'archive') {""")
C=rep(C,"  var msg = '', warn = false, say = '', heardTxt = '';\n  if (action === 'data') {","  var msg = '', warn = false, say = '', heardTxt = '', cat = null;\n  if (action === 'data') {")
C=rep(C,"    var cf = appCaptureFull(String(a.text || '').trim()); msg = cf.msg; say = cf.say;","    var cf = appCaptureFull(String(a.text || '').trim()); msg = cf.msg; say = cf.say;\n    if (cf.cat) cat = { ask: cf.cat, text: String(a.text || '').trim() };")
C=rep(C,"msg = '🎤 ' + heard.text + '\\n' + vf.msg; say = vf.say; heardTxt = heard.text; }","msg = '🎤 ' + heard.text + '\\n' + vf.msg; say = vf.say; heardTxt = heard.text; if (vf.cat) cat = { ask: vf.cat, text: heard.text }; }")
C=rep(C,"  return { msg: msg, warn: warn, say: say, heard: heardTxt, data: appData(true), ver: APP_VER };","  return { msg: msg, warn: warn, say: say, heard: heardTxt, cat: cat, data: appData(true), ver: APP_VER };")
C=rep(C,"  if (!parsed) return { msg: 'วีอ่านไม่ออก ลองพิมพ์ใหม่ครับ', say: 'วีฟังไม่ออก ลองพูดใหม่อีกครั้งครับ' };","  if (!parsed) return { msg: 'วีอ่านไม่ออก ลองพิมพ์ใหม่ครับ', say: 'วีฟังไม่ออก ลองพูดใหม่อีกครั้งครับ', cat: 'วีอ่านไม่ออกว่าเป็นงาน นัด หรือไอเดีย' };")
C=rep(C,"  return { msg: msg || 'จดแล้วครับ', say: say };\n}","  // v54: AI แค่ตอบ/ถามกลับ (chat ล้วน) = ยังไม่ได้บันทึกอะไร → แอปให้แมวบอก\n  var chatOnly = acts.length > 0 && acts.every(function (a) { return a.type === 'chat'; });\n  return { msg: msg || 'จดแล้วครับ', say: say, cat: chatOnly ? (msg || 'วียังไม่แน่ใจว่าจะจดเป็นอะไร') : '' };\n}")
C=rep(C,"      plan: String(r.plan || '').trim(), pct: r.pct, done: doneN[r.id] || 0,","      plan: String(r.plan || '').trim(), pct: r.pct, done: doneN[r.id] || 0,\n      log: String(r.process || '').split('\\n').map(function (l) { return l.trim(); }).filter(Boolean).slice(0, 6), spawned: String(r.process || '').indexOf(SPAWN_NOTE) >= 0,")
# ---------------- หน้าแอป ----------------
CAT='data:image/png;base64,'+CATB64
H=rep(H,"@media (prefers-reduced-motion:reduce){.boing,","""/* v54 แมววี: โผล่เมื่อยังไม่ได้บันทึก */
.catw{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(136px + env(safe-area-inset-bottom));width:min(calc(100% - 24px),536px);display:flex;align-items:flex-end;gap:10px;z-index:7}
.catav{width:68px;height:68px;flex-shrink:0;border-radius:50%;background:#DCE7F7;display:flex;align-items:flex-end;justify-content:center;position:relative;box-shadow:0 4px 14px rgba(20,27,43,.2);animation:catin .35s ease-out,cattilt 2.6s ease-in-out .5s infinite}
.catav img{width:80px;height:80px;margin-bottom:2px;pointer-events:none}
.catq{position:absolute;top:-8px;right:-6px;width:26px;height:26px;border-radius:50%;background:var(--warn);color:#fff;font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;animation:catq 1.1s ease-in-out infinite}
.vcb{flex:1;min-width:0;background:#fff;border-radius:16px 16px 16px 4px;padding:12px 14px;box-shadow:0 6px 22px rgba(20,27,43,.25);display:flex;flex-direction:column;gap:8px;font-size:14px;animation:catin .3s ease-out}
.vcb b{color:var(--warn);font-size:15px}
.vcb .q{font-size:12px;color:var(--mute);background:var(--soft);border-radius:8px;padding:6px 8px;white-space:pre-line;overflow-wrap:anywhere}
.vcb .r{display:flex;gap:6px;flex-wrap:wrap}
.vcb .r button{height:38px;padding:0 12px;border-radius:19px;border:1px solid var(--line);background:#fff;font-weight:600;font-size:13px;color:var(--ink)}
.vcb .r .p{background:var(--today);color:#fff;border-color:var(--today)}
@keyframes catin{from{transform:translateY(24px) scale(.7);opacity:0}to{transform:none;opacity:1}}
@keyframes cattilt{0%,60%,100%{transform:rotate(0)}70%{transform:rotate(-12deg)}80%{transform:rotate(9deg)}90%{transform:rotate(-4deg)}}
@keyframes catq{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@media (prefers-reduced-motion:reduce){.catav,.catq,.vcb{animation:none}}
@media (prefers-reduced-motion:reduce){.boing,""")
H=rep(H,"var CELEB = 'data:video/mp4;base64,__CELEB__';","var CELEB = 'data:video/mp4;base64,__CELEB__';\nvar CAT_IMG = '"+CAT+"';\n"+r"""/* v54: แมววีโผล่บอกเมื่อ AI ถามกลับ/อ่านไม่ออก = ยังไม่ได้บันทึก · S.cat = คิวเรื่องที่ค้าง */
function viewCat() {
  var c = S.cat && S.cat[0]; if (!c) return '';
  return '<div class="catw" role="alertdialog" aria-label="วีมีเรื่องถาม"><div class="catav"><img src="' + CAT_IMG + '" alt=""><span class="catq" aria-hidden="true">?</span></div><div class="vcb"><div><b>ยังไม่ได้บันทึกนะ</b>' + (S.cat.length > 1 ? ' <span style="font-size:12px;color:var(--mute)">(ค้างอีก ' + (S.cat.length - 1) + ' เรื่อง)</span>' : '') + '</div><div>' + esc(c.ask) + '</div>' +
    (c.text ? '<div class="q">“' + esc(c.text) + '”</div>' : '') +
    '<div class="r">' + (c.text ? '<button class="p" data-act="catsave">📝 จดเป็นงานเลย</button><button data-act="catedit">✏️ พิมพ์ใหม่</button>' : '') + '<button data-act="catx">ปิด</button></div></div></div>';
}
/* v54: ยืนยันก่อนลบเสมอ */
function viewDel() {
  var d = S.del; if (!d) return '';
  return '<div class="sheet" data-act="delbg" style="align-items:center;z-index:8"><div class="box" role="alertdialog" aria-label="ยืนยันการลบ" style="border-radius:18px;max-width:420px;margin:0 16px">' +
    '<h3 style="margin:0">ลบ' + (d.idea ? 'ไอเดีย' : ' project ') + 'นี้ถาวร?</h3><div style="font-size:15px;font-weight:600">' + esc(d.title) + '</div>' +
    '<div style="font-size:13px;color:var(--mute)">ลบแล้วกู้คืนไม่ได้' + (d.n ? ' · งานที่ยังไม่เสร็จ ' + d.n + ' งานจะถูกยกเลิกและเอาออกจากปฏิทินด้วย' : '') + '<br>ถ้าแค่อยากเก็บให้พ้นตา ใช้ 🗄 เก็บถาวร แทน</div>' +
    '<div class="two"><button data-act="delno" style="border:1px solid var(--line);background:#fff;color:var(--ink)">ยกเลิก</button><button data-act="delyes" style="border:0;background:#C62828;color:#fff">🗑 ลบเลย</button></div></div></div>';
}""")
H=rep(H,"(S.newVer ? '<button class=\"newver\"","viewCat() + (S.del ? viewDel() : '') + (S.newVer ? '<button class=\"newver\"")
H=rep(H,"    if (err) toast('⚠️ ' + (err.message || err) + '\\nดึงข้อมูลล่าสุดให้ใหม่แล้ว');","    if (res && res.cat) { (S.cat = S.cat || []).push(res.cat); var tt0 = $('toast'); if (tt0) tt0.classList.remove('on'); render(); }\n    else if (err) toast('⚠️ ' + (err.message || err) + '\\nดึงข้อมูลล่าสุดให้ใหม่แล้ว');")
H=rep(H,"  if (act === 'party') { S.arch = false; render(); return party(); }\n","""  if (act === 'party') { S.arch = false; render(); return party(); }
  if (act === 'catx') { (S.cat || []).shift(); return render(); }
  if (act === 'catsave') { var c1 = (S.cat || []).shift(); render(); if (!c1) return; toast('📝 จดเป็นงานวันนี้: ' + c1.text); return api('rawtask', { text: c1.text }); }
  if (act === 'catedit') { var c2 = (S.cat || []).shift(); S.tab = 'today'; S.sheet = null; render(); var qi = $('q'); if (qi && c2) { qi.value = c2.text; try { qi.focus(); } catch (e) {} } return; }
  if (act === 'pdel') {
    if (id && id.indexOf('tmp') === 0) return toast('กำลังบันทึกอยู่ รอแป๊บนึง');
    var dpj = findP(id) || arch().done.concat(arch().kept).filter(function (x) { return String(x.id) === String(id); })[0]; if (!dpj) return;
    S.del = { id: id, title: dpj.title, idea: dpj.status === 'i', n: (dpj.tasks || []).length }; return render();
  }
  if (act === 'delbg') { if (ev.target !== el) return; S.del = null; return render(); }
  if (act === 'delno') { S.del = null; return render(); }
  if (act === 'delyes') {
    var dd = S.del; S.del = null; S.sheet = null; if (!dd) return render();
    toast('🗑 ลบแล้ว: ' + dd.title);
    return api('pdelete', { id: dd.id }, function () { var kp = function (x) { return String(x.id) !== String(dd.id); }; var fp = findP(dd.id); if (fp) dropP(fp); var A = arch(); A.done = A.done.filter(kp); A.kept = A.kept.filter(kp); });
  }
""")
H=rep(H,"""    toast('▶️ เริ่มทำ ' + (findP(id) || {}).title);
    return api('start', { id: id }, function () { setStatus(id, 'a'); });
  }""","""    var sp = findP(id) || {};
    toast('▶️ เริ่มทำ ' + sp.title + (sp.status === 'i' ? '\\nไอเดียต้นทางยังเก็บไว้ที่เดิม' : ''));
    return api('start', { id: id }, function () {
      if (sp.status === 'i') { sp.spawned = true; D.projects.push({ id: 'tmp' + (++tmpN), title: sp.title, rm: sp.rm, status: 'a', next: '', plan: '', pct: null, done: 0, detail: sp.detail, tasks: [], log: [] }); }
      else setStatus(id, 'a');
    });
  }
  if (act === 'toproject') {
    S.sheet = null;
    var tp0 = findP(id) || {}, full = D.projects.filter(function (p) { return p.status === 'a'; }).length >= D.max;
    toast('↪ ย้ายไป Projects: ' + tp0.title + (full ? '\\n(ทำอยู่ครบ ' + D.max + ' เลยอยู่ในกลุ่มพัก)' : ''));
    return api('toproject', { id: id }, function () { setStatus(id, full ? 'p' : 'a'); });
  }""")
H=rep(H,"toast((act === 'pause' ? '⏸ พัก ' : '💡 เก็บเป็นไอเดีย ') + (findP(id) || {}).title);","toast((act === 'pause' ? '⏸ พัก ' : '↪ ย้ายไปไอเดีย: ') + (findP(id) || {}).title);")
# Projects: เฉพาะ กำลังทำ / พัก
H=rep(H,"[['a', 'กำลังทำ'], ['i', 'ไอเดีย'], ['p', 'พัก']]","[['a', 'กำลังทำ'], ['p', 'พัก']]",2)
H=rep(H,"  var P = D.projects, groups;","  var P = D.projects.filter(function (p) { return p.status !== 'i'; }), groups; // v54: ไอเดียอยู่หน้าไอเดียอย่างเดียว")
# ไอเดีย: เฉพาะไอเดีย + ป้าย "เป็น project แล้ว"
H=rep(H,"esc(p.detail || 'ยังไม่มีรายละเอียด') + '</span></button>'","esc(p.detail || 'ยังไม่มีรายละเอียด') + '</span>' + (p.spawned ? '<span style=\"font-size:11px;color:var(--pj);font-weight:600\">▶️ เป็น project แล้ว</span>' : '') + '</button>'")
i=H.find("  h += '<section class=\"sec\"><button data-act=\"paused\"")
j=H.find("'</section></main>';\n",i)
assert i>0 and j>i
H=H[:i]+"  h += '</main>'; // v54: ที่พักไว้ย้ายไปอยู่หน้า Projects\n"+H[j+len("'</section></main>';\n"):]
H=H.replace("var ideas = D.projects.filter(function (p) { return p.status === 'i'; }), paused = D.projects.filter(function (p) { return p.status === 'p'; });","var ideas = D.projects.filter(function (p) { return p.status === 'i'; });")
# การ์ด: บันทึกล่าสุด + ปุ่ม
H=rep(H,"  // ความคืบหน้า\n","""  // v54: บันทึกความคืบหน้า (ช่อง "ถึงไหนแล้ว" ในชีท) ล่าสุดบนสุด
  var logB = p.log && p.log.length ? '<div class="blk"><h4>บันทึกล่าสุด</h4>' + p.log.map(function (l) { return '<div style="font-size:13px;line-height:1.5">' + esc(l) + '</div>'; }).join('') + '</div>' : '';
  if (p.status === 'i') { // v54: ไอเดียไม่มีความคืบหน้า/งาน
    return h + logB + '<div class="acts" style="grid-template-columns:repeat(2,minmax(0,1fr))">' + b('start', '▶️ เริ่มทำ', 'var(--blue)') + b('toproject', '↪ ย้ายไป Projects', 'var(--pj)') + b('archive', '🗄 เก็บถาวร', 'var(--mute)') + b('pdel', '🗑 ลบ', '#C62828') + '</div>' +
      '<div style="font-size:12px;color:var(--mute)">▶️ เริ่มทำ = สร้าง project ใหม่ ไอเดียนี้ยังอยู่ · ↪ ย้าย = AI ลงผิดที่ ย้ายไปเป็น project เลย</div>' +
      '<button data-act="close" style="height:44px;border:0;background:var(--soft);border-radius:10px;font-weight:600;margin-top:4px">ปิด</button></div></div>';
  }
  // ความคืบหน้า
""")
H=rep(H,"  // งาน\n  var tasks = p.tasks || [];","  h += logB;\n  // งาน\n  var tasks = p.tasks || [];")
H=rep(H,"""  h += '<div class="acts">' + (p.status === 'a' ? '' : b('start', 'เริ่มทำ', 'var(--blue)')) + (p.status === 'p' ? '' : b('pause', 'พักไว้', 'var(--mute)')) + (p.status === 'i' ? '' : b('toidea', 'เก็บเป็นไอเดีย', 'var(--idea)')) + b('archive', '🗄 เก็บถาวร', 'var(--mute)') + '</div>'""","""  h += '<div class="acts" style="grid-template-columns:repeat(2,minmax(0,1fr))">' + (p.status === 'a' ? '' : b('start', '▶️ เริ่มทำ', 'var(--blue)')) + (p.status === 'p' ? '' : b('pause', '⏸ พักไว้', 'var(--mute)')) + b('toidea', '↪ ย้ายไปไอเดีย', 'var(--idea)') + b('archive', '🗄 เก็บถาวร', 'var(--mute)') + b('pdel', '🗑 ลบ', '#C62828') + '</div>'""")
H=rep(H,"""'<button class="pill" data-act="unarch" data-id="' + esc(x.id) + '">เอากลับมา</button></div>'""","""'<button class="pill" data-act="unarch" data-id="' + esc(x.id) + '">เอากลับมา</button><button class="pill" data-act="pdel" data-id="' + esc(x.id) + '" aria-label="ลบ ' + esc(x.title) + '" style="color:#C62828;min-width:0">🗑</button></div>'""")
# ---------------- รวมไฟล์ ----------------
mp4=MP4
OUT=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+mp4+'";\n'
u=OUT.encode('utf-16-le'); s=0
for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
open('Code.v54.gs','w',encoding='utf8',newline='').write(OUT)
print('OK Code.v54.gs length',len(u)//2,'checksum',s,'(ต้องได้ 456949 / 3259)')
assert (len(u)//2,s)==(456949,3259)
