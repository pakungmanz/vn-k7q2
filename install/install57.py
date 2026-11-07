# v57: เริ่มทำไอเดีย = ย้ายไปเป็น project (ไอเดียหายจากหน้าไอเดีย ไม่สร้างซ้ำ) · ไอเดียที่เคยแตกเป็น project แล้วซ่อน
#      · ยืนยันลบงาน มีตัวเลือก "📁 ย้ายไปเป็น project" (AI ลงผิดเป็นงาน)
# รันในโฟลเดอร์ที่มี Code.v56.gs : python patch57.py
import json,re,os
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v56.gs',encoding='utf8').read()
assert ck(B)==(463334,331),('base ไม่ใช่ v56',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v56';","var APP_VER = 'v57';")
# เริ่มทำไอเดีย → เปลี่ยนสถานะแถวเดิม (ไม่ spawn)
C=rep(C,"else { var fromIdea = p.status === ST_IDEA; if (fromIdea) p = spawnProject(p.id) || p; setProjectStatus(p.id, ST_ACTIVE); msg = '▶️ เริ่มทำ ' + p.title + (fromIdea ? ' (ไอเดียต้นทางยังอยู่)' : ''); }",
"else { var fromIdea = p.status === ST_IDEA; setProjectStatus(p.id, ST_ACTIVE); msg = '▶️ เริ่มทำ ' + p.title + (fromIdea ? ' (ย้ายออกจากไอเดียแล้ว)' : ''); } // v57: ไม่สร้างซ้ำ")
C=rep(C,"      if (pp.status === ST_IDEA) pp = spawnProject(pp.id) || pp;\n","")
C=rep(C,"""function spawnProject(id) {
  var o = findRow('roadmap', id);
  if (!o) return null;
  var nid = newId('R'), now = new Date(), sh = sheet('roadmap');
  sh.appendRow([nid, o.v[1], o.v[2], o.v[3], '', '', '', ST_IDEA, now, now]);
  sh.getRange(o.row, 5).setValue(dmy(now) + ' ' + SPAWN_NOTE + (o.v[4] ? '\\n' + o.v[4] : ''));
  return projectById(nid);
}""","""function spawnProject(id) { return projectById(id); } // v57: ไม่สร้างสำเนาแล้ว — ไอเดียกลายเป็น project แถวเดิม""")
# ไอเดียที่เคยแตกเป็น project แล้ว (v54-56) → ซ่อน
C=rep(C,"  var rows = roadmapRows(true).filter(function (r) { return r.status !== ST_DONE && r.status !== ST_ARCH && !/ไม่ต้องทำ/.test(r.status); });",
"  var rows = roadmapRows(true).filter(function (r) { return r.status !== ST_DONE && r.status !== ST_ARCH && !/ไม่ต้องทำ/.test(r.status) && !(r.status === ST_IDEA && String(r.process || '').indexOf(SPAWN_NOTE) >= 0); }); // v57: ไอเดียที่เป็น project แล้วซ่อน")
C=rep(C,"function parkedRows() { return roadmapRows().filter(function (r) { return r.status === ST_IDEA; }); }",
"function parkedRows() { return roadmapRows().filter(function (r) { return r.status === ST_IDEA && String(r.process || '').indexOf(SPAWN_NOTE) < 0; }); }")
# งาน → project
C=rep(C,"  } else if (action === 'tcancel') {","""  } else if (action === 'tproject') { // v57: AI ลงผิดเป็นงาน → ย้ายไปเป็น project (ยกเลิกงาน+ลบจากปฏิทิน)
    var tpo = findRow('tasks', a.id);
    if (!tpo) { msg = 'ไม่พบงานนี้'; warn = true; }
    else {
      var tpt = String(tpo.v[2] || '').trim(), tpl = tpo.v[11] ? projectById(tpo.v[11]) : null, tfl = activeProjects().length >= MAX_ACTIVE, tnow = new Date();
      sheet('roadmap').appendRow([newId('R'), tpl ? tpl.roadmap : '', tpt, '', dmy(tnow) + ' 📁 ย้ายมาจากงาน', '', '', tfl ? ST_PAUSE : ST_ACTIVE, tnow, tnow]);
      cancelItem('task', a.id);
      msg = '📁 ย้ายไปเป็น project: ' + tpt + (tfl ? ' (ทำอยู่ครบ ' + MAX_ACTIVE + ' เลยอยู่กลุ่มพัก)' : '');
    }
  } else if (action === 'tcancel') {""")
# ---------------- หน้าแอป ----------------
H=rep(H,"  var ideas = D.projects.filter(function (p) { return p.status === 'i'; });","  var ideas = D.projects.filter(function (p) { return p.status === 'i' && !p.spawned; });")
H=rep(H,"    toast('▶️ เริ่มทำ ' + sp.title + (sp.status === 'i' ? '\\nไอเดียต้นทางยังเก็บไว้ที่เดิม' : ''));\n    return api('start', { id: id }, function () {\n      if (sp.status === 'i') { sp.spawned = true; D.projects.push({ id: 'tmp' + (++tmpN), title: sp.title, rm: sp.rm, status: 'a', next: '', plan: '', pct: null, done: 0, detail: sp.detail, tasks: [], log: [] }); }\n      else setStatus(id, 'a');\n    });",
"    toast('▶️ เริ่มทำ ' + sp.title + (sp.status === 'i' ? '\\nย้ายจากไอเดียไป Projects แล้ว' : ''));\n    return api('start', { id: id }, function () { setStatus(id, 'a'); });")
# ปุ่มยืนยันลบงาน: ลบ / ย้ายไปเป็น project / ไม่ลบ
H=rep(H,"""    '<button type="button" data-act="tcancel" style="height:44px;border-radius:10px;border:1px solid #F3C1BB;background:' + (S.arm === 'tc' ? '#B42318' : '#fff') + ';color:' + (S.arm === 'tc' ? '#fff' : '#B42318') + ';font-weight:600">' + (S.arm === 'tc' ? 'แตะอีกครั้งเพื่อยืนยัน' : '🗑 ยกเลิกงานนี้') + '</button></div>' +""",
"""    '<button type="button" data-act="tcancel" style="height:44px;border-radius:10px;border:1px solid #F3C1BB;background:#fff;color:#B42318;font-weight:600">🗑 ยกเลิกงานนี้</button></div>' +
    (S.arm === 'tc' ? '<div class="tcq" role="group" aria-label="ยืนยัน"><div style="font-size:13px;color:var(--mute)">ยกเลิกงานนี้ หรือที่จริงควรเป็น project?</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">' +
      '<button type="button" data-act="tcancel" style="height:44px;border-radius:10px;border:0;background:#B42318;color:#fff;font-weight:600">🗑 ลบเลย</button>' +
      '<button type="button" data-act="tproj" style="height:44px;border-radius:10px;border:0;background:var(--pj);color:#fff;font-weight:600">📁 เป็น project</button>' +
      '<button type="button" data-act="tcoff" style="height:44px;border-radius:10px;border:1px solid var(--line);background:#fff;font-weight:600;color:var(--mute)">ไม่ลบ</button></div></div>' : '') +""")
H=rep(H,"    if (S.arm !== 'tc') { S.arm = 'tc'; render(); clearTimeout(S.armT); S.armT = setTimeout(function () { S.arm = null; render(); }, 4000); return; }\n    var tid = S.tsheet;",
"    if (S.arm !== 'tc') { S.arm = 'tc'; clearTimeout(S.armT); return render(); } // v57: ไม่หมดเวลาเอง มีปุ่ม ไม่ลบ\n    var tid = S.tsheet;")
H=rep(H,"  if (act === 'tcancel') {","""  if (act === 'tcoff') { S.arm = null; return render(); }
  if (act === 'tproj') { // v57
    var tpid = S.tsheet, tpo = taskById(tpid) || {}; S.arm = null; S.tsheet = null;
    if (String(tpid).indexOf('tmp') === 0) { render(); return toast('กำลังบันทึกงานนี้ รอแป๊บนึง'); }
    var tpf = D.projects.filter(function (p) { return p.status === 'a'; }).length >= D.max;
    toast('📁 ย้ายไปเป็น project: ' + tpo.title + (tpf ? '\\n(ทำอยู่ครบ ' + D.max + ' เลยอยู่กลุ่มพัก)' : ''));
    return api('tproject', { id: tpid }, function () { dropTask(tpid); D.projects.push({ id: 'tmp' + (++tmpN), title: tpo.title || '', rm: 'อื่นๆ', status: tpf ? 'p' : 'a', next: '', plan: '', pct: null, done: 0, detail: '', tasks: [], log: [] }); });
  }
  if (act === 'tcancel') {""")
H=rep(H,"#toast{","/* v57 */\n.tcq{display:flex;flex-direction:column;gap:8px;border:1px solid #F3C1BB;background:#FFF6F5;border-radius:12px;padding:10px}\n#toast{")
OUT=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
L,S=ck(OUT)
open('Code.v57.gs','w',encoding='utf8',newline='').write(OUT)
if os.environ.get('VEE_DEV'):
    open('app.v57.html','w',encoding='utf8',newline='').write(H); open('Code.gs','w',encoding='utf8',newline='').write(OUT)
print('OK Code.v57.gs length',L,'checksum',S)
