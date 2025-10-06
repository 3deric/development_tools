import glob
import os

#loops through all godot .tres files in a folder
#changes texture extension from png to jpg if its not a decal

def changeFilePaths(filename):
    print(f"{filename}\n")
    with open(filename, "r", encoding="utf-8") as file:
        data = file.readlines()
        i = 0
        for line in data:
            if ".png" in line and "decal" not in line:
                line = line.replace(".png", ".jpg")
                print(line)
            data[i] = line
            i+=1

    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(data)
  
#get all images of type jpg and resize if not a decal texture
for filename in glob.glob("*.tres"):
    changeFilePaths(filename)
