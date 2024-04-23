from PIL import Image, ImageFilter
import glob

#loops through all images files in a folder
#resizes the images to a specified resolution
#applies a blur filter to the background, in case the image doesnt fit the aspect ratio

#OutputResolution
out_width = 1920
out_height = 1080

def resizeBlur(file):
    print(file)
    img = Image.open(file)
    #Calculate percentage difference
    hpercent = (out_height / float(img.size[1]))

    #Change width based on percentage difference
    wsize = int((float(img.size[0]) * float(hpercent)))

    #resize image
    img = img.resize((wsize, out_height), Image.Resampling.LANCZOS)

    #copy image for background blur
    #resize image for backgroudn blur
    wpercent = (out_width/float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    blurImg = img.resize((out_width, hsize), Image.Resampling.LANCZOS)
    vCrop = (int(blurImg.size[1]) -1080 )/2
    blurImg = blurImg.crop((0,0+vCrop,1920,blurImg.size[1]-vCrop))
    #blurImg = blurImg.crop((0,0,1920,1080))

    #blur image for background
    blurImg = blurImg.filter(ImageFilter.GaussianBlur(10))

    #compose foreground image over background
    outImg = blurImg
    offset = int((1920 - img.size[0]) / 2)
    outImg.paste(img, (offset,0))

    outImg.save(file + '_resized.jpg')
  
  
#get all images of type jpg and apply filters
image_list = []
for filename in glob.glob('*.jpg'):
    im=Image.open(filename)
    resizeBlur(filename)
