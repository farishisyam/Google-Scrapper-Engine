import os
import argparse
import pandas as pd
import numpy as np
import csv
from PIL import Image
from PIL.ExifTags import TAGS
import urllib.request
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError
from urllib.parse import quote
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import gc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def getMetaData(imgname, out):
    try:
      metaData = {}
      
      imgFile = Image.open(imgname)
      print ("Getting meta data...")
      info = imgFile._getexif()
      if info:
        print ("found meta data!")
        for (tag, value) in info.items():
          tagname = TAGS.get(tag, tag)
          metaData[tagname] = value
          if not out:
            print (tagname, value)
          
        if not out:
          print ("Outputting to file...")
          with open(out, 'w') as f:
            for (tagname, value) in metaData.items():
              f.write(str(tagname)+"\t"+\
                str(value)+"\n")
    except :
        print("Failed...")

# x sebagai counter
x = 1   #Counter file
k = 0   #Counter Sukses
z = 0   #Counter Gagal
link = open("Image/Tarantula.txt", "r")
for a in link :
    print(f"Link : {a}")
    try:
        urllib.request.urlretrieve(f"{a}", "image.jpg")                             # Mendownload URL dan menyimpannya sebagai file image.jpg
        getMetaData("image.jpg", f"Metadata/Metadata{x}.csv")                       # Mengambil metadata dari image.jpg dan menyimpannya ke CSV
        df = pd.read_csv(open(f"Metadata/Metadata{x}.csv", "w"), sep="\t", header=None)  
        df['URL'] = a                                                                # Transpose CSV
        df.to_csv(f"C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/Metadata{x}URL.csv", sep="\t", header=None) #disimpan di lokasi yang bisa untuk LOAD DATA MySQL
        x += 1
        os.remove("image.jpg")                                                      # Menghapus file image.jpg
        k+=1
                                                           
        print(f"Jumlah data Sukses  : {k}")
    except:
        print("Link ini error...")
        z+=1                                                                     # Apabila gambar tidak dapat diambil metadatanya
        print(f"Jumlah data Gagal   : {z}")
else:
    print("cannot process links")                                                   #Apabila Link tidak dapat di proses sama sekali
    z+=1


print(f"Jumlah data Sukses  : {k}")
print(f"Jumlah data Gagal   : {z}")