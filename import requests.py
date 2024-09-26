import requests
from bs4 import BeautifulSoup
import time

def get_provincial_data(provincial_url):
    # Effettua una richiesta alla pagina provinciale
    response = requests.get(provincial_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Seleziona le righe della tabella provinciale
    provincial_rows = soup.select('table tbody tr')

    # Crea una lista per memorizzare i dati delle province
    provincial_data = []

    for row in provincial_rows:
        # Estrai il nome della provincia e il numero di capi di allevamento
        province_name = row.select_one('td:nth-child(1)').text.strip()  # Modifica secondo necessità
        cattle_count = row.select_one('td:nth-child(2)').text.strip()   # Modifica secondo necessità

        provincial_data.append((province_name, cattle_count))

    return provincial_data

def main():
    main_url = 'https://teseo.clal.it/?section=capi-bovini-italia-tipologie'  # URL della pagina principale
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Seleziona le righe della tabella principale
    rows = soup.select('table tbody tr')

    # Crea una lista per memorizzare i dati finali
    all_data = []

    for row in rows:
        # Estrai il nome della regione e il link
        region_name = row.select_one('td:nth-child(1)').text.strip()  # Modifica secondo necessità
        link_node = row.select_one('td:nth-child(2) a')                # Modifica secondo necessità

        if link_node:
            region_link = link_node['href']
            print(f"Regione: {region_name}, Link: {region_link}")

            # Recupera i dati per la provincia seguendo il link
            provincial_data = get_provincial_data(region_link)
            all_data.extend([(region_name, province_name, cattle_count) for province_name, cattle_count in provincial_data])

            # Aggiungi un delay di 2 secondi tra le richieste
            time.sleep(2)  # Puoi modificare il valore in base alle tue esigenze

    # Stampa l'intera tabella dei dati
    print("\nTabella dei Capi di Allevamento per Regione e Provincia:")
    print("Regione | Provincia | Capi di Allevamento")
    print("-" * 50)
    for region, province, count in all_data:
        print(f"{region} | {province} | {count}")

if __name__ == '__main__':
    main()
