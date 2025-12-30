import requests
import pandas as pd
from bs4 import BeautifulSoup
import re  # Додали бібліотеку для пошуку шаблонів (RegEx)

url = "https://www.audible.com/search?keywords=book&node=18573211011"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

items = soup.find_all('li', class_='productListItem')

data = []

for item in items:
    title_tag = item.find('h3', class_='bc-heading')
    title = title_tag.get_text(strip=True) if title_tag else "N/A"

    author_tag = item.find('li', class_='authorLabel')
    if author_tag:
        author = author_tag.get_text(strip=True).replace('By:', '').strip()
    else:
        author = "-"

    date_tag = item.find('li', class_='releaseDateLabel')
    if date_tag:
        date = date_tag.get_text(strip=True).replace('Release date:', '').strip()
    else:
        date = "-"

    price_tag = item.find('p', class_='buybox-regular-price')
    if price_tag:
        raw_text = price_tag.get_text(strip=True)
        found_price = re.search(r'\$\d+\.\d{2}', raw_text)
        if found_price:
            price = found_price.group()
        else:
            price = raw_text
    else:
        price = "-"

    data.append({
        'Title': title,
        'Author': author,
        'Date': date,
        'Price': price
    })

df = pd.DataFrame(data)
df.to_csv('audible_books.csv', index=False)

print(df)