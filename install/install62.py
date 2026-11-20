# v62: Vee อ่านออกเสียง (Google Cloud Text-to-Speech → ไฟล์เสียงเข้า Telegram ฟังตอนขับรถ)
#  แชท: "อ่านให้ฟัง ..." / "อ่าน: ..." · "สรุปให้ฟัง ..." · ตอบกลับข้อความด้วย "อ่าน" หรือ "สรุปให้ฟัง"
#        "ฟังทีหลัง ..." (เข้าคิว) · "ขับรถ" (ส่งทั้งคิว) · "ฟังวันนี้" · "ทดสอบเสียง" (เลือกเสียง)
#        ใต้ไฟล์เสียง: ✓ ฟังแล้ว · 💡 เก็บเป็นไอเดีย · 🔁 สรุปสั้นลง · สรุปเช้ามีปุ่ม 🔊 ฟังสรุปวันนี้
#  แอป: ปุ่ม 🎧 หัวหน้า วันนี้ → หน้า "ฟัง" (ม่วง) · 🔊 ฟัง บนการ์ด project/ไอเดีย · 📲 ส่งเป็นเสียง ใต้คำตอบ Vee
#  ต้องตั้ง Script Property: TTS_KEY (API key ของ Google Cloud ที่เปิด Text-to-Speech API) · TTS_VOICE (ไม่ใส่ = เลือก Chirp3-HD ไทยเอง)
# รันในโฟลเดอร์ที่มี Code.v61.gs : python patch62.py  → ได้ Code.v62.gs
import json,re
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v61.gs',encoding='utf8').read()
assert ck(B)==(564542,5749),('base ไม่ใช่ v61',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v61';","var APP_VER = 'v62';")
C=rep(C,"  log:      { name: 'Log',",
"""  listen:   { name: 'คิวฟัง',        headers: ['ID', 'สร้างเมื่อ', 'ชื่อ', 'ข้อความ', 'โหมด', 'ที่มา', 'สถานะ', 'ตัวอักษร', 'ส่งเมื่อ'] },
  log:      { name: 'Log',""")
C=rep(C,"    p4p: p4pData(), subs: subsData(), money: appMoney(),","    p4p: p4pData(), subs: subsData(), listen: lsData(), tts: ttsInfo(), money: appMoney(),")
# แชท: คำสั่งเสียงอ่าน (ก่อนคำสั่งเร็ว/AI)
C=rep(C,"""  if (handleAwaitInput(chatId, text, prefix)) return; // กำลังรอพิมพ์ต่อจากปุ่ม project
""","""  if (handleAwaitInput(chatId, text, prefix)) return; // กำลังรอพิมพ์ต่อจากปุ่ม project
  if (lsHandleText(chatId, text, msg)) return; // v62: อ่านให้ฟัง / สรุปให้ฟัง / ฟังทีหลัง / ขับรถ / ฟังวันนี้ / ทดสอบเสียง
""")
C=rep(C,"""  if (data.indexOf('ro:') === 0) return handleRosterCallback(cq, data);""","""  if (data.indexOf('ro:') === 0) return handleRosterCallback(cq, data);
  if (data.indexOf('ls:') === 0) return lsCallback(cq, data);""")
# สรุปเช้า: ปุ่ม 🔊
C=rep(C,"""  sendOwner('☀️ สวัสดีตอนเช้าครับ\\n\\n' + cl.text, cl.keyboard);""","""  sendOwner('☀️ สวัสดีตอนเช้าครับ\\n\\n' + cl.text, (cl.keyboard || []).concat([[{ text: '🔊 ฟังสรุปวันนี้', callback_data: 'ls:b' }]]));""")
# แอป
C=rep(C,"""  } else if (action === 'slip') {""","""  } else if (/^ls(add|send|del|drive|brief|now|proj|say)$/.test(action)) {
    var lr = lsApi(action, a); msg = lr.msg; warn = !!lr.warn;
  } else if (action === 'slip') {""")
# help
C=rep(C,"""function helpText() {
  return 'Vee Note 📒 พิมพ์บอกได้เลย เช่น\\n' +""","""function helpText() {
  return 'Vee Note 📒 พิมพ์บอกได้เลย เช่น\\n' +
    '• อ่านให้ฟัง <ข้อความ> / สรุปให้ฟัง <ข้อความ>  → ส่งเป็นไฟล์เสียง (ตอบกลับข้อความไหนด้วย "อ่าน" ก็ได้)\\n' +
    '• ฟังทีหลัง <ข้อความ> → เข้าคิว · ขับรถ → ส่งทั้งคิว · ฟังวันนี้ · ทดสอบเสียง\\n' +""")
LS_JS=r"""
/* ============================================================
 *  v62: Vee อ่านออกเสียง — Google Cloud Text-to-Speech → MP3 → Telegram (sendAudio)
 *  ฟังตอนขับรถได้ (ล็อกจอแล้วยังเล่น) · ฟรีเดือนละ 1 ล้านตัวอักษร (Chirp 3: HD) · เกินคิด $30/ล้านตัวอักษร
 *  Script Properties: TTS_KEY (จำเป็น) · TTS_VOICE (ไม่ใส่ = Chirp3-HD ไทยตัวแรก) · TTS_RATE (ความเร็ว 0.8–1.3, ปกติ 1)
 * ============================================================ */
var TTS_FREE = 1000000;        // ตัวอักษรฟรี/เดือน (Chirp 3: HD และ Neural2 · Standard/WaveNet ได้ 4 ล้าน)
var TTS_CHUNK = 1400;          // ตัวอักษรไทยต่อครั้ง (API รับไม่เกิน 5,000 ไบต์ · ไทย 1 ตัว = 3 ไบต์)
var TTS_MAX = 20000;           // ยาวเกินนี้ตัดทิ้ง (กันเผลอส่งหนังสือทั้งเล่ม)
var LS_WAIT = 'รอ', LS_SENT = 'ส่งแล้ว', LS_DONE = 'ฟังแล้ว', LS_DEL = 'ลบ';
var LS_SUM_SYS = 'คุณคือ Vee เลขาของหมอประภัทร (เรียกเขาว่า ภัทร) สรุปเนื้อหาที่ได้รับให้ภัทรฟังตอนขับรถ ' +
  'เขียนเป็นภาษาพูดไทยที่ฟังลื่น เป็นย่อหน้าสั้นๆ ห้ามใช้ markdown หัวข้อ bullet ตาราง อีโมจิ หรือลิงก์ ' +
  'เริ่มด้วยใจความสำคัญที่สุดก่อน ตัวเลขสำคัญให้คงไว้ ไม่แต่งข้อมูลที่ไม่มีในต้นฉบับ ตอบเฉพาะบทพูด';

function ttsKey() { return prop('TTS_KEY') || ''; }
function ttsMonth() { return fmt(new Date(), 'yyyy-MM'); }
function ttsUse() { var u = {}; try { u = JSON.parse(prop('TTS_USE') || '{}'); } catch (e) {} return u.m === ttsMonth() ? u : { m: ttsMonth(), c: 0 }; }
function ttsAddUse(n) {
  var u = ttsUse(); u.c = (+u.c || 0) + n; setProp('TTS_USE', JSON.stringify(u));
  try { ttsSubsRow(u.c); } catch (e) { log('tts', 'subs', '', e.message); }
  return u.c;
}
function ttsInfo() { var u = ttsUse(); return { ok: !!ttsKey(), used: +u.c || 0, free: TTS_FREE, voice: prop('TTS_VOICE') || prop('TTS_VOICE_AUTO') || '' }; }
/** แถวในหน้า 🔌 ค่าบริการระบบ: โควต้าตัวอักษรฟรีเดือนนี้ */
function ttsSubsRow(used) {
  var t = ensureTab('subs').sh, rows = readRows('subs'), row = rows.filter(function (o) { return o.v[0] === 'S_TTS'; })[0];
  var left = Math.max(0, TTS_FREE - used), now = new Date();
  if (!row) t.appendRow(['S_TTS', 'Google Text-to-Speech (เสียงอ่าน)', 'Vee note', 'โควต้า', left, TTS_FREE, 'ตัวอักษรฟรี', '', '', '', '', 'https://console.cloud.google.com/apis/api/texttospeech.googleapis.com/metrics', 'ฟรี 1 ล้านตัวอักษร/เดือน เกินคิด $30 ต่อล้าน · นับเองทุกครั้งที่อ่าน รีเซ็ตต้นเดือน', now, 'USD', 7, '']);
  else t.getRange(row.row, 5, 1, 2).setValues([[left, TTS_FREE]]), t.getRange(row.row, 14).setValue(now);
}
/** เก็บแต่ตัวหนังสือที่อ่านออกเสียงได้: ตัด markdown อีโมจิ ลิงก์ */
function ttsClean(s) {
  return String(s || '')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/\[([^\]]*)\]\((https?:[^)]*)\)/g, '$1')
    .replace(/https?:\/\/\S+/g, ' (ลิงก์) ')
    .replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, ' ')
    .replace(/[←-⇿⌀-➿⬀-⯿️‍]/g, ' ')
    .replace(/^\s{0,3}#{1,6}\s*/gm, '').replace(/^\s*[-*•·]\s+/gm, '').replace(/^\s*>\s?/gm, '')
    .replace(/[*_`|~]+/g, ' ')
    .replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
}
/** ตัดเป็นท่อน ≤ TTS_CHUNK ตัวอักษร: ตามบรรทัด → ช่องว่าง → ตัดดิบ */
function ttsChunks(text) {
  var out = [], cur = '';
  var push = function (p) {
    p = p.trim(); if (!p) return;
    if ((cur + '\n' + p).length <= TTS_CHUNK) { cur = cur ? cur + '\n' + p : p; return; }
    if (cur) out.push(cur); cur = '';
    while (p.length > TTS_CHUNK) {
      var cut = p.lastIndexOf(' ', TTS_CHUNK); if (cut < TTS_CHUNK / 2) cut = TTS_CHUNK;
      out.push(p.slice(0, cut).trim()); p = p.slice(cut).trim();
    }
    cur = p;
  };
  String(text).split(/\n+/).forEach(push);
  if (cur) out.push(cur);
  return out;
}
/** เลือกเสียงไทย: TTS_VOICE → ที่เคยหาไว้ → ถาม API หา Chirp3-HD ตัวแรก (ไม่มี → Neural2 → อะไรก็ได้) */
function ttsVoices() {
  var res = UrlFetchApp.fetch('https://texttospeech.googleapis.com/v1/voices?languageCode=th-TH&key=' + encodeURIComponent(ttsKey()), { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error(ttsErr(res));
  return (JSON.parse(res.getContentText()).voices || []).filter(function (v) { return (v.languageCodes || []).indexOf('th-TH') >= 0; })
    .map(function (v) { return { name: v.name, g: v.ssmlGender || '' }; });
}
function ttsVoice() {
  var v = prop('TTS_VOICE') || prop('TTS_VOICE_AUTO');
  if (v) return v;
  try {
    var vs = ttsVoices(), pick = vs.filter(function (x) { return /Chirp3-HD/.test(x.name); })[0] || vs.filter(function (x) { return /Neural2/.test(x.name); })[0] || vs[0];
    if (pick) { setProp('TTS_VOICE_AUTO', pick.name); return pick.name; }
  } catch (e) { log('tts', 'voices', '', e.message); }
  return '';
}
function ttsErr(res) {
  var code = res.getResponseCode(), m = ''; try { m = JSON.parse(res.getContentText()).error.message; } catch (e) { m = res.getContentText().slice(0, 200); }
  if (code === 403 && /not been used|disabled|SERVICE_DISABLED/i.test(m)) return 'ยังไม่ได้เปิด Text-to-Speech API ใน Google Cloud project ของ key นี้';
  if (code === 400 && /API key not valid/i.test(m)) return 'TTS_KEY ไม่ถูกต้อง';
  if (code === 403) return 'key นี้ไม่มีสิทธิ์ใช้ Text-to-Speech (' + m.slice(0, 120) + ')';
  return 'Text-to-Speech ' + code + ': ' + m.slice(0, 160);
}
/** ข้อความ → MP3 (หลายท่อนต่อกันเป็นไฟล์เดียว) */
function ttsSynth(text, voice) {
  if (!ttsKey()) return { ok: false, err: 'ยังไม่ได้ตั้งค่าเสียงอ่าน — ใส่ TTS_KEY ใน Script Properties ก่อน' };
  var clean = ttsClean(text); if (!clean) return { ok: false, err: 'ไม่มีตัวหนังสือให้อ่าน' };
  var cut = clean.length > TTS_MAX; if (cut) clean = clean.slice(0, TTS_MAX);
  voice = voice || ttsVoice();
  var rate = Math.max(0.7, Math.min(1.5, parseFloat(prop('TTS_RATE')) || 1));
  var parts = ttsChunks(clean), bytes = [], n = 0;
  for (var i = 0; i < parts.length; i++) {
    var body = { input: { text: parts[i] }, voice: voice ? { languageCode: 'th-TH', name: voice } : { languageCode: 'th-TH' }, audioConfig: { audioEncoding: 'MP3', speakingRate: rate } };
    if (/Chirp3-HD/.test(voice)) delete body.audioConfig.speakingRate; // Chirp 3: HD บางรุ่นไม่รับ speakingRate
    var res = UrlFetchApp.fetch('https://texttospeech.googleapis.com/v1/text:synthesize?key=' + encodeURIComponent(ttsKey()), { method: 'post', contentType: 'application/json', payload: JSON.stringify(body), muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) {
      var e = ttsErr(res); log('tts', parts[i].slice(0, 200), '', e);
      if (n) ttsAddUse(n);
      return { ok: false, err: '🔇 ' + e };
    }
    bytes = bytes.concat(Utilities.base64Decode(JSON.parse(res.getContentText()).audioContent));
    n += parts[i].length;
  }
  ttsAddUse(n);
  return { ok: true, blob: Utilities.newBlob(bytes, 'audio/mpeg', 'vee.mp3'), chars: n, cut: cut, voice: voice };
}
/** ส่งไฟล์เสียงเข้า Telegram (เล่นต่อได้ตอนล็อกจอ) */
function tgAudio(blob, title, caption, keyboard) {
  var p = { chat_id: String(prop('OWNER_CHAT_ID')), audio: blob, title: String(title || 'Vee อ่านให้ฟัง').slice(0, 60), performer: 'Vee' };
  if (caption) p.caption = String(caption).slice(0, 900);
  if (keyboard && keyboard.length) p.reply_markup = JSON.stringify({ inline_keyboard: keyboard });
  blob.setName(String(title || 'vee').replace(/[\\\/:*?"<>|\n]+/g, ' ').slice(0, 40) + '.mp3');
  var res = UrlFetchApp.fetch('https://api.telegram.org/bot' + prop('TELEGRAM_TOKEN') + '/sendAudio', { method: 'post', payload: p, muteHttpExceptions: true });
  var j = {}; try { j = JSON.parse(res.getContentText()); } catch (e) {}
  if (!j.ok) log('telegram', 'sendAudio ' + title, '', res.getContentText().slice(0, 500));
  return j;
}
function lsTitle(text) { var t = ttsClean(text).replace(/\s+/g, ' ').trim(); return t.length > 50 ? t.slice(0, 48) + '…' : t || 'ข้อความ'; }
function lsKb(id) { return [[{ text: '✓ ฟังแล้ว', callback_data: 'ls:d:' + id }, { text: '💡 เก็บเป็นไอเดีย', callback_data: 'ls:i:' + id }, { text: '🔁 สรุปสั้นลง', callback_data: 'ls:s:' + id }]]; }
/* ---------- คิวฟัง (แท็บ "คิวฟัง") ---------- */
function lsRows() { ensureTab('listen'); return readRows('listen'); }
function lsAdd(text, mode, src, title, status) {
  ensureTab('listen');
  var id = newId('L'), body = String(text || '').slice(0, 45000);
  sheet('listen').appendRow([id, new Date(), title || lsTitle(body), body, mode === 'สรุป' ? 'สรุป' : 'อ่าน', src || 'แชท', status || LS_WAIT, ttsClean(body).length, '']);
  return id;
}
function lsSet(id, col, val) { var o = findRow('listen', id); if (o) sheet('listen').getRange(o.row, col).setValue(val); return o; }
function lsData() {
  try {
    return lsRows().filter(function (o) { return o.v[6] === LS_WAIT || o.v[6] === LS_SENT; }).slice(-30).reverse()
      .map(function (o) { return { id: o.v[0], title: String(o.v[2]), mode: o.v[4], src: o.v[5], st: o.v[6] === LS_WAIT ? 'w' : 's', n: +o.v[7] || 0, at: isDate(o.v[1]) ? thDateTime(o.v[1]) : '' }; });
  } catch (e) { log('listen', '', '', e.stack || e); return []; }
}
/** สรุปด้วย AI ให้เป็นบทพูด (ยาวประมาณ words คำ) */
function lsSummarize(text, words) {
  var w = words || Math.max(80, Math.min(400, Math.round(ttsClean(text).length / 12)));
  return callClaude(LS_SUM_SYS + ' ความยาวประมาณ ' + w + ' คำ', String(text).slice(0, 60000), 2048).trim();
}
/** อ่าน/สรุป แล้วส่งเสียง · id = แถวในคิว (ไม่มี = สร้างใหม่สถานะ ส่งแล้ว) */
function lsSpeak(text, mode, src, id, title) {
  var speech = String(text || '').trim();
  if (!speech) return { ok: false, err: 'ไม่มีข้อความให้อ่าน' };
  if (!ttsKey()) return { ok: false, err: '🔇 ยังไม่ได้ตั้งค่าเสียงอ่าน — ใส่ TTS_KEY ใน Script Properties ก่อน (ดูขั้นตอนในคู่มือ v62)' };
  if (mode === 'สรุป') { try { speech = lsSummarize(speech); } catch (e) { return { ok: false, err: '⚠️ AI สรุปไม่ได้ตอนนี้: ' + e.message }; } }
  var r = ttsSynth(speech);
  if (!r.ok) return r;
  if (!id) id = lsAdd(text, mode, src, title, LS_SENT);
  var row = findRow('listen', id), name = title || (row ? String(row.v[2]) : lsTitle(text));
  var mins = Math.max(1, Math.round(r.chars / 700));
  var j = tgAudio(r.blob, (mode === 'สรุป' ? 'สรุป · ' : '') + name, '🎧 ' + name + ' · ~' + mins + ' นาที' + (r.cut ? ' (ยาวเกิน ตัดท้ายออก)' : ''), lsKb(id));
  if (!j.ok) return { ok: false, err: 'ส่งไฟล์เสียงเข้า Telegram ไม่สำเร็จ' + (j.description ? ': ' + j.description : '') };
  if (row) { var sh = sheet('listen'); sh.getRange(row.row, 7).setValue(LS_SENT); sh.getRange(row.row, 9).setValue(new Date()); }
  return { ok: true, id: id, chars: r.chars, name: name };
}
/** ส่งทุกเรื่องที่รอในคิว (เรียงเก่า→ใหม่) · ทีละไม่เกิน 6 เรื่องกันเกินเวลา Apps Script */
function lsDrive() {
  var wait = lsRows().filter(function (o) { return o.v[6] === LS_WAIT; });
  if (!wait.length) return { n: 0, left: 0, err: '' };
  var n = 0, err = '', t0 = Date.now();
  for (var i = 0; i < wait.length && n < 6 && Date.now() - t0 < 240000; i++) {
    var o = wait[i], r = lsSpeak(String(o.v[3]), o.v[4], o.v[5], o.v[0]);
    if (!r.ok) { err = r.err; break; }
    n++;
  }
  return { n: n, left: wait.length - n, err: err };
}
/** บทพูดสรุปวันนี้ (ไม่ใช้ AI): นัด · งาน project ที่ทำอยู่ · งานอื่น · project + งานถัดไป */
function lsBriefText() {
  var d = appData(false), L = ['สวัสดีครับภัทร วันนี้' + d.date];
  L.push(d.events.length ? 'วันนี้มีนัด ' + d.events.length + ' รายการ ' + d.events.map(function (e) { return (e.time === 'ทั้งวัน' ? 'ทั้งวัน ' : 'เวลา ' + e.time + ' น. ') + e.title + (e.place ? ' ที่ ' + e.place : ''); }).join(' ต่อด้วย ') : 'วันนี้ไม่มีนัด');
  var open = function (a) { return a.filter(function (t) { return !t.done; }); };
  var tp = open(d.tasksProject), to = open(d.tasksOther);
  if (tp.length) L.push('งานของ project ที่ทำอยู่ ' + tp.length + ' งาน ' + tp.map(function (t) { return t.title + (t.late ? ' ซึ่งเลยกำหนดแล้ว' : t.when ? ' เวลา ' + t.when + ' น.' : ''); }).join(' ต่อด้วย '));
  if (to.length) L.push('งานอื่นวันนี้ ' + to.map(function (t) { return t.title + (t.late ? ' ซึ่งเลยกำหนดแล้ว' : ''); }).join(' ต่อด้วย '));
  if (!tp.length && !to.length) L.push('วันนี้ยังไม่มีงานค้าง');
  var act = d.projects.filter(function (p) { return p.status === 'a'; });
  if (act.length) L.push('project ที่กำลังทำ ' + act.map(function (p) { return p.title + (p.next ? ' งานถัดไปคือ ' + p.next : ''); }).join(' และ '));
  L.push('ขับรถปลอดภัยนะครับ');
  return L.join('\n');
}
function lsBrief(src) { return lsSpeak(lsBriefText(), 'อ่าน', src || 'สรุปวันนี้', '', 'สรุปวันนี้ ' + dmy(new Date())); }
/** 🔊 บนการ์ด project/ไอเดีย: ให้ AI เล่าสถานะสั้นๆ (AI ล่ม → อ่านข้อมูลดิบ) */
function lsProjectText(id) {
  var p = projectById(id); if (!p) return '';
  var tasks = openTasks().filter(function (t) { return String(t.projectId) === String(p.id); }).slice(0, 8).map(function (t) { return t.title + (t.due ? ' (' + thDateTime(t.due, false) + ')' : ''); });
  var raw = (p.status === ST_IDEA ? 'ไอเดีย ' : 'project ') + p.title + '\nสถานะ: ' + p.status + '\nรายละเอียด: ' + (p.detail || '-') +
    '\nบันทึกความคืบหน้า (ใหม่อยู่บน): ' + (String(p.process || '').split('\n').slice(0, 6).join(' / ') || '-') + '\nแผนต่อไป: ' + (p.plan || '-') + '\nงานที่ยังค้าง: ' + (tasks.join(' / ') || '-');
  try { return callClaude(LS_SUM_SYS + ' เล่าภาพรวมให้ภัทรฟังว่า project นี้คืออะไร ถึงไหนแล้ว และควรทำอะไรต่อ ไม่เกิน 120 คำ', raw, 1024).trim(); }
  catch (e) { return raw; }
}
/* ---------- แชท ---------- */
function lsHandleText(chatId, text, msg) {
  var reply = msg && msg.reply_to_message, rtext = reply ? String(reply.text || reply.caption || '') : '';
  var m;
  if (/^(ขับรถ|โหมดขับรถ)$/.test(text)) {
    var dr = lsDrive();
    if (!dr.n && !dr.err) send(chatId, '🚗 คิวฟังว่างอยู่ครับ — พิมพ์ "ฟังทีหลัง <ข้อความ>" หรือเพิ่มในแอปหน้า 🎧 ฟัง\nหรือพิมพ์ "ฟังวันนี้" เพื่อฟังสรุปวันนี้');
    else if (dr.err) send(chatId, (dr.n ? '🚗 ส่งไป ' + dr.n + ' เรื่อง แล้วติดปัญหา\n' : '') + dr.err);
    else if (dr.left) send(chatId, '🚗 ส่ง ' + dr.n + ' เรื่องแล้ว ยังเหลือในคิว ' + dr.left + ' เรื่อง — พิมพ์ "ขับรถ" อีกครั้ง');
    return true;
  }
  if (/^(ฟังวันนี้|อ่านวันนี้|สรุปวันนี้ให้ฟัง)$/.test(text)) { var br = lsBrief('แชท'); if (!br.ok) send(chatId, br.err); return true; }
  if (/^ทดสอบเสียง$/.test(text)) { lsVoiceTest(chatId); return true; }
  if ((m = text.match(/^ฟังทีหลัง\s*[:：]?\s*([\s\S]*)$/))) {
    var lt = m[1].trim() || rtext;
    if (!lt) { send(chatId, 'พิมพ์ "ฟังทีหลัง" ตามด้วยข้อความ หรือตอบกลับข้อความที่อยากฟังด้วยคำว่า "ฟังทีหลัง"'); return true; }
    lsAdd(lt, lt.length > 3000 ? 'สรุป' : 'อ่าน', 'แชท');
    send(chatId, '🎧 เข้าคิวแล้ว: ' + lsTitle(lt) + (lt.length > 3000 ? ' (ยาว จะสรุปก่อนอ่าน)' : '') + '\nพิมพ์ "ขับรถ" เมื่อพร้อมฟัง');
    return true;
  }
  var sum = text.match(/^(?:สรุปให้ฟัง|สรุปแล้วอ่าน|สรุปอ่าน)\s*[:：]?\s*([\s\S]*)$/);
  var rd = sum ? null : (text.match(/^(?:อ่านให้ฟัง|อ่านออกเสียง)\s*[:：]?\s*([\s\S]*)$/) || text.match(/^อ่าน\s*[:：]\s*([\s\S]*)$/) || text.match(/^อ่าน\s+([\s\S]{200,})$/) || (reply && /^อ่าน$/.test(text) ? [text, ''] : null));
  var hit = sum || rd;
  if (!hit) return false;
  var body = String(hit[1] || '').trim() || rtext;
  if (!body) { send(chatId, 'พิมพ์ "' + (sum ? 'สรุปให้ฟัง' : 'อ่านให้ฟัง') + '" ตามด้วยข้อความ หรือกดตอบกลับข้อความที่อยากฟัง แล้วพิมพ์ "อ่าน"'); return true; }
  tg('sendChatAction', { chat_id: chatId, action: 'upload_voice' });
  var r = lsSpeak(body, sum ? 'สรุป' : 'อ่าน', 'แชท');
  if (!r.ok) send(chatId, r.err);
  return true;
}
/** Phase 0: ส่งตัวอย่างเสียงไทยประโยคเดียวกัน ให้ภัทรกดเลือก */
function lsVoiceTest(chatId) {
  if (!ttsKey()) return send(chatId, '🔇 ยังไม่ได้ตั้งค่าเสียงอ่าน — ใส่ TTS_KEY ใน Script Properties ก่อน');
  var vs; try { vs = ttsVoices(); } catch (e) { return send(chatId, '🔇 ' + e.message); }
  if (!vs.length) return send(chatId, 'ไม่พบเสียงภาษาไทยใน Google Text-to-Speech');
  var pick = [], seen = {};
  var add = function (f) { vs.filter(f).forEach(function (v) { if (pick.length < 5 && !seen[v.name]) { seen[v.name] = 1; pick.push(v); } }); };
  add(function (v) { return /Chirp3-HD/.test(v.name) && v.g === 'FEMALE'; }); pick = pick.slice(0, 2);
  add(function (v) { return /Chirp3-HD/.test(v.name) && v.g === 'MALE'; }); pick = pick.slice(0, 4);
  add(function (v) { return /Neural2/.test(v.name); });
  add(function (v) { return /Standard|Wavenet/i.test(v.name); });
  var line = 'สวัสดีครับภัทร วีอ่านให้ฟังแบบนี้ วันนี้มีนัดตรวจคนไข้เก้าโมงครึ่ง แล้วบ่ายสองโมงประชุมทีมคลินิก อย่าลืมแก้ e-book ให้เสร็จก่อนวันศุกร์นะครับ';
  send(chatId, '🎙 ตัวอย่างเสียงไทย ' + pick.length + ' แบบ (มีทั้งหมด ' + vs.length + ' เสียง) ฟังแล้วกด ✅ ใต้เสียงที่ชอบ\nเสียงที่ใช้อยู่: ' + (ttsVoice() || 'ค่าเริ่มต้นของ Google'));
  pick.forEach(function (v, i) {
    var r = ttsSynth(line, v.name);
    if (!r.ok) return send(chatId, v.name + ': ' + r.err);
    tgAudio(r.blob, 'เสียง ' + (i + 1) + ' · ' + v.name.replace('th-TH-', ''), (v.g === 'FEMALE' ? 'หญิง' : v.g === 'MALE' ? 'ชาย' : '') + ' · ' + v.name, [[{ text: '✅ ใช้เสียงนี้', callback_data: 'ls:v:' + v.name }]]);
  });
}
function lsCallback(cq, data) {
  var chatId = cq.message && cq.message.chat.id, ans = '', parts = data.split(':'), op = parts[1], id = parts.slice(2).join(':');
  var o = id && op !== 'v' ? findRow('listen', id) : null;
  if (op === 'b') { tg('answerCallbackQuery', { callback_query_id: cq.id, text: '🔊 กำลังทำเสียง…' }); var br = lsBrief('สรุปเช้า'); if (!br.ok) send(chatId, br.err); return; }
  if (op === 'v') { setProp('TTS_VOICE', id); ans = '✅ ใช้เสียง ' + id.replace('th-TH-', '') + ' แล้ว'; }
  else if (!o) ans = 'ไม่พบเรื่องนี้ในคิวฟัง';
  else if (op === 'd') { sheet('listen').getRange(o.row, 7).setValue(LS_DONE); ans = '✓ ฟังแล้ว: ' + o.v[2]; }
  else if (op === 'i') {
    var now = new Date();
    sheet('roadmap').appendRow([newId('R'), '', String(o.v[2]), ttsClean(String(o.v[3])).slice(0, 1500), '', '', '', ST_IDEA, now, now]);
    sheet('listen').getRange(o.row, 7).setValue(LS_DONE);
    ans = '💡 เก็บเป็นไอเดียแล้ว: ' + o.v[2];
  } else if (op === 's') {
    tg('answerCallbackQuery', { callback_query_id: cq.id, text: '🔁 กำลังสรุปให้สั้นลง…' });
    var st = ''; try { st = lsSummarize(String(o.v[3]), 80); } catch (e) { return send(chatId, '⚠️ AI สรุปไม่ได้ตอนนี้: ' + e.message); }
    var r = lsSpeak(st, 'อ่าน', 'สรุปสั้นลง', '', 'สั้น · ' + o.v[2]);
    if (!r.ok) send(chatId, r.err);
    return;
  }
  tg('answerCallbackQuery', { callback_query_id: cq.id, text: ans.slice(0, 190) });
}
/* ---------- แอป ---------- */
function lsApi(action, a) {
  var txt = String(a.text || '').trim(), mode = a.mode === 'สรุป' ? 'สรุป' : 'อ่าน', r;
  if (action === 'lsadd') { if (!txt) return { msg: 'วางข้อความก่อนครับ', warn: true }; lsAdd(txt, mode, 'แอป'); return { msg: '🎧 เข้าคิวแล้ว: ' + lsTitle(txt) }; }
  if (action === 'lsdel') { var d = lsSet(a.id, 7, LS_DEL); return { msg: d ? '🗑 เอาออกจากคิว: ' + d.v[2] : 'ไม่พบเรื่องนี้', warn: !d }; }
  if (action === 'lsdrive') {
    var dr = lsDrive();
    if (dr.err) return { msg: (dr.n ? 'ส่ง ' + dr.n + ' เรื่อง แล้วติดปัญหา: ' : '') + dr.err, warn: true };
    return dr.n ? { msg: '🚗 ส่ง ' + dr.n + ' เรื่องเข้า Telegram แล้ว' + (dr.left ? ' (เหลือ ' + dr.left + ' กดอีกครั้ง)' : '') } : { msg: 'คิวว่างอยู่ครับ', warn: true };
  }
  if (action === 'lsbrief') r = lsBrief('แอป');
  else if (action === 'lssend') { var o = findRow('listen', a.id); if (!o) return { msg: 'ไม่พบเรื่องนี้', warn: true }; r = lsSpeak(String(o.v[3]), o.v[4], o.v[5], o.v[0]); }
  else if (action === 'lsnow') { if (!txt) return { msg: 'วางข้อความก่อนครับ', warn: true }; r = lsSpeak(txt, mode, 'แอป'); }
  else if (action === 'lssay') { if (!txt) return { msg: 'ไม่มีคำตอบให้อ่าน', warn: true }; r = lsSpeak(txt, 'อ่าน', 'คำตอบ Vee', '', 'Vee ตอบ · ' + lsTitle(a.q || txt)); }
  else if (action === 'lsproj') { var p = projectById(a.id); if (!p) return { msg: 'ไม่พบ project นี้', warn: true }; r = lsSpeak(lsProjectText(a.id), 'อ่าน', 'project', '', p.title); }
  return r.ok ? { msg: '📲 ส่งเสียง "' + r.name + '" เข้า Telegram แล้ว' } : { msg: r.err, warn: true };
}
"""
C=C.rstrip('\n')+'\n'+LS_JS
# ---------------- หน้าแอป ----------------
H=rep(H,"--idea:#7A5500;","--ls:#6B4FBB;--ls-head:#E6DEFA;--ls-ink:#2E1E66;--ls-soft:#F4F0FD;--idea:#7A5500;")
# ปุ่ม 🎧 หัวหน้าวันนี้ (ข้าง ↻)
H=rep(H,"""<button class="rf" data-act="more" aria-label="โหลดแอปใหม่ / ทางลัดมือถือ" style="color:' + c[1] + '">↻</button>""",
"""<button class="rf" data-act="more" aria-label="โหลดแอปใหม่ / ทางลัดมือถือ" style="color:' + c[1] + '">↻</button><button class="lsb" data-act="tab" data-v="listen" aria-label="หน้าฟัง: Vee อ่านให้ฟัง" style="color:' + c[1] + '">🎧<span>ฟัง</span></button>""")
H=rep(H,".rf{position:absolute;",""".lsb{position:absolute;top:10px;right:48px;height:34px;border:1.5px solid currentColor;border-radius:17px;background:rgba(255,255,255,.14);padding:0 12px;display:flex;align-items:center;gap:4px;font:inherit;font-size:14px;font-weight:600}
.lsb span{font-size:13px}
.lsq{display:flex;align-items:center;gap:8px;padding:12px 14px;border-top:1px solid var(--line)}
.lsq:first-child{border-top:0}
.lsq .t{flex:1;min-width:0}.lsq .t b{display:block;font-weight:600;font-size:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lsq .t span{font-size:12px;color:var(--mute)}
.lsq button{width:40px;height:40px;border-radius:20px;border:1px solid var(--line);background:#fff;font-size:16px;flex:none}
.lsq button.go{border:0;background:var(--ls);color:#fff}
.lsbig{width:100%;min-height:64px;border:0;border-radius:16px;background:var(--ls);color:#fff;font:inherit;font-size:18px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:10px}
.lsdrv{width:100%;min-height:56px;border:2px solid var(--ls);border-radius:16px;background:#fff;color:var(--ls);font:inherit;font-size:16px;font-weight:700}
.lsmode{display:grid;grid-template-columns:1fr 1fr;gap:6px;background:var(--ls-soft);border-radius:12px;padding:4px}
.lsmode button{height:40px;border:0;border-radius:9px;background:none;font:inherit;font-weight:600;color:var(--ls-ink)}
.lsmode button.on{background:#fff;color:var(--ls);box-shadow:0 1px 3px rgba(0,0,0,.12)}
.rf{position:absolute;""")
# render: แท็บ listen
H=rep(H,"var accent = { today: 'var(--today)', pj: 'var(--pj)', idea: 'var(--idea)', money: 'var(--fin)', work: 'var(--wk)' }[S.tab];",
"var accent = { today: 'var(--today)', pj: 'var(--pj)', idea: 'var(--idea)', money: 'var(--fin)', work: 'var(--wk)', listen: 'var(--ls)' }[S.tab];")
H=rep(H,"var body = S.tab === 'today' ? viewToday() : S.tab === 'pj' ? viewProjects() : S.tab === 'money' ? viewMoney() : S.tab === 'work' ? viewWork() : viewIdeas();",
"var body = S.tab === 'today' ? viewToday() : S.tab === 'pj' ? viewProjects() : S.tab === 'money' ? viewMoney() : S.tab === 'work' ? viewWork() : S.tab === 'listen' ? viewListen() : viewIdeas();")
# คลิก
H=rep(H,"""  if (/^sub(open|edit|new|cancel|go|check|paid|del)$/.test(act)) return sbAct(act, id);""","""  if (/^sub(open|edit|new|cancel|go|check|paid|del)$/.test(act)) return sbAct(act, id);
  if (/^ls(mode|add|now|send|del|drive|brief|proj|say|back)$/.test(act)) return lsAct(act, id, v);""")
# 🔊 บนการ์ด project/ไอเดีย (ข้าง ✏️ แก้ไข)
H=rep(H,"""    '<button data-act="pedit" data-id="' + esc(p.id) + '" aria-label="แก้ไขชื่อและรายละเอียด" style="border:1px solid var(--line);background:#fff;border-radius:16px;height:32px;padding:0 12px;font-size:13px;font-weight:600;color:var(--pj)">✏️ แก้ไข</button></div>""",
"""    '<span style="display:flex;gap:6px"><button data-act="lsproj" data-id="' + esc(p.id) + '" aria-label="ให้ Vee เล่า project นี้เป็นเสียงเข้า Telegram" style="border:1px solid var(--line);background:#fff;border-radius:16px;height:32px;padding:0 12px;font-size:13px;font-weight:600;color:var(--ls)">🔊 ฟัง</button>' +
    '<button data-act="pedit" data-id="' + esc(p.id) + '" aria-label="แก้ไขชื่อและรายละเอียด" style="border:1px solid var(--line);background:#fff;border-radius:16px;height:32px;padding:0 12px;font-size:13px;font-weight:600;color:var(--pj)">✏️ แก้ไข</button></span></div>""")
# 📲 ใต้คำตอบ Vee
H=rep(H,"""    (window.speechSynthesis ? '<button class="btn" data-act="anssay" style="background:var(--today)">🔊 ฟังอีกครั้ง</button>' : '<div style="font-size:12px;color:var(--mute)">เครื่องนี้อ่านออกเสียงไม่ได้ (ลองเปิดผ่าน Chrome)</div>') +""",
"""    (window.speechSynthesis ? '<button class="btn" data-act="anssay" style="background:var(--today)">🔊 ฟังอีกครั้ง</button>' : '<div style="font-size:12px;color:var(--mute)">เครื่องนี้อ่านออกเสียงไม่ได้ (ลองเปิดผ่าน Chrome)</div>') +
    '<button class="btn" data-act="lssay" style="background:var(--ls)">📲 ส่งเป็นเสียงเข้า Telegram</button>' +""")
LS_UI=r"""
/* v62: หน้า "ฟัง" — Vee อ่านให้ฟัง (ส่งไฟล์เสียงเข้า Telegram ฟังตอนขับรถ) */
function lsAct(act, id, v) {
  if (act === 'lsback') { S.tab = 'today'; return render(); }
  if (act === 'lsmode') { S.lsm = v; return render(); }
  var ta = $('ls-text'), txt = ta ? ta.value.trim() : '', mode = S.lsm === 'สรุป' ? 'สรุป' : 'อ่าน';
  if (act === 'lsadd' || act === 'lsnow') {
    if (!txt) { toast('วางข้อความหรือลิงก์ก่อนครับ'); if (ta) ta.focus(); return; }
    if (ta) ta.value = ''; S.lstx = '';
    if (act === 'lsnow') toast('🎙 กำลังทำเสียง' + (mode === 'สรุป' ? ' (สรุปก่อน)' : '') + '… เดี๋ยวเด้งใน Telegram');
    return api(act, { text: txt, mode: mode }, act === 'lsadd' ? function () { (D.listen = D.listen || []).unshift({ id: 'tmp' + Date.now(), title: txt.replace(/\s+/g, ' ').slice(0, 48), mode: mode, src: 'แอป', st: 'w', n: txt.length, at: 'เมื่อกี้' }); } : null);
  }
  if (act === 'lssend') { toast('🎙 กำลังทำเสียง… เดี๋ยวเด้งใน Telegram'); return api('lssend', { id: id }, function () { (D.listen || []).forEach(function (x) { if (x.id === id) x.st = 's'; }); }); }
  if (act === 'lsdel') { if (S.arm !== 'ls' + id) { S.arm = 'ls' + id; return render(); } S.arm = null; return api('lsdel', { id: id }, function () { D.listen = (D.listen || []).filter(function (x) { return x.id !== id; }); }); }
  if (act === 'lsdrive') { toast('🚗 กำลังส่งทั้งคิวเข้า Telegram…'); return api('lsdrive', {}); }
  if (act === 'lsbrief') { toast('🎙 กำลังทำเสียงสรุปวันนี้… เดี๋ยวเด้งใน Telegram'); return api('lsbrief', {}); }
  if (act === 'lsproj') { toast('🎙 Vee กำลังเล่า project นี้… เดี๋ยวเด้งใน Telegram'); return api('lsproj', { id: id }); }
  if (act === 'lssay') { if (!S.ans) return; toast('🎙 กำลังทำเสียง… เดี๋ยวเด้งใน Telegram'); return api('lssay', { text: S.ans.say, q: S.ans.q }); }
}
function viewListen() {
  var L = D.listen || [], tt = D.tts || {}, wait = L.filter(function (x) { return x.st === 'w'; }), sent = L.filter(function (x) { return x.st === 's'; });
  var mode = S.lsm === 'สรุป' ? 'สรุป' : 'อ่าน';
  var h = '<header style="background:var(--ls-head);color:var(--ls-ink)"><button data-act="lsback" aria-label="กลับหน้าวันนี้" style="display:block;border:0;background:none;color:inherit;font:inherit;font-size:15px;font-weight:600;padding:4px 0;margin:0 0 4px">← วันนี้</button>' +
    '<h1>🎧 ฟัง</h1><div class="sub" style="color:var(--ls-ink);opacity:.8">Vee อ่านให้ฟังเป็นไฟล์เสียงใน Telegram · ล็อกจอแล้วยังเล่นต่อ</div></header><main>';
  if (!tt.ok) h += '<div class="card" style="padding:12px 14px;border:1.5px dashed var(--warn);color:var(--warn);font-size:14px;margin-top:12px">🔇 ยังไม่ได้ตั้งค่าเสียงอ่าน — ต้องใส่ TTS_KEY ใน Script Properties ก่อน ปุ่มในหน้านี้ถึงจะส่งเสียงได้</div>';
  h += '<section class="sec"><button class="lsbig" data-act="lsbrief">▶ ฟังสรุปวันนี้</button><div style="font-size:12px;color:var(--mute);margin-top:6px;text-align:center">นัด + งานวันนี้ + project ที่ทำอยู่ รวมเป็นเสียงเดียว</div></section>';
  h += '<section class="sec"><h2>วางข้อความ / คำตอบ ChatGPT</h2><div class="card" style="padding:12px;display:flex;flex-direction:column;gap:10px">' +
    '<textarea id="ls-text" class="vtxt" style="min-height:110px" placeholder="กด Copy คำตอบใน ChatGPT แล้ววางตรงนี้…">' + esc(S.lstx || '') + '</textarea>' +
    '<div class="lsmode" role="group" aria-label="วิธีอ่าน"><button data-act="lsmode" data-v="อ่าน" class="' + (mode === 'อ่าน' ? 'on' : '') + '" aria-pressed="' + (mode === 'อ่าน') + '">อ่านตรงๆ</button><button data-act="lsmode" data-v="สรุป" class="' + (mode === 'สรุป' ? 'on' : '') + '" aria-pressed="' + (mode === 'สรุป') + '">สรุปก่อนอ่าน</button></div>' +
    '<div class="grid2"><button data-act="lsadd" style="height:46px;border-radius:12px;border:1.5px solid var(--ls);background:#fff;color:var(--ls);font:inherit;font-weight:700">＋ เข้าคิวฟัง</button><button data-act="lsnow" style="height:46px;border-radius:12px;border:0;background:var(--ls);color:#fff;font:inherit;font-weight:700">📲 ส่งเลย</button></div></div></section>';
  var row = function (x) {
    var del = S.arm === 'ls' + x.id;
    return '<div class="lsq"><div class="t"><b>' + esc(x.title) + '</b><span>' + (x.mode === 'สรุป' ? 'สรุปก่อนอ่าน' : 'อ่านตรงๆ') + ' · ~' + Math.max(1, Math.round((x.n || 0) / 700)) + ' นาที · ' + esc(x.src || '') + (x.st === 's' ? ' · ส่งแล้ว' : '') + '</span></div>' +
      '<button class="go" data-act="lssend" data-id="' + esc(x.id) + '" aria-label="ส่งเรื่องนี้เป็นเสียงเข้า Telegram">▶</button>' +
      '<button data-act="lsdel" data-id="' + esc(x.id) + '" aria-label="' + (del ? 'แตะอีกครั้งเพื่อเอาออก' : 'เอาออกจากคิว') + '" style="' + (del ? 'background:#B42318;color:#fff;border:0;width:auto;padding:0 10px;font-size:13px' : '') + '">' + (del ? 'เอาออก?' : '🗑') + '</button></div>';
  };
  h += '<section class="sec"><h2>คิวฟัง (' + wait.length + ')</h2><div class="card">' + (wait.length ? wait.map(row).join('') : '<div class="empty">คิวว่าง — วางข้อความด้านบน หรือพิมพ์ในแชท "ฟังทีหลัง …"</div>') + '</div>' +
    (wait.length ? '<button class="lsdrv" data-act="lsdrive" style="margin-top:10px">🚗 ส่งทั้งคิวเข้า Telegram (' + wait.length + ')</button>' : '') + '</section>';
  if (sent.length) h += '<section class="sec"><h2>ส่งแล้ว ยังไม่ได้กดฟังแล้ว (' + sent.length + ')</h2><div class="card">' + sent.slice(0, 10).map(row).join('') + '</div></section>';
  h += '<section class="sec"><div style="font-size:12px;color:var(--mute);line-height:1.6">ในแชทพิมพ์ได้: "อ่านให้ฟัง …" · "สรุปให้ฟัง …" · ตอบกลับข้อความด้วย "อ่าน" · "ขับรถ" (ส่งทั้งคิว) · "ฟังวันนี้" · "ทดสอบเสียง"' +
    (tt.ok ? '<br>เดือนนี้ใช้ไป ' + Number(tt.used || 0).toLocaleString() + ' จากฟรี ' + Number(tt.free || 0).toLocaleString() + ' ตัวอักษร' + (tt.voice ? ' · เสียง ' + esc(String(tt.voice).replace('th-TH-', '')) : '') : '') + '</div></section>';
  return h + '</main>';
}
"""
H=rep(H,"function viewMore() {",LS_UI.strip('\n')+"\nfunction viewMore() {")
# จำข้อความที่พิมพ์ค้างไว้ในช่อง (render ใหม่ไม่หาย)
H=rep(H,"  var pek2 = el.getAttribute && el.getAttribute('data-pe');","  if (el.id === 'ls-text') S.lstx = el.value;\n  var pek2 = el.getAttribute && el.getAttribute('data-pe');")
out=C+'/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
open('Code.v62.gs','w',encoding='utf8',newline='\n').write(out)
print('OK Code.v62.gs',ck(out))
