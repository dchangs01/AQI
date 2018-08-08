"""Prints out to console the AQI of zipcodes in the 9-County Bay Area,
   and exports to CSV. Appends new AQI found to CSV as new column
   with timestamp.

   Script gets the AQI once every specified interval of time,
   and continues running for a specified amount of time.
"""
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import time
from time import sleep
from threading import Thread
root = tk.Tk()
root.withdraw()
messagebox.showinfo('Save Directory', 'Select directory to save CSV...')
save_dir = filedialog.askdirectory(parent=root)


class AQI:
    """Class Object
    """

    def __init__(self, zipcodes):
        """Constructor
        :param zipcodes: list of target zipcodes
        :type zipcodes: str[]
        """
        self.zipcodes = zipcodes
        self.columns = ['City', 'Zipcode', 'AQI on {}'.format(datetime.now())]
        try:
            self.aqi_df = pd.read_csv(save_dir + '/aqi.csv')
        except FileNotFoundError:
            self.aqi_df = pd.DataFrame(columns=self.columns)

    def get_aqi(self):
        """Gets the AQI and exports to CSV
        """
        print('Getting AQI...')

        aqi_list = []
        for z in self.zipcodes:
            webpage = 'https://airnow.gov/index.cfm?action=airnow.local_city&zipcode=' + z + '&submit=Go'
            page_html = urllib.request.urlopen(webpage)
            soup = BeautifulSoup(page_html, 'html.parser')
            city_html = soup.find('td', attrs={'class': 'ActiveCity'})
            aqi_html = soup.find('tr', attrs={'style': 'color:black;text-align:center;font-weight:200'})

            city = city_html.text.strip()
            aqi = aqi_html.text.strip()

            if self.aqi_df.shape[0] != 0:
                aqi_list.append(aqi)
            else:
                aqi_list.append([city, z, aqi])

        if self.aqi_df.shape[0] != 0:
            aqi_list = pd.Series(aqi_list)
            self.aqi_df['AQI on {}'.format(datetime.now())] = aqi_list.values
        else:
            aqi_list = pd.DataFrame(aqi_list, columns=self.columns)
            self.aqi_df = self.aqi_df.append(aqi_list, ignore_index=True)

        self.aqi_df.to_csv(save_dir + '/aqi.csv', index=False)
        print(self.aqi_df)

    def run_aqi(self):
        """Runs get_aqi() every 30 seconds
        """
        while True:
            self.get_aqi()
            time.sleep(30 - time.time() % 30)


if __name__ == '__main__':
    """Main
    """
    # Zipcodes targeted, 9-County Bay Area
    zipcodes = ['94501', '94507', '94901', '94558', '94124',
                '94010', '95122', '94534', '95476']

    aqi = AQI(zipcodes)
    t = Thread(target=aqi.run_aqi)
    t.daemon = True
    t.start()
    sleep(180)  # <-- Runs script for 180 seconds
