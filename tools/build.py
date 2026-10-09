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
    <p class="proto-note">只有授權的帳號能使用。第一次登入時，Google 會詢問是否允許存取雲端硬碟，請勾選並按「繼續」。App 只會使用你雲端硬碟裡的「樂器維護紀錄」資料夾。</p>
''')
rep('<span class="mode">樣板 · 存於此瀏覽器</span>', '<a class="mode" id="driveLink" href="https://drive.google.com/" target="_blank" rel="noopener">Google Drive</a>')
rep('<p>正式版：資料存在此帳號的 Google Drive「樂器維護紀錄」資料夾。</p>', '<p>紀錄與照片存在此帳號 Google Drive 的「樂器維護紀錄」資料夾。</p>')
rep('<button id="logoutBtn" class="btn-ghost warn" type="button">登出</button>', '<button id="shareOpen" class="btn-ghost" type="button">分享我的紀錄給對方…</button>\n        <button id="logoutBtn" class="btn-ghost warn" type="button">登出</button>')
rep('<label class="sr" for="statYear">年份</label>', '<label class="sr" for="statSrc">資料來源</label><select id="statSrc" hidden><option value="me">我的紀錄</option></select>\n          <label class="sr" for="statYear">年份</label>')
rep('  <div id="tip" class="tip" role="tooltip" hidden></div>\n', '  <div id="tip" class="tip" role="tooltip" hidden></div>\n'
    '  <section id="shareModal" class="modal" role="dialog" aria-modal="true" aria-labelledby="shareT" hidden>\n'
    '    <div class="sec-head"><h2 id="shareT" style="font-family:var(--f-display);font-size:20px">分享我的紀錄</h2><button class="x" id="shareX" type="button" aria-label="關閉">×</button></div>\n'
    '    <p class="hint">對方只能查看，不能修改或刪除。只能分享給授權名單上的帳號。</p>\n'
    '    <form id="shareForm" class="other"><input id="shareEmail" type="email" placeholder="對方的 Google 帳號" autocomplete="off" aria-label="對方的 Google 帳號"><button class="btn-primary sm" type="submit">分享</button></form>\n'
    '    <p id="shareMsg" class="hint" role="status"></p>\n'
    '    <p class="eyebrow">目前分享給</p><ul id="shareList" class="share-list"></ul>\n'
    '  </section>\n')
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
.share-list{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.share-list li{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:10px}
.share-list li span{display:grid;min-width:0;word-break:break-all}
.share-list small{color:var(--muted);font-size:12px}
.share-list li.hint,.share-list li.err{border:0;padding:4px 0}
.btn-ghost.sm2{padding:6px 12px;font-size:13px;white-space:nowrap}
#statSrc{font-family:var(--f-body)}
.badge.owner{background:var(--sunk);color:var(--fg)}
</style>''')

# ---- scripts: mock login → Google; local storage → Drive
s = re.sub(r"// 樣板用的示範名字；正式版直接讀取 Google 帳號名稱\nconst MOCK_NAMES = \{.*?\};\n", '', s, count=1)
cut('/* ================= Login ================= */', '/* ================= Tabs & version', drive_js)
rep("/* ---------- Statistics view ---------- */", "/* ---------- Statistics view ---------- */\n" + (ROOT / 'tools' / 'share.js.txt').read_text(encoding='utf-8'))
rep("state.photos[+inp.dataset.i]={url:URL.createObjectURL(inp.files[0]),name:inp.files[0].name,caption:''};",
    "state.photos[+inp.dataset.i]={url:URL.createObjectURL(inp.files[0]),file:inp.files[0],name:inp.files[0].name,caption:''};")
cut("$('#recForm').addEventListener('submit',e=>{", "/* ---------- 範例資料", save_js + '\n')
rep("const sessionPhotos={};   // recId → object URLs（樣板：照片只保留到關閉頁面）\n", '')
rep(" const mine=store.get('mi-records',[]).filter(r=>r.user===state.user);", " const mine=sourceRecords();")
rep("if(v==='list')renderRecords();", "if(v==='list'){renderRecords();refreshShared()}")
rep("function closeOverlays(){$('#sheet').hidden=true;$('#verModal').hidden=true;", "function closeOverlays(){$('#sheet').hidden=true;$('#verModal').hidden=true;const sm=document.getElementById('shareModal');if(sm)sm.hidden=true;")
rep("${r.sample?'<span class=\"badge mini sample\">範例</span>':''} · ${esc(r.customer", "${r.sample?'<span class=\"badge mini sample\">範例</span>':''}${r._owner?`<span class=\"badge mini owner\">${esc(r._owner)}</span>`:''} · ${esc(r.customer")
rep("${r.sample?' · 範例':''}`;", "${r.sample?' · 範例':''}${r._owner?' · '+r._owner+' 的紀錄':''}`;")
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
rep("const VERSIONS = [\n", "const VERSIONS = [\n  {v:'V8', date:'2026-10-10', items:[\n"
    "    '可查看對方的維修紀錄：帳號選單「分享我的紀錄給對方」，對方即可在歷史紀錄切換查看（唯讀）',\n"
    "    '歷史紀錄可切換資料來源：我的紀錄、對方的紀錄、全部（合併）；統計與月報跟著切換',\n"
    "    'Google 權限改為完整雲端硬碟範圍（App 只使用「樂器維護紀錄」資料夾）'\n"
    "  ]},\n  {v:'V7', date:'2026-10-09', items:[\n"
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
