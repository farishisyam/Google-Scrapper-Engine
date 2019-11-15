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



class basic:
  def url(self,word): 
    self.k = [] #sub
    self.scr = [] #link
    self.word = word.replace(" ", "+")#spasi
    self.keyword = self.word #keyword
    
    self.urlink="https://www.google.co.in/search?q="+self.keyword+"&source=lnms&tbm=isch&chips=q:"+self.keyword
    url = self.urlink

    return url

class auto:
  def proses(self,subs):
    self.url_part = []
    for i in subs:
      self.url_part.append(",g_1:" + i)

    self.url_part3 = [] 
    k= 0
    c = len(subs)
    self.url_part2 = self.url_part

    while k < c:
      for a in self.url_part2 :
        self.url_part3.append(self.urlink + a)
        for b in self.url_part2:
          if a == b:
            print(" ")
          else:
            z = a + b
            self.url_part3.append(self.urlink + z)
      self.url_part2.append(z)
      k+=1

    url_ppart = self.url_part3
    print(len(url_ppart))

    return url_ppart

class kat:
  def initsub(self, url):
    #scroll down
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    
    chrome = "chromedriver"
    browser = webdriver.Chrome(chrome, chrome_options=options)
    browser.delete_all_cookies()
    browser.get(url)
    
    for _ in range(900):
      browser.execute_script("window.scrollBy(0,900)")

    try:
      browser.find_element_by_id("smb").click()
      for i in range(900):
        browser.execute_script("window.scrollBy(0,900)")

    except:
      for i in range(900):
        browser.execute_script("window.scrollBy(0,900)")

    self.htm = browser.page_source.encode('utf-8').strip()
    self.html = str(self.htm)
    browser.close()

    self.headers = {}
    self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    print(type(self.html))
    self.soup = BeautifulSoup(self.html, "lxml")
    print(type(self.soup))
    #print(soups.prettify()[1:500000])

    #sub
    scraps = self.soup.find_all('div','Mw2I7')
    for p in scraps:
      self.k.append(p.find('span','dtviD').get_text().replace(" ","+"))
      
    #link
    scrap = self.soup.find_all('div','rg_bx rg_di rg_el ivg-i')
    for p in scrap:
      self.scr.append(json.loads(bytes(str(p.find('div','rg_meta notranslate').get_text()), 'utf-8').decode('unicode_escape'))['ou'])

    rk = self.k
    rs = self.scr

    return rk, rs

# Script untuk mengambil metadata  
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

class main(basic, auto, kat):
    def ha(self):
        print("SEMANGAT TA")
    
    
#------------- Main Program -------------#
d = main()
d.ha()
keyword = input("What Your images find?")
key = d.url(keyword)

#part automatic search
#link source gambar
#tab kategori
tab, link = d.initsub(key)
if tab != None :
  url = d.proses(tab)
  for i in url:
    tab, link = d.initsub(i)
    print(len(link))

  print(len(url))


check = True
while check == True:
    if len(tab) == 0:
      check = False
    else:
        url = d.proses(tab)
        for i in url:
            tab, link = d.initsub(i)
            print(len(link))
    
else:
    print("Gak ada Cuy")

# x sebagai counter
x = 1

for a in link :
    print(f"Link : {a}")
    try:
        urllib.request.urlretrieve(f"{a}", "image.jpg")                             # Mendownload URL dan menyimpannya sebagai file image.jpg
        getMetaData("image.jpg", f"Metadata/Metadata{x}.csv")                       # Mengambil metadata dari image.jpg dan menyimpannya ke CSV
        df = pd.read_csv(open(f"Metadata/Metadata{x}.csv"), sep="\t", header=None)  
        dft = df.T                                                                  # Transpose CSV
        dft.to_csv(f"Metadata/MetadataT{x}.csv", sep="\t", header=None)
        gc.collect()
        x += 1
        os.remove("image.jpg")                                                      # Menghapus file image.jpg


    except:
        print("Link ini error...")                                                  # Apabila gambar tidak dapat diambil metadatanya
else:
    print("cannot process links")

