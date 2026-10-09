"""Build the production app (index.html) from the prototype.

The prototype (prototype/index.html) is the design source; this script swaps the
mock login / browser storage for Google sign-in + Google Drive and wraps the page
in a full HTML document with PWA metadata.

Usage:  python tools/build.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'prototype' / 'index.html').read_text(encoding='utf-8')
drive_js = (ROOT / 'tools' / 'drive.js.txt').read_text(encoding='utf-8')
save_js = (ROOT / 'tools' / 'save.js.txt').read_text(encoding='utf-8')
s = src

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count}x, found {n}: {old[:80]!r}'
    s = s.replace(old, new)

def cut(start, end, new, include_end=False):
    global s
    i = s.index(start); j = s.index(end, i) + (len(end) if include_end else 0)
    s = s[:i] + new + s[j:]

# ---- login screen: real Google sign-in
cut('    <button id="gBtn" class="btn-google" type="button">', '  </div>\n</section>',
'''    <button id="gBtn" class="btn-google" type="button" disabled>
      <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <span id="gBtnTxt">載入中…</span>
    </button>
    <button id="otherAcct" class="link-btn" type="button">使用其他 Google 帳號</button>
    <p id="loginErr" class="err" role="alert" hidden></p>
    <p class="proto-note">只有授權的帳號能使用。第一次登入時，Google 會詢問是否允許本 App 存取「它自己建立的雲端硬碟檔案」，請按「允許」。</p>
''')
rep('<span class="mode">樣板 · 存於此瀏覽器</span>', '<a class="mode" id="driveLink" href="https://drive.google.com/" target="_blank" rel="noopener">Google Drive</a>')
rep('<p>正式版：資料存在此帳號的 Google Drive「樂器維護紀錄」資料夾。</p>', '<p>紀錄與照片存在此帳號 Google Drive 的「樂器維護紀錄」資料夾。</p>')
rep('<div class="save-row"><p id="formMsg" role="status"></p><button class="btn-primary" type="submit">儲存紀錄</button></div>',
    '<div class="save-row"><p id="formMsg" role="status"></p><button class="btn-primary" id="saveBtn" type="submit">儲存紀錄</button></div>')
rep('<label class="chk"><input type="checkbox" id="showSample" checked> 含範例資料</label>',
    '<label class="chk"><input type="checkbox" id="showSample"> 顯示示範資料</label>')
s = re.sub(r'<p class="hint" id="repNote">.*?</p>', '', s, count=1)
rep('  <div id="tip" class="tip" role="tooltip" hidden></div>\n',
    '  <div id="tip" class="tip" role="tooltip" hidden></div>\n'
    '  <div id="reauth" class="reauth" role="alertdialog" aria-labelledby="reauthT" hidden><p id="reauthT">Google 連線已逾時，請點一下繼續（資料不會遺失）。</p><button type="button" class="btn-primary sm" id="reauthBtn">重新連線</button></div>\n')

# ---- extra styles
rep('</style>', '''.link-btn{border:0;background:none;color:var(--accent);font-size:13.5px;text-decoration:underline;padding:4px;justify-self:center}
.btn-google:disabled{opacity:.6;cursor:progress}
a.mode{text-decoration:none;color:var(--muted)}
a.mode:hover{color:var(--accent);border-color:var(--accent)}
.ava img{width:100%;height:100%;border-radius:50%;object-fit:cover}
.ava{overflow:hidden}
.reauth{position:fixed;left:16px;right:16px;bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:90;max-width:520px;margin:0 auto;background:var(--fg);color:var(--surface);border-radius:14px;padding:12px 14px;display:flex;gap:12px;align-items:center;box-shadow:0 10px 30px rgb(0 0 0 / .25)}
.reauth p{margin:0;flex:1;font-size:14px}
.ph-err{color:var(--paper-muted)}
.btn-primary:disabled{opacity:.7;cursor:progress}
</style>''')

# ---- scripts: mock login → Google; local storage → Drive
s = re.sub(r"// 樣板用的示範名字；正式版直接讀取 Google 帳號名稱\nconst MOCK_NAMES = \{.*?\};\n", '', s, count=1)
cut('/* ================= Login ================= */', '/* ================= Tabs & version', drive_js)
rep("state.photos[+inp.dataset.i]={url:URL.createObjectURL(inp.files[0]),name:inp.files[0].name,caption:''};",
    "state.photos[+inp.dataset.i]={url:URL.createObjectURL(inp.files[0]),file:inp.files[0],name:inp.files[0].name,caption:''};")
cut("$('#recForm').addEventListener('submit',e=>{", "/* ---------- 範例資料", save_js + '\n')
rep("const sessionPhotos={};   // recId → object URLs（樣板：照片只保留到關閉頁面）\n", '')
rep(" const mine=store.get('mi-records',[]).filter(r=>r.user===state.user);", " const mine=DB.records;")
rep("function photoUrls(r){return r.sample?r.photos.map((_,k)=>samplePhoto(r,k)):(sessionPhotos[r.id]||[])}",
    "function photoUrls(r){return r.sample?r.photos.map((_,k)=>samplePhoto(r,k)):r.photos.map(p=>p.fileId?'fid:'+p.fileId:'')}")
rep('<img src="${urls[k]}" alt="照片 ${k+1}">', '${imgTag(urls[k],k)}')
rep(" $('#rvBody').querySelectorAll('.page').forEach((p,i)=>p.style.animationDelay=i*120+'ms');",
    " $('#rvBody').querySelectorAll('.page').forEach((p,i)=>p.style.animationDelay=i*120+'ms');hydrate($('#rvBody'));")
rep(" $('#lbImg').src=lb.urls[k];$('#lbImg').alt=`照片 ${k+1}`;",
    " const u=lb.urls[k],im=$('#lbImg');im.alt=`照片 ${k+1}`;\n if(u.startsWith('fid:')){im.removeAttribute('src');getPhotoUrl(u.slice(4)).then(x=>{if(lb.k===k)im.src=x}).catch(()=>{im.alt='照片無法載入'})}else im.src=u;")
rep(" body.querySelectorAll('.page').forEach((p,i)=>p.style.animationDelay=Math.min(i,6)*90+'ms');",
    " body.querySelectorAll('.page').forEach((p,i)=>p.style.animationDelay=Math.min(i,6)*90+'ms');repHydrate=hydrate(body);")
rep("function buildReport(){", "let repHydrate=Promise.resolve();\nfunction buildReport(){")
rep("$('#repPrint').addEventListener('click',()=>{try{window.print()}catch(e){}});",
    "$('#repPrint').addEventListener('click',async()=>{const b=$('#repPrint');b.disabled=true;b.textContent='載入照片中…';try{await repHydrate}catch(e){}b.disabled=false;b.textContent='列印／存成 PDF';window.print()});")
cut("const saved=store.get('mi-user',null);", "</script>", "initAuth();\n")
rep("const VERSIONS = [\n", "const VERSIONS = [\n  {v:'V7', date:'2026-10-09', items:[\n"
    "    '正式版上線：Google 帳號登入，只有授權帳號能使用',\n"
    "    '紀錄與照片存到登入者自己的 Google Drive「樂器維護紀錄」資料夾',\n"
    "    '照片上傳前自動壓縮（長邊 1600px）',\n"
    "    '可加到手機主畫面，全螢幕使用；月報可下載文字檔、列印或存成 PDF',\n"
    "    '示範資料預設關閉，可在統計頁開啟'\n"
    "  ]},\n")

# ---- full document wrapper (the prototype relied on the Artifact host's skeleton)
head_end = s.index('<!-- ============ Login')
head, body = s[:head_end], s[head_end:]
doc = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="管樂器維修保養紀錄：Google 帳號登入，紀錄與照片存在自己的 Google Drive。">
<meta name="theme-color" content="#85590C">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="樂器維護">
<link rel="manifest" href="manifest.webmanifest?v=2">
<link rel="icon" href="icons/icon-192.png?v=2" type="image/png">
<link rel="apple-touch-icon" href="icons/icon-180.png?v=2">
<script src="https://accounts.google.com/gsi/client" async defer></script>
<style>
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}}
body{{margin:0;-webkit-text-size-adjust:100%}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
{head}</head>
<body>
{body}</body>
</html>
'''
(ROOT / 'index.html').write_text(doc, encoding='utf-8')
print('built index.html', len(doc))
