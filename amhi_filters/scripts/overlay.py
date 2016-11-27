from PIL import Image
from resizeimage import resizeimage
import sys, os

if len(sys.argv) < 4:
    print "python script.py [background] [overlay] [outfile]"
else:
    back, overlay = map(Image.open, sys.argv[1:3])
    back = resizeimage.resize_cover(back, overlay.size)
    back = back.convert('L')
    out = Image.new("RGBA", back.size)
    out.paste(back)
    out.paste(overlay, (0, 0), overlay)
    out.save(sys.argv[3], "PNG")
