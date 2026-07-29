import sys, os
from PIL import Image, ImageDraw
slugs = sys.argv[2:]
out = sys.argv[1]
cell, pad, lab = 380, 10, 26
cols = min(3, len(slugs))
rows = (len(slugs)+cols-1)//cols
W = cols*(cell+pad)+pad
H = rows*(cell+lab+pad)+pad
sheet = Image.new("RGB",(W,H),"white")
d = ImageDraw.Draw(sheet)
for i,s in enumerate(slugs):
    p = f"images/{s}.png"
    if not os.path.exists(p): continue
    im = Image.open(p).convert("RGB"); im.thumbnail((cell,cell))
    c,r = i%cols, i//cols
    x = pad+c*(cell+pad); y = pad+r*(cell+lab+pad)
    sheet.paste(im,(x+(cell-im.width)//2, y))
    d.text((x+4, y+cell+6), s, fill="black")
sheet.save(out, quality=90)
print(out, sheet.size)
