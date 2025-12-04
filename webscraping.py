import pandas as pd
import requests
from bs4 import BeautifulSoup


def df_livres():
    r = requests.get('https://books.toscrape.com/index.html')

    content = r.content.decode('utf-8')
    soup = BeautifulSoup(content, "html.parser")

    article = soup.find_all('article', attrs={'class': 'product_pod'})
    liste_titre = [art.h3.a.text for art in article]
    liste_prix = [art.find('p', attrs={'class': 'price_color'}).text[1:] for art in article]
    liste_dispo = [art.find('p', attrs={'class': 'instock availability'}).text.strip() for art in article]
    liste_note = [art.find('p', attrs={'class': 'star-rating'}).get('class')[-1] for art in article]

    dictio = {
        'titre': liste_titre,
        'prix': liste_prix,
        'disponibilité': liste_dispo,
        'note': liste_note
    }

    df = pd.DataFrame(dictio)

    page = 2
    while True:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        r = requests.get(url)
        if r.status_code != 200:
            print("Nombre de pages :", page)
            break

        content = r.content.decode('utf-8')
        soup = BeautifulSoup(content, "html.parser")

        article = soup.find_all('article', attrs={'class': 'product_pod'})
        if not article:
            break
        liste_titre = [art.h3.a.text for art in article]
        liste_prix = [art.find('p', attrs={'class': 'price_color'}).text[1:] for art in article]
        liste_dispo = [art.find('p', attrs={'class': 'instock availability'}).text.strip() for art in article]
        liste_note = [art.find('p', attrs={'class': 'star-rating'}).get('class')[-1] for art in article]

        dictio = {
            'titre': liste_titre,
            'prix': liste_prix,
            'disponibilité': liste_dispo,
            'note': liste_note
        }

        df1 = pd.DataFrame(dictio)
        df = pd.concat([df, df1], axis = 0)
        page += 1

    note_chiffre = {
        "One" : 1,
        "Two" : 2,
        "Three" : 3,
        "Four" : 4,
        "Five" : 5
    }

    df["note"] = df['note'].map(note_chiffre)

    return df

df = df_livres()
print(df)


