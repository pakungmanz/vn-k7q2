# v59: หน้า "บันทึกภาระงาน" P4P — ปุ่มกลมไอคอนกระดาษต่อจากแท็บ การเงิน
#      พูด/พิมพ์ "วันนี้ตรวจคนไข้ รพ.สต. 97 คน" → "ตรวจ OPD รพ.สต. 97 คน = 485 แต้ม" ลงชีท + Google Calendar (วันละ 1 รายการทั้งวัน)
#      ตารางคะแนนตั้งต้น = P4P เวชศาสตร์ครอบครัว (P4P_FAMMED.xlsx) อยู่ในแท็บ "ตาราง P4P" แก้คะแนนเองได้
# v59b: ไมค์/แชทหน้าอื่นไม่ลงภาระงาน — ลงได้เฉพาะในหน้า บันทึกภาระงาน
# รันในโฟลเดอร์ที่มี Code.v58.gs : python patch59b.py  → ได้ Code.v59b.gs
import json,re,os
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v58.gs',encoding='utf8').read()
assert ck(B)==(481319,2087),('base ไม่ใช่ v58',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v58';","var APP_VER = 'v59b';")
C=rep(C,"  log:      { name: 'Log',",
"""  p4pt:     { name: 'ตาราง P4P',      headers: ['รหัส', 'หมวด', 'งาน', 'หน่วย', 'คะแนน/หน่วย', 'นาที', 'คำที่ใช้เรียก (AI ใช้ตัดสินใจ)', 'ชื่อย่อ (โชว์ในแอป/ปฏิทิน)'] },
  p4p:      { name: 'ภาระงาน P4P',    headers: ['ID', 'วันที่', 'รหัส', 'งาน', 'หมวด', 'จำนวน', 'หน่วย', 'คะแนน/หน่วย', 'คะแนน', 'ข้อความที่พูด', 'สร้างเมื่อ', 'CalendarEventID', 'วีเดา'] },
  log:      { name: 'Log',""")
# event ของ P4P ไม่ต้องโผล่เป็นนัดในหน้า วันนี้
C=rep(C,"if (!title || /^[☐✅]/.test(title)) return; // งานของ Vee","if (!title || /^[☐✅]/.test(title) || title.indexOf(P4P_EV_PREFIX) === 0) return; // งานของ Vee")
C=rep(C,"    money: appMoney(), cats: moneyCats(),","    p4p: p4pData(), money: appMoney(), cats: moneyCats(),")
C=rep(C,"var msg = '', warn = false, say = '', heardTxt = '', cat = null;","var msg = '', warn = false, say = '', heardTxt = '', cat = null, wask = null;")
C=rep(C,"return { msg: msg, warn: warn, say: say, heard: heardTxt, cat: cat, data: appData(true), ver: APP_VER };",
        "return { msg: msg, warn: warn, say: say, heard: heardTxt, cat: cat, wask: wask, data: appData(true), ver: APP_VER };")
C=rep(C,"""  } else if (action === 'slip') {""","""  } else if (action === 'p4p' || action === 'p4pvoice') {
    var ptx = String(a.text || '').trim();
    if (action === 'p4pvoice') {
      var pb = String(a.b64 || '');
      if (!pb || pb.length > 8000000) throw new Error('เสียงยาวเกินไป พูดสั้นลงหน่อยครับ');
      var pm = String(a.mime || 'audio/webm').split(';')[0], pext = /mp4|m4a|aac/.test(pm) ? 'm4a' : /ogg/.test(pm) ? 'ogg' : /wav/.test(pm) ? 'wav' : 'webm';
      var ph = groqStt(Utilities.newBlob(Utilities.base64Decode(pb), pm, 'p4p.' + pext), 'p4p ' + (a.sec || '?') + 's');
      if (!ph.ok) { msg = ph.error; warn = true; wask = ph.error; ptx = ''; } else { ptx = ph.text; heardTxt = ph.text; }
    }
    if (ptx) {
      var pc = p4pCapture(ptx, a.date);
      msg = (action === 'p4pvoice' ? '🎤 ' + ptx + '\\n' : '') + pc.msg; warn = !!pc.warn; wask = pc.ask ? (action === 'p4pvoice' ? 'ได้ยินว่า “' + ptx + '”\\n' : '') + pc.ask : '';
    }
  } else if (action === 'p4padd') {
    var pa = p4pAdd([{ k: a.k, q: a.q, d: a.date, sure: true }], 'เพิ่มเองในแอป');
    msg = pa.length ? '📋 ' + p4pLine(pa[0]) : 'ใส่จำนวนก่อนครับ'; warn = !pa.length;
  } else if (action === 'p4pedit') {
    var pe = p4pEdit(a.id, a.k, a.q, a.date);
    msg = pe ? '✏️ ' + p4pLine(pe) : 'ไม่พบรายการนี้'; warn = !pe;
  } else if (action === 'p4pdel') {
    var pdl = p4pDel(a.id); msg = pdl ? '🗑 ลบ ' + pdl : 'ไม่พบรายการนี้';
  } else if (action === 'slip') {""")
# v59b: ภาระงานลงได้เฉพาะหน้า บันทึกภาระงาน (action p4p/p4pvoice/p4padd/p4pedit) — แชท/ไมค์หน้าอื่นไม่ cross มาลง P4P
P4P_JS=r"""
/* ============================================================
 *  v59: บันทึกภาระงาน P4P
 *  พูด/พิมพ์ "วันนี้ตรวจคนไข้ รพ.สต. 97 คน" → AI แยกเป็นรหัสงานในตาราง → คิดแต้ม → ลงชีท "ภาระงาน P4P"
 *  + Google Calendar: วันละ 1 รายการทั้งวัน "📋 P4P 485 แต้ม · ..." (อัปเดตทุกครั้งที่แก้/ลบ)
 *  ตารางคะแนนอยู่ในแท็บ "ตาราง P4P" (ภัทรแก้คะแนน/เพิ่มแถวเองได้) ตั้งต้นจาก P4P เวชศาสตร์ครอบครัว (P4P_FAMMED.xlsx)
 * ============================================================ */
var P4P_STD = 0.26;                          // แต้ม/นาที (แพทย์)
var P4P_TARGET = 3000, P4P_GUARANTEE = 2200;  // ต่อเดือน · override: property P4P_TARGET / P4P_GUARANTEE
var P4P_CALENDAR = 'PatKung regular work';    // override: property P4P_CALENDAR
var P4P_MODEL = 'claude-sonnet-5-5';          // ต้องแม่น · override: property P4P_MODEL
var P4P_EV_PREFIX = '📋 P4P';
var P4P_SECTIONS = [
  ['admin', 'งานบริหาร', '👥'], ['acad', 'งานวิชาการ', '🎓'], ['svc', 'งานบริการ OPD / ER', '🩺'], ['ipd', 'IPD', '🛌'],
  ['fm_hosp', 'บริการในโรงพยาบาล (FM)', '🏥'], ['fm_comm', 'บริการในชุมชน', '🏡'], ['fm_tele', 'Telemed และ Home Ward', '📱'],
  ['proc', 'หัตถการในโรงพยาบาล', '💉'], ['teach', 'งานสอนแพทย์ประจำบ้าน', '📚'], ['extra', 'งานเสนอเพิ่ม', '⭐']
];
function p4pR2(x) { return Math.round((+x || 0) * 100) / 100; }
function p4pSec(id) { var s = P4P_SECTIONS.filter(function (x) { return x[0] === id; })[0]; return s ? s[1] : id; }
/** ตารางตั้งต้น: [รหัส, หมวด, งาน, หน่วย, คะแนน/หน่วย, นาที, คำเรียกอื่น, ชื่อย่อ] — คะแนนงานบริหาร/วิชาการ = นาที × 0.26 × เท่า */
function p4pSeed() {
  var S = P4P_STD, out = [];
  var add = function (k, s, n, u, sc, min, h, a) { out.push([k, p4pSec(s), n, u, sc == null ? '' : sc, min || '', h || '', a || n]); };
  [['mt_exec', 'ประชุมคณะกรรมการบริหารโรงพยาบาล', 'ประชุมกก.บริหาร รพ.', 'กรรมการบริหาร, ประชุมบริหาร รพ.'],
   ['mt_pct', 'ประชุม PCT / ยุทธศาสตร์ / งานคุณภาพ', 'ประชุม PCT/คุณภาพ', 'PCT, HA, คุณภาพ, ยุทธศาสตร์'],
   ['mt_org', 'ประชุมองค์กรแพทย์', 'ประชุมองค์กรแพทย์', 'องค์กรแพทย์']].forEach(function (m) {
    [['_3', 'ประธาน', 3], ['_25', 'เลขา', 2.5], ['_2', 'กรรมการ', 2], ['_1', 'ไม่ระบุบทบาท', 1]].forEach(function (ro) {
      add(m[0] + ro[0], 'admin', m[1] + ' — ' + ro[1] + ' ×' + ro[2], 'ครั้ง', p4pR2(180 * S * ro[2]), 180, m[3], m[2] + ' (' + ro[1] + ')');
    });
  });
  add('mt_ext', 'admin', 'ประชุมคณะกรรมการตามคำสั่งต่างๆ นอกหน่วยงาน (2 เท่า)', 'ครั้ง', p4pR2(180 * S * 2), 180, 'ประชุมนอก รพ. ตามคำสั่ง เช่น สสจ./อำเภอ', 'ประชุมกก.นอกหน่วยงาน');
  add('sp_out_free', 'acad', 'วิทยากรนอกโรงพยาบาล (3 เท่า กรณีไม่ได้รับค่าตอบแทน)', 'ชั่วโมง', p4pR2(60 * S * 3), 60, 'บรรยายนอก รพ. ไม่ได้ค่าตอบแทน', 'วิทยากรนอก รพ. (ไม่มีค่าตอบแทน)');
  add('sp_out_paid', 'acad', 'วิทยากรนอกโรงพยาบาล (1.5 เท่า กรณีได้รับค่าตอบแทน)', 'ชั่วโมง', p4pR2(60 * S * 1.5), 60, 'บรรยายนอก รพ. ได้ค่าตอบแทน', 'วิทยากรนอก รพ. (มีค่าตอบแทน)');
  add('sp_in', 'acad', 'วิทยากรในโรงพยาบาล (2 เท่า)', 'ชั่วโมง', p4pR2(60 * S * 2), 60, 'บรรยาย/สอนใน รพ.', 'วิทยากรใน รพ.');
  add('acad_in', 'acad', 'ร่วมงานประชุมวิชาการภายในโรงพยาบาล (1.5 เท่า)', 'ชั่วโมง', p4pR2(60 * S * 1.5), 60, 'ประชุมวิชาการ/อบรมใน รพ.', 'ประชุมวิชาการใน รพ.');
  add('acad_out', 'acad', 'ร่วมงานประชุมวิชาการภายนอกโรงพยาบาล (2 เท่า ไม่รวมวันเดินทาง)', 'ชั่วโมง', p4pR2(60 * S * 2), 60, 'ประชุมวิชาการ/อบรมนอก รพ.', 'ประชุมวิชาการนอก รพ.');
  add('g_opd_spec', 'svc', 'ตรวจรักษาผู้ป่วยนอกคลินิกเฉพาะทาง*', 'ราย/วัน', 6, '', 'คลินิกเฉพาะทางอื่นของ รพ. (ไม่ใช่ NCD/palliative ของ FM)', 'OPD คลินิกเฉพาะทาง');
  add('g_opd', 'svc', 'ตรวจผู้ป่วยนอกทั่วไป*', 'ราย/วัน', 5, '', 'OPD ทั่วไป, OPD ปกส/ประกันสังคม, all D, เวร OPD, OPD นอกเวลา, OPD เช้า/เย็น', 'ตรวจ OPD');
  add('g_opd_cx', 'svc', 'ผู้ป่วยนอกซับซ้อน > 10 นาที', 'ราย/วัน', 10, '', 'ผู้ป่วยซับซ้อนใน OPD ทั่วไป', 'OPD ซับซ้อน >10 นาที');
  add('g_consult_opd', 'svc', 'รับ Consult ผู้ป่วยที่ OPD', 'ราย/วัน', 6, '', 'consult ที่ OPD', 'Consult ที่ OPD');
  add('g_er_nu', 'svc', 'ตรวจผู้ป่วย ER (non-urgent)', 'ราย/วัน', 5, '', 'ER ไม่ด่วน, non-urgent', 'ER non-urgent');
  add('g_er_u', 'svc', 'ตรวจผู้ป่วย ER (urgent)', 'ราย/วัน', 8, '', 'ER ด่วน, urgent', 'ER urgent');
  add('g_er_e', 'svc', 'ผู้ป่วย ER (emergency)', 'ราย/วัน', 10, '', 'ER ฉุกเฉิน, emergency, resuscitation', 'ER emergency');
  add('g_special', 'svc', 'ตรวจพิเศษ (PR, PV, Ultrasound)', 'ราย/วัน', 10, '', 'PR, PV, ultrasound, U/S, อัลตราซาวด์', 'ตรวจพิเศษ PR/PV/US');
  add('g_round1', 'ipd', 'Round ผู้ป่วยในไม่หนัก (วันละ 1 ครั้ง/ราย)', 'ราย/วัน', 6, '', 'ราวด์วอร์ดผู้ป่วยใน (งานกลาง)', 'Round IPD (งานกลาง)');
  add('g_round2', 'ipd', 'Round ผู้ป่วยในไม่หนัก (วันละ 2 ครั้งขึ้นไป/ราย)', 'ราย/วัน', 8, '', 'round วันละ 2 ครั้ง', 'Round IPD ≥2 ครั้ง');
  add('g_icu', 'ipd', 'Round ผู้ป่วยหนัก ICU', 'ราย/วัน', 10, '', 'ICU, ผู้ป่วยหนัก', 'Round ICU');
  add('g_consult_ward', 'ipd', 'รับ Consult ต่างแผนก', 'ราย/วัน', 10, '', 'consult ward/ต่างแผนก', 'Consult ต่างแผนก');
  add('fm_ncd', 'fm_hosp', 'ตรวจ OPD โรคเรื้อรังไม่ติดต่อ', 'ราย/วัน', 5, 10, 'คลินิก NCD, DM, HT, เบาหวาน, ความดัน ใน รพ.', 'ตรวจ OPD NCD');
  add('fm_geri', 'fm_hosp', 'ตรวจผู้ป่วยนอกเฉพาะทาง (ผู้สูงอายุและประคับประคอง)', 'ราย/วัน', 6, 12, 'OPD palliative, คลินิกผู้สูงอายุ, ประคับประคอง', 'OPD ผู้สูงอายุ/Palliative');
  add('fm_cx10', 'fm_hosp', 'ผู้ป่วยนอกซับซ้อน > 10 นาที', 'ราย/วัน', 10, 20, 'ผู้ป่วยซับซ้อนในคลินิก FM', 'OPD ซับซ้อน >10 นาที (FM)');
  add('fm_cx30', 'fm_hosp', 'ผู้ป่วยนอกซับซ้อน > 30 นาที (เช่น Advance care plan, CGA)', 'ราย/วัน', 15, 30, 'ACP, advance care plan, CGA, family meeting', 'OPD ซับซ้อน >30 นาที (ACP/CGA)');
  add('fm_round1', 'fm_hosp', 'Round ผู้ป่วยในไม่หนัก (วันละ 1 ครั้ง/ราย)', 'ราย/วัน', 6, 12, 'round ward, ราวด์ IPD, ผู้ป่วยใน', 'Round IPD');
  add('fm_pal2', 'fm_hosp', 'Round ผู้ป่วยในประคับประคอง (วันละ 2 ครั้งขึ้นไป/ราย)', 'ราย/วัน', 10, 20, 'round palliative วันละ 2 ครั้ง', 'Round Palliative ≥2 ครั้ง');
  add('fm_palcx', 'fm_hosp', 'Round ผู้ป่วยในประคับประคองที่ซับซ้อน (มากกว่า 30 นาที)', 'ราย/วัน', 15, 30, 'round palliative ซับซ้อน >30 นาที', 'Round Palliative ซับซ้อน');
  add('c_pcu', 'fm_comm', 'ตรวจ OPD โรคเรื้อรังไม่ติดต่อและโรคอื่นๆ ใน รพ.สต.', 'ราย/วัน', 5, 10, 'ออก รพ.สต., ตรวจที่ รพ.สต./PCU/PCC/ศสม.', 'ตรวจ OPD รพ.สต.');
  add('c_consult', 'fm_comm', 'รับ Consult จาก รพ.สต. และร้านยา', 'ราย/วัน', 1.2, 3.5, 'consult จาก รพ.สต./ร้านยา ทางโทร/ไลน์', 'Consult รพ.สต./ร้านยา');
  add('c_hv_new', 'fm_comm', 'เยี่ยมบ้าน รายใหม่', 'ราย/วัน', 30, 120, 'เยี่ยมบ้านรายใหม่', 'เยี่ยมบ้าน รายใหม่');
  add('c_hv_old', 'fm_comm', 'เยี่ยมบ้าน รายเก่า', 'ราย/วัน', 20, 60, 'เยี่ยมบ้านรายเก่า, เยี่ยมซ้ำ', 'เยี่ยมบ้าน รายเก่า');
  add('c_proc', 'fm_comm', 'หัตถการในชุมชน (Debridement, I&D, paracentesis ฯลฯ)', 'ราย/วัน', 10, 30, 'หัตถการที่บ้าน/ในชุมชน', 'หัตถการในชุมชน');
  add('c_tele', 'fm_comm', 'Teleconsult ให้คำปรึกษา รพช./หน่วยบริการในเครือข่าย', 'ราย', 7, 15, 'teleconsult รพช./เครือข่าย', 'Teleconsult เครือข่าย');
  add('c_conf', 'fm_comm', 'Case conference / นิเทศเครือข่าย', 'ครั้ง', 30, 60, 'case conference เครือข่าย, นิเทศ', 'Case conference/นิเทศ');
  add('hw_admit', 'fm_tele', 'Admit Home Ward ทั่วไป (แรกรับ บันทึก รพ. + สปสช.)', 'ราย/วัน', 25, 50, 'admit home ward', 'Admit Home Ward');
  add('hw_dying', 'fm_tele', 'Admit Home Ward Active Dying', 'ราย/วัน', 25, 50, 'home ward active dying', 'Admit HW Active Dying');
  add('hw_tele', 'fm_tele', 'โปรแกรม Telemedicine Home Ward Round', 'ราย/วัน', 7, 18, 'round home ward ทาง telemed', 'Telemed Home Ward Round');
  add('tm_ncd', 'fm_tele', 'โปรแกรม Telemedicine ของ OPD โรคเรื้อรังไม่ติดต่อ', 'ราย/วัน', 7, 18, 'telemed NCD', 'Telemed NCD');
  add('p_para', 'proc', 'Abdominal paracentesis', 'ราย/วัน', null, '', 'tap ascites', 'Abdominal paracentesis');
  add('p_arthro', 'proc', 'Arthrocentesis', 'ราย/วัน', null, '', 'เจาะข้อ', 'Arthrocentesis');
  add('p_cpr', 'proc', 'CPR', 'ราย/วัน', 20, '', 'ปั๊มหัวใจ', 'CPR');
  add('p_debr', 'proc', 'Debridement at OPD', 'ราย/วัน', 10, '', '', 'Debridement');
  add('p_defib', 'proc', 'Defibrillation', 'ราย/วัน', 5, '', '', 'Defibrillation');
  add('p_ett', 'proc', 'Endotracheal intubation', 'ราย/วัน', 10, '', 'ใส่ท่อช่วยหายใจ, ET tube', 'Intubation');
  add('p_exc', 'proc', 'Excision at OPD', 'ราย/วัน', 10, '', '', 'Excision');
  add('p_icd', 'proc', 'ICD insertion', 'ราย/วัน', 15, '', 'ใส่สายระบายทรวงอก', 'ICD insertion');
  add('p_id', 'proc', 'Incision & Drainage at OPD', 'ราย/วัน', 5, '', 'I&D, ผ่าฝี', 'I&D');
  add('p_lp', 'proc', 'Lumbar puncture', 'ราย/วัน', 15, '', 'LP, เจาะหลัง', 'Lumbar puncture');
  add('p_needle', 'proc', 'Needle thoracocentesis', 'ราย/วัน', 10, '', '', 'Needle thoracocentesis');
  add('p_cardio', 'proc', 'Synchronized cardioversion', 'ราย/วัน', 5, '', '', 'Cardioversion');
  add('p_thora', 'proc', 'Thoracocentesis', 'ราย/วัน', 5, '', 'เจาะปอด', 'Thoracocentesis');
  add('t_conf', 'teach', 'Case conference / Topic conference / Teaching round', 'ราย', 15, 60, 'สอน resident, แพทย์ประจำบ้าน, teaching round, topic', 'สอน Resident');
  add('x_unit', 'extra', 'ออกหน่วยแพทย์ / รับเสด็จ', 'ครั้ง', p4pR2(480 * 0.5), 480, 'ออกหน่วย พอ.สว., รับเสด็จ', 'ออกหน่วยแพทย์/รับเสด็จ');
  add('x_mc', 'extra', 'งานพิธีกรของโรงพยาบาล', 'ครั้ง', 15, 60, 'พิธีกร', 'พิธีกร รพ.');
  return out;
}
var _p4pT = null, _p4pReady = false;
function p4pReady() { if (_p4pReady) return; _p4pReady = true; var t = ensureTab('p4pt'); if (t.sh.getLastRow() < 2) { var seed = p4pSeed(); t.sh.getRange(2, 1, seed.length, 8).setValues(seed); } ensureTab('p4p'); }
/** หน่วยที่โชว์: ราย/วัน → คน (หัตถการ = ราย) · ชั่วโมง → ชม. */
function p4pUnit(u, s) { u = String(u || 'ราย').trim(); var b = u.replace(/\/วัน$/, ''); return b === 'ราย' && u !== 'ราย' ? (s === p4pSec('proc') ? 'ราย' : 'คน') : b === 'ชั่วโมง' ? 'ชม.' : b; }
function p4pTable() {
  if (_p4pT) return _p4pT;
  p4pReady();
  _p4pT = readRows('p4pt').map(function (o) {
    var sc = o.v[4], s = String(o.v[1] || '').trim() || p4pSec('extra');
    return { k: String(o.v[0]).trim(), s: s, n: String(o.v[2]).trim(), u: String(o.v[3] || 'ราย').trim(), sc: sc === '' || sc == null || isNaN(+sc) ? null : +sc,
      min: +o.v[5] || 0, h: String(o.v[6] || '').trim(), a: String(o.v[7] || '').trim() || String(o.v[2]).trim() };
  }).filter(function (x) { return x.k && x.n; });
  return _p4pT;
}
function p4pItem(k) { k = String(k || '').trim(); return p4pTable().filter(function (x) { return x.k === k; })[0] || null; }
function p4pRows() {
  p4pReady();
  return readRows('p4p').map(function (o) {
    return { row: o.row, id: String(o.v[0]), d: isDate(o.v[1]) ? ymd(o.v[1]) : String(o.v[1]).slice(0, 10), k: String(o.v[2]).trim(), n: String(o.v[3]), s: String(o.v[4]),
      q: +o.v[5] || 0, u: String(o.v[6] || ''), sc: o.v[7] === '' || o.v[7] == null ? null : +o.v[7], pts: +o.v[8] || 0, raw: String(o.v[9] || ''), ev: String(o.v[11] || ''), g: !!String(o.v[12] || '') };
  });
}
/** แต้มของรายการ = จำนวน × คะแนน/หน่วยในตารางปัจจุบัน (แก้ตารางแล้วยอดเก่าเปลี่ยนตาม) · ไม่มีรหัสในตารางแล้ว = ใช้ค่าที่บันทึกไว้ */
function p4pPts(r) { var it = p4pItem(r.k), sc = it ? it.sc : r.sc; return sc == null ? 0 : p4pR2(r.q * sc); }
function p4pShort(r) { var it = p4pItem(r.k); return (it ? it.a : r.n) + ' ' + money(r.q) + ' ' + p4pUnit(it ? it.u : r.u, it ? it.s : r.s); }
function p4pLine(r) { return p4pShort(r) + ' = ' + money(p4pPts(r)) + ' แต้ม' + (r.d !== ymd(new Date()) ? ' (' + dmy(parseLocal(r.d, 12)) + ')' : ''); }
function p4pYmd(s, def) { s = String(s || '').trim(); return /^\d{4}-\d{2}-\d{2}$/.test(s) && parseLocal(s, 12) ? s : def; }
function p4pCalName() { return prop('P4P_CALENDAR') || P4P_CALENDAR; }
function p4pNum(k, def) { var v = +prop(k); return v > 0 ? v : def; }
/** เพิ่มรายการ (set = แทนยอดเดิมของรหัสนั้นในวันนั้น) แล้วอัปเดตปฏิทินของวันที่แตะ */
function p4pAdd(list, raw) {
  var now = new Date(), today = ymd(now), days = {}, out = [];
  (list || []).forEach(function (e) {
    var it = p4pItem(e.k); if (!it) return;
    var q = p4pR2(String(e.q == null ? '' : e.q).replace(/,/g, '')); if (!(q > 0) || q > 10000) return;
    var d = p4pYmd(e.d, today), sh = sheet('p4p');
    if (e.set) p4pRows().filter(function (r) { return r.d === d && r.k === it.k; }).reverse().forEach(function (r) { sh.deleteRow(r.row); });
    var pts = it.sc == null ? 0 : p4pR2(q * it.sc), id = newId('W');
    sh.appendRow([id, parseLocal(d, 12), it.k, it.n, it.s, q, it.u, it.sc == null ? '' : it.sc, pts, String(raw || '').slice(0, 300), now, '', e.sure === false ? '?' : '']);
    days[d] = 1; out.push({ id: id, d: d, k: it.k, n: it.n, s: it.s, q: q, u: it.u, sc: it.sc, g: e.sure === false });
  });
  Object.keys(days).forEach(p4pSyncDay);
  return out;
}
function p4pEdit(id, k, q, d) {
  var r = p4pRows().filter(function (x) { return x.id === String(id); })[0]; if (!r) return null;
  var it = p4pItem(k || r.k); if (!it) return null;
  var nq = p4pR2(String(q == null ? '' : q).replace(/,/g, '')); nq = nq > 0 ? nq : r.q;
  var nd = p4pYmd(d, r.d), sh = sheet('p4p');
  sh.getRange(r.row, 2, 1, 8).setValues([[parseLocal(nd, 12), it.k, it.n, it.s, nq, it.u, it.sc == null ? '' : it.sc, it.sc == null ? 0 : p4pR2(nq * it.sc)]]);
  sh.getRange(r.row, 13).setValue('');
  p4pSyncDay(r.d); if (nd !== r.d) p4pSyncDay(nd);
  return { id: r.id, d: nd, k: it.k, n: it.n, s: it.s, q: nq, u: it.u, sc: it.sc };
}
function p4pDel(id) {
  var r = p4pRows().filter(function (x) { return x.id === String(id); })[0]; if (!r) return '';
  var t = p4pShort(r); sheet('p4p').deleteRow(r.row); p4pSyncDay(r.d); return t;
}
/** ปฏิทิน: 1 รายการทั้งวันต่อวัน หาจากชื่อที่ขึ้นต้น 📋 P4P (ลบใน Google Calendar ไป = สร้างใหม่ตอนแก้ครั้งถัดไป) */
function p4pSyncDay(d) {
  try {
    var rows = p4pRows().filter(function (r) { return r.d === d; });
    var g = getCal(p4pCalName()), cal = g.cal, day = parseLocal(d, 0), nx = new Date(day.getTime() + 86400000);
    var mine = cal.getEvents(day, nx).filter(function (ev) {
      if (String(ev.getTitle() || '').indexOf(P4P_EV_PREFIX) !== 0) return false;
      try { return !ev.isAllDayEvent() || ymd(ev.getAllDayStartDate()) === d; } catch (e) { return true; }
    });
    if (!rows.length) { mine.forEach(function (ev) { try { ev.deleteEvent(); } catch (e) {} }); return; }
    var tot = 0, lines = rows.map(function (r) { var p = p4pPts(r); tot += p; return '• ' + p4pShort(r) + ' = ' + money(p) + ' แต้ม'; });
    tot = p4pR2(tot);
    var title = (P4P_EV_PREFIX + ' ' + money(tot) + ' แต้ม · ' + rows.map(p4pShort).join(', ')).slice(0, 250);
    var desc = 'บันทึกภาระงาน P4P (จาก Vee Note — แก้ในแอป ไม่ต้องแก้ตรงนี้)\n' + lines.join('\n') + '\nรวม ' + money(tot) + ' แต้ม';
    var ev = mine[0];
    if (ev) { if (ev.getTitle() !== title) ev.setTitle(title); try { ev.setDescription(desc); } catch (e) {} mine.slice(1).forEach(function (x) { try { x.deleteEvent(); } catch (e) {} }); }
    else ev = cal.createAllDayEvent(title, day, { description: desc });
    var eid = ev.getId(), sh = sheet('p4p');
    rows.forEach(function (r) { if (r.ev !== eid) sh.getRange(r.row, 12).setValue(eid); });
  } catch (e) { log('p4p-cal', d, '', e.message); }
}
/** ตารางงานในปฏิทินของวันนั้น (ตารางเวร/รพ.สต.) — ใช้เดาว่าตรวจที่ไหนเมื่อภัทรไม่ได้บอก */
function p4pCalCtx(d) {
  var out = [], seen = {};
  try {
    var day = parseLocal(d, 0), nx = new Date(day.getTime() + 86400000);
    [p4pCalName(), ROSTER_CALENDAR, 'เวร วาริน', 'Fammed'].forEach(function (n) {
      if (seen[n]) return; seen[n] = 1;
      var g = getCal(n); if (!g.found) return;
      g.cal.getEvents(day, nx).forEach(function (ev) {
        var t = String(ev.getTitle() || '').trim();
        if (!t || t.indexOf(P4P_EV_PREFIX) === 0 || /^[☐✅]/.test(t)) return;
        out.push((ev.isAllDayEvent() ? 'ทั้งวัน' : hm(ev.getStartTime()) + '-' + hm(ev.getEndTime())) + ' ' + t + ' [' + g.name + ']');
      });
    });
  } catch (e) {}
  return out.slice(0, 15).join('\n');
}
function p4pSystem(d, calCtx) {
  var dd = parseLocal(d, 12), y1 = ymd(new Date(dd.getTime() - 86400000)), y2 = ymd(new Date(dd.getTime() - 2 * 86400000));
  var pcus = []; try { pcus = pcuList().map(function (p) { return p.name; }); } catch (e) {}
  if (!pcus.length) pcus = PCU_SEED.map(function (p) { return p[0]; });
  return [
    'คุณช่วยหมอประภัทร (แพทย์เวชศาสตร์ครอบครัว) บันทึกภาระงาน P4P: แปลงคำพูดเป็นรายการตามตารางรหัสด้านล่าง ต้องแม่นยำ เพราะใช้คิดแต้มจริง',
    'ตอบ JSON บรรทัดเดียวเท่านั้น ไม่มีคำอธิบาย: {"entries":[{"k":"รหัส","q":จำนวน,"d":"YYYY-MM-DD","set":false,"sure":true}],"ask":""}',
    'กติกา:',
    '- k ต้องเป็นรหัสในตารางเท่านั้น ห้ามแต่งใหม่ · q = จำนวนตามหน่วยของรหัสนั้น (คน/ราย/ครั้ง/ชั่วโมง ทศนิยมได้) ตัวเลขไทยหรือคำอ่าน (เก้าสิบเจ็ด) แปลงเป็นตัวเลข',
    '- พูดหลายงานในประโยคเดียว → แยกเป็นหลาย entries',
    '- d: "วันนี้" หรือไม่บอกวัน = ' + d + ' (วัน' + TH_DAYS_FULL[dd.getDay()] + ') · "เมื่อวาน" = ' + y1 + ' · "เมื่อวานซืน" = ' + y2 + ' · บอกวันที่แบบไทย dd/mm/yy เป็นปี พ.ศ. ให้ตอบเป็น ค.ศ.',
    '- set=true เฉพาะเมื่อผู้ใช้บอกว่า แก้/เปลี่ยนเป็น/จริงๆ ได้/ไม่ใช่...แต่เป็น (แทนยอดเดิมของรหัสนั้นในวันนั้น) ปกติ set=false (บวกเพิ่ม)',
    '- ตรวจคนไข้ที่ รพ.สต./PCU/PCC/ศสม. หรือเอ่ยชื่อ รพ.สต. → c_pcu' + (pcus.length ? ' (ชื่อ รพ.สต.: ' + pcus.join(', ') + ')' : ''),
    '- คลินิก NCD/DM/HT/เบาหวาน/ความดัน ใน รพ. → fm_ncd · OPD palliative/ผู้สูงอายุ → fm_geri · OPD ทั่วไป/ปกส/all D/เวร OPD → g_opd · round ward ผู้ป่วยในทั่วไป → fm_round1',
    '- ผู้ป่วยซับซ้อน: บอก >10 นาที → fm_cx10 · ACP/CGA/family meeting/>30 นาที → fm_cx30 · ไม่บอกว่าซับซ้อนใช้รหัสปกติ',
    '- "ตรวจคนไข้ X คน" ไม่บอกที่ → ดูตารางงานในปฏิทินของวันนั้นด้านล่าง (เช่น มี รพ.สต. → c_pcu, NCD → fm_ncd, OPD palliative → fm_geri, ปกส/OPD → g_opd, IPD → fm_round1) แล้วใส่ sure=false ; ไม่มีข้อมูลเลย → g_opd sure=false',
    '- ประชุมไม่บอกบทบาท → รหัสลงท้าย _1 sure=false · งานวิชาการ/วิทยากรนับเป็นชั่วโมง ไม่บอกชั่วโมง → ถามใน ask (entries ว่างสำหรับรายการนั้น)',
    '- เดารหัสเมื่อไม่ชัด ให้ sure=false · ชัดเจน sure=true',
    '- ไม่ใช่ภาระงาน หรือไม่มีจำนวน → ไม่ใส่ใน entries แล้วถามกลับสั้นๆ ภาษาไทยใน ask (ลงท้าย ครับ)',
    'ตาราง (รหัส | หมวด | งาน | หน่วย | แต้ม/หน่วย | คำเรียกอื่น):',
    p4pTable().map(function (x) { return x.k + ' | ' + x.s + ' | ' + x.n + ' | ' + x.u + ' | ' + (x.sc == null ? '-' : x.sc) + (x.h ? ' | ' + x.h : ''); }).join('\n'),
    'ตารางงานในปฏิทินวันที่ ' + d + ':\n' + (calCtx || '(ไม่มี)')
  ].join('\n');
}
/** ข้อความ → บันทึก · คืน { msg, ask, warn, saved } */
function p4pCapture(text, date) {
  text = String(text || '').trim();
  if (!text) return { msg: '', ask: 'ยังไม่ได้ยินอะไรเลยครับ', warn: true, saved: [] };
  var today = ymd(new Date()), d = p4pYmd(date, today), j = null, raw = '';
  try { raw = callClaude(p4pSystem(d, p4pCalCtx(d)), text, 800, prop('P4P_MODEL') || P4P_MODEL); j = extractJson(raw); }
  catch (e) { log('p4p', text, '', e.message); return { msg: '⚠️ AI ใช้ไม่ได้ชั่วคราว ลองใหม่อีกครั้ง หรือกด ＋ เพิ่มเอง', ask: '⚠️ AI ใช้ไม่ได้ชั่วคราว ยังไม่ได้บันทึก — ลองใหม่อีกครั้ง หรือกด ＋ เพิ่มเอง ครับ', warn: true, saved: [] }; }
  log('p4p', text, raw, j ? '' : 'JSON ไม่ถูกต้อง');
  var lo = ymd(new Date(Date.now() - 400 * 86400000)), hi = ymd(new Date(Date.now() + 2 * 86400000));
  var list = ((j && j.entries) || []).map(function (e) {
    var ed = p4pYmd(e.d, d); if (ed < lo || ed > hi) ed = d;
    return { k: e.k, q: e.q, d: ed, set: e.set === true, sure: e.sure !== false };
  });
  var saved = p4pAdd(list, text), ask = String((j && j.ask) || '').trim();
  if (!saved.length) return { msg: ask || 'วียังจับไม่ได้ว่าเป็นภาระงานอะไร', ask: ask || 'วียังจับไม่ได้ว่าเป็นภาระงานอะไร ลองพูดแบบ “ตรวจ รพ.สต. 97 คน” หรือ “เยี่ยมบ้านรายใหม่ 2 ราย” ครับ', warn: true, saved: [] };
  var guess = saved.some(function (s) { return s.g; });
  var msg = '📋 ' + saved.map(p4pLine).join('\n📋 ') + (guess ? '\nวีเดาบางรายการ (ป้ายส้ม) แตะเพื่อเช็คได้' : '') + (ask ? '\n' + ask : '');
  return { msg: msg, ask: ask, warn: false, saved: saved };
}
/** ข้อมูลให้แอป: ตาราง + รายการ 2 เดือนล่าสุด + ยอดรายเดือนย้อนหลัง 12 เดือน */
function p4pData() {
  try {
    var now = new Date(), from = ymd(new Date(now.getFullYear(), now.getMonth() - 1, 1)), m12 = fmt(new Date(now.getFullYear(), now.getMonth() - 11, 1), 'yyyy-MM');
    var t = p4pTable(), known = {}, months = {}, list = [];
    t.forEach(function (x) { known[x.k] = 1; });
    p4pRows().forEach(function (r) {
      var p = p4pPts(r), ym = r.d.slice(0, 7);
      if (ym >= m12) months[ym] = p4pR2((months[ym] || 0) + p);
      if (r.d >= from) { var o = { id: r.id, d: r.d, k: r.k, q: r.q, p: p }; if (r.g) o.g = 1; if (!known[r.k]) o.n = r.n + ' ' + money(r.q) + ' ' + p4pUnit(r.u, r.s); if (r.raw) o.r = r.raw.slice(0, 120); list.push(o); }
    });
    return { items: t.map(function (x) { return { k: x.k, s: x.s, n: x.n, a: x.a, u: p4pUnit(x.u, x.s), sc: x.sc }; }),
      secs: P4P_SECTIONS.map(function (s) { return { t: s[1], ic: s[2] }; }), list: list, months: months, from: from,
      target: p4pNum('P4P_TARGET', P4P_TARGET), guarantee: p4pNum('P4P_GUARANTEE', P4P_GUARANTEE), cal: p4pCalName() };
  } catch (e) { log('p4p-data', '', '', e.message); return null; }
}
"""
C=rep(C,"/** เปลี่ยนทุกครั้งที่แก้แอป",P4P_JS.lstrip('\n')+"/** เปลี่ยนทุกครั้งที่แก้แอป")
# ---------------- หน้าแอป ----------------
H=rep(H,"#party{","""/* v59: บันทึกภาระงาน P4P */
:root{--wk:#0E7C74;--wk-head:#BFE7E1;--wk-ink:#06403B;--wk-soft:#EDF7F5}
nav{grid-template-columns:repeat(2,minmax(0,1fr)) 84px repeat(2,minmax(0,1fr)) 52px;padding-right:6px}
nav .wkb{align-self:center;justify-self:center;width:42px;height:42px;border-radius:21px;padding:0;background:var(--wk-soft);border:1.5px solid #9FD6CE;color:var(--wk);gap:0}
nav .wkb.on{background:var(--wk);border-color:var(--wk);color:#fff;box-shadow:0 3px 10px rgba(14,124,116,.35)}
nav .vbtn.wk{background:var(--wk);box-shadow:0 4px 14px rgba(14,124,116,.35)}
.wkhd{background:linear-gradient(160deg,#CDEEE9,#A9DDD5);color:var(--wk-ink);padding-bottom:14px}
.wkhd .wkbig{width:46px;height:46px;border-radius:23px;background:rgba(255,255,255,.55);display:flex;align-items:center;justify-content:center;color:var(--wk);flex-shrink:0}
.wkbar{position:relative;height:12px;background:rgba(255,255,255,.65);border-radius:6px;margin-top:8px}
.wkbar i{position:absolute;left:0;top:0;bottom:0;border-radius:6px;background:var(--wk);transition:width .4s ease}
.wkbar b{position:absolute;top:-4px;width:2px;height:20px;background:var(--wk-ink);opacity:.55;border-radius:1px}
.wkleft{display:flex;justify-content:space-between;gap:8px;font-size:12px;margin-top:4px}
.wkday{display:flex;align-items:center;gap:8px}
.wkday>button{width:44px;height:44px;border-radius:22px;border:1px solid var(--line);background:#fff;font-size:20px;color:var(--wk);flex-shrink:0}
.wkday .t{flex:1;text-align:center;font-weight:700;font-size:15px;color:var(--wk-ink)}
.wkday .t small{display:block;font-weight:500;font-size:12px;color:var(--mute)}
.wkday .td{height:32px;padding:0 12px;border-radius:16px;border:1px solid var(--wk);background:#fff;color:var(--wk);font-size:13px;font-weight:600;width:auto}
.wke{display:flex;align-items:center;gap:12px;padding:12px 16px;border:0;border-bottom:1px solid var(--soft);background:none;width:100%;text-align:left;font:inherit;color:inherit;cursor:pointer;min-height:56px}
.wke:last-child{border-bottom:0}
.wke .ic{width:38px;height:38px;border-radius:11px;background:var(--wk-soft);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:19px}
.wke .t{font-size:15px;font-weight:600}
.wke .s{font-size:12px;color:var(--mute)}
.wke .p{font-weight:700;color:var(--wk);white-space:nowrap;font-size:16px;text-align:right}
.wke .p small{display:block;font-size:11px;font-weight:500;color:var(--mute)}
.wkp .ic{animation:wkpulse 1.1s ease-in-out infinite}
@keyframes wkpulse{0%,100%{opacity:1}50%{opacity:.35}}
.wkg{display:inline-block;font-size:11px;font-weight:600;color:var(--warn);background:#FFF1DC;border-radius:8px;padding:1px 7px;margin-left:6px;vertical-align:2px}
.wkask{border:1px solid #F3D19E;background:#FFF8EC;border-radius:14px;padding:10px 12px;display:flex;gap:10px;align-items:flex-start;font-size:14px;white-space:pre-line}
.wkask img{width:36px;height:36px;border-radius:18px;background:#DCE7F7;flex-shrink:0}
.wkask button{width:32px;height:32px;border-radius:16px;border:0;background:rgba(0,0,0,.06);flex-shrink:0}
.wkadd{height:44px;border-radius:12px;border:1.5px dashed var(--wk);background:#fff;color:var(--wk);font-weight:600}
.wkhint{font-size:12px;color:var(--mute);padding:0 4px}
.wksr{display:flex;align-items:center;gap:10px;padding:10px 16px;border-bottom:1px solid var(--soft)}
.wksr:last-child{border-bottom:0}
.wksr .nm{flex:1;min-width:0;font-size:14px}
.wksr .br{height:6px;background:var(--soft);border-radius:3px;margin-top:4px;overflow:hidden}
.wksr .br i{display:block;height:100%;background:var(--wk);border-radius:3px}
.wksr b{font-size:14px;color:var(--wk-ink);white-space:nowrap}
.wkdays{display:flex;flex-wrap:wrap;gap:6px;padding:12px 16px}
.wkdays button{height:36px;padding:0 10px;border-radius:18px;border:1px solid var(--line);background:#fff;font-size:13px}
.wkdays button.on{background:var(--wk);border-color:var(--wk);color:#fff;font-weight:600}
.wkcalc{font-size:15px;color:var(--wk-ink);background:var(--wk-soft);border-radius:10px;padding:10px 12px}
.wknote{font-size:12px;color:var(--mute);line-height:1.6;padding:0 4px 8px}
#party{""")
WK_ICON=r"""  paper: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.2 2.8h8l4.8 4.8v12.6a1.4 1.4 0 0 1-1.4 1.4H6.2a1.4 1.4 0 0 1-1.4-1.4V4.2a1.4 1.4 0 0 1 1.4-1.4z"/><path d="M14.2 2.8v4.8H19" fill="currentColor" fill-opacity=".25"/><path d="M7.8 12.6h2.1l1.3-2.4 1.9 4.6 1.3-2.2h1.9"/><path d="M8 17.4h8"/></svg>',
  paperBig: '<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><path d="M8 3h11.5L26 9.5V27a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" fill="#fff" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M19.5 3v6.5H26" fill="#BFE7E1" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M10 16.5h3l1.8-3.4 2.6 6.4 1.8-3h3" fill="none" stroke="#E5484D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.5 23h11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="24" cy="25" r="5.2" fill="#F2C230" stroke="#fff" stroke-width="1.6"/><path d="M21.8 25.2l1.5 1.5 2.9-3.1" fill="none" stroke="#06403B" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"""
H=rep(H,"  send: '<svg width=\"20\"",WK_ICON+"  send: '<svg width=\"20\"")
# แท็บ + ปุ่มกลมกระดาษ (ต่อจาก การเงิน)
H=rep(H,"var accent = { today: 'var(--today)', pj: 'var(--pj)', idea: 'var(--idea)', money: 'var(--fin)' }[S.tab];",
        "var accent = { today: 'var(--today)', pj: 'var(--pj)', idea: 'var(--idea)', money: 'var(--fin)', work: 'var(--wk)' }[S.tab];")
H=rep(H,"S.tab === 'money' ? viewMoney() : viewIdeas();","S.tab === 'money' ? viewMoney() : S.tab === 'work' ? viewWork() : viewIdeas();")
H=rep(H,"var vb = '<button class=\"vbtn' + (V.rec ? ' rec' : V.busy ? ' busy' : '') + '\" data-act=\"voice\" aria-label=\"' + (V.rec ? 'หยุดแล้วส่ง' : 'พูดกับ Vee')",
        "var vb = '<button class=\"vbtn' + (V.rec ? ' rec' : V.busy ? ' busy' : S.tab === 'work' ? ' wk' : '') + '\" data-act=\"voice\" aria-label=\"' + (V.rec ? 'หยุดแล้วส่ง' : S.tab === 'work' ? 'พูดภาระงาน' : 'พูดกับ Vee')")
H=rep(H,": V.busy ? 'กำลังฟัง…' : 'พูดกับ Vee') + '</span></button>';",": V.busy ? 'กำลังฟัง…' : S.tab === 'work' ? 'พูดภาระงาน' : 'พูดกับ Vee') + '</span></button>';\n  var wkb = '<button class=\"wkb' + (S.tab === 'work' ? ' on' : '') + '\" data-act=\"tab\" data-v=\"work\" aria-label=\"บันทึกภาระงาน\"' + (S.tab === 'work' ? ' aria-current=\"page\"' : '') + '>' + ICON.paper + '</button>';")
H=rep(H,"'<nav>' + tabs.slice(0, 2).join('') + vb + tabs.slice(2).join('') + '</nav>'","'<nav>' + tabs.slice(0, 2).join('') + vb + tabs.slice(2).join('') + wkb + '</nav>'")
H=rep(H,"(S.ans ? viewAns() : '')","(S.ans ? viewAns() : '') + (S.we ? viewWEdit() : '')")
# เสียง/ช่องพิมพ์ใหญ่ ตอนอยู่หน้าบันทึกภาระงาน → ลง P4P
H=rep(H,"    toast('🎤 ส่งแล้ว กำลังฟัง…');\n    api('voice', { b64: String(fr.result).split(',')[1], mime: type, sec: sec });",
        "    toast('🎤 ส่งแล้ว กำลังฟัง…');\n    if (S.tab === 'work') { S.wpend = (S.wpend || 0) + 1; S.wask = ''; render(); return api('p4pvoice', { b64: String(fr.result).split(',')[1], mime: type, sec: sec, date: S.wdate || todayStr() }); }\n    api('voice', { b64: String(fr.result).split(',')[1], mime: type, sec: sec });")
H=rep(H,"  if (kind === 'vtext') { var vt = f.text.value.trim(); if (!vt) return; S.vsheet = false; render();",
        "  if (kind === 'vtext' && S.tab === 'work') { var wv = f.text.value.trim(); if (!wv) return; S.vsheet = false; return wkSend(wv); }\n  if (kind === 'wquick') { var wq = f.text.value.trim(); if (!wq) return; f.text.value = ''; return wkSend(wq); }\n  if (kind === 'vtext') { var vt = f.text.value.trim(); if (!vt) return; S.vsheet = false; render();")
H=rep(H,"    running = false;\n","    running = false;\n    if (job.action === 'p4p' || job.action === 'p4pvoice') { S.wpend = Math.max(0, (S.wpend || 0) - 1); if (res) S.wask = res.wask || ''; else if (err) S.wask = '⚠️ ' + (err.message || err) + ' — ยังไม่ได้บันทึก'; }\n")
H=rep(H,"(job.action === 'capture' || job.action === 'voice' || res.warn)","(job.action === 'capture' || job.action === 'voice' || /^p4p/.test(job.action) || res.warn)")
H=rep(H,"  var act = el.getAttribute('data-act'), id = el.getAttribute('data-id'), v = el.getAttribute('data-v');\n",
        "  var act = el.getAttribute('data-act'), id = el.getAttribute('data-id'), v = el.getAttribute('data-v');\n  if (/^w(day|today|go|edit|new|save|del|close|askx)$/.test(act)) return wkAct(act, id, v, el, ev);\n")
WK_UI=r"""/* v59: บันทึกภาระงาน P4P — พูด/พิมพ์ → วีแยกเป็นรายการ + แต้ม · แตะรายการเพื่อแก้/ลบ (เปลี่ยนบนจอทันที) */
var WK_MON = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'];
var WK_WD = ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'];
function wkD() { return (D && D.p4p) || { items: [], secs: [], list: [], months: {}, target: 3000, guarantee: 2200, cal: '', from: '' }; }
function wkIt(k) { var a = wkD().items; for (var i = 0; i < a.length; i++) if (a[i].k === k) return a[i]; return null; }
function wkN(n) { return (Math.round((+n || 0) * 100) / 100).toLocaleString('en-US', { maximumFractionDigits: 2 }); }
function wkIc(s) { var a = wkD().secs; for (var i = 0; i < a.length; i++) if (a[i].t === s) return a[i].ic; return '📋'; }
function wkLabel(e) { var it = wkIt(e.k); return it ? it.a + ' ' + wkN(e.q) + ' ' + it.u : (e.n || e.k); }
function wkPts(k, q) { var it = wkIt(k); return it && it.sc != null ? Math.round(it.sc * (+q || 0) * 100) / 100 : 0; }
function wkShift(d, n) { var p = d.split('-'), x = new Date(+p[0], +p[1] - 1, +p[2] + n); return x.getFullYear() + '-' + ('0' + (x.getMonth() + 1)).slice(-2) + '-' + ('0' + x.getDate()).slice(-2); }
function wkWd(d) { var p = d.split('-'); return WK_WD[new Date(+p[0], +p[1] - 1, +p[2]).getDay()]; }
function wkMon(ym) { return WK_MON[+ym.slice(5, 7) - 1] + ' ' + (+ym.slice(0, 4) + 543); }
function wkTot(ym) { return wkD().months[ym] || 0; }
function wkSend(text) {
  S.wpend = (S.wpend || 0) + 1; S.wask = ''; render();
  toast('📋 รับแล้ว วีกำลังแยกภาระงาน…');
  api('p4p', { text: text, date: S.wdate || todayStr() });
}
function wkRow(e) {
  var it = wkIt(e.k), un = it && it.sc == null;
  return '<button class="wke" data-act="wedit" data-id="' + esc(e.id) + '"><span class="ic" aria-hidden="true">' + wkIc(it ? it.s : '') + '</span><span class="col"><span class="t">' + esc(wkLabel(e)) +
    (e.g ? '<span class="wkg">วีเดา แตะเช็ค</span>' : '') + '</span><span class="s">' + (it ? esc(it.s) + (un ? ' · ยังไม่มีแต้มในตาราง' : ' · ' + wkN(it.sc) + ' แต้ม/' + esc(it.u)) : 'ไม่มีรหัสนี้ในตารางแล้ว') + '</span></span>' +
    '<span class="p">' + wkN(e.p) + '<small>แต้ม</small></span></button>';
}
function viewWork() {
  var W = wkD(), today = todayStr(), day = S.wdate || (S.wdate = today), ym = day.slice(0, 7), tot = wkTot(ym), tg = W.target || 3000, gu = W.guarantee || 0;
  var pct = Math.min(100, tot / tg * 100), gp = Math.min(100, gu / tg * 100);
  var left = tot >= tg ? '🎉 ถึงเป้าเดือนนี้แล้ว' : gu && tot >= gu ? '✓ ผ่านแต้มประกัน · อีก ' + wkN(tg - tot) + ' ถึงเป้า' : 'อีก ' + wkN(gu ? gu - tot : tg - tot) + ' แต้มถึง' + (gu ? 'แต้มประกัน' : 'เป้า');
  var list = W.list.filter(function (e) { return e.d === day; }), dtot = 0; list.forEach(function (e) { dtot += +e.p || 0; });
  var h = '<header class="wkhd"><div class="h1r"><div><h1>บันทึกภาระงาน</h1><div class="sub">P4P ' + wkMon(ym) + ' · <b>' + wkN(tot) + '</b> / ' + wkN(tg) + ' แต้ม</div></div><span class="wkbig">' + ICON.paperBig + '</span></div>' +
    '<div class="wkbar" role="img" aria-label="ได้ ' + wkN(tot) + ' จากเป้า ' + wkN(tg) + ' แต้ม"><i style="width:' + pct.toFixed(1) + '%"></i>' + (gu && gu < tg ? '<b style="left:' + gp.toFixed(1) + '%" title="แต้มประกัน"></b>' : '') + '</div>' +
    '<div class="wkleft"><span>' + left + '</span><span>' + Math.round(pct) + '%</span></div></header><main style="background:var(--wk-soft)">';
  if (S.wask) h += '<div class="wkask" role="status">' + (typeof CAT_IMG === 'string' && CAT_IMG.length > 40 ? '<img src="' + CAT_IMG + '" alt="">' : '') + '<div style="flex:1">' + esc(S.wask) + '</div><button data-act="waskx" aria-label="ปิด">✕</button></div>';
  h += '<div class="wkday"><button data-act="wday" data-v="-1" aria-label="วันก่อนหน้า">‹</button><div class="t">' + (day === today ? 'วันนี้' : 'วัน' + wkWd(day)) + ' ' + beDMY(day) + '<small>' + (day === today ? 'วัน' + wkWd(day) : '') + '</small></div>' +
    (day !== today ? '<button class="td" data-act="wtoday">วันนี้</button>' : '') + '<button data-act="wday" data-v="1" aria-label="วันถัดไป"' + (day >= today ? ' disabled style="opacity:.3"' : '') + '>›</button></div>';
  h += '<form class="quick" data-form="wquick" style="border-radius:14px;border:0"><label class="sr" for="wk-q">พิมพ์ภาระงาน</label><input id="wk-q" name="text" autocomplete="off" placeholder="เช่น ตรวจ รพ.สต. 97 คน, เยี่ยมบ้านใหม่ 2"><button class="send" style="background:var(--wk)" aria-label="บันทึก">' + ICON.send + '</button></form>' +
    '<div class="wkhint">หรือกดไมค์สีเขียวตรงกลางแล้วพูด เช่น “วันนี้ตรวจคนไข้ รพ.สต. ได้ 97 คน”</div>';
  var pend = ''; for (var i = 0; i < (S.wpend || 0); i++) pend += '<div class="wke wkp"><span class="ic" aria-hidden="true">⏳</span><span class="col"><span class="t">วีกำลังแยกภาระงาน…</span><span class="s">แป๊บเดียวครับ</span></span></div>';
  h += '<section class="sec"><div class="ghd"><h3 style="color:var(--wk)">' + (day === today ? 'ภาระงานวันนี้' : 'ภาระงาน ' + beDMY(day)) + '</h3><span>รวม <b>' + wkN(dtot) + '</b> แต้ม</span></div><div class="card">' + pend +
    (list.length ? list.map(wkRow).join('') : pend ? '' : '<div class="empty">ยังไม่มีบันทึก — พูดหรือพิมพ์ได้เลย</div>') + '</div><button class="wkadd" data-act="wnew">＋ เพิ่มเอง (เลือกจากตาราง)</button></section>';
  // สรุปเดือน: ตามหมวด + วันที่บันทึก
  var ml = W.list.filter(function (e) { return e.d.slice(0, 7) === ym; });
  if (ml.length) {
    var bs = {}, bd = {}, mx = 0;
    ml.forEach(function (e) { var it = wkIt(e.k), s = it ? it.s : 'อื่นๆ'; bs[s] = (bs[s] || 0) + (+e.p || 0); bd[e.d] = (bd[e.d] || 0) + (+e.p || 0); });
    var ss = Object.keys(bs).sort(function (a, b) { return bs[b] - bs[a]; }); ss.forEach(function (s) { if (bs[s] > mx) mx = bs[s]; });
    h += '<section class="sec"><div class="ghd"><h3 style="color:var(--wk)">สรุป ' + wkMon(ym) + ' ตามหมวด</h3><span>' + Object.keys(bd).length + ' วันที่บันทึก</span></div><div class="card">' +
      ss.map(function (s) { return '<div class="wksr"><span aria-hidden="true">' + wkIc(s) + '</span><div class="nm">' + esc(s) + '<div class="br"><i style="width:' + (mx ? bs[s] / mx * 100 : 0).toFixed(1) + '%"></i></div></div><b>' + wkN(bs[s]) + '</b></div>'; }).join('') +
      '<div class="wkdays">' + Object.keys(bd).sort().reverse().map(function (d) { return '<button data-act="wgo" data-v="' + d + '" class="' + (d === day ? 'on' : '') + '">' + beDMY(d).slice(0, 5) + ' · ' + wkN(bd[d]) + '</button>'; }).join('') + '</div></div></section>';
  }
  var ms = Object.keys(W.months || {}).sort().reverse().slice(0, 6);
  if (ms.length > 1 || (ms.length && ms[0] !== ym)) h += '<section class="sec"><div class="ghd"><h3 style="color:var(--wk)">ย้อนหลังรายเดือน</h3><span>เป้า ' + wkN(tg) + '</span></div><div class="card">' +
    ms.map(function (m) { var v = W.months[m]; return '<div class="wksr"><div class="nm">' + wkMon(m) + '<div class="br"><i style="width:' + Math.min(100, v / tg * 100).toFixed(1) + '%"></i></div></div><b>' + wkN(v) + '</b></div>'; }).join('') + '</div></section>';
  h += '<div class="wknote">📆 ลง Google Calendar “' + esc(W.cal || '') + '” ให้อัตโนมัติ วันละ 1 รายการทั้งวัน (📋 P4P …) อัปเดตทุกครั้งที่แก้/ลบ<br>แก้คะแนนต่อหน่วยหรือเพิ่มงานใหม่ได้ในชีท แท็บ “ตาราง P4P”</div>';
  return h + '</main>';
}
function viewWEdit() {
  var e = S.we, W = wkD(), isNew = e.id === 'new', it = wkIt(e.k);
  var opts = W.secs.map(function (s) {
    var its = W.items.filter(function (x) { return x.s === s.t; }); if (!its.length) return '';
    return '<optgroup label="' + esc(s.ic + ' ' + s.t) + '">' + its.map(function (x) { return '<option value="' + esc(x.k) + '"' + (x.k === e.k ? ' selected' : '') + '>' + esc(x.a) + (x.sc == null ? ' (ยังไม่มีแต้ม)' : ' · ' + wkN(x.sc)) + '</option>'; }).join('') + '</optgroup>';
  }).join('');
  var other = W.items.filter(function (x) { return !W.secs.some(function (s) { return s.t === x.s; }); });
  if (other.length) opts += '<optgroup label="อื่นๆ">' + other.map(function (x) { return '<option value="' + esc(x.k) + '"' + (x.k === e.k ? ' selected' : '') + '>' + esc(x.a) + '</option>'; }).join('') + '</optgroup>';
  return '<div class="sheet" data-act="wclose"><div class="box" role="dialog" aria-label="' + (isNew ? 'เพิ่มภาระงาน' : 'แก้ภาระงาน') + '"><h3>' + (isNew ? '＋ เพิ่มภาระงาน' : '✏️ แก้ภาระงาน') + '</h3>' +
    (e.r ? '<div style="font-size:13px;color:var(--mute)">ที่พูดไว้: “' + esc(e.r) + '”</div>' : '') +
    (e.g ? '<div style="font-size:13px;color:var(--warn)">วีเดารหัสงานนี้ เช็คแล้วกดบันทึกเพื่อยืนยัน</div>' : '') +
    '<div class="form" style="padding:0"><label for="we-k">งาน</label><select id="we-k" data-we="k">' + opts + '</select>' +
    (it && it.n !== it.a ? '<div style="font-size:12px;color:var(--mute)">' + esc(it.n) + '</div>' : '') +
    '<label for="we-q">จำนวน (' + esc(it ? it.u : '') + ')</label><input id="we-q" data-we="q" inputmode="decimal" autocomplete="off" value="' + esc(e.q) + '">' +
    '<label for="we-d">วันที่</label><input id="we-d" type="date" data-we="d" value="' + esc(e.d) + '">' +
    '<div class="wkcalc">= <b id="we-p">' + wkN(wkPts(e.k, e.q)) + '</b> แต้ม' + (it && it.sc != null ? ' <span style="color:var(--mute);font-size:13px">(' + wkN(it.sc) + ' × จำนวน)</span>' : it ? ' <span style="color:var(--warn);font-size:13px">ยังไม่มีแต้มในตาราง</span>' : '') + '</div></div>' +
    '<div class="two"><button data-act="wsave" style="border:0;background:var(--wk);color:#fff">บันทึก</button>' +
    (isNew ? '' : '<button data-act="wdel" style="border:1px solid #F3C1BB;background:' + (S.arm === 'wdel' ? '#B42318' : '#fff') + ';color:' + (S.arm === 'wdel' ? '#fff' : '#B42318') + '">' + (S.arm === 'wdel' ? 'แตะอีกครั้งเพื่อลบ' : '🗑 ลบ') + '</button>') + '</div>' +
    '<button data-act="wclose" style="height:44px;border:0;background:var(--soft);border-radius:10px;font-weight:600">ปิด</button></div></div>';
}
function wkRecalc(ym) { var W = wkD(), s = 0; W.list.forEach(function (e) { if (e.d.slice(0, 7) === ym) s += +e.p || 0; }); if (!W.from || ym + '-01' >= W.from) W.months[ym] = Math.round(s * 100) / 100; }
function wkAct(act, id, v, el, ev) {
  var W = wkD();
  if (act === 'wclose') { if (el.classList.contains('sheet') && ev.target !== el) return; S.we = null; S.arm = null; return render(); }
  if (act === 'waskx') { S.wask = ''; return render(); }
  if (act === 'wday') { var nd = wkShift(S.wdate || todayStr(), +v); if (nd > todayStr()) return; S.wdate = nd; return render(); }
  if (act === 'wtoday') { S.wdate = todayStr(); return render(); }
  if (act === 'wgo') { S.wdate = v; render(); var m = document.querySelector('main'); if (m) m.scrollTop = 0; return; }
  if (act === 'wnew') { S.arm = null; S.we = { id: 'new', k: (W.items[0] || {}).k || '', q: '', d: S.wdate || todayStr() }; return render(); }
  if (act === 'wedit') { var e = W.list.filter(function (x) { return x.id === id; })[0]; if (!e) return; if (/^tmp/.test(e.id)) return toast('รอบันทึกแป๊บนึงครับ'); S.arm = null; S.we = { id: e.id, k: e.k, q: e.q, d: e.d, r: e.r || '', g: !!e.g }; return render(); }
  if (act === 'wsave') {
    var f = S.we, q = parseFloat(String(f.q || '').replace(/,/g, ''));
    if (!wkIt(f.k)) return toast('เลือกงานก่อนครับ');
    if (!(q > 0)) return toast('ใส่จำนวนก่อนครับ');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(f.d || '')) return toast('เลือกวันที่ก่อนครับ');
    S.we = null; S.arm = null;
    var p = wkPts(f.k, q), lab = wkLabel({ k: f.k, q: q });
    toast('📋 ' + lab + ' = ' + wkN(p) + ' แต้ม');
    if (f.id === 'new') return api('p4padd', { k: f.k, q: q, date: f.d }, function () { W.list.push({ id: 'tmp' + (++tmpN), d: f.d, k: f.k, q: q, p: p }); wkRecalc(f.d.slice(0, 7)); });
    return api('p4pedit', { id: f.id, k: f.k, q: q, date: f.d }, function () {
      W.list.forEach(function (x) { if (x.id === f.id) { var om = x.d.slice(0, 7); x.k = f.k; x.q = q; x.d = f.d; x.p = p; delete x.g; wkRecalc(om); } });
      wkRecalc(f.d.slice(0, 7));
    });
  }
  if (act === 'wdel') {
    if (S.arm !== 'wdel') { S.arm = 'wdel'; return render(); }
    var did = S.we.id, de = W.list.filter(function (x) { return x.id === did; })[0]; S.we = null; S.arm = null;
    toast('🗑 ลบ ' + (de ? wkLabel(de) : ''));
    return api('p4pdel', { id: did }, function () { W.list = W.list.filter(function (x) { return x.id !== did; }); if (de) wkRecalc(de.d.slice(0, 7)); });
  }
}
function wkInput(ev) {
  var el = ev.target, k = el && el.getAttribute && el.getAttribute('data-we'); if (!k || !S.we) return;
  S.we[k] = el.value;
  if (k === 'k') return render();
  var pe = $('we-p'); if (pe) pe.textContent = wkN(wkPts(S.we.k, S.we.q));
}
document.addEventListener('input', wkInput);
document.addEventListener('change', wkInput);
"""
H=rep(H,"function viewMore() {",WK_UI+"function viewMore() {")
assert "Code.v58" not in H
out=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
open('Code.v59b.gs','w',encoding='utf8',newline='\n').write(out)
print('OK Code.v59b.gs',ck(out))
