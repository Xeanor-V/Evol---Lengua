from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageDraw, ImageColor, ImageTk
import tkMessageBox
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import math

root = Tk()
root.geometry('{}x{}'.format(1215, 680))
	
Ba = 1
Bb = 1
Sa = 1
Sb = 1

name_of_colors = ["black", "white", "mediumvioletred", "midnightblue", "mediumblue", "forestgreen", "yellow", "orange", "red"]

currconfV = [[]]

cellsizeV = 1
sval = 1

highV = 1
wideV = 1
	
dir_x = [1, 1, 1, 0, 0, -1, -1, -1, 0]
dir_y = [1, 0, -1, 1, -1, 1, 0, -1, 0]

datavalidated = 0

running = 0

def Showcells():
	global highV, wideV, Ba, Bb, Sa, Sb, currconfV, cellsizeV, sval
	#print currconfV
	caGrid.delete("all")
	image1 = Image.new("RGB", (wideV * (cellsizeV + sval), highV * (cellsizeV + sval)), (255, 255, 255))
	imagename = "RuleB{0}{1}_S{2}{3}img.png".format(Ba, Bb, Sa, Sb)
	draw = ImageDraw.Draw(image1)
	viewyv = 0.0
	dval = 0
	if (cellsizeV != 0):
		dval = 1
	for i in range(highV):
		for j in range(wideV):
			#if (currconfV[i][j] == 1):
			draw.setfill(1)
			draw.rectangle([(j * (cellsizeV + sval)), (i * (cellsizeV + sval)), ((j + 1) * (cellsizeV + sval)) - 1 - dval, ((i + 1) * (cellsizeV + sval)) - 1 - dval], fill = name_of_colors[currconfV[i][j] + 1])
	caGrid.delete("all")
	image1.save(imagename)
	imm = ImageTk.PhotoImage(file = './'+imagename)
	label = Label(image=imm)
	label.image = imm
	
	caGrid.create_image(0, 0, image = imm)
	caGrid.configure(scrollregion = caGrid.bbox('all'))
	if ((i % 150 == 0) and (i > 150)):
		viewyv += float(300.0 / float(generationsV * 2))
	caGrid.yview_moveto(viewyv)
	caGrid.update_idletasks()

def ValidData():
	global Ba, Bb, Sa, Sb, wideV, highV, currconfV, cellsizeV, sval, datavalidated
	print "Random Generated Initial Configuration: ", randomIniConfV.get()
	print "Rule: ", ruleEntry.get()
	print "High: ", highEntry.get()
	print "Wide Size: ", wideEntry.get()
	print "Random Percentage: ", randomPercentageEntry.get()
	print "Cell Size: ", cellsizeEntry.get()
		
	try:
		wideV = int(wideEntry.get())
		if (not(wideV > 0)):
			raise
	except:
		tkMessageBox.showinfo("Invalid Data", "Wide Value must be a positive integer")
		return False

	try:
		highV = int(highEntry.get())
		if (not(highV > 0)):
			raise
	except:
		tkMessageBox.showinfo("Invalid Data", "High Value must be a positive integer")
		return False
	
	try:
		cellsizeV = int(cellsizeEntry.get())
		if (not(cellsizeV >= 0)):
			raise
		sval = 2
		if (cellsizeV == 0):
			sval = 1 
	except:
		tkMessageBox.showinfo("Invalid Data", "CellSize Value must be a non-negative integer")
		return False
	
	currconfV = [[0 for i in range(wideV)] for j in range(highV)]
	
	for i in xrange(wideV):
		currconfV[0][i] = -1
		currconfV[highV - 1][i] = -1
	for i in xrange(highV):
		currconfV[i][0] = -1
		currconfV[i][wideV - 1] = -1
	
	if (randomIniConfV.get() == 1):
		try:
			randomPercentageV = float(randomPercentageEntry.get())
			if (not((randomPercentageV >= 0.0) and (randomPercentageV <= 100.0))):
				raise
			manyOnes = int((randomPercentageV * float(wideV * highV)) / 100.0)
			print 'From {0} cells {1} will start alive'.format(wideV * highV, manyOnes)
			while (manyOnes):
				pos = random.randint(1, (wideV * highV) - 2)
				xi = pos % wideV
				yi = pos / wideV
				while (currconfV[yi][xi] != 0):
					pos = random.randint(1, (wideV * highV) - 2)
					xi = pos % wideV
					yi = pos / wideV					
				currconfV[yi][xi] = random.randint(2, len(name_of_colors) - 2)
				manyOnes -= 1
		except:
			tkMessageBox.showinfo("Invalid Data", "Random Percentage Value must be a real value between 0.0 and 100.0")
			return False
	datavalidated = 1
	Showcells()
	return True

def AddCell(event):
	global wideV, highV, currconfV, cellsizeV, sval
	nx = event.x / (cellsizeV + sval)
	ny = event.y / (cellsizeV + sval)
	if ((ny < 0) or (ny >= highV) or (nx < 0) or (nx >= wideV)):
		return
	currconfV[ny][nx] = 1
	Showcells()

def SubCell(event):
	global wideV, highV, currconfV, cellsizeV, sval
	nx = event.x / (cellsizeV + sval)
	ny = event.y / (cellsizeV + sval)
	if ((ny < 0) or (ny >= highV) or (nx < 0) or (nx >= wideV)):
		return
	currconfV[ny][nx] = 1
	Showcells()
	
def CountNeighbors(yi, xi):
	global currconfV, wideV, highV, dir_x, dir_y
	res = 0
	Colors = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	manywc = 0.0
	for i in range(9):
		nx = (xi + dir_x[i] + wideV) % wideV
		ny = (yi + dir_y[i] + highV) % highV
		if (currconfV[ny][nx] > 0):
			Colors[ currconfV[ny][nx] - 1 ] += 1.0
			manywc += 1.0
	
	if (manywc == 0.0):
		return 0
	
	##Calcular % del color
	max1 = -1.0
	max2 = -1.0
	maxidx1 = 0
	maxidx2 = 0
	for i in xrange(len(Colors)):
		Colors[i] = Colors[i] / manywc
		if((Colors[i] > max1) and (Colors[i] != 0.0)):
			maxidx2 = maxidx1
			max2 = max1
			max1 = Colors[i]
			maxidx1 = i + 1
		elif ((Colors[i] > max2) and (Colors[i] != 0.0)):
			maxidx2 = i + 1
			max2 = Colors[i]
	
	if(max1 == -1.0):
		return 0

	#print Colors
	#print "{0} {1}".format(maxidx1, maxidx2)
		
	if(currconfV[xi][yi] == 0):
		return maxidx1
	if((currconfV[xi][yi] == maxidx1) and (max1 >= 0.5)):
		return maxidx1
	if(max1 >= 0.5):
		return maxidx1

	return int(math.ceil( float(maxidx1 + maxidx2) / 2.0))
	
def CalcNewState():
	global Ba, Bb, Sa, Sb, currconfV, wideV, highV
	tmp = [[0 for i in range(wideV)] for j in range(highV)]
	for i in range(highV):
		for j in range(wideV):
			if currconfV[i][j] == -1:
				tmp[i][j] = -1
				continue
			tmp[i][j] = CountNeighbors(i, j)
	currconfV = tmp

def Process():
	global running
	if (running):
		CalcNewState()
		Showcells()	
	root.after(100, Process)
	
def runCallBack():
	global datavalidated, running, currconfV
	if (datavalidated == 0):
		if (not(ValidData())):
			return
	running = True

def stopCallBack():
	global running
	running = False;

dataButton = Button(root, text = " RUN ", command = runCallBack)
dataButton.grid(row = 0,column = 0)

dataButton = Button(root, text = "STOP", command = stopCallBack)
dataButton.grid(row = 1,column = 0)

highLabel = Label(root, text = "High: ")
highLabel.grid(row = 0, column = 1)

highEntry = Entry(root, width = 15)
highEntry.grid(row = 0, column = 2)

wideLabel = Label(root, text = "Wide: ")
wideLabel.grid(row = 1, column = 1)

wideEntry = Entry(root, width = 15)
wideEntry.grid(row = 1, column = 2)

ruleLabel = Label(root, text = "Rule: ")
ruleLabel.grid(row = 0, column = 4)

ruleEntry = Entry(root, width = 15)
ruleEntry.grid(row = 0, column = 5)

dataButton = Button(root, text = "Read Data", command = ValidData)
dataButton.grid(row = 0,column = 3)

randomIniConfV = IntVar()
randomIniConfCheck = Checkbutton(root, text = "Random Generated Initial Configuration", variable = randomIniConfV)
randomIniConfCheck.grid(row = 1, column = 3)

randomPsercentageLabel = Label(root, text = "Random Percentage: ")
randomPsercentageLabel.grid(row = 1, column = 4)

randomPercentageEntry = Entry(root, width = 15)
randomPercentageEntry.grid(row = 1, column = 5)

cellsizeLabel = Label(root, text = "Cell Size (Px): ")
cellsizeLabel.grid(row = 1, column = 6)

cellsizeEntry = Entry(root, width = 15)
cellsizeEntry.grid(row = 1, column = 7)

caGrid = Canvas(root, width = 1100, height = 600, background = "gray")

vbar = Scrollbar(root, orient = VERTICAL)
vbar.config(command = caGrid.yview)

hbar = Scrollbar(root, orient = HORIZONTAL)
hbar.config(command = caGrid.xview)
	
caGrid.grid(columnspan = 7, sticky = W)
caGrid.config(yscrollcommand = vbar.set, xscrollcommand = hbar.set)
vbar.grid(row = 2, column = 7, sticky = 'ns')
hbar.grid(row = 3, columnspan = 7, sticky = 'ew')

caGrid.bind("<Button 1>", AddCell)
caGrid.bind("<Button 3>", SubCell)

Process()

root.mainloop()
