# -*- coding: utf-8 -*-
import sys,os,time

import urllib3
from tika import parser
from pws import Google
from pws import Bing
import requests
from bs4 import BeautifulSoup
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import string
import nltk 
from nltk.corpus import wordnet 
nltk.download('wordnet')

printable = set(string.printable)

linkl = []; counter = 0;counter2 = 0; fileName1 = "";alrinuse = []; alrinuse2 = []

synonyms = [] 
antonyms = [] 

googlestring = '"uni" OR "fh" -springer -buy :pdf'

pathname = os.path.dirname(sys.argv[0]) 
spath = os.path.abspath(pathname)

def searchit(string):
	global counter,fileName1,alrinuse,synonyms,antonyms
	for syn in wordnet.synsets(string): 
		for l in syn.lemmas(): 
			synonyms.append(l.name()) 
			if l.antonyms(): 
				antonyms.append(l.antonyms()[0].name()) 
	synonyms.append(string)
	print(set(synonyms)) 
	#time.sleep(999)
	if synonyms:
		for x in synonyms:
			searchstr = " ".join((string, googlestring))
			cache = Google.search(query=searchstr, num=100, start=1, country_code="")
			#print(Bing.search('hello world', 5, 2))
			link = (cache['url'])
			print (link)
			#for key in cache:
			#   print ("key: %s , value: %s" % (key, cache[key]))
			   
			page = requests.get(link)
			soup = BeautifulSoup(page.content)
			links = soup.findAll("a")
			for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
				cache1 = re.split(":(?=http)",link["href"].replace("/url?q=",""))
				cache2 = str(cache1)
				if any(link in s for s in alrinuse):
					pass
				else:
					if ".pdf" in cache2:
						cache2 = cache2[2:cache2.find(".pdf") + 4]
						linkl.append(cache2)
						alrinuse.extend([link])
					else:
						pass
					if ".PDF" in cache2:
						cache2 = cache2[2:cache2.find(".PDF") + 4]
						linkl.append(cache2)
						alrinuse.extend([link])
					else:
						pass
	else:
		pass

			
	#linkl2 = ['https://pawn.physik.uni-wuerzburg.de/einfuehrung/SS06/23%20Induktion.pdf']
	for link in linkl:
		link = ''.join(link)
		if any(link in s for s in alrinuse2):
			pass
		else:
			try:
				response = requests.get((link), stream=True, timeout=(float(3.059)))
				if response.status_code == 200:
					try:
						try:
							cache3 = str(link)
							if cache3.find("webcache") == -1:
								print (link)
								urllib3.disable_warnings()
								url = link
								fileName = r"file"
								fileName1 = "".join((fileName, str(counter)))
								fileName = "".join((fileName1, ".pdf"))
								with urllib3.PoolManager() as http:
									r = http.request('GET', url)
									with open(fileName, 'wb') as fout:
										fout.write(r.data)
								counter=counter+1	
								alrinuse2.extend([link])
							else:
								pass				
						except:
							try:
								fileName = r"file"
								fileName1 = "".join((fileName, str(counter)))
								fileName = "".join((fileName, ".pdf"))
								url = link
								r = requests.get(url, stream=True)
								with open(fileName, 'wb') as fd:
									for chunk in r.iter_content(chunk_size):
										fd.write(2000)
								counter=counter+1	
							except AttributeError:
								pass
					except:
						pass
				else:
					pass
			except requests.exceptions.Timeout:
				pass
			except requests.exceptions.SSLError:
				pass

	
def pdfpages(path):
	from PyPDF2 import PdfFileReader
	pdf = PdfFileReader(open(path,'rb'))
	numb = pdf.getNumPages()
	print (numb)
	return numb
		
def pdfparser(data):
	global fileName1,counter2			
	fileName = r"file"
	with open(data, 'rb') as fp:
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
		# Create a PDF interpreter object.
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		# Process each page contained in the document.

		for page in PDFPage.get_pages(fp):
			interpreter.process_page(page)
			cache =  retstr.getvalue()
			data = filter(lambda x: x in printable, cache)
		fileName1 = "".join((fileName, str(counter2)))
		cachen = "".join((fileName1, ".txt"))	
		f = open(cachen,'a')
		f.write(data)
		f.close()
		#print data

if __name__ == "__main__":
	searchit(str(sys.argv[1]))
	
	for file in os.listdir(pathname):
		try:
			if file.endswith(".pdf"):
				if os.path.getsize(file) < 500000 or pdfpages(pathf) < 4:
					os.remove(file)
				else:
					print(os.path.join(pathname, file))
					pathf = (os.path.join(pathname, file))
					if (pdfpages(pathf) > 4):
						pdfparser(pathf)
						counter2 = counter2 + 1
					#pathf=pathf.replace('\\',"//")
					#pdfparser(pathf)  	
		except:
			pass
		

#pdfparser(sys.argv[1])  		
		
