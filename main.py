from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
URL = "YOUR_LINKEDIN_JOB_LINK"  # LinkedIn job link to start from
YOUR_EMAIL = "YOUR_EMAIL"  # Your LinkedIn email
YOUR_PASSWORD = "YOUR_PASSWORD"  # Your LinkedIn password
CHROME_DRIVER_LOCATION = "YOUR_CHROME_DRIVER_LOCATION"  # Path to ChromeDriver executable

# Function to abort the current job application process
def abort_application(driver):
    try:
        print("Aborting application")
        # Find and click the close button of the modal
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
        )
        close_button.click()
        time.sleep(2)
        # Find and click the discard button to confirm the abort
        discard_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn"))
        )
        discard_button.click()
    except (NoSuchElementException, TimeoutException):
        print("Could not find modal dismiss or discard button.")

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the WebDriver
driver = webdriver.Chrome(CHROME_DRIVER_LOCATION, options=chrome_options)
wait = WebDriverWait(driver, 15)  # Increased wait time

# Open the LinkedIn job link
driver.get(URL)

# Click the Sign In button
try:
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/nav/div/a[2]')))
    sign_in_button.click()
except TimeoutException:
    print("Sign-in button not found")
    driver.quit()
    exit()

# Sign in with provided credentials
try:
    email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_field.send_keys(YOUR_EMAIL)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(YOUR_PASSWORD)
    password_field.send_keys(Keys.ENTER)
except TimeoutException:
    print("Sign-in form not found")
    driver.quit()
    exit()

# Wait for the user to solve the CAPTCHA manually
input("Press Enter when you have solved the Captcha")

# Get job listings
try:
    all_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
except TimeoutException:
    print("No job listings found")
    driver.quit()
    exit()

# Loop through all job listings to apply
for index in range(len(all_listings)):
    print("Opening Listing")
    try:
        # Refetch listings to avoid stale elements
        all_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
        listing = all_listings[index]
        listing.click()
        time.sleep(3)  # Wait for the job listing to load

        # Click the Apply button
        apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button")))
        apply_button.click()
        time.sleep(2)  # Wait for the apply modal to load

        # Loop to navigate through the application steps
        while True:
            try:
                # Click the Next button
                next_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Next') or contains(@aria-label, 'Continue')]")
                if next_buttons:
                    print("Next button found")
                    next_buttons[0].click()
                    print("Clicked Next button")
                    time.sleep(2)  # Wait for the next step to load
                    continue

                # Click the Review button
                review_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Review')]")
                if review_buttons:
                    print("Review button found")
                    review_buttons[0].click()
                    print("Clicked Review button")
                    time.sleep(2)  # Wait for the review step to load
                    continue

                # Click the Submit application button
                submit_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Submit application')]")
                if submit_buttons:
                    print("Submit application button found")
                    submit_buttons[0].click()
                    print("Submitting job application")
                    time.sleep(2)  # Wait for the submission to process
                    break

                # If no Next, Review, or Submit button is found, abort the application
                print("No Next, Review, or Submit button found, skipping this application")
                abort_application(driver)
                break

            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                print(f"Exception occurred: {str(e)}")
                abort_application(driver)
                break

        # Ensure modal is closed before moving on
        try:
            close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss")))
            close_button.click()
        except (TimeoutException, NoSuchElementException):
            print("Close button not found after submitting application.")

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
        print(f"Exception occurred: {str(e)}")
        abort_application(driver)
        print("No application button, skipped.")
        continue

# Wait for a few seconds before closing the browser
time.sleep(5)
driver.quit()
