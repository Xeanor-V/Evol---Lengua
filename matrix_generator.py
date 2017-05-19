from PIL import Image
im = Image.open("mapa.bmp")
pix = im.load()
mtr = []
for i in xrange(im.size[0]):
	tmp = []
	for j in xrange(im.size[1]):
		if (pix[i, j] == 255):
			tmp.append(0)
		else:
			tmp.append(-1)
	mtr.append(tmp)
print mtr;
