
'''
Prints out to console the AQI of cities in the 9-County Bay Area,
and exports to .csv file - can be opened in Excel
'''

import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool

# Zipcodes targeted, 9-County Bay Area
zipcodes = ['94501', '94507', '94901', '94558', '94124', 
		'94010', '95122', '94534', '95476']

# Writes the zipcode city and its AQI to aqi.csv
def writeData(zipcode):

	webpage = 'https://airnow.gov/index.cfm?action=airnow.local_city&zipcode=' + zipcode + '&submit=Go'
	page_html = urllib.request.urlopen(webpage)

	soup = BeautifulSoup(page_html, 'html.parser')

	city_html = soup.find('td', attrs={'class': 'ActiveCity'})
	aqi_html = soup.find('tr', attrs={'style': 'color:black;text-align:center;font-weight:200'})

	city = city_html.text.strip()
	aqi = aqi_html.text.strip()

	print('\nThe AQI in ' + city + ' is: ' + aqi)

	with open('aqi.csv', 'a', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow([city, aqi, datetime.now()])

# Main
if __name__ == '__main__':

	'''
	# Write over previous data
	with open('aqi.csv', 'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['City', 'AQI', 'Date/Time Accessed'])
	'''

	# Multiprocessing
	with Pool(4) as p:
		p.map(writeData, zipcodes)


	# Newline
	with open('aqi.csv', 'a', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['', '', ''])







