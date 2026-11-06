# v55: tag เลข project บนการ์ดงาน (1/2/3 = project ที่กำลังทำ · อื่นๆ = ไม่ผูก) + ผูกงานแล้วลงบันทึก project เอง
# รันในโฟลเดอร์ที่มี Code.v54.gs : python patch55.py
import json,re,os
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v54.gs',encoding='utf8').read()
assert ck(B)==(456949,3259),('base ไม่ใช่ v54',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v54';","var APP_VER = 'v55';")
C=rep(C,"ไม่เกี่ยวกับ project ไหนชัดๆ = null',","ไม่เกี่ยวกับ project ไหนชัดๆ หรือข้อความสั้น/จดรีบๆ ที่บริบทไม่พอ = null (ไปอยู่กลุ่ม อื่นๆ ผู้ใช้เลือก project เองในแอป)',")
C=rep(C,"function setProjectStatus(id, st) { return updateProject(id, '', null, st); }\n","""function setProjectStatus(id, st) { return updateProject(id, '', null, st); }
/** v55: งานถูกผูกเข้า project → ลงบันทึกของ project (📌 ชื่องาน) */
function logTaskLink(projectId, title) {
  if (!projectId) return;
  try { if (projectById(projectId)) updateProject(projectId, '📌 ' + title, null, null); } catch (e) { log('action', 'logTaskLink ' + projectId, '', e.message); }
}
""")
C=rep(C,"          if (pjOf) {\n            lines.push('🔗 ' + t.title + ' → ' + pjOf.title);","          if (pjOf) {\n            logTaskLink(pjOf.id, t.title);\n            lines.push('🔗 ' + t.title + ' → ' + pjOf.title);")
C=rep(C,"      var nt = addTask(tt, ds, roadmapCalendar(pp.roadmap), { projectId: pp.id });","      var nt = addTask(tt, ds, roadmapCalendar(pp.roadmap), { projectId: pp.id });\n      logTaskLink(pp.id, nt.title);")
C=rep(C,"  } else if (action === 'toproject') {","""  } else if (action === 'ttag') { // v55: เลือก project ของงาน (pid ว่าง = อื่นๆ)
    var tgo = findRow('tasks', a.id), tgp = a.pid ? projectById(a.pid) : null;
    if (!tgo) { msg = 'ไม่พบงานนี้'; warn = true; }
    else if (a.pid && (!tgp || tgp.status === ST_DONE || tgp.status === ST_ARCH)) { msg = 'ไม่พบ project นี้'; warn = true; }
    else {
      sheet('tasks').getRange(tgo.row, 12).setValue(tgp ? tgp.id : '');
      if (tgp && String(tgo.v[11]) !== String(tgp.id)) logTaskLink(tgp.id, tgo.v[2]);
      msg = '🏷 ' + tgo.v[2] + ' → ' + (tgp ? tgp.title : 'อื่นๆ');
    }
  } else if (action === 'toproject') {""")
C=rep(C,"  var projects = rows.map(function (r) {","  var actOrd = rows.filter(function (r) { return r.status === ST_ACTIVE; }).map(function (r) { return String(r.id); }); // v55: เลข tag 1,2,3 ตามลำดับในชีท\n  var projects = rows.map(function (r) {")
C=rep(C,"    return { id: r.id, title: r.title, rm: rmName(r), status: st,","    return { id: r.id, no: actOrd.indexOf(String(r.id)) + 1, title: r.title, rm: rmName(r), status: st,")
C=rep(C,"      project: p ? p.title + rmTag(p) : '' };\n  };","      project: p ? p.title + rmTag(p) : '', pid: p ? String(p.id) : '' };\n  };")
C=rep(C,"date: t.due ? ymd(t.due) : '', time: noTime ? '' : hm(t.due), project: p ? p.title + rmTag(p) : '' };","date: t.due ? ymd(t.due) : '', time: noTime ? '' : hm(t.due), project: p ? p.title + rmTag(p) : '', pid: p ? String(p.id) : '' };")
# ---------------- หน้าแอป ----------------
H=rep(H,"/* v54 แมววี: โผล่เมื่อยังไม่ได้บันทึก */","""/* v55 tag เลข project */
.tg{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;padding:0 6px;border-radius:11px;color:#fff;font-size:12px;font-weight:700;line-height:1;flex-shrink:0}
.tg.o{background:var(--soft);color:var(--mute);font-weight:600}
.tgb{margin-right:12px;border:0;background:none;padding:8px 4px;flex-shrink:0;cursor:pointer}
.tgl{display:flex;align-items:center;gap:10px;width:100%;min-height:48px;padding:8px 12px;border:1px solid var(--line);border-radius:12px;background:#fff;text-align:left;font-size:15px;color:var(--ink)}
.tgl.on{border-color:var(--today);background:var(--today-sub);font-weight:600}
/* v54 แมววี: โผล่เมื่อยังไม่ได้บันทึก */""")
H=rep(H,"function taskRow(t) {\n  return '<button class=\"row' + (t.done ? ' done' : '') + '\" data-act=\"toggle\" data-id=\"' + esc(t.id) + '\" aria-pressed=\"' + (t.done ? 'true' : 'false') + '\">' +","""/* v55: ป้ายเลข project — เลขเดียวกันบนการ์ด project และการ์ดงาน */
var TAGC = ['#3B6FBF', '#2E8B57', '#E07B00', '#8E44AD', '#C2185B', '#00838F'];
function pNo(pid) { var p = pid && findP(pid); return p && p.status === 'a' && p.no ? p.no : 0; }
function tagChip(no, sm) { return no ? '<span class="tg" style="background:' + TAGC[(no - 1) % TAGC.length] + '">' + no + '</span>' : '<span class="tg o">' + (sm ? '–' : 'อื่นๆ') + '</span>'; }
function viewTag() {
  var t = taskById(S.tagfor); if (!t) return '';
  var cur = pNo(t.pid) ? String(t.pid) : '';
  var act = D.projects.filter(function (p) { return p.status === 'a' && p.no; }).sort(function (a, b) { return a.no - b.no; });
  return '<div class="sheet" data-act="tgclose" style="z-index:6"><div class="box" role="dialog" aria-label="เลือก project ของงาน"><h3 style="margin:0">งานนี้อยู่ project ไหน</h3><div style="font-size:14px;color:var(--mute)">' + esc(t.title) + '</div>' +
    act.map(function (p) { return '<button class="tgl' + (cur === String(p.id) ? ' on' : '') + '" data-act="tgset" data-v="' + esc(p.id) + '">' + tagChip(p.no) + '<span>' + esc(p.title) + '</span></button>'; }).join('') +
    '<button class="tgl' + (cur ? '' : ' on') + '" data-act="tgset" data-v="">' + tagChip(0) + '<span>ยังไม่ผูก project (จดรีบๆ ไว้ก่อน)</span></button>' +
    '<button data-act="tgclose" style="height:44px;border:0;background:var(--soft);border-radius:10px;font-weight:600;margin-top:4px">ปิด</button></div></div>';
}
function setTag(id, pid) {
  var p = pid ? findP(pid) : null, lab = p ? p.title + ' (' + p.rm + ')' : '';
  var mv = null, same = function (t) { return String(t.id) === String(id); };
  allDayTasks().forEach(function (t) { if (same(t)) { t.pid = pid; t.project = lab; mv = mv || t; } });
  var td = D.tasksProject.concat(D.tasksOther).filter(same)[0];
  if (td) { D.tasksProject = D.tasksProject.filter(function (t) { return !same(t); }); D.tasksOther = D.tasksOther.filter(function (t) { return !same(t); }); (pid ? D.tasksProject : D.tasksOther).push(td); }
  D.projects.forEach(function (x) { x.tasks = (x.tasks || []).filter(function (t) { return String(t.id) !== String(id); }); });
  if (p && mv && !mv.done) (p.tasks = p.tasks || []).push({ id: mv.id, title: mv.title, when: mv.when, late: mv.late });
}
function taskRow(t) {
  return '<div class="prow"><button class="row' + (t.done ? ' done' : '') + '" data-act="toggle" data-id="' + esc(t.id) + '" aria-pressed="' + (t.done ? 'true' : 'false') + '">' +""")
H=rep(H,"    (t.late ? '<span class=\"w\">เลยกำหนด · ' + esc(t.when) + '</span>' : (t.when ? '<span class=\"s\">' + esc(t.when) + '</span>' : '')) + '</span></button>';\n}","    (t.late ? '<span class=\"w\">เลยกำหนด · ' + esc(t.when) + '</span>' : (t.when ? '<span class=\"s\">' + esc(t.when) + '</span>' : '')) + '</span></button>' +\n    '<button class=\"tgb\" data-act=\"tagpick\" data-id=\"' + esc(t.id) + '\" aria-label=\"เลือก project ของงานนี้\">' + tagChip(pNo(t.pid)) + '</button></div>';\n}")
# การ์ดแก้งาน: แถว project
H=rep(H,"'<h3>แก้ไขงาน</h3>' + (t.project ? '<div style=\"font-size:12px;color:var(--mute);margin-top:-6px\">' + esc(t.project) + '</div>' : '') +","'<h3>แก้ไขงาน</h3>' + '<button type=\"button\" data-act=\"tagpick\" data-id=\"' + esc(t.id) + '\" style=\"display:flex;align-items:center;gap:8px;border:1px solid var(--line);background:#fff;border-radius:10px;padding:8px 10px;text-align:left;font-size:13px;color:var(--mute)\">' + tagChip(pNo(t.pid)) + '<span style=\"flex:1\">' + esc(pNo(t.pid) ? t.project : 'ยังไม่ผูก project') + '</span><span style=\"color:var(--today);font-weight:600\">เปลี่ยน</span></button>' +")
# Projects: เลขหน้าชื่อ · การ์ด project: เลขที่หัว
H=rep(H,"'\"></span><span class=\"col\"><span class=\"t\">' + esc(p.title) + (g.tag ? ' (' + esc(p.rm) + ')' : '') + '</span>","'\"></span><span class=\"col\"><span class=\"t\">' + (p.status === 'a' && p.no ? tagChip(p.no) + ' ' : '') + esc(p.title) + (g.tag ? ' (' + esc(p.rm) + ')' : '') + '</span>")
H=rep(H,"esc(p.rm) + ' · ' + st + '</div>'","(p.status === 'a' && p.no ? tagChip(p.no) + ' ' : '') + esc(p.rm) + ' · ' + st + '</div>'")
# render + handlers
H=rep(H,"viewCat() + (S.del ? viewDel() : '')","viewCat() + (S.tagfor ? viewTag() : '') + (S.del ? viewDel() : '')")
H=rep(H,"  if (act === 'toggle' && !ev.target.closest('.chk') && taskById(id)) return openTask(id);","""  if (act === 'tagpick') { if (id && id.indexOf('tmp') === 0) return toast('กำลังบันทึกงานนี้ รอแป๊บนึง'); S.tagfor = id; return render(); }
  if (act === 'tgclose') { if (ev.target !== el && el.classList.contains('sheet')) return; S.tagfor = null; return render(); }
  if (act === 'tgset') {
    var tgid = S.tagfor; S.tagfor = null; var np0 = v ? findP(v) : null;
    toast('🏷 ' + (np0 ? np0.no + ' · ' + np0.title : 'อื่นๆ'));
    return api('ttag', { id: tgid, pid: v || '' }, function () { setTag(tgid, v || ''); });
  }
  if (act === 'toggle' && !ev.target.closest('.chk') && taskById(id)) return openTask(id);""")
mp4=MP4
OUT=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+mp4+'";\n'
L,S=ck(OUT)
open('Code.v55.gs','w',encoding='utf8',newline='').write(OUT)
if os.environ.get('VEE_DEV'):
    open('app.v55.html','w',encoding='utf8',newline='').write(H); open('Code.gs','w',encoding='utf8',newline='').write(OUT)
print('OK Code.v55.gs length',L,'checksum',S)
