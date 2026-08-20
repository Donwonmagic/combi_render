import sys
from PIL import Image, ImageDraw
src, out, x0,y0,x1,y1, S = sys.argv[1], sys.argv[2], *[int(v) for v in sys.argv[3:7]], int(sys.argv[7])
im = Image.open(src).convert('RGB').crop((x0,y0,x1,y1))
im = im.resize(((x1-x0)*S,(y1-y0)*S), Image.LANCZOS)
d = ImageDraw.Draw(im)
step = int(sys.argv[8]) if len(sys.argv)>8 else 10
for x in range(x0 - x0%step, x1+1, step):
    px=(x-x0)*S
    maj = (x%(step*5)==0)
    d.line([(px,0),(px,im.height)], fill=(0,200,255) if maj else (0,120,160), width=2 if maj else 1)
    if maj: d.text((px+2,2), str(x), fill=(0,255,255))
for y in range(y0 - y0%step, y1+1, step):
    py=(y-y0)*S
    maj = (y%(step*5)==0)
    d.line([(0,py),(im.width,py)], fill=(255,0,255) if maj else (150,0,150), width=2 if maj else 1)
    if maj: d.text((2,py+2), str(y), fill=(255,0,255))
im.save(out); print(out, im.size)
