import sys, os
from PIL import Image
# usage: crop.py src x0 y0 x1 y1 scale out
src,x0,y0,x1,y1,scale,out = sys.argv[1:8]
im = Image.open(src).convert('RGB')
x0,y0,x1,y1 = map(int,(x0,y0,x1,y1)); scale=float(scale)
c = im.crop((x0,y0,x1,y1))
w,h = c.size
c = c.resize((int(w*scale),int(h*scale)), Image.NEAREST if scale>=4 else Image.LANCZOS)
c.save(out)
print(out, c.size, 'from', (x0,y0,x1,y1), 'scale',scale)
