#This python script generates a list of blocks with values and positions. 
#These blocks can be used to create lego mosaics in blender.
#Data is stored in a csv file.
#The blocks are defined as bitmask values in a 4 by 4 raster.

from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import csv
import math
import random
import sys


im = Image.open(sys.argv[1])
width = int(sys.argv[2])
name = str(sys.argv[1]).split(".")[0]
colours = str(sys.argv[3])

contrast = 1.5
saturation = 2.0

#Predefined blocks
blocks = [1,3,7,15,17,51,255,273,4369,13107,65535]

palette_simple = [
	21,21,21, #black
	100,103,101, #stone grey
	244,244,244, #white
	160,161,159, #Medium Stone Grey
	0,57,94, #earth blue
	0,108,183, #bright blue
	0,153,212, #medium blue
	0,175,77, #bright green
	0,74,45, #dark green
	247,209,18, #yellow
	245,125,32, #bright orange
	166,83,34, #medium nougat
	252,195,158, #light nougat
	221,196,142, #brick yellow
	221,26,33, #bright red
	232,80,156 #medium reddish violet
	]
	
palette_greyscale = [
	21,21,21, #black
	100,103,101, #stone grey
	160,161,159, #Medium Stone Grey
	244,244,244 #white
]

#Lego Color Palette, padded with white for 64 colours
palette_full = [ 
	21,21,21, #black
	100,103,101, #stone grey
	244,244,244, #white
	160,161,159, #Medium Stone Grey
	150,117,180, #medium lavender
	188,166,208, #lavender
	78,47,146, #medium lilac
	0,57,94, #earth blue
	0,108,183, #bright blue
	0,153,212, #medium blue
	120,191,234, #light royal blue
	103,130,151, #sand blue
	0,163,218, #dark azur
	0,190,211, #medium azur
	24,158,159, #bright bluish green
	111,148,122, #sand green
	0,74,45, #earth green
	0,175,77, #bright green
	0,74,45, #dark green
	154,202,60, #bright yellowish green
	204,225,151, #spring yellowish green
	130,131,83, #olive green
	255,205,3, #bright yellow
	247,209,18, #transparent yellow
	255,245,121, #cool yellow
	195,151,55, #warm gold
	249,108,98, #vibrant coral
	245,125,32, #bright orange
	59,24,13, #dark brown
	105,46,20, #reddish brown
	166,83,34, #dark orange
	166,83,34, #medium nougat
	222,139,95, #nougat
	252,195,158, #light nougat
	148,126,95, #sand yellow
	221,196,142, #brick yellow
	127,19,27, #new dark red
	221,26,33, #bright red
	229,30,38, #red
	232,80,156, #medium reddish violet
	181,28,125, #bright reddish violet
	233,93,162, #bright purple
	246,173,205, #light purple
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244, #white
	244,244,244 #white
	]
	
palette_special = [
	#232,80,156, #transparent medium reddish violet
	#229,30,38, #transparent red
	#151,137,108, #transparent brown
	#245,136,48, #transparent bright orange
	#240,87,41, #flourescent reddish orange
	#210,161,42, #warm gold drum laquered
	#224,192,119, #metalized gold
	#0,168,79, #transparent green
	#150,199,83, #transparent bright green
	#227,224,41, #transparent flourescent green
	#227,224,41, #transparent flourescent green glitter
	#251,171,24, #flame yellow orange
	#91,193,191, #light blue with glitter
	#91,193,191, #transparent light blue
	#193,228,218, #aqua
	#0,153,212, #transparent blue
	#132,200,226, #transparent fluorescent blue
	#118,114,181, #bright violet glitter
	#118,114,181, #transparent bright violer
	#119,119,121, #cool silver 
	#135,141,143, #silver metallic
	#205,206,208, #metallized silver
	#66,66,62, #titianium metallic
	#239,239,238, #transparent white
	#239,239,238, #white glitter
]

    
if colours == "full":
	p_img = Image.new('P', (16,16))
	p_img.putpalette(palette_full * 4)
	print("using full palette")

if colours == "greyscale":
	p_img = Image.new('P', (16, 16))
	p_img.putpalette(palette_greyscale * 64)
	print("using greyscale palette")

if colours == "simple":
	p_img = Image.new('P', (16, 16))
	p_img.putpalette(palette_simple * 16)
	print("using simple palette")

	

#getting source width, height and aspect
w, h = im.size
a = h/w

#calculating new height based on width and aspect ratio
height = round(width * a)

#resizing 
im = im.resize((width,height), resample =0)

#increase contrast and saturation
im = ImageEnhance.Contrast(im).enhance(contrast)
im = ImageEnhance.Color(im).enhance(saturation)

#reducing image colors
im = im.quantize(palette=p_img, dither=0)
preview = im

preview = im.resize((w,h), resample = 0)
preview.show()

#Flipping the image horizontal
im = ImageOps.mirror(im)

#readim the image into a list
imVals=list(im.getdata())
image = []
for i in range(0,height):
        pixels = []
        for j in range(i * width, i * width + width):
                pixels.append(imVals[j])
        image.append(pixels)

#Function to create the bitmask value
#returns bitmask and color value as rgb
#-----------------------------------------------------------#
def bitmask(x,y,val):
        #current bitmask
        bitmask = 0 

        for bitH in range(0,4):
                for bitW in range(0,4):
                        if x + bitW < cols and y + bitH < lines:
                                if image[y+bitH][x+bitW]==val and visited[y+bitH][x+bitW] == 0:
                                        bitmask+=int(math.pow(2, bitW + 4 * bitH))

        bitmaskBin = format(bitmask, '016b')

        lastvalidBin = 0
        for block in blocks:
                blockBin = format(block, '016b')
                i = 16
                while i > 0: 
                        i-=1 #increment index by 1 
                        if bitmaskBin[i:].zfill(16) == blockBin:
                                lastvalidBin = blockBin                           
                        
                lastvalidBin = lastvalidBin.zfill(16)

        i=0
        for c in map(int, str(lastvalidBin[::-1])):

                for bitH in range(0,4):
                        for bitW in range(0,4):
                                bit = bitW + 4 * bitH
                                if i == bit and c == 1:
                                        visited[y+bitH][x+bitW] = 1
                i+=1   
        val = str(val)
        val = val.replace('(', "") 
        val = val.replace(')', "") 
        return str(int(lastvalidBin,2)) + str(',') + str(val)
#-----------------------------------------------------------#        
#end of function

#array that marks fields as consumed/ visited
visited = []
#array that holds the data for csv output
placedblocks = []
#height and length of image
lines = len(image)
cols = len(image[0])

#filling arrays with placeholders
for i in image:
        values = []
        for j in i:
                values.append(0)
        visited.append(values)

for i in image:
        values = []
        for j in i:
                values.append(0)
        placedblocks.append(values)

#loop through the image and set the bitmask value for each pixel
y = 0 #current line
for i in image: 
        x = 0 #current column, gets reset every line
        for j in i:
                if visited[y][x]==0:
                        placedblocks[y][x] = bitmask(x,y,j)#call bitmaks on current x and y coordinate    
                x+=1 #increment column by one
        y+=1 #increment line by one
     
#print values for debug purposes
#for i in placedblocks:
        #print(i)

#output file as csv
#only saves coordinates with a valid bitmask value
with open(name+".csv", mode='w') as image_file: #linux
#with open('Drive:/imagefile.csv', mode='wb') as image_file: #windows
        image_writer = csv.writer(image_file, delimiter=',', quotechar ='',escapechar=' ', quoting=csv.QUOTE_NONE)
        y = 0 
        for row in placedblocks:
                x = 0
                for val in row:
                        if val != 0:
                                image_writer.writerow([x,y,val])
                        x+=1
                y+=1
