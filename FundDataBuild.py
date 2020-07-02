# RSS connection for Kerrisdale Advisors, LLC

# import required modules
import feedparser
from lxml import html
import requests
import xml.etree.ElementTree as ET 
import csv 
import os

def getfunds(filename):
	# list of integers representing the number of quarters to read
	quarters = []
	# list of CIK numbers
	ciks = []
	# list of Urls for given CIK
	urls = []
	# reads csv file with list of funds
	with open(filename, newline='') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		for row in reader:
			if row['CIK'] not in ciks:
				ciks.append(row['CIK'])
				quarters.append(row['Num Quarters'])
				urls.append('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + row['CIK'] \
					+ '&type=13F-HR%25&dateb=&owner=exclude&start=0&count=40&output=atom')
	# returns list of RSS feeds, list of num_quarters, list of rss urls
	return quarters, urls, ciks

def get13FUrl(rss, num_quarters):
	d = feedparser.parse(rss)
	links = []
	dates = []
	num_entries = len(d.entries)
	if  num_entries < num_quarters:
		num_quarters = num_entries
	for i in range(num_quarters):
		links.append(d.entries[i]['link'])
		dates.append(d.entries[i]['filing-date'])

	return d['feed']['title'], links, dates, num_quarters


def getXML(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	infotable = tree.xpath('//tr[@class="blueRow"]//td[@scope="row"]//a')
	if len(infotable) < 2:
		print('XML format does not exist.')
		return None

	return 'https://sec.gov' + infotable[1].attrib['href']	
	

def loadRSS(url): 
  
	# creating HTTP response object from given url 
	resp = requests.get(url) 

	# creating folder
	if not os.path.exists('./run'):
		os.mkdir('./run')
  
	# saving the xml file 
	with open('./run/13F.xml', 'wb') as f: 
		f.write(resp.content) 
		  
  
def parseXML(xmlfile, filer, date): 
  
	# create element tree object 
	tree = ET.parse(xmlfile) 
  
	# get root element 
	root = tree.getroot() 
  
	# create empty list for news items 
	items = [] 
	for table in root:
		news = {} 
		for info in table:
			news['Filer'] = filer
			news['Filing Date'] = date
			if info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}nameOfIssuer':
				news['Issuer'] = info.text
			elif info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}titleOfClass':
				news['Class'] = info.text
			elif info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}cusip':
				news['Cusip'] = info.text
			elif info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}value':
				news['Value'] = info.text
			elif info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}shrsOrPrnAmt':
				for ssh in info:
					if ssh.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}sshPrnamt':
						news['Shares Amount'] = ssh.text
					elif ssh.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}sshPrnamtType':
						news['Shares Type'] = ssh.text
			elif info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}investmentDiscretion':
				news['Discretion'] = info.text
			elif info.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}votingAuthority':
				for vote in info:
					if vote.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}Sole':
						news['Sole'] = vote.text
					elif vote.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}Shared':
						news['Shared'] = vote.text
					elif vote.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}None':
						news['None'] = vote.text

		items.append(news)

	# return news items list 
	return items 
  
  
def savetoCSV(newsitems, filename): 
  
	# specifying the fields for csv file 
	fields = ['Filer', 'Filing Date', 'Issuer', 'Class', 'Cusip', 'Value', 'Shares Amount', 'Shares Type', 'Discretion', 'Sole', 'Shared', 'None'] 

	# writing to csv file 
	with open(filename, 'a') as csvfile: 
  
		# creating a csv dict writer object 
		writer = csv.DictWriter(csvfile, fieldnames = fields) 
  
		# check if csv file is empty
		if (os.stat(filename).st_size == 0):
			# writing headers (field names) 
			writer.writeheader() 
  
		# writing data rows 
		writer.writerows(newsitems) 




def main(): 

	# Read list of fund input
	fundfile = './FundList.csv'
	quarters, cik_feeds, ciks = getfunds(fundfile)

	# Loop through following set of steps for each fund
	for i in range(len(cik_feeds)):
		print('Loading data from cik: ' + ciks[i])
		rss = cik_feeds[i]
		num_quarters = int(quarters[i])
		# use rss from web to get url of most recent 13F filing
		filer, urls, dates, num_quarters = get13FUrl(rss, num_quarters)
		# find location of xml file on web
		for i in range(num_quarters):
			xml = getXML(urls[i])
			if not xml:
				continue
			# load rss from web to update existing xml file 
			loadRSS(xml)
			# parse xml file 
			items = parseXML('./run/13F.xml', filer, dates[i])
			# store items in a csv file 
			savetoCSV(items, './run/HedgeDB.csv') 
	# END LOOP


if __name__ == "__main__": 
	# calling main function 
	main() 