rom selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to scrape movie titles from the given URL
def scrape_movie_titles(url):
    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    movie_titles = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = last_height

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(3)

        # Check the new scroll height and compare it with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Wait a little longer to ensure the new content has loaded
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height

    # Find all movie titles in the list
    items = driver.find_elements(By.CSS_SELECTOR, "h3.ipc-title__text")
    for item in items:
        title = item.text.strip()
        movie_titles.append(title)

    driver.quit()
    return movie_titles


# URL of the IMDB movie list page
url = "https://www.imdb.com/list/ls046196709/?sort=list_order%2Casc"

# Scrape movie titles
movie_titles = scrape_movie_titles(url)

# Display the movie titles
for i, title in enumerate(movie_titles, 1):
    print(f"{i}. {title}")

# Save movie titles to a file with UTF-8 encoding
with open('imdb_movie_titles.txt', 'w', encoding='utf-8') as file:
    for title in movie_titles:
        file.write(f"{title}\n")

print(f"\nTotal movies scraped: {len(movie_titles)}")
print("Movie titles have been saved to 'imdb_movie_titles.txt'.")