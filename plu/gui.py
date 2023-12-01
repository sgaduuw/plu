import io
import smtplib as sm
from base64 import b64encode
from datetime import datetime
from email.message import EmailMessage

import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
# from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from retry_requests import retry

from plu.database import SessionLocal, engine
from plu.models import Group, Transactions, User

import pathlib as pl
import os

today = datetime.today().strftime('%Y-%m-%d')
path_base = '.'
backup_base = path_base + '/backup/'
backup_today = backup_base + today

if not os.path.exists(backup_base):
    os.mkdir(backup_base)
if not os.path.exists(backup_today):
    os.mkdir(backup_today)

df_transactions = pd.read_sql_table(
    'transactions',
    con=engine
)

df_users = pd.read_sql_table(
    'users',
    con=engine
)

df_groups = pd.read_sql_table(
    'groups',
    con=engine
)

df_users.to_csv(path_or_buf=backup_today + '/users.csv')
df_groups.to_csv(path_or_buf=backup_today + '/groups.csv')
df_transactions.to_csv(path_or_buf=backup_today + '/transactions.csv')


db = SessionLocal()


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()

        uic.loadUi('paraplu.ui',self)
        self.show()

        self.login.clicked.connect(self.call_login)
        self.execute.clicked.connect(self.create_transaction)
        self.pushButton.clicked.connect(self.send_email)

    def call_login(self):
        l_username = self.username.text()
        l_password = self.password.text()
        print(f"klik: {l_username} - {l_password}")
        try:
            q = db.query(User).filter(
                User.username == l_username,
                User.password == l_password
            ).first() is not None
        except:
            msg = QMessageBox()
            msg.setText('Dat ging fout')
            msg.exec_()
        else:
            print(q)
            self.label_3.setEnabled(True)
            self.label_4.setEnabled(True)
            self.quantity.setEnabled(True)
            self.price.setEnabled(True)
            self.execute.setEnabled(True)

    def create_transaction(self):
        l_quantity = self.quantity.text()
        l_price = float(self.price.text().replace(',', '.'))
        l_user = db.query(User).filter(User.username == self.username.text()).first()
        print(f"Transactions: {l_user}")
        try:
            transaction = Transactions(
                amount=l_quantity,
                price=l_price,
                user_id = l_user.id
            )
        except:
            msg = QMessageBox()
            msg.setText('Dat ging fout')
            msg.exec_()
        else:
            print(transaction)
            db.add(transaction)
            db.commit()

    def backup(self):
        df_users.to_csv(path_or_buf=backup_today + 'users.csv')
        df_groups.to_csv(path_or_buf=backup_today + 'groups.csv')
        df_transactions.to_csv(path_or_buf=backup_today + 'transactions.csv')


    def inventory(self):
        pass

    def send_email(self):
        smtp_connection = "smtp-mail.outlook.com"
        skillsoft_email = "email"
        skillsoft_password = "password"

        email_connection = sm.SMTP(host=smtp_connection, port=25)
        email_connection.starttls()
        email_connection.login(user = skillsoft_email, password = skillsoft_password)

        my_destination_email = "<insert email here"

        
        aantal_paraplus = df_transactions['amount'].sum()

        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 51.85667,
            "longitude": 4.53472,
            "daily": ["precipitation_hours", "precipitation_probability_max"],
            "timezone": "Europe/Berlin"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_precipitation_hours = daily.Variables(0).ValuesAsNumpy()
        daily_precipitation_probability_max = daily.Variables(1).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s"),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        daily_data["precipitation_hours"] = daily_precipitation_hours
        daily_data["precipitation_probability_max"] = daily_precipitation_probability_max

        daily_dataframe = pd.DataFrame(data = daily_data)

        print(daily_dataframe.head())

        plot = daily_dataframe.plot(kind='line', x='date')
        fig = plot.get_figure()

        img_format = 'png'

        f = io.BytesIO()
        fig.savefig(f, format=img_format)
        f.seek(0)
        img_data = f.read()

        mail_content = f"""
        Aantal paraplu's in voorraad: {aantal_paraplus}
        """

        print(f"Inhoud mail:\n{mail_content}")

        msg = EmailMessage()
        msg['Subject'] = f"Inventory {today}"
        msg['From'] = skillsoft_email
        msg['To'] = my_destination_email

        msg.add_header('Content-Type','text/html')
        msg.set_content(mail_content)
        msg.add_attachment(img_data, maintype='image', subtype=img_format)

        email_connection.send_message(msg)


def main():
    print('dit is main')
    app = QApplication([])
    window = MyGUI()

    app.exec_()

if __name__ == '__main__':
    main()
