import requests
from bs4 import BeautifulSoup
import csv

def scrape_books():
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    scraped_data = []
    
    for book in books:
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text
        availability = book.select_one('p.availability').text.strip()
        rating = book.p['class'][1]  # Star rating is in the second class
        
        scraped_data.append({
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating
        })
    
    return scraped_data

def save_to_csv(data, filename='books.csv'):
    keys = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    print("Starting web scraping...")
    scraped_books = scrape_books()
    
    if scraped_books:
        print(f"Successfully scraped {len(scraped_books)} books.")
        save_to_csv(scraped_books)
        print("Data saved to books.csv")
    else:
        print("No data was scraped.")