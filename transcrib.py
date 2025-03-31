from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import time
import tempfile
import atexit



# Verify Brave browser installation
browser_path = "/bin//brave"  # Standard Linux Brave path

# Ensure ChromeDriver exists and is executable
webdriver_path = "//home//shubham//Documents//chromedriver-linux64//chromedriver"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()

# Create temporary profile directory
temp_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={temp_dir}")

# Modern headless mode configuration
chrome_options.add_argument("--headless=new")  # New headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Set browser location
chrome_options.binary_location = browser_path
# Set up the WebDriver
# Initialize driver inside function
s=Service(webdriver_path)
def get_transcribe(video_id):
    driver = webdriver.Chrome(service=s, options=chrome_options)
    atexit.register(driver.quit)
    
    try:
        #eg. video_id = 'l9ZO_m7v5j8'
        url = f"https://youtube.com/watch?v={video_id}"
        
        
        # Open the website
        driver.get(url)
        print("Successfully initialized WebDriver and opened URL")

    except Exception as e:
        print(f"Critical error during initialization: {str(e)}")
        raise


    # Wait for the page to load
    time.sleep(3)

    # Wait for search results to load
    time.sleep(3)

    wait = WebDriverWait(driver,30)
    moreButton= wait.until(ec.presence_of_element_located((By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]')))
    moreButton.click()
    print('more button clicked')

    showTransc= wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/div[2]/ytd-structured-description-content-renderer/div/ytd-video-description-transcript-section-renderer/div[3]/div/ytd-button-renderer/yt-button-shape/button')))
    showTransc.click()

    print('show transcribe clicked.')

    path= '//*[@id="segments-container"]/ytd-transcript-segment-renderer/div/yt-formatted-string'
    # Extract information (example: titles of search results)
    time.sleep(6)
    try: # Find all elements using the common XPath 
        elements = driver.find_elements(By.XPATH, path) 
        print(f"Found {len(elements)} elements.") 
        count_range= len(elements) 
        if elements: 
            # Iterate through the list of elements and print their text 

            text = [element.text for element in elements]
            text = " ".join(text)
            return text
            
            
        else:
            print("No elements found with the provided XPath.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.quit()

# text=get_transcribe()
# print(text)
