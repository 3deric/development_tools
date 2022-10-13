#This python script generates a list of blocks with values and positions. 
#These blocks can be used to create lego mosaics in blender.
#Data is stored in a csv file.
#The blocks are defined as bitmask values in a 4 by 4 raster.

from PIL import Image, ImageOps 
import csv
import math
import random

width = 64
posterize = 2

#Predefined blocks
blocks = [1,3,7,15,17,51,255,273,4369,13107,65535]

#opening a image file and saving it as a pixel array
#im = Image.open("Drive:/imagefile.png") #windows format
im = Image.open("/home/user/imagefile.jpg") #linux format

#getting source width, height and aspect
w, h = im.size
a = h/w

#calculating new height based on width and aspect ratio
height = round(width * a)
print(width)
print(height)
print(a)

#resizing 
im = im.resize((width,height), resample =0)

#reducing image colors
im = ImageOps.posterize(im, posterize) 
im.save("/home/user/imagefileresized.jpg")

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
with open('/home/user/imagefile.csv', mode='w') as image_file: #linux
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
