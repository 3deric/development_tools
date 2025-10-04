from PIL import Image
import glob
import os

#loops through all png images in a folder
#resizes images based on a multiplier
#outputs images as jpg 

#Resolution multiplier
out_res = 0.5

def resizeAndConvert(file):
    print(file)
    img = Image.open(file)
    outImg = img.convert('RGB')
    outImg = outImg.resize((int(img.size[0] * out_res), int(img.size[1] * out_res)), Image.Resampling.LANCZOS)
    outImg.save(os.path.splitext(file)[0] + '.jpg')
  

#get all images of type jpg and apply filters
image_list = []
for filename in glob.glob('*.png'):
    im=Image.open(filename)
    resizeAndConvert(filename)
    os.remove(filename)
