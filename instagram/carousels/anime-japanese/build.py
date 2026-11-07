#!/usr/bin/env python3
"""Generate the 10-slide 'Anime Japanese that gets you fired' carousel as HTML.

Optional images: drop files into images/ with these names and re-run.
  cover.png    anime character shouting (cover, right side)
  stake.png    anime character bowing / panicking office scene (slide 2)
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
HANDLE = "@raj_in_jp"
TOTAL = 10


def img(name):
    p = os.path.join(IMG, name)
    return f"images/{name}" if os.path.exists(p) else None


CSS = """
@font-face{font-family:Dela;src:url(fonts/DelaGothicOne.ttf)}
.jp{font-family:NotoJP,'Noto Color Emoji',sans-serif!important;font-weight:900}
@font-face{font-family:Brush;src:url(fonts/YujiSyuku.ttf)}
@font-face{font-family:Archivo;src:url(fonts/ArchivoBlack.ttf)}
@font-face{font-family:NotoJP;src:url(fonts/NotoSansJP-500.ttf);font-weight:500}
@font-face{font-family:NotoJP;src:url(fonts/NotoSansJP-700.ttf);font-weight:700}
@font-face{font-family:NotoJP;src:url(fonts/NotoSansJP-900.ttf);font-weight:900}
:root{--cream:#FFF7EE;--ink:#141414;--pink:#E8175D;--pink2:#FFD9E5;--green:#0E9F56;--green2:#DDF7E8;--yellow:#FFD23F}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#888;font-family:NotoJP,'Noto Color Emoji',sans-serif;color:var(--ink)}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--cream);margin:0 0 20px}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(232,23,93,.13) 3px,transparent 3.5px);background-size:28px 28px;
  -webkit-mask-image:radial-gradient(ellipse at 100% 0%,#000 0%,transparent 60%);mask-image:radial-gradient(ellipse at 100% 0%,#000 0%,transparent 60%)}
.top{position:absolute;top:56px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.handle{font-family:Archivo;font-size:32px;letter-spacing:.5px}
.handle b{color:var(--pink)}
.pg{font-family:Archivo;font-size:32px;background:var(--ink);color:#fff;border-radius:999px;padding:8px 26px}
.bottom{position:absolute;bottom:52px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;font-family:Archivo,'Noto Color Emoji';font-size:30px;z-index:5}
.swipe{color:var(--pink)}
.bar{position:absolute;left:0;right:0;bottom:0;height:18px;background:var(--pink)}
/* content slide */
.c{position:absolute;top:150px;left:72px;right:72px;bottom:130px;display:flex;flex-direction:column}
.tag{display:inline-block;align-self:flex-start;font-family:Dela;font-size:34px;background:var(--pink);color:#fff;padding:10px 24px;border-radius:12px;transform:rotate(-2deg)}
.wordrow{display:flex;align-items:center;gap:36px;margin-top:34px}
.word{font-family:Brush;font-size:300px;line-height:1;position:relative}
.word.long{font-size:210px}
.x{position:absolute;right:-30px;top:-20px;width:110px;height:110px;border-radius:50%;background:var(--pink);color:#fff;font-family:Archivo;font-size:70px;
  display:flex;align-items:center;justify-content:center;transform:rotate(12deg);box-shadow:6px 6px 0 var(--ink)}
.romaji{font-family:Dela;font-size:52px;margin-top:8px}
.mean{font-family:NotoJP;font-weight:900;font-size:44px;margin-top:6px}
.mean span{background:var(--yellow);padding:0 10px}
.desc{font-weight:700;font-size:42px;line-height:1.45;margin-top:34px}
.meter{display:flex;align-items:center;gap:18px;margin-top:30px;font-family:Archivo;font-size:30px}
.meter i{display:inline-block;width:62px;height:30px;border-radius:8px;border:4px solid var(--ink);background:#fff}
.meter i.on{background:var(--pink)}
.say{margin-top:auto;background:var(--green2);border:5px solid var(--green);border-radius:28px;padding:30px 36px;display:flex;align-items:center;gap:28px;box-shadow:10px 10px 0 var(--ink)}
.say .ok{flex:none;width:92px;height:92px;border-radius:50%;background:var(--green);color:#fff;font-family:Archivo;font-size:58px;display:flex;align-items:center;justify-content:center}
.say small{display:block;font-family:Archivo;font-size:28px;color:var(--green);letter-spacing:1px}
.say b{font-family:NotoJP;font-weight:900;font-size:60px}
.say em{font-style:normal;font-weight:700;font-size:34px;color:#333;margin-left:8px}
.no{margin-top:auto;background:var(--ink);color:#fff;border-radius:28px;padding:34px 38px;font-family:Dela;font-size:52px;box-shadow:10px 10px 0 var(--pink)}
.no small{display:block;font-family:NotoJP;font-weight:700;font-size:34px;color:#ffb3cb;margin-top:10px}
"""


def frame(n, inner, swipe=True, extra=""):
    sw = '<span class="swipe">SWIPE →</span>' if swipe else '<span></span>'
    return f"""<section class="slide" id="s{n}">{extra}<div class="dots"></div>
<div class="top"><div class="handle"><b>@</b>raj_in_jp</div><div class="pg">{n}/{TOTAL}</div></div>
{inner}
<div class="bottom"><span>ANIME vs REAL LIFE</span>{sw}</div><div class="bar"></div></section>"""


def meter(label, n):
    cells = "".join(f'<i class="{"on" if k < n else ""}"></i>' for k in range(5))
    return f'<div class="meter">{label} {cells}</div>'


def word_slide(n, word, romaji, meaning, desc, mlabel, mval, say=None, say_note="", never=None, long=False):
    if say:
        bottom = f'<div class="say"><div class="ok">✓</div><div><small>SAY THIS INSTEAD</small><b>{say}</b><em>{say_note}</em></div></div>'
    else:
        bottom = f'<div class="no">{never[0]}<small>{never[1]}</small></div>'
    inner = f"""<div class="c">
<div class="tag">ANIME ONLY ✕</div>
<div class="wordrow"><div class="word{' long' if long else ''}">{word}<div class="x">✕</div></div></div>
<div class="romaji">{romaji}</div>
<div class="mean"><span>{meaning}</span></div>
<div class="desc">{desc}</div>
{meter(mlabel, mval)}
{bottom}
</div>"""
    return frame(n, inner)


slides = []

# 1 COVER
cov = img("cover.png")
cover_img = (f'<img src="{cov}" style="position:absolute;right:-20px;bottom:110px;height:640px;z-index:2">' if cov else
             '<div style="position:absolute;right:50px;bottom:150px;z-index:2;transform:rotate(6deg)">'
             '<div style="background:#fff;border:8px solid #141414;border-radius:56px;padding:22px 44px 30px;font-family:Brush;font-size:135px;line-height:1;box-shadow:14px 14px 0 #E8175D">お前！</div>'
             '<div style="width:0;height:0;border-left:36px solid transparent;border-right:36px solid transparent;border-top:60px solid #141414;margin-left:80px"></div></div>')
slides.append(f"""<section class="slide" id="s1">
<div style="position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 85% 70%,rgba(232,23,93,.10) 0deg 6deg,transparent 6deg 14deg)"></div>
<div class="top"><div class="handle"><b>@</b>raj_in_jp</div><div class="pg">1/{TOTAL}</div></div>
<div style="position:absolute;top:165px;left:120px;right:120px;z-index:3">
  <div class="tag" style="font-size:36px">ANIME vs REAL LIFE</div>
  <div style="font-family:Dela;font-size:104px;line-height:1.04;margin-top:30px">ANIME<br>JAPANESE<br>THAT GETS<br>YOU</div>
  <div style="display:inline-block;font-family:Dela;font-size:176px;line-height:1;color:#fff;background:var(--pink);padding:6px 34px 18px;margin-top:18px;transform:rotate(-4deg);box-shadow:12px 12px 0 var(--ink)">FIRED</div>
</div>
{cover_img}
<div style="position:absolute;left:120px;bottom:170px;z-index:3;font-weight:900;font-size:42px;line-height:1.4">Fine on screen.<br><span style="background:var(--yellow);padding:0 10px">Rude in real life.</span></div>
<div class="bottom"><span></span><span class="swipe">SWIPE →</span></div><div class="bar"></div></section>""")

# 2 STAKE
st = img("stake.png")
stake_visual = (f'<img src="{st}" style="width:100%;height:560px;object-fit:cover;border-radius:28px;border:6px solid #141414;margin-top:auto;box-shadow:12px 12px 0 #E8175D">' if st else
                '<div style="margin-top:auto;display:flex;gap:28px;align-items:stretch">'
                '<div style="flex:1;background:#fff;border:6px solid #141414;border-radius:28px;padding:34px;box-shadow:10px 10px 0 #E8175D">'
                '<div style="font-family:Archivo;font-size:30px;color:#E8175D">YOU, TO YOUR BOSS</div>'
                '<div style="font-family:Brush;font-size:118px;line-height:1.2;margin-top:24px;white-space:nowrap">おい、<br>お前！</div></div>'
                '<div style="flex:1;background:#141414;color:#fff;border-radius:28px;padding:34px;box-shadow:10px 10px 0 #E8175D">'
                '<div style="font-family:Archivo;font-size:30px;color:#FFD23F">YOUR BOSS</div>'
                '<div style="font-size:150px;line-height:1.1;margin-top:20px">😨</div>'
                '<div class="jp" style="font-size:56px;margin-top:10px">…はい？</div></div></div>')
slides.append(frame(2, f"""<div class="c">
<div style="font-family:Dela;font-size:78px;line-height:1.15;margin-top:30px">Anime taught you<br>Japanese.</div>
<div style="font-family:Dela;font-size:78px;line-height:1.15;margin-top:24px">It also taught you<br>to <span style="color:var(--pink)">insult your<br>boss.</span></div>
{stake_visual}
</div>"""))

# 3-8 words
slides.append(word_slide(3, "お前", "omae", '= "you"',
    "Every anime rival says it. Between close friends it's fine. To anyone above you, it's rude.",
    "RUDENESS", 3, say="名前 + さん", say_note="their name + san"))
slides.append(word_slide(4, "てめえ", "temee", '= a rougher "you"',
    "This is how anime characters talk right before a fight. In real life, these are fighting words too.",
    "RUDENESS", 5, never=("Just don't. ✕", "No polite version. Use their name + さん."), long=True))
slides.append(word_slide(5, "貴様", "kisama", '= "you"',
    "Centuries ago it was respectful. Today it sounds like pure hate. Villains love it.",
    "RUDENESS", 5, say="名前 + さん", say_note="their name + san"))
slides.append(word_slide(6, "俺様", "oresama", '= "I, the great one"',
    "Pure anime ego. Say it at work and you're the joke of the office.",
    "RUDENESS", 4, say="私", say_note="watashi"))
slides.append(word_slide(7, "だぜ", "daze", "= tough-guy ending",
    "Sounds cool in a shounen fight. At a shop counter it sounds like you're doing a bad impression.",
    "CRINGE", 4, say="です", say_note="desu"))
slides.append(word_slide(8, "拙者", "sessha · <span class='jp' style='font-weight:700'>でござる</span>", "= samurai speech",
    "Straight out of a samurai anime. Use it in real life and people will laugh, kindly but loudly.",
    "CRINGE", 5, say="私 · です", say_note="watashi · desu"))

# 9 RECAP
rows = [("お前・てめえ・貴様", "名前 + さん"), ("俺様・拙者", "私"), ("だぜ・でござる", "です")]
rows_html = "".join(
    f'<div style="display:flex;align-items:center;gap:22px;margin-top:44px">'
    f'<div style="flex:1.5;background:var(--pink2);border:5px solid var(--pink);border-radius:22px;padding:38px 22px;font-family:NotoJP;font-weight:900;font-size:40px;white-space:nowrap">✕ {a}</div>'
    f'<div style="font-family:Archivo;font-size:60px">→</div>'
    f'<div style="flex:1;background:var(--green2);border:5px solid var(--green);border-radius:22px;padding:38px 22px;font-family:NotoJP;font-weight:900;font-size:42px">✓ {b}</div></div>'
    for a, b in rows)
slides.append(frame(9, f"""<div class="c">
<div class="tag" style="background:var(--ink)">SCREENSHOT THIS 📸</div>
<div style="font-family:Dela;font-size:76px;line-height:1.1;margin-top:34px">The cheat sheet</div>
<div style="display:flex;gap:22px;margin-top:36px;font-family:Archivo;font-size:32px"><div style="flex:1.5;color:var(--pink)">ANIME</div><div style="width:60px"></div><div style="flex:1;color:var(--green)">REAL LIFE</div></div>
{rows_html}
<div style="margin-top:auto;font-weight:900;font-size:40px;line-height:1.4">Not sure? <span style="background:var(--yellow);padding:0 10px">Name + さん and です</span> are always safe.</div>
</div>"""))

# 10 CTA
slides.append(f"""<section class="slide" id="s10" style="background:var(--pink);color:#fff">
<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.18) 3px,transparent 3.5px);background-size:28px 28px"></div>
<div class="top"><div class="handle" style="color:#fff">@raj_in_jp</div><div class="pg" style="background:#fff;color:var(--pink)">{TOTAL}/{TOTAL}</div></div>
<div style="position:absolute;top:230px;left:96px;right:96px;z-index:3;text-align:center">
  <div style="font-size:170px;line-height:1">📩</div>
  <div style="font-family:Dela;font-size:92px;line-height:1.12;margin-top:40px">Send this to<br>your anime<br>friend</div>
  <div style="font-weight:900;font-size:46px;margin-top:34px">before they visit Japan.</div>
  <div style="display:inline-block;margin-top:70px;background:#fff;color:var(--ink);border-radius:999px;padding:24px 46px;font-family:Archivo;font-size:40px;box-shadow:10px 10px 0 var(--ink)">More real Japanese → <span style="color:var(--pink)">@raj_in_jp</span></div>
</div>
<div class="bottom" style="color:#fff"><span>ANIME vs REAL LIFE</span><span>ANIME HUB</span></div>
<div class="bar" style="background:var(--ink)"></div></section>""")

with open(os.path.join(HERE, "slides.html"), "w") as f:
    f.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(slides)}</body></html>")
print("wrote slides.html", len(slides), "slides")
