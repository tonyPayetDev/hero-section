#!/usr/bin/env python3
# Computes the timeline CFG (scene cuts + word-timed captions) from the real
# voice.mp3 and injects it into index.template.html -> public/index.html.
import subprocess, re, os, json, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(HERE, "public/assets/voice.mp3")
TPL   = os.path.join(HERE, "public/index.template.html")
OUT   = os.path.join(HERE, "public/index.html")

def dur(path):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","csv=p=0",path]).decode().strip())

D_AUDIO = dur(VOICE)

def speech_span(path, d):
    p = subprocess.run(["ffmpeg","-i",path,"-af","silencedetect=noise=-40dB:d=0.18",
                        "-f","null","-"], capture_output=True, text=True)
    log = p.stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends   = [float(x) for x in re.findall(r"silence_end: ([-\d.]+)", log)]
    onset = 0.0
    if starts and starts[0] < 0.6 and ends:
        onset = ends[0]
    offset = d
    if starts and starts[-1] > d*0.6:
        offset = starts[-1]
    anchors=[]
    for i,s in enumerate(starts):
        e = ends[i] if i < len(ends) else d
        anchors.append((s+e)/2.0)
    return onset, offset, anchors

ONSET, OFFSET, ANCHORS = speech_span(VOICE, D_AUDIO)
SPEECH = OFFSET - ONSET

NARRATION = ("Ta boutique Shopify perd des ventes chaque nuit sans que tu le saches. "
"Un client remplit son panier, ferme l'onglet, et personne ne le relance. "
"J'ai construit un workflow n8n qui repere les paniers abandonnes en temps reel, "
"et envoie un message automatique apres vingt minutes, avec un code promo limite dans le temps. "
"Chez un client reunionnais, ca a recupere plusieurs commandes qui partaient droit chez un concurrent. "
"Le meme scenario t'alerte aussi quand un produit passe sous cinq unites en stock, "
"pour ne jamais tomber en rupture en pleine promo. Deux problemes regles d'un coup. "
"Commente le mot SHOPIFY et je t'envoie le workflow complet.")

raw = NARRATION.split()
words=[]
for w in raw:
    if not re.search(r"[\wàâäéèêëïîôöùûüç]", w):
        if words:
            words[-1]["pause"]=max(words[-1]["pause"], 3.5 if w in (":","?","!") else 2.0)
        continue
    pause=0.0
    if w.endswith(('.', '!', '?')): pause=4.0
    elif w.endswith(','): pause=2.0
    elif w.endswith(':'): pause=3.0
    words.append({"w":w,"pause":pause})

for it in words:
    clean=re.sub(r"[^\wàâäéèêëïîôöùûüç']","",it["w"],flags=re.I)
    it["wt"]=max(2.2,len(clean))+it["pause"]

tw=sum(it["wt"] for it in words)
t=ONSET
for it in words:
    it["start"]=t; t+=SPEECH*it["wt"]/tw; it["end"]=t

def snap(tt):
    if not ANCHORS: return tt
    b=min(ANCHORS,key=lambda a:abs(a-tt))
    return b if abs(b-tt)<0.45 else tt

def norm(s):
    s=unicodedata.normalize("NFKD",s.lower())
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^\w]","",s)

def idx_of(marker,after=0):
    for i in range(after,len(words)):
        if norm(words[i]["w"])==marker: return i
    return None

i_jai   = idx_of("jai")       # scene 2 : "J'ai construit un workflow..."
i_chez  = idx_of("chez")      # scene 3 : "Chez un client reunionnais..."
i_meme  = idx_of("meme")      # broll   : "Le meme scenario t'alerte aussi..."
i_quand = idx_of("quand")     # scene 4 : "...quand un produit passe sous cinq unites..."
i_deux  = idx_of("deux")      # scene 5 : "Deux problemes regles... Commente le mot SHOPIFY"

S2=round(snap(words[i_jai]["start"]),2)
S3=round(snap(words[i_chez]["start"]),2)
BROLL=round(snap(words[i_meme]["start"]),2)
S4=round(snap(words[i_quand]["start"]),2)
if S4-BROLL < 1.5:            # keep the broll a real ~1.6s beat, not a flash
    S4=round(BROLL+1.7,2)
S5=round(snap(words[i_deux]["start"]),2)
DURC=round(D_AUDIO+0.55,2)

# captions
HOTMAP={"shopify":"hot","nuit":"ohot","panier":"hot","relance":"vhot",
 "workflow":"hot","paniers":"hot","abandonnes":"ohot","reel":"hot",
 "automatique":"vhot","minutes":"hot","promo":"ohot","reunionnais":"vhot",
 "commandes":"hot","concurrent":"ohot","scenario":"vhot","alerte":"hot",
 "stock":"hot","cinq":"hot","rupture":"ohot","deux":"ohot",
 "complet":"hot","recupere":"vhot"}
def up(s): return s.upper()
caps=[]; cur=[]; curchars=0
def flush():
    global cur,curchars
    if not cur: return
    txt=" ".join(up(x["w"].rstrip('.,?!:')) for x in cur)
    tag=""
    for x in cur:
        c=norm(x["w"])
        if c in HOTMAP:
            tag=HOTMAP[c]+":"+up(x["w"].rstrip('.,?!:')); break
    caps.append([round(cur[0]["start"],2),txt,tag]); cur=[]; curchars=0
for it in words:
    wtxt=up(it["w"].rstrip('.,?!:'))
    if cur and (len(cur)>=3 or curchars+1+len(wtxt)>21): flush()
    cur.append(it); curchars+=(1 if curchars else 0)+len(wtxt)
    if it["pause"]>=3.0: flush()
flush()

CFG={"dur":DURC,"audio":round(D_AUDIO,2),"onset":round(ONSET,2),"offset":round(OFFSET,2),
     "cuts":{"s1":0.0,"s2":S2,"s3":S3,"broll":BROLL,"s4":S4,"s5":S5},
     "capEnd":round(OFFSET,2),"caps":caps}
print("CFG",json.dumps(CFG,ensure_ascii=False))

# --- SFX audio block (palette v1 roles re-timed on THIS video's cuts) --------
sfx=[]
def add(i,f,ts,v): sfx.append((i,f,round(max(0.0,ts),2),v))
o=ONSET
add("sfx-hook","sfx-glitch-hard.mp3",o+0.05,0.26)
add("sfx-hook-imp","sfx-impact.mp3",o+0.05,0.20)
for k,c in enumerate([S2,S3,BROLL,S4,S5]):
    add("sfx-zoom-%d"%(k+1),"sfx-zoom.mp3",c-1.2,0.18)
add("sfx-click-1","sfx-click.mp3",S2+0.12,0.18)
add("sfx-click-2","sfx-click.mp3",S3+0.12,0.18)
add("sfx-click-3","sfx-click.mp3",S4+0.12,0.18)
add("sfx-verdict","sfx-notify.mp3",max(o+3.0,S2-1.0),0.16)
add("sfx-o1","sfx-click-soft.mp3",S2+1.55,0.13)
add("sfx-o2","sfx-click-soft.mp3",S2+1.80,0.13)
add("sfx-o3","sfx-click-soft.mp3",S2+2.05,0.13)
add("sfx-valid","sfx-confirm.mp3",S3+1.35,0.18)
add("sfx-strike-1","sfx-whoosh-lat.mp3",S3+2.15,0.14)
add("sfx-strike-2","sfx-whoosh-lat.mp3",S3+2.45,0.14)
add("sfx-r1","sfx-click-soft.mp3",S4+0.50,0.13)
add("sfx-r2","sfx-click-soft.mp3",S4+0.80,0.13)
add("sfx-r3","sfx-click-soft.mp3",S4+1.10,0.13)
add("sfx-limit","sfx-notify.mp3",S5+0.25,0.16)
CTAW=round(S5+1.7,2)
add("sfx-cta-pop","sfx-pop.mp3",CTAW,0.24)
add("sfx-cta-imp","sfx-impact.mp3",CTAW,0.18)
add("sfx-cta-sub","sfx-click-soft.mp3",CTAW+1.3,0.13)

audio_lines=[]
audio_lines.append('  <audio id="voice" src="assets/voice.mp3" data-start="0" data-duration="%s" data-volume="1"></audio>'%round(D_AUDIO,2))
audio_lines.append('  <audio id="bgm" src="assets/flowers_horror.mp3" data-start="0" data-duration="%s" data-volume="0.05"></audio>'%DURC)
for i,f,ts,v in sfx:
    audio_lines.append('  <audio id="%s" src="assets/%s" data-start="%s" data-volume="%s"></audio>'%(i,f,ts,v))
AUDIO_BLOCK="\n".join(audio_lines)

BROLL_DUR=round(S4-BROLL,2)

tpl=open(TPL,encoding="utf-8").read()
tpl=(tpl.replace("__CFG_JSON__", json.dumps(CFG,ensure_ascii=False))
        .replace("__AUDIO_BLOCK__", AUDIO_BLOCK)
        .replace("__DUR__", str(DURC))
        .replace("__BROLL_START__", str(BROLL))
        .replace("__BROLL_DUR__", str(BROLL_DUR)))
open(OUT,"w",encoding="utf-8").write(tpl)
print("WROTE",OUT,"cuts",CFG["cuts"],"ncaps",len(caps),"nsfx",len(sfx),"ctaw",CTAW)
