from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to scrape book titles from the given URL
def scrape_book_titles(base_url):
    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    book_titles = []
    start = 0

    while True:
        url = f"{base_url}?start={start}&sort=time&playable=0&sub_type="
        try:
            driver.get(url)
            time.sleep(5)  # Wait for the page to load

            # Find all book titles on the current page
            items = driver.find_elements(By.CSS_SELECTOR, "div.bd.doulist-subject > div.title > a")
            if not items:
                break

            for item in items:
                title = item.text.strip()
                book_titles.append(title)

            start += 25

        except Exception as e:
            print(f"Error occurred at start={start}: {e}")
            time.sleep(5)  # Wait and retry

    driver.quit()
    return book_titles

# Base URL of the Douban book list page
base_url = "https://www.douban.com/doulist/49300014/"

# Scrape book titles
book_titles = scrape_book_titles(base_url)

# Display the book titles
for i, title in enumerate(book_titles, 1):
    print(f"{i}. {title}")

# Save book titles to a file with UTF-8 encoding
with open('douban_book_titles.txt', 'w', encoding='utf-8') as file:
    for title in book_titles:
        file.write(f"{title}\n")

print(f"\nTotal books scraped: {len(book_titles)}")
print("Book titles have been saved to 'douban_book_titles.txt'.")