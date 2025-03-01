import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

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

# Function to convert 'k' and 'M' to numerical form
def parse_k_or_m(value):
    if 'k' in value.lower():
        return int(float(value.lower().replace('k', '').strip()) * 1000)
    elif 'm' in value.lower():
        return int(float(value.lower().replace('m', '').strip()) * 1000000)
    else:
        return int(value.strip())  # Return as integer if no 'k' or 'M' present

# Function to extract the number of buyers
def extract_number_of_buyers(driver):
    try:
        # Locate the element that contains the number of verified buyers
        buyers_element = driver.find_element(By.CSS_SELECTOR, "div.index-countDesc")
        number_of_buyers = buyers_element.text.strip().split()[0]  # Extracting only the number (before "Verified Buyers")
        return parse_k_or_m(number_of_buyers)  # Convert to numerical form
    except Exception as e:
        print(f"Error extracting number of buyers: {e}")
        return 0  # Return 0 if there's an error or not found

# Function to extract the number of reviews from 'Customer Reviews' section
def extract_number_of_reviews(driver):
    try:
        # Locate the element that contains the number of customer reviews
        reviews_element = driver.find_element(By.CSS_SELECTOR, "div.detailed-reviews-headline")
        number_of_reviews = reviews_element.text.strip().split('(')[-1].split(')')[0]  # Extracting the number from within parentheses
        return parse_k_or_m(number_of_reviews)  # Convert to numerical form
    except Exception as e:
        print(f"Error extracting number of reviews: {e}")
        return 0  # Return 0 if there's an error or not found

# Function to extract product ID from supplier-styleId
def extract_product_id(driver):
    try:
        # Locate the element with class 'supplier-styleId' and extract the product ID
        product_id_element = driver.find_element(By.CSS_SELECTOR, "span.supplier-styleId")
        product_id = product_id_element.text.strip()  # Extracting text (product ID)
        return product_id
    except Exception as e:
        print(f"Error extracting product ID: {e}")
        return None  # Return None if there's an error or not found

# Function to extract star ratings counts for 5, 4, 3, 2, and 1 stars
def extract_star_ratings(driver):
    ratings = {
        "5_star": 0,
        "4_star": 0,
        "3_star": 0,
        "2_star": 0,
        "1_star": 0,
    }
    try:
        # Locate the rating bars for each star (5, 4, 3, 2, and 1)
        rating_elements = driver.find_elements(By.CSS_SELECTOR, "div.index-flexRow.index-ratingBarContainer")

        for element in rating_elements:
            star_count = element.find_element(By.CSS_SELECTOR, "div.index-count").text.strip()
            star_rating = element.find_element(By.CSS_SELECTOR, "progress").get_attribute("data-rating")
            
            star_count = parse_k_or_m(star_count)  # Convert count to numerical form

            # Assign the star count to the respective rating
            if star_rating == '5':
                ratings["5_star"] = star_count
            elif star_rating == '4':
                ratings["4_star"] = star_count
            elif star_rating == '3':
                ratings["3_star"] = star_count
            elif star_rating == '2':
                ratings["2_star"] = star_count
            elif star_rating == '1':
                ratings["1_star"] = star_count
        
        return ratings
    except Exception as e:
        print(f"Error extracting star ratings: {e}")
        return ratings  # Return all zeros if error occurs

# Function to write the product data into a new CSV file
def write_product_data_to_csv(data, output_csv):
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "Product Link", "Image URL", "Category", "Gender", "Brand", "Description", "Ratings", "Ratings Count",
                "Price", "Product ID", "Number of Buyers", "Number of Reviews", "5_star", "4_star", "3_star", "2_star", "1_star"
            ])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Product data saved to {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Main function to scrape data from product links stored in CSV
def scrape_product_details_from_links(input_csv, output_csv):
    try:
        driver = setup_driver()

        # Read product links from the existing CSV file
        with open(input_csv, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            product_links = [row["Product Link"] for row in reader]  # Extracting all product links

        # List to store the product data
        all_product_data = []

        # Scrape product data from each link
        for link in product_links:
            driver.get(link)
            time.sleep(3)  # Allow time for the page to load fully

            # Extract product ID, number of buyers, number of reviews, and star ratings
            product_id = extract_product_id(driver)
            number_of_buyers = extract_number_of_buyers(driver)
            number_of_reviews = extract_number_of_reviews(driver)
            star_ratings = extract_star_ratings(driver)

            # Read additional product details (from the first scraper) from the CSV
            with open(input_csv, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Product Link"] == link:
                        product_data = {
                            "Product Link": row["Product Link"],
                            "Image URL": row["Image URL"],
                            "Category": row["Category"],
                            "Gender": row["Gender"],
                            "Brand": row["Brand"],
                            "Description": row["Description"],
                            "Ratings": row["Ratings"],
                            "Ratings Count": row["Ratings Count"],
                            "Price": row["Price"],
                            "Product ID": product_id,
                            "Number of Buyers": number_of_buyers,
                            "Number of Reviews": number_of_reviews,
                            "5_star": star_ratings["5_star"],
                            "4_star": star_ratings["4_star"],
                            "3_star": star_ratings["3_star"],
                            "2_star": star_ratings["2_star"],
                            "1_star": star_ratings["1_star"],
                        }
                        all_product_data.append(product_data)
                        break

        # Write the extracted data to a new CSV file
        if all_product_data:
            write_product_data_to_csv(all_product_data, output_csv)
        else:
            print("No data was scraped; output file will not be created.")

    except Exception as e:
        print(f"Error in the main execution: {e}")
    finally:
        # Close the driver after scraping
        if 'driver' in locals():
            driver.quit()

# Run the script
if __name__ == "__main__":
    input_csv = "fashion-recommendor/data_output/multiProductLinksAndImages.csv"  # Input CSV containing product links
    output_csv = "fashion-recommendor/data_output/product_details.csv"  # Output CSV to save the detailed product data

    scrape_product_details_from_links(input_csv, output_csv)
