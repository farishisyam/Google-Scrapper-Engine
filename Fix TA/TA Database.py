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
import time

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
          print(tagname, value)
          with open(out, 'w') as f:
            for (tagname, value) in metaData.items():
              f.write(str(tagname)+"\t"+\
                str(value)+"\n")
          
    except Exception as e:
        print("Failed...")
        print(e)

getMetaData("image.jpg", "image.csv")
# x sebagai counter
x = 1   #Counter file
y = 1   #Counter Sukses
z = 0   #Counter Gagal
link = open("scrap_url.txt", "r").read().split("\n")
#with open("Images.txt", 'rb') as f:
  #link = f.read()
for a in link :
    
    
    try:
      print(f"Link : {a}")
      print(y)
      y+=1
      urllib.request.urlretrieve(f"{a}", "image.jpg")                             # Mendownload URL dan menyimpannya sebagai file image.jpg
      metaData = {}
      
      imgFile = Image.open("image.jpg")
      out = f"Metadata/Metadata{x}.csv"
      print ("Getting meta data...")
      info = imgFile._getexif()
      if info:
        print ("found meta data!")
        for (tag, value) in info.items():
          tagname = TAGS.get(tag, tag)
          metaData[tagname] = value                   
          #print(tagname, value)
          with open(out, 'w') as f:
            for (tagname, value) in metaData.items():
              f.write(str(tagname)+"\t"+\
                str(value)+"\n")
          df = pd.read_csv(open(f"Metadata/Metadata{x}.csv"), sep="\t", header=None)  
          df['URL'] = a                                                                # Transpose CSV
          df.to_csv(f"C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/Metadata{x}URL.csv", sep="\t", header=None) #disimpan di lokasi yang bisa untuk LOAD DATA MySQL

        x+=1        
    except Exception as e:
        print(e)                                                  # Apabila gambar tidak dapat diambil metadatanya
  
                 
   
else:
    print("cannot process links")

