import requests
import json
import pandas as pd
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# URL de la page (à adapter avec tes propres paramètres)

# Ajouter tes cookies de session ici si nécessaire
cookies = {
    "PHPSESSID": "u348c45ha8cjolgb4vcdvpv661"
}
all_data = []

for i in range (1,100):
    url = "https://www.winamax.fr/account/history.php?to_display=sitngo&history_date_from_day=01&history_date_from_month=02&history_date_from_year=2024&history_date_to_day=28&history_date_to_month=12&history_date_to_year=2025"
    if i>1:
        url += f"&order_by=&page={i}"
    

    # Récupérer les données depuis l'URL
    response = requests.get(url, headers=headers, cookies=cookies) # Fixed the condition to check if the response text is not None
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")[1:]  # On ignore la première ligne si c'est l'en-tête
        page_data = []

        data = []
        for row in rows:
            cols = row.find_all("td")
            if cols and ("Expresso" in cols[1].text.strip() or "EXPRESSO" in cols[1].text.strip()):
                date = cols[0].text.strip()
                tournoi = "Expresso"
                buy_in = cols[2].text.strip()
                gagné = int(cols[5].text.strip())==1
                if gagné and float(buy_in) >+0.23:
                    gain = float(cols[6].text.strip().replace("\xa0€","").replace(',','.')) - float(buy_in)
                else:
                    gain = - float(buy_in)    
                if abs(float(cols[2].text.strip()))>=0.23:
                    # print(cols[2].text.strip())
                    # print(cols[8].text.strip())
                    # print(url)
                    multiplicateur=float(cols[8].text.strip().replace("\xa0€","").replace(',','.'))/float(cols[2].text.strip())
                else:
                    multiplicateur=0
                page_data.append([date,tournoi,gagné,buy_in,gain,multiplicateur])
        all_data.extend(page_data)
    
df = pd.DataFrame(all_data, columns=["Date", "Tournoi", "Gagné","Buy-in", "Gain","Multiplicateur"])
    # Exporter les données vers un fichier Excel
   
output_file = "historique_expresso.xlsx"
df.to_excel(output_file, index=False)