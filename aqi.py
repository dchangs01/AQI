import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
import numpy as np


class AQI:
    """Prints out to console the AQI of cities in the 9-County Bay Area and exports to CSV
    """
    def __init__(self, zipcodes):
        """Constructor
        :param zipcodes: list of target zipcodes
        :type zipcodes: str
        """
        self.zipcodes = zipcodes
        self.aqi_array = np.array([['City', 'AQI', 'Date/Time Accessed']])

    def write_data(self, zipcode):
        """Writes the zipcode city and its AQI to aqi.csv
        """
        webpage = 'https://airnow.gov/index.cfm?action=airnow.local_city&zipcode=' + zipcode + '&submit=Go'
        page_html = urllib.request.urlopen(webpage)

        soup = BeautifulSoup(page_html, 'html.parser')

        city_html = soup.find('td', attrs={'class': 'ActiveCity'})
        aqi_html = soup.find('tr', attrs={'style': 'color:black;text-align:center;font-weight:200'})

        city = city_html.text.strip()
        aqi = aqi_html.text.strip()

        print('The AQI in ' + city + ' is: ' + aqi)

        return [city, aqi, datetime.now()]

    def mp_write(self):
        """Multiprocessing
        """
        with Pool(4) as p:
            self.aqi_array = np.append(self.aqi_array, p.map(self.write_data, self.zipcodes), axis=0)

    def to_csv(self, save_directory):
        """Save data array to CSV
        :param save_directory: directory to save data table in
        :type save_directory: str
        """
        print('Saving to CSV...')
        np.savetxt(save_directory + '/aqi.csv', self.aqi_array, delimiter=',', encoding='utf-8', fmt='%s')


if __name__ == '__main__':
    """Main
    """
    # Zipcodes targeted, 9-County Bay Area
    zipcodes = ['94501', '94507', '94901', '94558', '94124',
                '94010', '95122', '94534', '95476']

    save_directory = '/home/daniel/AQI'

    aqi = AQI(zipcodes)
    aqi.mp_write()
    aqi.to_csv(save_directory)
    print(aqi.aqi_array)
