import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import time
starttime = time.time()
root = tk.Tk()
root.withdraw()
messagebox.showinfo('Save Direcotry', 'Select directory to save CSV...')
save_dir = filedialog.askdirectory(parent=root)


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
        try:
            self.aqi_df = pd.read_csv(save_dir + '/aqi.csv')
        except FileNotFoundError:
            self.aqi_df = pd.DataFrame(columns=self.columns)

    def get_aqi(self, zipcodes):
        """Gets the AQI and exports to CSV
        :param zipcodes: zipcodes targeted
        :type zipcodes: str[]
        """
        print('Getting AQI...')

        aqi_list = []
        for z in zipcodes:
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


if __name__ == '__main__':
    """Main
    """
    # Zipcodes targeted, 9-County Bay Area
    zipcodes = ['94501', '94507', '94901', '94558', '94124',
                '94010', '95122', '94534', '95476']

    aqi = AQI(zipcodes)
    while aqi.aqi_df.shape[1] < 10:  # <-- Once the table hits 10 columns, program ends.
        aqi.get_aqi(zipcodes)
        #time.sleep(21600 - time.time() % 21600)  # <-- Gets the AQI every 6 hours 
        time.sleep(30 - time.time() % 30)  # <-- Gets the AQI every 30 seconds
