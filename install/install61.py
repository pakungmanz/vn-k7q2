# v61: หน้า "ค่าบริการระบบ" — ปุ่มกลมเล็ก 🔌 ในหน้าการเงิน (หัวหน้า ข้างปุ่ม ⚙︎ หมวด)
#      ทุกบริการที่ Vee note / ตัดคลิป / เว็บ morprapat ต้องใช้: หลอดเครดิตคงเหลือ หรือ จำนวนวันก่อนหมดอายุ
#      กดแถวเพื่อกาง: ลิงก์ไปเติมเงิน/ต่ออายุ · ✏ แก้ยอด · 💸 จ่ายแล้ว (ลงรายจ่าย บช.คลินิก + เลื่อนวันต่ออายุ)
#      อัตโนมัติ: วันหมดอายุโดเมน (RDAP) · พื้นที่ Google Drive · สถานะ Anthropic/Groq/Telegram จาก error จริง
#                 · ประมาณยอดเครดิต Anthropic ที่ใช้ไปจาก token ของแต่ละครั้ง · เตือนในสรุปเช้า
# รันในโฟลเดอร์ที่มี Code.v60.gs : python patch61.py  → ได้ Code.v61.gs
import json,re,os,sys
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v60.gs',encoding='utf8').read()
assert ck(B)==(530828,2587),('base ไม่ใช่ v60',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
SEED_ROWS=json.loads(r'''[["S_ANTH", "Anthropic API (สมองของบอท)", "Vee note", "เครดิต", 13.37, 15, "USD", "", "", "", true, "https://platform.claude.com/settings/billing", "เติมอัตโนมัติ: ต่ำกว่า $5 เติมกลับเป็น $15 · 30 วันใช้ ~$1.55 (เช็ค 19/11/69)", "USD", 7, ""], ["S_GROQ", "Groq (ถอดเสียง)", "Vee note", "ฟรี", "", "", "", "", "", "", "", "https://console.groq.com/settings/billing", "Whisper large-v3 · ยังไม่ได้เช็คแพ็กเกจ (ต้องล็อกอิน)", "บาท", 7, ""], ["S_TG", "Telegram Bot", "Vee note", "ฟรี", "", "", "", "", "", "", "", "https://t.me/BotFather", "", "บาท", 7, ""], ["S_GAS", "Google Apps Script + Sheet + Calendar", "Vee note", "ฟรี", "", "", "", "", "", "", "", "https://script.google.com/home", "บัญชี patkungmanz", "บาท", 7, ""], ["S_GH", "GitHub Pages (หน้าแอป)", "Vee note", "ฟรี", "", "", "", "", "", "", "", "https://github.com/pakungmanz/vn-k7q2", "", "บาท", 7, ""], ["S_DRIVE", "Google One 100 GB (พื้นที่ Drive)", "ทุกระบบ", "พื้นที่", 11.1, 100, "GB ว่าง", "2027-01-14", 700, 12, true, "https://one.google.com/storage", "Basic 100 GB ฿700/ปี · พื้นที่ว่างดึงเองทุกเช้า", "บาท", 7, ""], ["S_CLAUDE", "Claude Max (5x)", "ตัดคลิป", "รายเดือน", "", "", "", "2026-11-20", 107, 1, true, "https://claude.ai/settings/billing", "Visa ลงท้าย 6778 · ราคารวม VAT", "USD", 7, ""], ["S_GEM", "Gemini API (media-senses)", "ตัดคลิป", "ต่อรายการ", "", "", "", "", "", "", "", "https://console.cloud.google.com/billing", "Tier 1 จ่ายตามใช้ · ยอดเงินดูใน Google Cloud Billing", "บาท", 7, ""], ["S_PR", "Adobe Premiere Pro", "ตัดคลิป", "รายเดือน", "", "", "", "", "", 1, true, "https://account.adobe.com/plans", "ยังไม่ได้เช็ควันตัดเงิน (ต้องล็อกอิน)", "บาท", 7, ""], ["S_HOST", "Hostatom โฮสติ้ง morprapat.com", "เว็บ", "รายปี", "", "", "", "", "", 12, "", "https://support.hostatom.com/clientarea.php?action=services", "ยังไม่ได้เช็ค (ต้องล็อกอิน)", "บาท", 7, ""], ["S_DOM", "โดเมน morprapat.com", "เว็บ", "รายปี", "", "", "", "", "", 12, "", "https://support.hostatom.com/clientarea.php?action=domains", "วันหมดอายุดึงเองทุกเช้า", "บาท", 7, ""], ["S_SLIP", "SlipOK (ตรวจสลิป)", "เว็บ", "โควต้า", "", "", "สลิป", "", "", "", "", "https://slipok.com/", "ไม่มีแดชบอร์ดเว็บ ดูโควต้าผ่าน LINE bot ของ SlipOK", "บาท", 7, ""], ["S_STRIPE", "Stripe", "เว็บ", "ต่อรายการ", "", "", "", "", "", "", "", "https://dashboard.stripe.com/", "ไม่มีรายเดือน หักค่าธรรมเนียมต่อรายการ", "บาท", 7, ""], ["S_UPD", "UpdraftPlus สำรองเว็บ", "เว็บ", "สุขภาพ", "", "", "", "", "", "", "", "https://morprapat.com/wp-admin/options-general.php?page=updraftplus", "สำรองสำเร็จล่าสุด 10/08/69 หลังจากนั้น fail", "บาท", 7, ""], ["S_LINE", "LINE OA (แพ็กเกจฟรี + Premium ID)", "คลินิก", "รายปี", "", "", "", "", "", 12, "", "https://manager.line.biz/", "ข้อความรายเดือนใช้แพ็กเกจฟรี · Premium ID ต่อรายปี — ยังไม่ได้เช็ควันหมด (ต้องล็อกอิน)", "บาท", 7, ""], ["S_LINEP", "LINE Premium", "ส่วนตัว", "รายเดือน", "", "", "", "2026-12-07", 169, 1, true, "https://play.google.com/store/account/subscriptions", "LINE ส่วนตัว · ตัดผ่าน Google Play", "บาท", 7, ""]]''')
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v60';","var APP_VER = 'v61';")
C=rep(C,"  log:      { name: 'Log',",
"""  subs:     { name: 'ค่าบริการระบบ',  headers: ['ID', 'บริการ', 'ระบบ', 'ชนิด', 'คงเหลือ', 'เต็ม', 'หน่วย', 'หมดอายุ/ต่ออายุ', 'ราคา', 'รอบบิล (เดือน)', 'ตัดเงินอัตโนมัติ', 'ลิงก์เติม/ต่อ', 'หมายเหตุ', 'อัปเดตเมื่อ', 'สกุลเงิน', 'เตือนก่อน (วัน)', 'บัญชีที่จ่าย'] },
  log:      { name: 'Log',""")
C=rep(C,"    p4p: p4pData(), money: appMoney(),","    p4p: p4pData(), subs: subsData(), money: appMoney(),")
# ตัวนับ: Claude (ok/err + ค่าใช้จ่ายประมาณ) · Groq · Telegram
C=rep(C,"""  var code = res.getResponseCode();
  var body = JSON.parse(res.getContentText());
  if (code !== 200) throw new Error('Claude API ' + code + ': ' + (body.error && body.error.message));""","""  var code = res.getResponseCode();
  var body = {}; try { body = JSON.parse(res.getContentText()); } catch (e) {}
  if (code !== 200) { subsMark('anth', false, code + ' ' + (body.error && body.error.message || '')); throw new Error('Claude API ' + code + ': ' + (body.error && body.error.message)); }
  subsMark('anth', true, '', anthCost(body.model || model || prop('MODEL') || DEFAULT_MODEL, body.usage));""")
C=rep(C,"""    if (res.getResponseCode() !== 200 || !j.text) {
      log('voice', 'HTTP ' + res.getResponseCode(), body.slice(0, 500), 'transcribe fail');""","""    if (res.getResponseCode() !== 200 || !j.text) {
      if (res.getResponseCode() !== 200) subsMark('groq', false, res.getResponseCode() + ' ' + (j.error && j.error.message || ''));
      log('voice', 'HTTP ' + res.getResponseCode(), body.slice(0, 500), 'transcribe fail');""")
C=rep(C,"""    var text = String(j.text).trim();
    log('voice', label, text, '');""","""    var text = String(j.text).trim();
    subsMark('groq', true);
    log('voice', label, text, '');""")
C=rep(C,"""  var res = tg('sendMessage', p);
  if (!res.ok) log('telegram', text, '', JSON.stringify(res));""","""  var res = tg('sendMessage', p);
  if (!res.ok) log('telegram', text, '', JSON.stringify(res));
  if (!res.ok && (res.error_code === 401 || res.error_code === 404)) subsMark('tg', false, res.error_code + ' ' + (res.description || ''));""")
# สรุปเช้า: เตือนค่าบริการ
C=rep(C,"""  staleCheck();
  if (parseInt(fmt(new Date(), 'u'), 10) % 7 === 0)""","""  staleCheck();
  try { var sa = subsAlerts(); if (sa) sendOwner(sa); } catch (e) { log('subs', '', '', e.stack || e); }
  if (parseInt(fmt(new Date(), 'u'), 10) % 7 === 0)""")
C=rep(C,"""  } else if (action === 'slip') {""","""  } else if (action === 'subsave') {
    var sv = subsSave(a); msg = sv ? '🔌 บันทึก ' + sv : 'ไม่พบบริการนี้'; warn = !sv;
  } else if (action === 'subpaid') {
    var sp = subsPaid(a.id, a.amt); msg = sp.msg; warn = !!sp.warn;
  } else if (action === 'subdel') {
    var sd = subsDel(a.id); msg = sd ? '🗑 ลบ ' + sd : 'ไม่พบบริการนี้'; warn = !sd;
  } else if (action === 'subcheck') {
    var sc = subsAuto(true); msg = '🔄 เช็คแล้ว' + (sc.length ? ' · ' + sc.join(' · ') : '');
  } else if (action === 'slip') {""")
SUB_JS=r"""
/* ============================================================
 *  v61: ค่าบริการระบบ (subscription / เครดิต / วันหมดอายุ)
 *  แท็บ "ค่าบริการระบบ" 1 แถว = 1 บริการ · ภัทรแก้ในแอป (✏) หรือในชีทตรงๆ ก็ได้
 *  ชนิด: เครดิต (หลอด = คงเหลือ/เต็ม) · รายเดือน/รายปี (หลอด = วันที่เหลือ/รอบบิล) · ฟรี (ดูแค่สถานะ) · พื้นที่ (GB ว่าง/ทั้งหมด)
 *  ดึงเอง: โดเมน (RDAP) · Google Drive · Anthropic/Groq/Telegram ใช้ได้ไหม (จาก error จริง) · เครดิต Anthropic ที่ใช้ไป (ประมาณจาก token)
 * ============================================================ */
var SUBS_SEED = __SEED__;
var SUBS_DOMAIN = 'morprapat.com';
var SUBS_ACCT = 'คลินิก', SUBS_CAT = 'ซอฟต์แวร์/เครื่องมือ';
/** ราคา Anthropic $/ล้าน token [input, output] — ใช้ประมาณยอดเครดิตที่ใช้ไประหว่างรอเช็คหน้า Billing */
var ANTH_PRICE = [[/haiku-4-5/, 1, 5], [/haiku/, 0.1, 0.5], [/sonnet/, 2, 10], [/opus-5-5/, 4, 20], [/opus/, 5, 25], [/fable/, 8, 40]];
var _subsOk = false;
function ensureSubs() {
  if (_subsOk) return; _subsOk = true;
  var t = ensureTab('subs');
  if (t.made && SUBS_SEED.length) {
    var now = new Date();
    t.sh.getRange(2, 1, SUBS_SEED.length, 17).setValues(SUBS_SEED.map(function (r) {
      var x = r.slice(0, 13); while (x.length < 13) x.push('');
      if (x[7] && /^\d{4}-\d{2}-\d{2}$/.test(x[7])) x[7] = new Date(x[7] + 'T00:00:00');
      x.push(now, r[13] || 'บาท', r[14] || 7, r[15] || ''); return x; }));
    t.sh.setFrozenRows(1);
  }
}
function anthCost(model, u) {
  if (!u) return 0;
  var p = ANTH_PRICE.filter(function (x) { return x[0].test(String(model)); })[0] || [null, 4, 20];
  var inp = (u.input_tokens || 0) + (u.cache_creation_input_tokens || 0) * 1.25 + (u.cache_read_input_tokens || 0) * 0.1;
  return (inp * p[1] + (u.output_tokens || 0) * p[2]) / 1e6;
}
/** บันทึกสถานะล่าสุดของ API (เขียนเมื่อสถานะเปลี่ยน หรือมีค่าใช้จ่ายเพิ่ม) */
function subsMark(svc, ok, msg, cost) {
  try {
    var k = 'SUBS_H_' + svc, h = {}; try { h = JSON.parse(prop(k) || '{}'); } catch (e) {}
    var now = Date.now(), dirty = false;
    if (ok) { if (!h.ok || h.err > h.ok || now - h.ok > 3600000) { h.ok = now; dirty = true; } }
    else { h.err = now; h.msg = String(msg || '').slice(0, 200); dirty = true; }
    if (cost) { h.spent = (h.spent || 0) + cost; h.n = (h.n || 0) + 1; dirty = true; }
    if (dirty) setProp(k, JSON.stringify(h));
  } catch (e) {}
}
function subsHealth(svc) { try { return JSON.parse(prop('SUBS_H_' + svc) || '{}'); } catch (e) { return {}; } }
function subsRows() {
  ensureSubs();
  return readRows('subs').map(function (o) { var v = o.v; return { row: o.row, id: String(v[0]), name: String(v[1] || ''), sys: String(v[2] || ''), kind: String(v[3] || ''),
    left: v[4] === '' ? null : Number(v[4]), full: v[5] === '' ? null : Number(v[5]), unit: String(v[6] || ''), date: isDate(v[7]) ? v[7] : null,
    price: v[8] === '' ? null : Number(v[8]), cycle: Number(v[9]) || 0, auto: v[10] === true || /^(true|ใช่|y|yes|✓)$/i.test(String(v[10])), url: String(v[11] || ''), note: String(v[12] || ''), upd: isDate(v[13]) ? v[13] : null,
    cur: String(v[14] || 'บาท'), remind: v[15] === '' || v[15] == null ? 7 : Number(v[15]) || 0, acct: String(v[16] || '') }; });
}
var SUBS_HSVC = { S_ANTH: 'anth', S_GROQ: 'groq', S_TG: 'tg' };
function addMonths(d, n) { var x = new Date(d.getTime()); var day = x.getDate(); x.setDate(1); x.setMonth(x.getMonth() + n); var last = new Date(x.getFullYear(), x.getMonth() + 1, 0).getDate(); x.setDate(Math.min(day, last)); return x; }
function subsView(r) {
  var today = new Date(ymd(new Date()) + 'T00:00:00'), o = { id: r.id, name: r.name, sys: r.sys, kind: r.kind, unit: r.unit, price: r.price, cycle: r.cycle, auto: r.auto, url: r.url, note: r.note, cur: r.cur, remind: r.remind, acct: r.acct,
    left: r.left, full: r.full, date: r.date ? ymd(r.date) : '', upd: r.upd ? ymd(r.upd) : '', pct: null, days: null, lvl: 'na', line: '' };
  var hs = SUBS_HSVC[r.id] ? subsHealth(SUBS_HSVC[r.id]) : null;
  if (r.id === 'S_ANTH' && r.left != null && hs && hs.spent) { o.left = Math.max(0, Math.round((r.left - hs.spent) * 100) / 100); o.spent = Math.round(hs.spent * 100) / 100; }
  if (r.date) o.days = Math.round((r.date.getTime() - today.getTime()) / 86400000);
  if (o.left != null && o.full) {
    o.pct = Math.max(0, Math.min(100, o.left / o.full * 100));
    o.lvl = o.pct < 10 ? 'bad' : o.pct < 25 ? 'warn' : 'ok';
    o.line = 'เหลือ ' + fmtNum(o.left) + (o.unit ? ' ' + o.unit : '') + ' จาก ' + fmtNum(o.full);
  } else if (o.left != null) { o.line = 'เหลือ ' + fmtNum(o.left) + (o.unit ? ' ' + o.unit : ''); o.lvl = 'ok'; }
  if (o.days != null) {
    var span = (r.cycle || (/ปี/.test(r.kind) ? 12 : 1)) * 30.4;
    var rd = r.remind || 7, dp = Math.max(0, Math.min(100, o.days / span * 100)), dl = o.days < 0 ? 'bad' : o.days <= rd ? (r.auto ? 'warn' : 'bad') : (!r.auto && o.days <= rd * 3) ? 'warn' : 'ok';
    var dt = o.days < 0 ? 'หมดอายุแล้ว ' + (-o.days) + ' วัน' : o.days === 0 ? (r.auto ? 'ตัดเงินวันนี้' : 'หมดอายุวันนี้') : (r.auto ? 'ตัดเงินอีก ' : 'หมดอายุอีก ') + o.days + ' วัน';
    if (o.pct == null) { o.pct = dp; o.lvl = dl; o.line = dt; } else { o.line += ' · ' + dt; if (dl === 'bad' || (dl === 'warn' && o.lvl === 'ok')) o.lvl = dl; }
  }
  if (hs && (hs.ok || hs.err)) {
    o.hok = hs.ok ? fmt(new Date(hs.ok), 'yyyy-MM-dd HH:mm') : ''; o.herr = hs.err ? fmt(new Date(hs.err), 'yyyy-MM-dd HH:mm') : '';
    if (hs.err && (!hs.ok || hs.err > hs.ok)) { o.lvl = 'bad'; o.hmsg = hs.msg || ''; o.line = '⚠️ ใช้ไม่ได้ล่าสุด: ' + (hs.msg || 'error') + (o.line ? ' · ' + o.line : ''); }
    else if (!o.line) { o.line = 'ใช้งานได้ปกติ'; o.lvl = 'ok'; }
    if (o.pct == null && o.lvl === 'ok') o.pct = 100;
  }
  if (!o.line && r.kind === 'สุขภาพ' && r.note) { o.line = r.note; o.lvl = /fail|ไม่ได้|พัง|error/i.test(r.note) ? 'bad' : 'ok'; o.pct = o.lvl === 'ok' ? 100 : 5; }
  if (!o.line) o.line = /ฟรี/.test(r.kind) ? 'ฟรี ไม่ต้องต่ออายุ' : r.kind === 'ต่อรายการ' ? 'ไม่มีรายเดือน หักต่อรายการ' : 'ยังไม่ได้กรอก';
  if (/ฟรี|ต่อรายการ/.test(r.kind) && o.pct == null && o.lvl === 'na') { o.pct = 100; o.lvl = 'ok'; }
  return o;
}
function fmtNum(n) { return Number(n).toLocaleString('en-US', { maximumFractionDigits: 2 }); }
function subsData() { try { return subsRows().map(subsView); } catch (e) { log('subs', '', '', e.stack || e); return []; } }
/** ดึงข้อมูลอัตโนมัติ (สรุปเช้า + ปุ่ม 🔄) · force=false ทำไม่เกินวันละครั้ง */
function subsAuto(force) {
  var out = [];
  if (!force && prop('SUBS_AUTO_AT') === ymd(new Date())) return out;
  setProp('SUBS_AUTO_AT', ymd(new Date()));
  var rows = subsRows(), sh = sheet('subs'), now = new Date(), byId = {}; rows.forEach(function (r) { byId[r.id] = r; });
  // 1) โดเมน .com จาก RDAP ของ Verisign
  var dom = byId.S_DOM;
  if (dom) try {
    var res = UrlFetchApp.fetch('https://rdap.verisign.com/com/v1/domain/' + SUBS_DOMAIN, { muteHttpExceptions: true });
    if (res.getResponseCode() === 200) {
      var ev = (JSON.parse(res.getContentText()).events || []).filter(function (e) { return e.eventAction === 'expiration'; })[0];
      if (ev) { var ex = new Date(ev.eventDate); var exd = new Date(ymd(ex) + 'T00:00:00');
        if (!dom.date || ymd(dom.date) !== ymd(exd)) { sh.getRange(dom.row, 8).setValue(exd); out.push('โดเมนหมด ' + ymd(exd)); }
        sh.getRange(dom.row, 14).setValue(now); }
    } else out.push('RDAP ' + res.getResponseCode());
  } catch (e) { out.push('เช็คโดเมนไม่ได้'); }
  // 2) พื้นที่ Google Drive (GB ว่าง / ทั้งหมด)
  var dr = byId.S_DRIVE;
  if (dr) try {
    var lim = DriveApp.getStorageLimit(), used = DriveApp.getStorageUsed(), gb = 1073741824;
    sh.getRange(dr.row, 5, 1, 3).setValues([[Math.round((lim - used) / gb * 10) / 10, Math.round(lim / gb * 10) / 10, 'GB ว่าง']]); sh.getRange(dr.row, 14).setValue(now);
  } catch (e) { out.push('เช็ค Drive ไม่ได้'); }
  // 3) ตัดเงินอัตโนมัติแล้วเลยวัน → เลื่อนไปรอบถัดไป
  rows.forEach(function (r) {
    if (!r.auto || !r.date || !r.cycle || r.date.getTime() >= new Date(ymd(now) + 'T00:00:00').getTime()) return;
    var d = r.date, g = 0; while (d.getTime() < new Date(ymd(now) + 'T00:00:00').getTime() && g++ < 60) d = addMonths(d, r.cycle);
    sh.getRange(r.row, 8).setValue(d); out.push(r.name + ' → ' + ymd(d));
  });
  return out;
}
/** ข้อความเตือนในสรุปเช้า (ว่าง = ไม่มีอะไรต้องดู) */
function subsAlerts() {
  try { subsAuto(false); } catch (e) { log('subs', 'auto', '', e.stack || e); }
  var list = subsData().filter(function (o) { return o.lvl === 'bad' || (o.lvl === 'warn' && (o.days == null || o.days <= (o.remind || 7))); });
  if (!list.length) return '';
  return '🔌 ค่าบริการที่ต้องดู\n' + list.map(function (o) { return (o.lvl === 'bad' ? '🔴 ' : '🟡 ') + o.name + ' — ' + o.line + (o.url ? '\n   ' + o.url : ''); }).join('\n') + '\n\n(ดูทั้งหมด: แอป → การเงิน → 🔌)';
}
function subsSave(a) {
  var rows = subsRows(), r = a.id ? rows.filter(function (x) { return x.id === String(a.id); })[0] : null, sh = sheet('subs');
  var num = function (v) { v = String(v == null ? '' : v).replace(/[,฿$\s]/g, ''); return v === '' || isNaN(Number(v)) ? '' : Number(v); };
  var dt = /^\d{4}-\d{2}-\d{2}$/.test(String(a.date || '')) ? new Date(a.date + 'T00:00:00') : '';
  var vals = [String(a.name || (r && r.name) || '').trim(), String(a.sys || '').trim(), String(a.kind || '').trim(), num(a.left), num(a.full), String(a.unit || '').trim(), dt, num(a.price), num(a.cycle), !!a.auto, String(a.url || '').trim(), String(a.note || '').trim(), new Date()];
  if (!vals[0]) return '';
  var extra = [String(a.cur || 'บาท').trim() || 'บาท', a.remind === '' || a.remind == null ? 7 : num(a.remind), String(a.acct || '').trim()];
  if (!r) { sh.appendRow([newId('S')].concat(vals, extra)); return vals[0]; }
  sh.getRange(r.row, 2, 1, 13).setValues([vals]); sh.getRange(r.row, 15, 1, 3).setValues([extra]);
  if (r.id === 'S_ANTH' && vals[3] !== '' && vals[3] !== r.left) { var h = subsHealth('anth'); h.spent = 0; h.n = 0; setProp('SUBS_H_anth', JSON.stringify(h)); }
  if (SUBS_HSVC[r.id] && String(a.fixed) === '1') { var h2 = subsHealth(SUBS_HSVC[r.id]); h2.err = 0; h2.msg = ''; setProp('SUBS_H_' + SUBS_HSVC[r.id], JSON.stringify(h2)); }
  return vals[0];
}
/** 💸 จ่ายแล้ว: ลงรายจ่าย บช.คลินิก หมวด ซอฟต์แวร์/เครื่องมือ + เลื่อนวันต่ออายุไป 1 รอบ */
function subsPaid(id, amt) {
  var r = subsRows().filter(function (x) { return x.id === String(id); })[0];
  if (!r) return { msg: 'ไม่พบบริการนี้', warn: true };
  var baht = Number(String(amt == null ? '' : amt).replace(/[,฿\s]/g, '')) || (r.cur === 'บาท' ? r.price : 0);
  if (!baht) return { msg: 'ใส่ยอดที่จ่ายจริง (บาท) ก่อนครับ', warn: true };
  var ac = r.acct || (r.sys === 'ส่วนตัว' ? ACCT_DEFAULT : SUBS_ACCT);
  var m = addMoney('รายจ่าย', 'ค่า ' + r.name, baht, ac === ACCT_DEFAULT ? 'ของใช้' : ac === SUBS_ACCT ? SUBS_CAT : 'อื่นๆ', 'แอป', 'ค่าบริการระบบ' + (r.cur !== 'บาท' && r.price ? ' (' + r.price + ' ' + r.cur + ')' : ''), new Date(), ac);
  var nx = '';
  if (r.cycle) { var d = r.date || new Date(ymd(new Date()) + 'T00:00:00'); d = addMonths(d, r.cycle); sheet('subs').getRange(r.row, 8).setValue(d); nx = ' · รอบถัดไป ' + thDateTime(d, false); }
  sheet('subs').getRange(r.row, 14).setValue(new Date());
  return { msg: '💸 ลงรายจ่าย ' + money(m.amount) + ' บ. บช.' + m.acct + nx };
}
function subsDel(id) {
  var r = subsRows().filter(function (x) { return x.id === String(id); })[0];
  if (!r) return '';
  sheet('subs').deleteRow(r.row); return r.name;
}
"""
SEEDJS=json.dumps(SEED_ROWS,ensure_ascii=False)
C=C.rstrip('\n')+'\n'+SUB_JS.replace('__SEED__',SEEDJS)
assert 'function thDateTime' in C
# ---------------- หน้าแอป ----------------
H=rep(H,"#party{","""/* v61: ค่าบริการระบบ */
.subb{width:30px;height:30px;border-radius:15px;border:1px solid rgba(74,40,0,.25);background:transparent;color:var(--fin-ink);font-size:14px;padding:0;flex-shrink:0;display:flex;align-items:center;justify-content:center;margin-left:auto;margin-right:6px}
.subb.on{background:#fff;border-color:#fff}
.sbhd{display:flex;align-items:center;gap:8px;justify-content:space-between}
.sbhd h2{margin:0}
.sbhd button{height:32px;padding:0 12px;border-radius:16px;border:1px solid var(--line);background:#fff;font-size:13px;color:var(--fin-ink)}
.sbsum{display:flex;gap:8px;flex-wrap:wrap;font-size:13px}
.sbsum span{background:#fff;border-radius:12px;padding:6px 10px}
.sbg{font-size:12px;font-weight:700;color:var(--mute);padding:10px 16px 2px;letter-spacing:.02em}
.sbr{border-bottom:1px solid var(--soft)}
.sbr:last-child{border-bottom:0}
.sbr>button{display:flex;flex-direction:column;gap:5px;width:100%;padding:11px 16px;border:0;background:none;text-align:left;font:inherit;color:inherit;cursor:pointer}
.sbr .t{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600}
.sbr .t .nm{flex:1;min-width:0}
.sbr .t .cv{font-size:12px;color:var(--mute);font-weight:400;transition:transform .2s}
.sbr.open .t .cv{transform:rotate(180deg)}
.sbr .dot{width:9px;height:9px;border-radius:5px;flex-shrink:0;margin:0}
.sbr .tr{height:8px;background:var(--soft);border-radius:4px;overflow:hidden}
.sbr .tr i{display:block;height:100%;border-radius:4px}
.sbr .ln{font-size:12px;color:var(--mute)}
.sbr .ln.bad{color:#B42318;font-weight:600}
.sbx{padding:0 16px 14px;display:flex;flex-direction:column;gap:8px;font-size:13px}
.sbx .kv{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;color:var(--ink)}
.sbx .kv b{font-weight:500;color:var(--mute)}
.sbx .bt{display:flex;gap:8px;flex-wrap:wrap}
.sbx .bt button{height:40px;padding:0 14px;border-radius:12px;border:1px solid var(--line);background:#fff;font-size:14px;font-weight:600}
.sbx .bt .go{background:var(--fin);border-color:var(--fin);color:#fff;flex:1}
.sbf{display:flex;flex-direction:column;gap:6px}
.sbf label{font-size:12px;color:var(--mute)}
.sbf input,.sbf select{height:40px;border:1px solid var(--line);border-radius:10px;padding:0 10px;font:inherit;font-size:15px;background:#fff;width:100%;box-sizing:border-box;min-width:0}
.sbf .g2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sbf .g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
.sbf .ck{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--ink)}
.sbf .ck input{width:20px;height:20px}
.sbnote{font-size:12px;color:var(--mute);line-height:1.6;padding:0 4px}
.sbtot{padding:12px 16px;gap:2px}
.sbtot span{font-size:12px;color:var(--mute)}
.sbtot b{font-size:20px;color:var(--fin-ink)}
.sbtot small{font-size:12px;color:var(--mute)}
.sbf fieldset{border:1px solid var(--line);border-radius:12px;padding:8px 12px 12px;margin:4px 0 0;display:flex;flex-direction:column;gap:6px;min-width:0}
.sbf legend{font-size:13px;font-weight:600;color:var(--fin-ink);padding:0 4px}
.sbf fieldset small{font-size:11px;color:var(--mute);line-height:1.5}
.sbf .crd,.sbf .cyc{display:none}
.sbf[data-k="เครดิต"] .crd,.sbf[data-k="โควต้า"] .crd,.sbf[data-k="พื้นที่"] .crd{display:flex}
.sbf[data-k="รายเดือน"] .cyc,.sbf[data-k="รายปี"] .cyc,.sbf[data-k="พื้นที่"] .cyc,.sbf[data-k="โควต้า"] .cyc,.sbf[data-k="เครดิต"] .cyc{display:grid}
.sbf[data-k="ฟรี"] .pay,.sbf[data-k="สุขภาพ"] .pay,.sbf[data-k="ฟรี"] .exp,.sbf[data-k="สุขภาพ"] .exp{display:none}
.sbpay{display:flex;flex-direction:column;gap:6px;background:var(--soft);border-radius:12px;padding:10px 12px}
.sbpay label{font-size:12px;color:var(--mute)}
.sbpay div{display:flex;gap:8px}
.sbpay input{flex:1;min-width:0;height:42px;border:1px solid var(--line);border-radius:10px;padding:0 10px;font:inherit;font-size:17px}
.sbpay button{height:42px;padding:0 14px;border-radius:10px;border:0;background:var(--fin);color:#fff;font-weight:600}
.sbpay small{font-size:11px;color:var(--mute)}
#party{""")
H=rep(H,"""<button data-act="mtab" data-v="cat" class="catb' + (S.mtab === 'cat' ? ' on' : '') + '" aria-label="จัดการหมวดและบัญชี">⚙︎ หมวด</button>""",
        """<button data-act="mtab" data-v="sub" class="subb' + (S.mtab === 'sub' ? ' on' : '') + '" aria-label="ค่าบริการระบบ" title="ค่าบริการระบบ">🔌</button><button data-act="mtab" data-v="cat" class="catb' + (S.mtab === 'cat' ? ' on' : '') + '" aria-label="จัดการหมวดและบัญชี">⚙︎ หมวด</button>""")
H=rep(H,"""    '<div class="actabs" role="tablist" aria-label="บัญชี">' + (S.mtab === 'add'""","""    (S.mtab === 'sub' ? '' : '<div class="actabs" role="tablist" aria-label="บัญชี">' + (S.mtab === 'add'""")
H=rep(H,"""}).join('') + '</div>' +
    '</header><main style="background:' + (col""","""}).join('') + '</div>') +
    '</header><main style="background:' + (S.mtab === 'sub' ? '#F4F6FA' : col""")
H=rep(H,"""(col ? ';--ac:' + col.bg""","""(S.mtab !== 'sub' && col ? ';--ac:' + col.bg""")
H=rep(H,"else if (S.mtab === 'asset') h += moneyAssets(); else h += moneyCats();","else if (S.mtab === 'asset') h += moneyAssets(); else if (S.mtab === 'sub') h += moneySubs(); else h += moneyCats();")
SUB_UI=r"""/* v61: ค่าบริการระบบ */
var SB_SYS = ['Vee note', 'ตัดคลิป', 'เว็บ', 'คลินิก', 'ทุกระบบ', 'ส่วนตัว'];
var SB_KIND = [['รายเดือน', '📅 รายเดือน'], ['รายปี', '🗓 รายปี'], ['เครดิต', '💳 เติมเครดิต'], ['โควต้า', '🎟 โควต้า/แพ็กเกจ'], ['พื้นที่', '💾 พื้นที่'], ['ต่อรายการ', '🧾 จ่ายตามใช้'], ['ฟรี', '🆓 ฟรี'], ['สุขภาพ', '🩺 ดูสถานะ']];
var SB_UNITS = ['USD', 'บาท', 'ครั้ง', 'สลิป', 'ข้อความ', 'GB ว่าง', 'นาที', 'token'];
function sbMoney(n, cur) { return cur === 'USD' ? '$' + fmtN(n) : baht(n) + ' ' + (cur || 'บาท'); }
function sbCyc(c) { return !c ? '' : c === 12 ? 'ปี' : c === 1 ? 'เดือน' : c + ' เดือน'; }
var SB_COL = { ok: '#2E7D5B', warn: '#D99A00', bad: '#C0392B', na: '#9AA4B5' };
function moneySubs() {
  var L = D.subs || [], n = { ok: 0, warn: 0, bad: 0, na: 0 }; L.forEach(function (o) { n[o.lvl] = (n[o.lvl] || 0) + 1; });
  var h = '<section class="sec"><div class="sbhd"><h2>🔌 ค่าบริการระบบ</h2><button data-act="subcheck">🔄 เช็คตอนนี้</button></div>' +
    '<div class="sbsum">' + (n.bad ? '<span style="color:' + SB_COL.bad + '">🔴 ต้องจัดการ ' + n.bad + '</span>' : '') + (n.warn ? '<span style="color:' + SB_COL.warn + '">🟡 ใกล้ถึง ' + n.warn + '</span>' : '') +
    '<span style="color:' + SB_COL.ok + '">🟢 ปกติ ' + n.ok + '</span>' + (n.na ? '<span style="color:var(--mute)">⚪ รอกรอก ' + n.na + '</span>' : '') + '</div>';
  var tot = {}; L.forEach(function (o) { if (o.price && o.cycle && /รายเดือน|รายปี|พื้นที่|โควต้า/.test(o.kind)) tot[o.cur || 'บาท'] = (tot[o.cur || 'บาท'] || 0) + o.price / o.cycle; });
  var tk = Object.keys(tot);
  if (tk.length) h += '<div class="card sbtot"><span>ค่าใช้จ่ายประจำ เฉลี่ยต่อเดือน</span><b>' + tk.map(function (c) { return sbMoney(Math.round(tot[c] * 100) / 100, c); }).join(' + ') + '</b><small>รวม ' + tk.map(function (c) { return sbMoney(Math.round(tot[c] * 12), c); }).join(' + ') + ' ต่อปี (เฉพาะรายการที่ใส่ราคา)</small></div>';
  if (S.sube !== 'new') h += '<button class="wkadd" data-act="subnew" style="border-color:var(--fin);color:var(--fin)">＋ เพิ่มรายการติดตาม</button>';
  var ord = { bad: 0, warn: 1, na: 2, ok: 3 };
  SB_SYS.concat(['อื่นๆ']).forEach(function (sys) {
    var g = L.filter(function (o) { return sys === 'อื่นๆ' ? SB_SYS.indexOf(o.sys) < 0 : o.sys === sys; }).sort(function (a, b) { return ord[a.lvl] - ord[b.lvl] || (a.days == null ? 9e9 : a.days) - (b.days == null ? 9e9 : b.days); });
    if (!g.length) return;
    h += '<div class="card" style="padding:2px 0"><div class="sbg">' + esc(sys) + '</div>' + g.map(sbRow).join('') + '</div>';
  });
  if (!L.length) h += '<div class="card"><div class="empty">ยังไม่มีรายการ — กด ＋ เพิ่ม</div></div>';
  h += S.sube === 'new' ? '<div class="card" style="padding:14px 16px"><b style="color:var(--fin);font-size:16px">＋ เพิ่มรายการติดตาม</b>' + sbForm({ id: '', sys: 'คลินิก', kind: 'รายเดือน', cycle: 1, cur: 'บาท', remind: 7, auto: true }) + '</div>' : '<button class="wkadd" data-act="subnew" style="border-color:var(--fin);color:var(--fin)">＋ เพิ่มรายการติดตาม</button>';
  h += '<div class="sbnote">ดึงเอง: วันหมดอายุโดเมน · พื้นที่ Drive · Anthropic/Groq/Telegram ใช้ได้ไหม (ดูจาก error จริง) · เครดิต Anthropic ที่ใช้ไป (ประมาณจาก token ของบอท ไม่รวมที่ใช้ที่อื่น) — ที่เหลือกรอกเองตอนเติม/ต่ออายุ แล้ววีจะเตือนในสรุปเช้าเมื่อใกล้หมด</div></section>';
  return h;
}
function sbRow(o) {
  var open = S.subo === o.id, c = SB_COL[o.lvl] || SB_COL.na;
  var h = '<div class="sbr' + (open ? ' open' : '') + '"><button data-act="subopen" data-id="' + esc(o.id) + '" aria-expanded="' + open + '">' +
    '<span class="t"><span class="dot" style="background:' + c + '"></span><span class="nm">' + esc(o.name) + '</span><span class="cv">▾</span></span>' +
    '<span class="tr"><i style="width:' + (o.pct == null ? 0 : Math.max(3, o.pct)) + '%;background:' + c + '"></i></span>' +
    '<span class="ln' + (o.lvl === 'bad' ? ' bad' : '') + '">' + esc(o.line) + '</span></button>';
  if (!open) return h + '</div>';
  if (S.sube === o.id) return h + '<div class="sbx">' + sbForm(o) + '</div></div>';
  var kv = [];
  if (o.kind) kv.push(['ชนิด', o.kind + (o.auto ? (o.kind === 'เครดิต' ? ' · เติมเงินอัตโนมัติ' : ' · ตัดเงินอัตโนมัติ') : '')]);
  if (o.left != null) kv.push(['คงเหลือ', fmtN(o.left) + (o.unit ? ' ' + o.unit : '') + (o.full ? ' / ' + fmtN(o.full) : '') + (o.spent ? ' (ใช้ไป ~' + fmtN(o.spent) + ' ตั้งแต่กรอก)' : '')]);
  if (o.date) kv.push([o.auto ? 'ตัดเงินรอบหน้า' : 'หมดอายุ', dLabel(o.date)]);
  if (o.price) kv.push(['ราคา', sbMoney(o.price, o.cur) + (o.cycle && o.kind !== 'เครดิต' ? ' / ' + sbCyc(o.cycle) : '')]);
  if (o.price || o.acct) kv.push(['จ่ายจาก', 'บช.' + (o.acct || (o.sys === 'ส่วนตัว' ? ACCT0 : 'คลินิก'))]);
  if (o.date) kv.push(['เตือนก่อน', (o.remind || 7) + ' วัน']);
  if (o.hok) kv.push(['ใช้ได้ล่าสุด', dLabel(o.hok.slice(0, 10)) + ' ' + o.hok.slice(11)]);
  if (o.hmsg) kv.push(['error ล่าสุด', dLabel(o.herr.slice(0, 10)) + ' ' + o.herr.slice(11) + ' · ' + o.hmsg]);
  if (o.note) kv.push(['หมายเหตุ', o.note]);
  if (o.upd) kv.push(['อัปเดต', dLabel(o.upd)]);
  return h + '<div class="sbx"><div class="kv">' + kv.map(function (x) { return '<b>' + x[0] + '</b><span>' + esc(x[1]) + '</span>'; }).join('') + '</div><div class="bt">' +
    (o.url ? '<button class="go" data-act="subgo" data-id="' + esc(o.id) + '">🔗 ไปเติม/ต่ออายุ</button>' : '') +
    '<button data-act="subedit" data-id="' + esc(o.id) + '">✏ แก้</button>' +
    (o.kind !== 'ฟรี' && o.kind !== 'สุขภาพ' ? '<button data-act="subpaid" data-id="' + esc(o.id) + '">💸 จ่ายแล้ว</button>' : '') + '</div>' +
    (S.arm === 'p' + o.id ? '<form class="sbpay" data-form="subpay" data-id="' + esc(o.id) + '"><label for="sp-a">ยอดที่จ่ายจริง (บาท)' + (o.cur !== 'บาท' && o.price ? ' · ราคา ' + sbMoney(o.price, o.cur) : '') + '</label><div><input id="sp-a" name="amt" inputmode="decimal" autocomplete="off" value="' + (o.cur === 'บาท' && o.price ? o.price : '') + '" placeholder="0"><button class="go">ลงรายจ่าย</button></div><small>ลงเป็นรายจ่าย บช.' + esc(o.acct || (o.sys === 'ส่วนตัว' ? ACCT0 : 'คลินิก')) + (o.cycle && o.kind !== 'เครดิต' ? ' แล้วเลื่อนวันตัดเงินไปอีก 1 ' + sbCyc(o.cycle) : '') + '</small></form>' : '') +
    '</div></div>';
}
function fmtN(n) { return Number(n).toLocaleString('en-US', { maximumFractionDigits: 2 }); }
function sbForm(o) {
  var v = function (x) { return esc(x == null ? '' : x); };
  var k = o.kind || 'รายเดือน', kinds = SB_KIND.some(function (x) { return x[0] === k; }) ? SB_KIND : [[k, k]].concat(SB_KIND);
  var sel = function (name, list, cur) { return '<select id="sb-' + name + '" name="' + name + '">' + list.map(function (x) { var val = Array.isArray(x) ? x[0] : x, lb = Array.isArray(x) ? x[1] : x; return '<option value="' + esc(val) + '"' + (val === cur ? ' selected' : '') + '>' + esc(lb) + '</option>'; }).join('') + '</select>'; };
  var sys = SB_SYS.indexOf(o.sys) < 0 && o.sys ? [o.sys].concat(SB_SYS) : SB_SYS, acs = accNames();
  return '<form class="sbf" data-form="sub" data-id="' + v(o.id) + '" data-k="' + v(k) + '">' +
    '<label for="sb-name">ชื่อรายการ</label><input id="sb-name" name="name" value="' + v(o.name) + '" autocomplete="off" placeholder="เช่น Canva Pro, ค่าโฮสต์เว็บ">' +
    '<div class="g2"><span class="sbf"><label for="sb-sys">ใช้กับระบบ</label>' + sel('sys', sys, o.sys || 'คลินิก') + '</span><span class="sbf"><label for="sb-kind">รูปแบบการจ่าย</label>' + sel('kind', kinds, k) + '</span></div>' +
    '<fieldset class="pay"><legend>💰 ค่าใช้จ่าย</legend>' +
      '<div class="g2"><span class="sbf"><label for="sb-price">ราคา</label><input id="sb-price" name="price" inputmode="decimal" value="' + v(o.price) + '" placeholder="0"></span><span class="sbf"><label for="sb-cur">สกุลเงิน</label>' + sel('cur', [['บาท', '฿ บาท'], ['USD', '$ USD']], o.cur || 'บาท') + '</span></div>' +
      '<div class="g2 cyc"><span class="sbf"><label for="sb-cycle">จ่ายทุกกี่เดือน</label><input id="sb-cycle" name="cycle" inputmode="numeric" value="' + v(o.cycle || '') + '" placeholder="1 = รายเดือน, 12 = รายปี"></span><label class="ck"><input type="checkbox" name="auto"' + (o.auto ? ' checked' : '') + '> ตัดบัตร/เติมอัตโนมัติ</label></div>' +
      '<span class="sbf"><label for="sb-acct">จ่ายจากบัญชี (ตอนกด 💸 จ่ายแล้ว)</label>' + sel('acct', [['', 'อัตโนมัติ (ส่วนตัว→ส่วนตัว, อื่นๆ→คลินิก)']].concat(acs), o.acct || '') + '</span>' +
    '</fieldset>' +
    '<fieldset class="crd"><legend>💳 เครดิต / โควต้า</legend>' +
      '<div class="g3"><span class="sbf"><label for="sb-left">เหลืออยู่</label><input id="sb-left" name="left" inputmode="decimal" value="' + v(o.left) + '"></span><span class="sbf"><label for="sb-full">เต็ม</label><input id="sb-full" name="full" inputmode="decimal" value="' + v(o.full) + '"></span><span class="sbf"><label for="sb-unit">หน่วย</label><input id="sb-unit" name="unit" list="sb-units" value="' + v(o.unit) + '" placeholder="USD"></span></div>' +
      '<datalist id="sb-units">' + SB_UNITS.map(function (u) { return '<option value="' + esc(u) + '">'; }).join('') + '</datalist>' +
      '<small>หลอดจะเหลืองเมื่อเหลือน้อยกว่า 25% และแดงเมื่อน้อยกว่า 10%</small>' +
    '</fieldset>' +
    '<fieldset class="exp"><legend>⏰ หมดอายุ / ตัดเงิน</legend>' +
      '<div class="g2"><span class="sbf"><label for="sb-date">วันหมดอายุ หรือวันตัดเงินรอบหน้า</label><input id="sb-date" name="date" type="date" value="' + v(o.date) + '"></span><span class="sbf"><label for="sb-remind">เตือนก่อนกี่วัน</label><input id="sb-remind" name="remind" inputmode="numeric" value="' + v(o.remind == null ? 7 : o.remind) + '"></span></div>' +
      '<small>เตือนในสรุปเช้า 07:00 ใน Telegram · ถ้าตัดเงินอัตโนมัติ วีเลื่อนวันไปรอบถัดไปให้เองเมื่อเลยวัน</small>' +
    '</fieldset>' +
    '<label for="sb-url">ลิงก์ไปเติมเงิน / ต่ออายุ</label><input id="sb-url" name="url" inputmode="url" value="' + v(o.url) + '" placeholder="https://">' +
    '<label for="sb-note">หมายเหตุ</label><input id="sb-note" name="note" value="' + v(o.note) + '" placeholder="เช่น บัตรที่ใช้ตัด, อีเมลที่สมัคร">' +
    (o.hmsg ? '<label class="ck"><input type="checkbox" name="fixed" value="1"> แก้แล้ว (ล้างสถานะ error)</label>' : '') +
    '<div class="bt" style="display:flex;gap:8px"><button class="btn" style="background:var(--fin);flex:1">' + (o.id ? 'บันทึก' : 'เพิ่มรายการ') + '</button><button type="button" class="del" data-act="subcancel">ยกเลิก</button>' +
    (o.id ? '<button type="button" class="del' + (S.arm === 'd' + o.id ? ' arm' : '') + '" data-act="subdel" data-id="' + v(o.id) + '">' + (S.arm === 'd' + o.id ? 'ยืนยันลบ' : '🗑') + '</button>' : '') + '</div></form>';
}
document.addEventListener('change', function (ev) {
  var t = ev.target, f = t.form;
  if (!f || f.getAttribute('data-form') !== 'sub' || t.name !== 'kind') return;
  f.setAttribute('data-k', t.value);
  if (f.elements.cycle && (t.value === 'รายเดือน' || t.value === 'รายปี')) f.elements.cycle.value = t.value === 'รายปี' ? 12 : 1;
  if (t.value === 'เครดิต' && f.elements.unit && !f.elements.unit.value) f.elements.unit.value = 'USD';
});
function sbAct(act, id) {
  var o = (D.subs || []).filter(function (x) { return x.id === id; })[0];
  if (act === 'subopen') { S.subo = S.subo === id ? null : id; S.sube = null; S.arm = null; return render(); }
  if (act === 'subedit') { S.sube = id; return render(); }
  if (act === 'subnew') { S.sube = 'new'; S.subo = null; return render(); }
  if (act === 'subcancel') { S.sube = null; S.arm = null; return render(); }
  if (act === 'subgo') { if (o && o.url) tgOpen(o.url); return; }
  if (act === 'subcheck') { toast('🔄 กำลังเช็ค…'); return api('subcheck', {}); }
  if (act === 'subpaid') { S.arm = S.arm === 'p' + id ? null : 'p' + id; render(); var ai = $('sp-a'); if (ai) try { ai.focus(); } catch (e) {} return; }
  if (act === 'subdel') { if (S.arm !== 'd' + id) { S.arm = 'd' + id; return render(); } S.arm = null; S.sube = null; S.subo = null; return api('subdel', { id: id }, function () { D.subs = (D.subs || []).filter(function (x) { return x.id !== id; }); }); }
}
"""
H=rep(H,"function viewMore() {",SUB_UI+"function viewMore() {",1)
H=rep(H,"  if (/^w(day|today|go|edit|new|save|del|close|askx|pick)$/.test(act)) return wkAct(act, id, v, el, ev);\n",
        "  if (/^w(day|today|go|edit|new|save|del|close|askx|pick)$/.test(act)) return wkAct(act, id, v, el, ev);\n  if (/^sub(open|edit|new|cancel|go|check|paid|del)$/.test(act)) return sbAct(act, id);\n")
H=rep(H,"  if (kind === 'wquick') {","""  if (kind === 'sub') {
    var sa = { id: f.getAttribute('data-id') || '' }; ['name', 'sys', 'kind', 'left', 'full', 'unit', 'date', 'cycle', 'price', 'url', 'note', 'cur', 'remind', 'acct'].forEach(function (k) { sa[k] = f.elements[k] ? f.elements[k].value.trim() : ''; });
    sa.auto = !!(f.elements.auto && f.elements.auto.checked); sa.fixed = f.elements.fixed && f.elements.fixed.checked ? '1' : '';
    if (!sa.name) return toast('ใส่ชื่อบริการก่อนครับ');
    if (sa.url && !/^https?:\\/\\//.test(sa.url)) return toast('ลิงก์ต้องขึ้นต้นด้วย https://');
    S.sube = null; toast('🔌 กำลังบันทึก…'); return api('subsave', sa);
  }
  if (kind === 'subpay') {
    var pa = f.elements.amt.value.replace(/[,฿\\s]/g, '');
    if (!(Number(pa) > 0)) return toast('ใส่ยอดที่จ่ายจริง (บาท) ก่อนครับ');
    S.arm = null; toast('💸 กำลังลงรายจ่าย…'); return api('subpaid', { id: f.getAttribute('data-id'), amt: pa });
  }
  if (kind === 'wquick') {""")
assert "Code.v60" not in H
out=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
open('Code.v61.gs','w',encoding='utf8',newline='\n').write(out)
print('OK Code.v61.gs',ck(out))
