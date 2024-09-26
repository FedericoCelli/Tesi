import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Funzione per creare un database e una tabella
def create_database():
    conn = sqlite3.connect('capi_allevamento.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CapiAllevamento (
            Regione TEXT,
            Provincia TEXT,
            Capi INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_provincial_data(provincial_url):
    response = requests.get(provincial_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    provincial_rows = soup.select('table tbody tr')
    provincial_data = []

    for row in provincial_rows:
        province_name = row.select_one('td:nth-child(1)').text.strip()
        cattle_count = int(row.select_one('td:nth-child(2)').text.strip())
        provincial_data.append((province_name, cattle_count))

    return provincial_data

def save_data(region_name, provincial_data):
    conn = sqlite3.connect('capi_allevamento.db')
    cursor = conn.cursor()
    for province_name, cattle_count in provincial_data:
        cursor.execute('''
            INSERT INTO CapiAllevamento (Regione, Provincia, Capi)
            VALUES (?, ?, ?)
        ''', (region_name, province_name, cattle_count))
    conn.commit()
    conn.close()

def main():
    create_database()
    main_url = 'https://teseo.clal.it/?section=capi-bovini-italia-tipologie'
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select('table tbody tr')

    for row in rows:
        region_name = row.select_one('td:nth-child(1)').text.strip()
        link_node = row.select_one('td:nth-child(2) a')

        if link_node:
            region_link = link_node['href']
            provincial_data = get_provincial_data(region_link)
            save_data(region_name, provincial_data)
            time.sleep(2)

if __name__ == '__main__':
    main()
