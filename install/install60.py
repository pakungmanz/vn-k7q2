# v60: เกณฑ์ P4P ใหม่ (P4P FAMMED Update 3, 15 พ.ย. 2569) + คิดคะแนนย้อนหลังทั้งหมด
#      + ภาระงานที่ไม่ตรงเกณฑ์/ไม่แน่ใจ → ลงปฏิทินไว้ก่อน (ยังไม่นับแต้ม) แล้วแมววีถาม พร้อม 2 ตัวเลือกที่ใกล้สุด
# รันในโฟลเดอร์ที่มี Code.v59b.gs : python patch60.py  → ได้ Code.v60.gs
import json,re
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v59b.gs',encoding='utf8').read()
assert ck(B)==(525625,6774),('base ไม่ใช่ v59b',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
def cut(s,a,b,n):
    i=s.index(a); j=s.index(b,i); return s[:i]+n+s[j:]
# ---------------- หลังบ้าน ----------------
C=rep(C,"var APP_VER = 'v59b';","var APP_VER = 'v60';")
# ประชุม: ไฟล์ใหม่สูตร = 180 นาที × 0.26 (ไม่มีแถวแยกบทบาทแล้ว)
C=cut(C,"  [['mt_exec', 'ประชุมคณะกรรมการบริหารโรงพยาบาล'","  add('mt_ext',","""  add('mt_exec', 'admin', 'ประชุมคณะกรรมการบริหารโรงพยาบาล', 'ครั้ง', p4pR2(180 * S), 180, 'กรรมการบริหาร, ประชุมบริหาร รพ.', 'ประชุมกก.บริหาร รพ.');
  add('mt_pct', 'admin', 'ประชุม PCT/ ยุทธศาสตร์/ งานคุณภาพ', 'ครั้ง', p4pR2(180 * S), 180, 'PCT, HA, คุณภาพ, ยุทธศาสตร์', 'ประชุม PCT/คุณภาพ');
  add('mt_org', 'admin', 'ประชุมองค์กรแพทย์', 'ครั้ง', p4pR2(180 * S), 180, 'องค์กรแพทย์', 'ประชุมองค์กรแพทย์');
""")
C=rep(C,"  add('x_unit', 'extra', 'ออกหน่วยแพทย์ / รับเสด็จ', 'ครั้ง', p4pR2(480 * 0.5), 480, 'ออกหน่วย พอ.สว., รับเสด็จ', 'ออกหน่วยแพทย์/รับเสด็จ');\n  add('x_mc', 'extra', 'งานพิธีกรของโรงพยาบาล', 'ครั้ง', 15, 60, 'พิธีกร', 'พิธีกร รพ.');",
"""  add('x_unit_free', 'extra', 'ออกหน่วยแพทย์/รับเสด็จ (3 เท่า กรณีไม่ได้รับค่าตอบแทน)', 'ครั้ง', 370, 480, 'ออกหน่วย พอ.สว., รับเสด็จ ไม่ได้ค่าตอบแทน', 'ออกหน่วยแพทย์/รับเสด็จ (ไม่มีค่าตอบแทน)');
  add('x_unit_paid', 'extra', 'ออกหน่วยแพทย์/รับเสด็จ (1.5 เท่า กรณีได้รับค่าตอบแทน)', 'ครั้ง', 180, 480, 'ออกหน่วย พอ.สว., รับเสด็จ ได้ค่าตอบแทน', 'ออกหน่วยแพทย์/รับเสด็จ (มีค่าตอบแทน)');
  add('x_mc', 'extra', 'งานพิธีกรของโรงพยาบาล', 'ครั้ง', 50, 60, 'พิธีกร', 'พิธีกร รพ.');""")
C=rep(C,"/** ตารางตั้งต้น: [รหัส, หมวด, งาน, หน่วย, คะแนน/หน่วย, นาที, คำเรียกอื่น, ชื่อย่อ] — คะแนนงานบริหาร/วิชาการ = นาที × 0.26 × เท่า */",
        "/** ตาราง = P4P FAMMED Update 3 (15 พ.ย. 2569): [รหัส, หมวด, งาน, หน่วย, คะแนน/หน่วย, นาที, คำเรียกอื่น, ชื่อย่อ] */\nvar P4P_TABLE_VER = 'FAMMED-U3-2569-11-15';")
# ครั้งแรกที่รัน v60: เขียนตารางใหม่ทับแท็บ ตาราง P4P + แปลงรหัสเก่า + คิดแต้มทุกแถวใหม่ + อัปเดตปฏิทิน
C=rep(C,"function p4pReady() { if (_p4pReady) return; _p4pReady = true; var t = ensureTab('p4pt'); if (t.sh.getLastRow() < 2) { var seed = p4pSeed(); t.sh.getRange(2, 1, seed.length, 8).setValues(seed); } ensureTab('p4p'); }",
"""function p4pReady() { if (_p4pReady) return; _p4pReady = true; var t = ensureTab('p4pt'); if (t.sh.getLastRow() < 2) { var seed = p4pSeed(); t.sh.getRange(2, 1, seed.length, 8).setValues(seed); setProp('P4P_TABLE_VER', P4P_TABLE_VER); } ensureTab('p4p'); p4pMigrate(t.sh); }
function p4pMigrate(tsh) {
  if (prop('P4P_TABLE_VER') === P4P_TABLE_VER) return;
  try {
    var seed = p4pSeed(), last = tsh.getLastRow(), blank = [];
    tsh.getRange(2, 1, seed.length, 8).setValues(seed);
    for (var i = seed.length + 2; i <= last; i++) blank.push(['', '', '', '', '', '', '', '']);
    if (blank.length) tsh.getRange(seed.length + 2, 1, blank.length, 8).setValues(blank);
    _p4pT = null;
    var sh = sheet('p4p'), days = {}, n = 0;
    p4pRows().forEach(function (r) {
      var nk = r.k, pend = '', m = /^(mt_exec|mt_pct|mt_org)_\\d+$/.exec(r.k);
      if (m) nk = m[1];
      if (r.k === 'x_unit') { nk = ''; pend = 'opts:x_unit_free,x_unit_paid'; }
      var it = nk ? p4pItem(nk) : null;
      if (nk && !it) pend = 'opts:';
      var v = it ? [it.k, it.n, it.s, r.q, it.u, it.sc == null ? '' : it.sc, it.sc == null ? 0 : p4pR2(r.q * it.sc)] : ['', r.n, '', r.q, r.u, '', 0];
      sh.getRange(r.row, 3, 1, 7).setValues([v]);
      if (pend) sh.getRange(r.row, 13).setValue(pend);
      days[r.d] = 1; n++;
    });
    setProp('P4P_TABLE_VER', P4P_TABLE_VER);
    Object.keys(days).forEach(p4pSyncDay);
    log('p4p-migrate', P4P_TABLE_VER, n + ' แถว', '');
  } catch (e) { log('p4p-migrate', P4P_TABLE_VER, '', e.message); }
}""")
# แถวรอเลือกเกณฑ์: รหัสว่าง + คอลัมน์ วีเดา = "opts:k1,k2"
C=rep(C,"ev: String(o.v[11] || ''), g: !!String(o.v[12] || '') };",
        "ev: String(o.v[11] || ''), g: String(o.v[12] || '') === '?', o: /^opts:/.test(String(o.v[12] || '')) ? String(o.v[12]).slice(5).split(',').filter(String) : null };")
C=rep(C,"function p4pShort(r) { var it = p4pItem(r.k); return (it ? it.a : r.n) + ' ' + money(r.q) + ' ' + p4pUnit(it ? it.u : r.u, it ? it.s : r.s); }",
        "function p4pShort(r) { var it = p4pItem(r.k); return (it ? it.a : r.n) + ' ' + money(r.q) + ' ' + p4pUnit(it ? it.u : r.u || 'คน', it ? it.s : r.s) + (it ? '' : ' (รอเลือกเกณฑ์)'); }")
C=rep(C,"function p4pLine(r) { return p4pShort(r) + ' = ' + money(p4pPts(r)) + ' แต้ม'",
        "function p4pLine(r) { return p4pShort(r) + (p4pItem(r.k) ? ' = ' + money(p4pPts(r)) + ' แต้ม' : '')")
C=rep(C,"""    var it = p4pItem(e.k); if (!it) return;
    var q = p4pR2(String(e.q == null ? '' : e.q).replace(/,/g, '')); if (!(q > 0) || q > 10000) return;
    var d = p4pYmd(e.d, today), sh = sheet('p4p');""","""    var it = p4pItem(e.k);
    var q = p4pR2(String(e.q == null ? '' : e.q).replace(/,/g, '')); if (!(q > 0) || q > 10000) return;
    var d = p4pYmd(e.d, today), sh = sheet('p4p');
    // v60: ไม่ตรงเกณฑ์/ไม่แน่ใจ → ลงไว้ก่อน (ยังไม่นับแต้ม) + 2 ตัวเลือกที่ใกล้สุด ให้ภัทรเลือก
    if (!it || e.sure === false) {
      var opts = [], seen = {};
      [it ? it.k : ''].concat(e.opts || []).forEach(function (k) { var x = p4pItem(k); if (x && !seen[x.k] && opts.length < 2) { seen[x.k] = 1; opts.push(x.k); } });
      var label = String(e.label || (it ? it.a : '') || 'ภาระงาน').trim().slice(0, 80), pid = newId('W');
      sh.appendRow([pid, parseLocal(d, 12), '', label, '', q, String(e.u || (it ? it.u : '') || 'คน').trim(), '', 0, String(raw || '').slice(0, 300), now, '', 'opts:' + opts.join(',')]);
      days[d] = 1; out.push({ id: pid, d: d, k: '', n: label, s: '', q: q, u: String(e.u || 'คน'), sc: null, o: opts });
      return;
    }""")
C=rep(C,"var it = p4pItem(k || r.k); if (!it) return null;","var it = p4pItem(k || r.k); if (!it) return null; // รอเลือกเกณฑ์ + เลือกแล้ว = กลายเป็นแถวปกติ")
C=cut(C,"function p4pSystem(","/** ข้อความ → บันทึก",r"""function p4pSystem(d, calCtx) {
  var dd = parseLocal(d, 12), y1 = ymd(new Date(dd.getTime() - 86400000)), y2 = ymd(new Date(dd.getTime() - 2 * 86400000));
  var pcus = []; try { pcus = pcuList().map(function (p) { return p.name; }); } catch (e) {}
  if (!pcus.length) pcus = PCU_SEED.map(function (p) { return p[0]; });
  return [
    'คุณช่วยหมอประภัทร (แพทย์เวชศาสตร์ครอบครัว รพ.วารินชำราบ) บันทึกภาระงาน P4P ตามเกณฑ์ในตารางด้านล่างเท่านั้น ต้องแม่นยำ เพราะใช้คิดแต้มจริง ห้ามเดาเอง',
    'ตอบ JSON บรรทัดเดียวเท่านั้น ไม่มีคำอธิบาย: {"entries":[{"k":"รหัส หรือ \"\"","q":จำนวน,"u":"คน|ราย|ครั้ง|ชม.","d":"YYYY-MM-DD","set":false,"label":"ชื่องานสั้นๆ ตามที่ผู้ใช้พูด","opts":["รหัสใกล้สุด","รหัสใกล้รองลงมา"]}],"ask":""}',
    'กติกา:',
    '- ใส่ k เฉพาะเมื่องานที่พูดตรงกับแถวในตารางชัดเจนแน่นอน (ชื่องาน/สถานที่/ชนิดตรงกัน) · ถ้าไม่ตรงกับแถวไหนเลย หรือก้ำกึ่งเทียบได้หลายแถว หรือต้องเดา → k="" แล้วใส่ opts = 2 รหัสในตารางที่ใกล้เคียงที่สุด (ใกล้สุดก่อน) เพื่อให้ผู้ใช้เลือกเอง ระบบจะลงปฏิทินไว้ก่อนโดยยังไม่นับแต้ม',
    '- label = ชื่องานสั้นๆ ตามที่ผู้ใช้พูด (เช่น "ตรวจ รพ.สต.เทศบาล3") · q = จำนวนตามหน่วย (คน/ราย/ครั้ง/ชั่วโมง ทศนิยมได้) ตัวเลขไทยหรือคำอ่านแปลงเป็นตัวเลข · ถ้าไม่มีจำนวนเลย ไม่ต้องใส่ entry แล้วถามใน ask',
    '- พูดหลายงานในประโยคเดียว → แยกเป็นหลาย entries',
    '- d: "วันนี้" หรือไม่บอกวัน = ' + d + ' (วัน' + TH_DAYS_FULL[dd.getDay()] + ') · "เมื่อวาน" = ' + y1 + ' · "เมื่อวานซืน" = ' + y2 + ' · "วันที่ 12" = วันที่ 12 ของเดือนนี้ (ถ้าเกินวันนี้ = เดือนก่อน) · วันที่แบบไทย dd/mm/yy เป็นปี พ.ศ. ให้ตอบเป็น ค.ศ.',
    '- set=true เฉพาะเมื่อผู้ใช้บอกว่า แก้/เปลี่ยนเป็น/จริงๆ ได้/ไม่ใช่...แต่เป็น (แทนยอดเดิมของรหัสนั้นในวันนั้น) ปกติ set=false (บวกเพิ่ม)',
    '- คำพูดถอดจากเสียงอาจสะกดเพี้ยน เช่น "รอพอสต."/"รพ. ต."/"รพสต" = รพ.สต. · ชื่อ รพ.สต. ที่รู้จัก: ' + pcus.join(', ') + ' (เช่น "โน้นเกษม"="โนนเกษม", "เทศสบัญ 3"="เทศบาล3")',
    '- ตัวอย่างที่ตรงเกณฑ์ชัดเจน: ตรวจคนไข้ที่ รพ.สต. → c_pcu · คลินิก NCD/DM/HT ใน รพ. → fm_ncd · OPD palliative/ผู้สูงอายุ → fm_geri · OPD ทั่วไป/ประกันสังคม/ปกส/all D → g_opd · ACP/CGA → fm_cx30 · เยี่ยมบ้านรายใหม่/เก่า → c_hv_new/c_hv_old',
    '- "ตรวจคนไข้ X คน" ไม่บอกที่/ชนิด → k="" และ opts จากตารางงานในปฏิทินของวันนั้นด้านล่าง (ถ้ามี) ไม่งั้น g_opd กับ c_pcu',
    '- ออกหน่วยแพทย์/รับเสด็จ ไม่บอกว่าได้ค่าตอบแทนไหม → k="" opts ["x_unit_free","x_unit_paid"] · วิทยากร/ประชุมวิชาการไม่บอกชั่วโมง → ถามใน ask',
    'ตาราง (รหัส | หมวด | งาน | หน่วย | แต้ม/หน่วย | คำเรียกอื่น):',
    p4pTable().map(function (x) { return x.k + ' | ' + x.s + ' | ' + x.n + ' | ' + x.u + ' | ' + (x.sc == null ? '-' : x.sc) + (x.h ? ' | ' + x.h : ''); }).join('\n'),
    'ตารางงานในปฏิทินวันที่ ' + d + ':\n' + (calCtx || '(ไม่มี)')
  ].join('\n');
}
""")
C=rep(C,"    return { k: e.k, q: e.q, d: ed, set: e.set === true, sure: e.sure !== false };",
        "    return { k: e.k, q: e.q, u: e.u, d: ed, set: e.set === true, sure: e.sure !== false, label: e.label, opts: Array.isArray(e.opts) ? e.opts : [] };")
C=rep(C,"""  var guess = saved.some(function (s) { return s.g; });
  var msg = '📋 ' + saved.map(p4pLine).join('\\n📋 ') + (guess ? '\\nวีเดาบางรายการ (ป้ายส้ม) แตะเพื่อเช็คได้' : '') + (ask ? '\\n' + ask : '');""",
"""  var pend = saved.filter(function (s) { return !s.k; });
  var msg = saved.map(function (s) { return (s.k ? '📋 ' : '❓ ') + p4pLine(s); }).join('\\n') + (pend.length ? '\\nไม่พบเกณฑ์คะแนน — ลงปฏิทินไว้แล้ว เลือกเกณฑ์ในหน้าภาระงานได้เลย' : '') + (ask ? '\\n' + ask : '');""")
C=rep(C,"if (r.raw) o.r = r.raw.slice(0, 120); list.push(o);","if (r.raw) o.r = r.raw.slice(0, 120); if (r.o) o.o = r.o; list.push(o);")
C=rep(C,"if (!known[r.k]) o.n = r.n + ' ' + money(r.q) + ' ' + p4pUnit(r.u, r.s);","if (!known[r.k]) o.n = r.n + ' ' + money(r.q) + ' ' + p4pUnit(r.u || 'คน', r.s);")
# ---------------- หน้าแอป ----------------
H=rep(H,".wkcalc{",""".wkpend{flex-direction:column;align-items:stretch;gap:8px;border-color:#F3C1BB;background:#FFF6F5}
.wkpend .hd{display:flex;gap:10px;align-items:center}
.wkpend .hd b{font-size:15px;color:#9A3412}
.wkopts{display:flex;flex-direction:column;gap:6px}
.wkask .wkopts button{width:100%;height:auto;min-height:44px;border-radius:12px;border:1.5px solid var(--wk);background:#fff;color:var(--wk-ink);font-weight:600;text-align:left;padding:8px 12px;display:flex;justify-content:space-between;gap:8px;align-items:center}
.wkask .wkopts button span{color:var(--wk);white-space:nowrap}
.wkask .wkopts button.alt{border:1px dashed var(--line);color:var(--mute);font-weight:500}
.wkwait{display:inline-block;font-size:11px;font-weight:600;color:#9A3412;background:#FFE4DE;border-radius:8px;padding:1px 7px;margin-left:6px;vertical-align:2px}
.wkcalc{""")
H=rep(H,"(e.g ? '<span class=\"wkg\">วีเดา แตะเช็ค</span>' : '')","(e.o ? '<span class=\"wkwait\">รอเลือกเกณฑ์</span>' : e.g ? '<span class=\"wkg\">วีเดา แตะเช็ค</span>' : '')")
H=rep(H,"(it ? esc(it.s) + (un ? ' · ยังไม่มีแต้มในตาราง' : ' · ' + wkN(it.sc) + ' แต้ม/' + esc(it.u)) : 'ไม่มีรหัสนี้ในตารางแล้ว')",
        "(it ? esc(it.s) + (un ? ' · ยังไม่มีแต้มในตาราง' : ' · ' + wkN(it.sc) + ' แต้ม/' + esc(it.u)) : e.o ? 'ลงปฏิทินแล้ว · ยังไม่นับแต้ม' : 'ไม่มีรหัสนี้ในตารางแล้ว')")
H=rep(H,"""  if (S.wask) h += '<div class="wkask" role="status">'""","""  // v60: ภาระงานที่ไม่ตรงเกณฑ์ → แมววีถาม + 2 ตัวเลือกใกล้สุด
  W.list.filter(function (e) { return e.o; }).forEach(function (e) {
    var cat = typeof CAT_IMG === 'string' && CAT_IMG.length > 40 ? '<img src="' + CAT_IMG + '" alt="">' : '';
    h += '<div class="wkask wkpend" role="alertdialog" aria-label="ไม่พบเกณฑ์คะแนน"><div class="hd">' + cat + '<div style="flex:1"><b>ไม่พบเกณฑ์คะแนนในภาระงานนี้ครับ</b><div style="font-size:13px">“' + esc(e.n) + '” · ' + beDMY(e.d) + ' · ลงปฏิทินไว้แล้ว</div></div></div>' +
      '<div style="font-size:13px;color:var(--mute)">จะให้คิดคะแนนจากอันไหน</div><div class="wkopts">' +
      e.o.map(function (k) { var it = wkIt(k); return it ? '<button data-act="wpick" data-id="' + esc(e.id) + '" data-v="' + esc(k) + '">' + esc(it.a) + '<span>' + (it.sc == null ? 'ยังไม่มีแต้ม' : wkN(wkPts(k, e.q)) + ' แต้ม') + '</span></button>' : ''; }).join('') +
      '<button class="alt" data-act="wedit" data-id="' + esc(e.id) + '">เลือกเกณฑ์อื่น / แก้จำนวน / ลบ…</button></div></div>';
  });
  if (S.wask) h += '<div class="wkask" role="status">'""")
H=rep(H,"  if (/^w(day|today|go|edit|new|save|del|close|askx)$/.test(act)) return wkAct(act, id, v, el, ev);","  if (/^w(day|today|go|edit|new|save|del|close|askx|pick)$/.test(act)) return wkAct(act, id, v, el, ev);")
H=rep(H,"S.arm = null; S.we = { id: e.id, k: e.k, q: e.q, d: e.d, r: e.r || '', g: !!e.g }; return render(); }",
        "S.arm = null; S.we = { id: e.id, k: e.k || (e.o && e.o[0]) || '', q: e.q, d: e.d, r: e.r || '', g: !!e.g || !!e.o }; return render(); }\n  if (act === 'wpick') { var pe = W.list.filter(function (x) { return x.id === id; })[0]; if (!pe || !wkIt(v)) return; var pp = wkPts(v, pe.q); toast('📋 ' + wkLabel({ k: v, q: pe.q }) + ' = ' + wkN(pp) + ' แต้ม'); return api('p4pedit', { id: id, k: v }, function () { pe.k = v; pe.p = pp; delete pe.o; delete pe.n; delete pe.g; wkRecalc(pe.d.slice(0, 7)); }); }")
H=rep(H,"W.list.forEach(function (x) { if (x.id === f.id) { var om = x.d.slice(0, 7); x.k = f.k; x.q = q; x.d = f.d; x.p = p; delete x.g; wkRecalc(om); } });",
        "W.list.forEach(function (x) { if (x.id === f.id) { var om = x.d.slice(0, 7); x.k = f.k; x.q = q; x.d = f.d; x.p = p; delete x.g; delete x.o; delete x.n; wkRecalc(om); } });")
H=rep(H,"(e.g ? '<div style=\"font-size:13px;color:var(--warn)\">วีเดารหัสงานนี้ เช็คแล้วกดบันทึกเพื่อยืนยัน</div>' : '')",
        "(e.g ? '<div style=\"font-size:13px;color:var(--warn)\">ยังไม่ได้ยืนยันเกณฑ์ เลือกแล้วกดบันทึกเพื่อนับแต้ม</div>' : '')")
out=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
open('Code.v60.gs','w',encoding='utf8',newline='\n').write(out)
print('OK Code.v60.gs',ck(out))
