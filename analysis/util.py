import numpy as np
from PIL import Image
from scipy import ndimage

def load(p):
    im = Image.open(p).convert('RGB')
    a = np.asarray(im).astype(np.float32)/255.0
    return im, a

def hsv(a):
    mx=a.max(2); mn=a.min(2); v=mx
    s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    d=mx-mn; h=np.zeros_like(mx); m=(d>1e-6)
    i=m&(mx==r); h[i]=((g-b)[i]/d[i])%6
    i=m&(mx==g); h[i]=((b-r)[i]/d[i])+2
    i=m&(mx==b); h[i]=((r-g)[i]/d[i])+4
    return h*60.0, s, v

def lum(a):
    return 0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]

def crop_zoom(path, box, scale, out):
    im = Image.open(path).convert('RGB')
    c = im.crop(box)
    c = c.resize((int(c.width*scale), int(c.height*scale)), Image.LANCZOS)
    c.save(out)
    return c.size

def crop_zoom_grid(path, box, scale, out, step=10, origin=None, color=(0,255,0)):
    """draw a grid in ORIGINAL pixel coords every `step` px"""
    from PIL import ImageDraw, ImageFont
    im = Image.open(path).convert('RGB')
    c = im.crop(box).resize((int((box[2]-box[0])*scale), int((box[3]-box[1])*scale)), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    x0,y0,x1,y1 = box
    sx = ((x0+step-1)//step)*step
    for X in range(sx, x1, step):
        px = (X-x0)*scale
        major = (X % (step*5)==0)
        d.line([(px,0),(px,c.height)], fill=(255,0,255) if major else color, width=2 if major else 1)
        if major: d.text((px+2,2), str(X), fill=(255,255,0))
    sy = ((y0+step-1)//step)*step
    for Y in range(sy, y1, step):
        py = (Y-y0)*scale
        major = (Y % (step*5)==0)
        d.line([(0,py),(c.width,py)], fill=(255,0,255) if major else color, width=2 if major else 1)
        if major: d.text((2,py+2), str(Y), fill=(255,255,0))
    c.save(out)
    return c.size
