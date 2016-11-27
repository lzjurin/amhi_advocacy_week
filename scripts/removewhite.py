from PIL import Image
import sys

path = sys.argv[1]

img = Image.open(path)
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == item[1] == item[2]:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save(path, path.split('.')[-1].upper())
