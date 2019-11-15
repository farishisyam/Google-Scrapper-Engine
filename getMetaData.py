import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import os
import pandas as pd
import numpy as np
import csv

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

			if out:
				print ("Outputting to file...")
				with open(out, 'w') as f:
					for (tagname, value) in metaData.items():
						f.write(str(tagname)+"\t"+\
							str(value)+"\n")
		
	except:
		print ("Failed")

dircont = input("Input Directory : ")
directory = os.listdir(dircont)

for files in directory:
	if files.endswith(('jpg','JPG','png','PNG','tiff','TIFF')):
		file_path = os.path.join(dircont, files)
		print(file_path)

	getMetaData(file_path, "Metadata/Metadata.csv")
	print("csv file created...")

	df = pd.read_csv(open("Metadata/Metadata.csv"), sep="\t", header=None)

	dft = df.T

	dft.to_csv("Metadata/MetadataT.csv", sep="\t", header=None)
	print("Transpose Succeed...")