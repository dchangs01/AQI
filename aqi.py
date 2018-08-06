import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
messagebox.showinfo('Save Direcotry', 'Select directory to save CSV...')
save_dir = filedialog.askdirectory()


class AQI:
    """Prints out to console the AQI of cities in the 9-County Bay Area and exports to CSV.
       Appends new AQI found to CSV as new column with timestamp.
    """

    def __init__(self, zipcodes):
        """Constructor
        :param zipcodes: list of target zipcodes
        :type zipcodes: str
        """
        self.zipcodes = zipcodes
        self.columns = ['City', 'Zipcode', 'AQI on {}'.format(datetime.now())]
        self.temp_list = []
        try:
            self.aqi_df = pd.read_csv(save_dir + '/aqi.csv')
        except FileNotFoundError:
            self.aqi_df = pd.DataFrame(columns=self.columns)

    def get_data(self, zipcode):
        """Gets the AQI within the specified zipcode
        :param zipcode: target zipcode
        :type zipcode: str
        """
        print('Getting {} AQI...'.format(zipcode))

        webpage = 'https://airnow.gov/index.cfm?action=airnow.local_city&zipcode=' + zipcode + '&submit=Go'
        page_html = urllib.request.urlopen(webpage)
        soup = BeautifulSoup(page_html, 'html.parser')
        city_html = soup.find('td', attrs={'class': 'ActiveCity'})
        aqi_html = soup.find('tr', attrs={'style': 'color:black;text-align:center;font-weight:200'})

        city = city_html.text.strip()
        aqi = aqi_html.text.strip()

        if self.aqi_df.shape[0] != 0:
            self.temp_list.append(aqi)
        else:
            self.temp_list.append([city, zipcode, aqi])


if __name__ == '__main__':
    """Main
    """
    # Zipcodes targeted, 9-County Bay Area
    zipcodes = ['94501', '94507', '94901', '94558', '94124',
                '94010', '95122', '94534', '95476']

    aqi = AQI(zipcodes)
    for i in zipcodes:
        aqi.get_data(i)
    aqi.temp_list = np.array(aqi.temp_list)
    if aqi.aqi_df.shape[0] != 0:
        aqi.temp_list = pd.Series(aqi.temp_list)
        aqi.aqi_df['AQI on {}'.format(datetime.now())] = aqi.temp_list.values
    else:
        aqi.temp_list = pd.DataFrame(aqi.temp_list, columns=aqi.columns)
        aqi.aqi_df = aqi.aqi_df.append(aqi.temp_list, ignore_index=True)

    aqi.aqi_df.to_csv(save_dir + '/aqi.csv', index=False)
