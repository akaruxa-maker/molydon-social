import sys; sys.path.insert(0,'.')
from render2 import *
raw=Image.open(SRC/"univ-krovni-raw.jpg").convert("RGB")
sq=raw.crop((0,0,744,744))
img=background("roof-forest",darken_top=0.9,darken_bottom=0.9,bright=0.55,blur=3)
d=ImageDraw.Draw(img); logo(img)
y=headline(d,HEAD_Y,[("NEMA NOSAČA",WHITE),("ZA TVOJ AUTO?",YEL)],size=86)
# foto panel
S=560; ph=sq.resize((S,S),Image.LANCZOS)
x0,y0=W-60-S,y+20
fr=Image.new("RGBA",(S+12,S+12),YEL+(255,)); fm=Image.new("L",(S+12,S+12),0); ImageDraw.Draw(fm).rounded_rectangle((0,0,S+12,S+12),40,fill=255)
img.paste(fr,(x0-6,y0-6),fm)
m=Image.new("L",(S,S),0); ImageDraw.Draw(m).rounded_rectangle((0,0,S,S),36,fill=255); img.paste(ph,(x0,y0),m)
d=ImageDraw.Draw(img)
checklist(d,y+30,["Za stare aute i modele bez nosača","Ravni krov, bez bušenja","Aluminij, 108 cm, nosivost 70 kg","Brava s 2 ključa","Samo auti s 4 vrata"],size=32,maxw=300)
price_badge(img,250,1080,"87,55 €","set 2 šipke","UNIVERZALNI",r=135)
footer(img,cta="POGLEDAJ NA MOLYDON.HR",note="DOSTAVA NA PODRUČJU CIJELE HRVATSKE")
save(img,"/home/claude/molydon-social/media/x-univ-krovni.jpg")
