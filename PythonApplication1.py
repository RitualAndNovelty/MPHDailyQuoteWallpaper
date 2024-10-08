import ctypes
from PIL import Image, ImageFont, ImageDraw
import random
from datetime import date
import textwrap
from pathlib import Path

today = date.today()
quoteFile = open(str(Path.cwd())+"\\newQuoteFile.txt", "r", encoding="utf8")

#find the day's quote
quoteList = quoteFile.readlines()
todaysQuote = [s for s in quoteList if str(today.month) + "/" + str(today.day) in s]
quoteFile.close()

#determine background and font colors/establish typecase
r, g, b = random.randrange(230,250), random.randrange(200,230), random.randrange(190,230)
bgColor = (r, g, b)
fontColor = (r-100, g-100, b-100)
fontFile = str(Path.cwd())+"\\LibreBodoni.ttf"

#get today's quote and append the attribution
txt = todaysQuote[0]
withoutDate = txt[txt.index("- ")+2:]
wrappedTxt = textwrap.wrap(withoutDate, width=53, break_long_words = False)
wrappedTxt.append("\n")
wrappedTxt.append("Manly P. Hall")

#create the image to hold the quote
imgWidth, imgHeight = 1000, 200
imgHeight+=(len(wrappedTxt)*50)
image = Image.new('RGB',(imgWidth, imgHeight), color=bgColor)
fontsize = 5
img_fraction = 0.9
thefont = ImageFont.truetype(fontFile, fontsize)

#adjust font size based on longest line
longestLineNum = 0
for line in range(0, len(wrappedTxt)):
    if thefont.getlength(wrappedTxt[line])>thefont.getlength(wrappedTxt[longestLineNum]):
        longestLineNum = line

while thefont.getlength(wrappedTxt[longestLineNum]) < img_fraction*image.size[0]:
    fontsize += 1
    thefont = ImageFont.truetype(fontFile, fontsize)
finalFont = ImageFont.truetype(fontFile, fontsize)

#create the base png
draw = ImageDraw.Draw(image) 

#find starting verticle point and for each line of the quote, draw it beneath the last, adjusting its horizontal position to center
txtPad = 2
totalTextHeight = 0
multiplier = (finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3]+txtPad)*(len(wrappedTxt))
vertSpacing = (imgHeight-multiplier)/2
for line in range(0, len(wrappedTxt)):
    draw.text(((imgWidth-finalFont.getbbox(wrappedTxt[line])[2])/2,vertSpacing), text=wrappedTxt[line], fill=fontColor, font=finalFont)
    vertSpacing += (finalFont.getbbox(wrappedTxt[len(wrappedTxt)-1])[3]+txtPad)

#save the new image as a png
imgName = "txt2png.png"
finalImg = image.save(imgName)

#change wallpaper to new image
wallpaperPath = str(Path.cwd())+"\\"+imgName
ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaperPath, 3)