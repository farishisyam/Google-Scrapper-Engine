import urllib.request
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError
from urllib.parse import quote
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
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
    #print(type(self.html))
    self.soup = BeautifulSoup(self.html, "lxml")
    #print(type(self.soup))
    #print(soups.prettify()[1:500000])

    #sub
    scraps = self.soup.find_all('div','Mw2I7')
    for p in scraps:
      self.k.append(p.find('span','dtviD').get_text().replace(" ","+"))
      
    #link
    scrap = self.soup.find_all('div','rg_bx rg_di rg_el ivg-i')
    for p in scrap:
      self.scr.append(json.loads(bytes(str(p.find('div','rg_meta notranslate').get_text()), 'utf-8').decode('unicode_escape'))['ou'])

    count_img = 1
    count_img_check = 1
    #for images skip||||||||||||NEXT Check Apakah sudah ada di DB ato belum XXXXXXXXXXXXXX Belum Kelar
    for imgg in self.img3:
      for img2 in self.scr:
        print('proses harap sabar')
        print('img ke-',count_img)
        print(img2)
        if imgg == img2:
          print('sama')
          self.img_sama+=1
        elif imgg != img2:
          print('***************')
          print('---------------')
          print('+++++++++++++++')
          print('<<<<masuk>>>>>>')
          print('+++++++++++++++')
          print('---------------')
          print('***************')
          #notepad img
          file_img = open("Images.txt", "r+") # buka file untuk ditulis
          teks = file_img.readlines()
          img_note = "{}\n".format(img2)
          file_img.write(img_note)# tulis teks ke file
          file_img.close()# tutup file
          #notepad img_sama
          file_img_sama = open("Catetan_img.txt", "r+") # buka file untuk ditulis
          teks_sama = file_img_sama.readlines()
          img_sama_note = "{}\n".format(self.img_sama)
          file_img_sama.write(img_sama_note)# tulis teks ke file
          file_img_sama.close()# tutup file
        else:
          print('ada yg error')
        count_img+=1
        #count_img_check+=1

    for ram in self.img3:
      if ram == '':
        self.img3.remove('')
      elif ram != '':
        pass
      else:
        print('ada yg error')
      

    for img2 in self.scr:
      self.img3.append(img2) #img pembanding utk check

    rk = self.k
    print(len(self.scr))

    return rk

  def proses(self,subs_part2):
    file_link_sch_sama = open("Catetan_link.txt", "r+") # buka file untuk ditulis
    sch1sama = file_link_sch_sama.readlines()
    serach_file = len(sch1sama)
    if serach_file == 0 :
      self.link_search_sama = 0
    elif serach_file < 0:
      self.link_search_sama = sch1sama[serach_file-1]
    file_link_sch_sama.close()

    file_img_stack_sama = open("Catetan_img.txt", "r+") # buka file untuk ditulis
    imgstksama = file_img_stack_sama.readlines()
    imgstkfile = len(imgstksama)
    if imgstkfile == 0 :
      self.img_sama = 0
    elif imgstkfile < 0:
      self.img_sama = imgstksama[imgstkfile-1]
    file_img_stack_sama.close()
      
    self.url_check = ['']
    self.url_finish = []
    self.url_part2 = [subs_part2]
    self.img3 = ['']
    stop = True
    count=1
    while (stop == True):
      for ii in self.url_part2:
        print('array ke-',count)
        #stack
        file_link = open("Link_Stack.txt","r+")
        stack = file_link.readlines()
        link_stack = len(stack)
        if link_stack == 0:
          link_stack_in = "{}\n".format(ii)
          file_link.write(link_stack_in)# tulis teks ke file
          jojo = ii
        elif link_stack > 0:
          for check_stack in stack:
            if ii == check_stack:
              pass
            elif ii != check_stack:
              link_stack_in = "{}\n".format(ii)
              file_link.write(link_stack_in)# tulis teks ke file
              jojo = ii
            else:
              print('ada yg error')
        else:
          print('ada yg error')
        file_link.close()

        subs = self.initsub(jojo)
        self.url_part = []
        for i in subs:
          self.url_part.append(",g_1:" + i)

        self.url_part2 = [] 
        k = 0
        c = len(subs)

        #for link searrch
        while k < c:
          for a in self.url_part :
            self.url_part2.append(self.urlink + a)
            for b in self.url_part:
              z = a + b
              self.url_part2.append(self.urlink + z)
              #check
              for d in self.url_part2:
                for dd in self.url_check:
                  if d == dd:
                    self.url_part2.remove(d)
                    self.link_search_sama+=1
                  else:
                    self.url_finish.append(d)
          self.url_part.append(z)
          k+=1
          #notepad link_sch_sama
          file_sch_sama = open("Catetan_link.txt", "r+") # buka file untuk ditulis
          sch1_sama = file_sch_sama.readlines()
          img_sama_note = "{}\n".format(self.link_search_sama)
          file_sch_sama.write(img_sama_note)# tulis teks ke file
          file_sch_sama.close()# tutup file

        for rem in self.url_check:
          if rem == '':
            self.url_check.remove('')
          elif rem != '':
            pass
          else:
            print('ada yg error')
        count+=1

      #end or not
      if len(self.url_check) == len(self.url_finish):
        yes = "Berhasil"
        stop = False
      elif len(self.url_check) != len(self.url_finish):
        for pindah in self.url_part2:
          self.url_check.append(pindah)
      else:
        print('ada yg error')

    return yes

class main(basic, kat):
  def ha(self):
    print("SEMANGAT TA")
    
#------------- Main Program -------------#
d = main()
d.ha()
#txt Images
file1 = open("Images.txt", "w")
file1.close()
# buka file untuk ditulis
file2 = open("Catetan_img.txt", "w")
file2.close()
# buka file untuk ditulis
file3 = open("Link_Stack.txt", "w")
file3.close()
# buka file untuk ditulis
file3 = open("Catetan_link.txt", "w")
file3.close()
keyword = input("What Your images find?")
key = d.url(keyword)
yes = d.proses(key)
print(yes)
