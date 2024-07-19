import ctypes
from PIL import Image, ImageFont, ImageDraw
import random
from datetime import date
import textwrap

today = date.today()
print("today's date: ", today.month, "/", today.day)

quoteFile = open("C:\\Users\\Ex Voce\\source\\repos\\PythonApplication1\\PythonApplication1\\newQuoteFile.txt", "r", encoding="utf8")
'''newQFile = open("C:\\Users\\Ex Voce\\source\\repos\\PythonApplication1\\PythonApplication1\\editedQuoteFile.txt", "w")
ogTextList = quoteFile.readlines()
oneLiner = ""
for line in ogTextList:
    #oneLiner = oneLiner+line.removesuffix("\n") + " "
    if "/" in line:
        oneLiner = oneLiner+"\n"+line.removesuffix("\n") + " "
    else:
        oneLiner = oneLiner+line.removesuffix("\n") + " "

newQFile.write(oneLiner)'''

#this works for finding the day's quote
quoteList = quoteFile.readlines()
todaysQuote = [s for s in quoteList if str(today.month) + "/" + str(today.day) in s]
print(todaysQuote[0])
quoteFile.close()

#figure out a good range for colors
bgColor = (random.randrange(230,250), random.randrange(200,230), random.randrange(190,230))
fontColor = (random.randrange(0,130), random.randrange(0,130), random.randrange(0,130))

txt = todaysQuote[0]
withoutDate = txt[txt.index("- ")+2:]
wrappedTxt = textwrap.wrap(withoutDate, width=53, break_long_words = False)
wrappedTxt.append("\n")
wrappedTxt.append("Manly P. Hall")
#Maybe: create a variable height based on the number of lines of text?
imgWidth, imgHeight = 1000, 200
imgHeight+=(len(wrappedTxt)*50)
image = Image.new('RGB',(imgWidth, imgHeight), color=bgColor)
fontsize = 5
img_fraction = 0.9
thefont = ImageFont.truetype("C:\\Users\\Ex Voce\\Desktop\\LibreBodoni.ttf", fontsize)

longestLineNum = 0
for line in range(0, len(wrappedTxt)):
    if thefont.getlength(wrappedTxt[line])>thefont.getlength(wrappedTxt[longestLineNum]):
        longestLineNum = line
#print("longest line is " +str(longestLineNum))

#adjust font size based on longest line
while thefont.getlength(wrappedTxt[longestLineNum]) < img_fraction*image.size[0]:
    fontsize += 1
    thefont = ImageFont.truetype("C:\\Users\\Ex Voce\\Desktop\\LibreBodoni.ttf", fontsize)

#fontsize -= 0
#print (fontsize)
finalFont = ImageFont.truetype("C:\\Users\\Ex Voce\\Desktop\\LibreBodoni.ttf", fontsize)
draw = ImageDraw.Draw(image) #create the base png

#center this stuff
#find starting verticle point
txtPad = 2
totalTextHeight = 0
multiplier = (finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3]+txtPad)*(len(wrappedTxt))
'''for line in range(0, len(wrappedTxt)):
    totalTextHeight += (finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3]+txtPad)
#totalTextHeight+=finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3]+txtPad'''
vertSpacing = (imgHeight-multiplier)/2
#print("top spacing: " + str(vertSpacing) + " multiplier: " + str((imgHeight-multiplier)/2- (txtPad*len(wrappedTxt))))
#for each line of the quote, draw it beneath the last
for line in range(0, len(wrappedTxt)):
    draw.text(((imgWidth-finalFont.getbbox(wrappedTxt[line])[2])/2,vertSpacing), text=wrappedTxt[line], fill=fontColor, font=finalFont)
    vertSpacing += (finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3]+txtPad)
#print("bottom spacing: " + str(imgHeight - vertSpacing))#(vertSpacing-txtPad + finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3])))
#save the new image as a png
image.save("txt2png.png")

#change wallpaper to new image
wallpaperPath = "C:\\Users\\Ex Voce\\source\\repos\\PythonApplication1\\PythonApplication1\\txt2png.png"
ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaperPath, 3)
print("changedTxt")