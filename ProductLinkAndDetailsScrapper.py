from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import csv
import time
from urllib.parse import parse_qs, urlparse

# Setup the WebDriver
def setup_driver():
    try:
        # Path to Geckodriver (update this to the correct path)
        service = Service("C:/Program Files (x86)/geckodriver.exe")
        
        # Firefox binary path (update this if Firefox is in a different location)
        options = webdriver.FirefoxOptions()
        options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
        
        # Initialize WebDriver
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error setting up the WebDriver: {e}")
        raise

# Function to extract Category and Gender from the URL and page
def extract_category_and_gender(url, driver):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Extract category from 'rawQuery'
    category = query_params.get("rawQuery", ["Unknown"])[0]
    
    # Extract gender based on the page's gender filter options
    gender = "Unknown"
    try:
        gender_element = driver.find_element(By.CSS_SELECTOR, "label.common-customRadio.gender-label input:checked")
        gender_value = gender_element.get_attribute('value') if gender_element else ""
        if "men" in gender_value and "women" in gender_value:
            # Check the order of 'men' and 'women' in the value string
            if gender_value.split(",")[0] == "men":
                gender = "M"  # Men comes first
            else:
                gender = "F"  # Women comes first
        elif "men" in gender_value:
            gender = "M"  # Only men
        elif "women" in gender_value:
            gender = "F"  # Only women
    except Exception as e:
        print(f"Error extracting gender: {e}")

    return category, gender

# Function to clean and convert the rating count to a numerical value
def convert_rating_count(rating_count):
    if 'k' in rating_count.lower():  # If 'k' is present, multiply by 1000
        return int(float(rating_count.lower().replace('k', '').strip()) * 1000)
    elif 'm' in rating_count.lower():  # If 'm' is present, multiply by 1000000
        return int(float(rating_count.lower().replace('m', '').strip()) * 1000000)
    else:  # If no 'k' or 'm', simply return the integer value
        return int(rating_count.strip())

# Function to extract product links, image URLs, and additional information
def extract_product_links_and_images(url, driver, max_links=500):
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load fully

    product_data = []
    category, gender = extract_category_and_gender(url, driver)  # Extract category and gender from the URL and page

    try:
        # Locate the container for product results
        product_list = driver.find_elements(By.CSS_SELECTOR, "ul.results-base > li.product-base")
        
        # Iterate through the product list and extract links and image URLs
        for product in product_list[:max_links]:  # Limit to max_links
            try:
                link_element = product.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href")
                
                # Extract the image URL (looking for <img> tag inside the product-imageSliderContainer)
                image_element = product.find_element(By.CSS_SELECTOR, "div.product-imageSliderContainer img")
                image_url = image_element.get_attribute("src") if image_element else "No Image"
                
                # Extract additional information
                brand_element = product.find_element(By.CSS_SELECTOR, "h3.product-brand")
                brand = brand_element.text if brand_element else "No Brand"
                
                description_element = product.find_element(By.CSS_SELECTOR, "h4.product-product")
                description = description_element.text if description_element else "No Description"
                
                ratings_element = product.find_element(By.CSS_SELECTOR, "div.product-ratingsContainer span")
                ratings = ratings_element.text if ratings_element else "No Ratings"
                
                # Clean the ratings count to remove the '|' character
                ratings_count_element = product.find_element(By.CSS_SELECTOR, "div.product-ratingsCount")
                ratings_count = ratings_count_element.text if ratings_count_element else "No Ratings Count"
                ratings_count = ratings_count.replace('|', '').strip()  # Remove the '|' and any surrounding spaces
                ratings_count = convert_rating_count(ratings_count)  # Convert to numeric value
                
                price_element = product.find_element(By.CSS_SELECTOR, "div.product-price span")
                price = price_element.text if price_element else "No Price"
                
                # Remove extra price if found
                if price.count("Rs.") > 1:
                    price = price.split("Rs.")[1].strip()  # Only keep the second price value (after Rs.)
                
                # Add to product data list
                product_data.append({
                    "Product Link": link,
                    "Image URL": image_url,
                    "Category": category,
                    "Gender": gender,
                    "Brand": brand,
                    "Description": description,
                    "Ratings": ratings,
                    "Ratings Count": ratings_count,
                    "Price": price
                })
            except Exception as e:
                print(f"Error extracting product info: {e}")

        if not product_data:
            print("No product data found. Please check the page structure or URL.")
    
    except Exception as e:
        print(f"Error extracting product links and images: {e}")

    return product_data

# Function to write the product data into a CSV file
def write_links_and_images_to_csv(data, output_csv):
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Product Link", "Image URL", "Category", "Gender", "Brand", "Description", "Ratings", "Ratings Count", "Price"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Product data saved to {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    try:
        driver = setup_driver()

        # List of URLs to scrape
        urls = [
            "https://www.myntra.com/shirts?f=Gender%3Amen%2Cmen%20women&rawQuery=shirts",
            "https://www.myntra.com/shirts?f=Gender%3Amen%20women%2Cwomen&rawQuery=shirts",
            "https://www.myntra.com/jeans?f=Gender%3Amen%2Cmen%20women&rawQuery=jeans",
            "https://www.myntra.com/jeans?f=Gender%3Amen%20women%2Cwomen&rawQuery=jeans",
            "https://www.myntra.com/tshirts?f=Gender%3Amen%2Cmen%20women&rawQuery=tshirts",
            "https://www.myntra.com/tshirts?f=Gender%3Amen%20women%2Cwomen&rawQuery=tshirts",
            "https://www.myntra.com/sweaters?f=Gender%3Amen%2Cmen%20women&rawQuery=sweaters",
            "https://www.myntra.com/sweaters?f=Gender%3Amen%20women%2Cwomen&rawQuery=sweaters",
            "https://www.myntra.com/jackets?f=Gender%3Amen%2Cmen%20women&rawQuery=jackets",
            "https://www.myntra.com/jackets?f=Gender%3Amen%20women%2Cwomen&rawQuery=jackets",
            "https://www.myntra.com/kurta?f=Gender%3Amen%2Cmen%20women&rawQuery=kurta",
            "https://www.myntra.com/kurta?f=Gender%3Amen%20women%2Cwomen&rawQuery=kurta",
            "https://www.myntra.com/sherwani?f=Gender%3Amen%2Cmen%20women&rawQuery=sherwani",
            "https://www.myntra.com/saree?f=Gender%3Amen%20women%2Cwomen&rawQuery=saree"
        ]
        
        output_csv = "C:\\Users\\AIC-07\\Desktop\\fashion-recommendor\\fashion-recommendor\\data_output\\multiProductLinksAndImages.csv"  # Path to save product data

        # Extract product data from all URLs
        all_product_data = []
        for url in urls:
            print(f"Scraping up to 500 product links and images from: {url}")
            product_data = extract_product_links_and_images(url, driver, max_links=500)  # Scrape 500 from each URL
            all_product_data.extend(product_data)

        # Write the extracted data to a CSV file
        if all_product_data:
            write_links_and_images_to_csv(all_product_data, output_csv)
        else:
            print("No data was scraped; output file will not be created.")
    
    except Exception as e:
        print(f"Error in the main execution: {e}")
    finally:
        # Close the driver after scraping
        if 'driver' in locals():
            driver.quit()
