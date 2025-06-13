import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def Test():
    print("working")
def scrape_avalon():
    # Set up Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Load the page
    url = "https://www.avaloncommunities.com/california/san-jose-apartments/avalon-morrison-park/#community-unit-listings"
    driver.get(url)
    time.sleep(5)  # Wait for JS

    # Extract listings
    units = driver.find_elements(By.CLASS_NAME, "availability-container__item")
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # File path
    csv_file = "/home/yourname/project/data/avalon_listings.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write header only once
        if not file_exists:
            writer.writerow(["timestamp", "details", "model", "price"])

        for unit in units:
            try:
                model = unit.find_element(By.CLASS_NAME, "availability-item__bed-bath").text
                price = unit.find_element(By.CLASS_NAME, "availability-item__pricing").text
                details = unit.find_element(By.CLASS_NAME, "availability-item__title").text
                writer.writerow([timestamp, details, model, price])
            except Exception as e:
                print("Error parsing unit:", e)

    driver.quit()
scrape_avalon()
Test()
