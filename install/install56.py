# v56: ข้อความแจ้งเตือน (toast) มีแมววีโผล่มาด้วย — ฝั่งหน้าแอปล้วน ไม่แตะหลังบ้าน ไม่เพิ่มการโหลด (ใช้รูปแมวที่ฝังอยู่แล้วจาก v54)
# รันในโฟลเดอร์ที่มี Code.v55.gs : python patch56.py
import json,re,os
def ck(t):
    u=t.encode('utf-16-le'); s=0
    for k in range(0,len(u),2): s=(s+int.from_bytes(u[k:k+2],'little'))%9973
    return (len(u)//2,s)
B=open('Code.v55.gs',encoding='utf8').read()
assert ck(B)==(462457,8240),('base ไม่ใช่ v55',ck(B))
C=B[:B.find('\n/* APP_HTML')]+'\n'
H=json.loads(re.search(r'\nvar APP_HTML = (".*");\n',B).group(1))
MP4=re.search(r'\nvar CELEB_MP4 = "([^"]*)";',B).group(1)
def rep(s,o,n,cnt=1):
    assert s.count(o)==cnt,('ไม่เจอ/เจอซ้ำ',s.count(o),o[:70])
    return s.replace(o,n)
C=rep(C,"var APP_VER = 'v55';","var APP_VER = 'v56';")
H=rep(H,"#toast{position:fixed;left:50%;bottom:150px;transform:translateX(-50%);background:var(--ink);color:#fff;padding:10px 16px;border-radius:12px;font-size:14px;max-width:88%;white-space:pre-line;opacity:0;transition:opacity .2s;pointer-events:none;z-index:9}\n#toast.on{opacity:1}",
"#toast{position:fixed;left:50%;bottom:150px;transform:translateX(-50%);background:var(--ink);color:#fff;padding:10px 16px;border-radius:12px;font-size:14px;max-width:88%;white-space:pre-line;opacity:0;transition:opacity .2s;pointer-events:none;z-index:9;display:flex;align-items:center;gap:10px;width:max-content}\n#toast.on{opacity:1}\n#toast.wc{padding:6px 16px 6px 6px;border-radius:26px}\n#toast .tcat{width:40px;height:40px;flex-shrink:0;border-radius:50%;background:#DCE7F7;overflow:hidden;display:flex;align-items:flex-end;justify-content:center}\n#toast .tcat img{width:46px;height:46px;margin-bottom:-2px}\n#toast.on .tcat{animation:tcatin .35s ease-out}\n@keyframes tcatin{0%{transform:scale(.4) rotate(-12deg)}70%{transform:scale(1.12) rotate(4deg)}100%{transform:none}}\n@media (prefers-reduced-motion:reduce){#toast.on .tcat{animation:none}}")
H=rep(H,"function toast(m) { if (!m) return; var t = $('toast'); t.textContent = m; t.classList.add('on');",
"function toast(m) { if (!m) return; var t = $('toast'), ci = typeof CAT_IMG === 'string' && CAT_IMG.length > 40; // v56: แมววีโผล่มากับข้อความ\n  t.innerHTML = (ci ? '<span class=\"tcat\" aria-hidden=\"true\"><img src=\"' + CAT_IMG + '\" alt=\"\"></span>' : '') + '<span>' + esc(m) + '</span>';\n  t.classList.toggle('wc', ci); t.classList.remove('on'); void t.offsetWidth; t.classList.add('on');")
OUT=C.rstrip('\n')+'\n/* APP_HTML: generated from app.html */\nvar APP_HTML = '+json.dumps(H,ensure_ascii=False)+';\n'+'\n/* CELEB_MP4: generated from assets/celeb.mp4 */\nvar CELEB_MP4 = "'+MP4+'";\n'
L,S=ck(OUT)
open('Code.v56.gs','w',encoding='utf8',newline='').write(OUT)
if os.environ.get('VEE_DEV'):
    open('app.v56.html','w',encoding='utf8',newline='').write(H); open('Code.gs','w',encoding='utf8',newline='').write(OUT)
print('OK Code.v56.gs length',L,'checksum',S)
