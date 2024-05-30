from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "YOUR_LINKEDIN_JOB_LINK"
YOUR_EMAIL = "YOUR_EMAIL"
YOUR_PASSWORD = "YOUR_PASSWORD"
CHROME_DRIVER_LOCATION = "YOUR_CHROME_DRIVER_LOCATION"

def abort_application(driver):
    try:
        print("Aborting application")
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
        )
        close_button.click()
        time.sleep(2)
        discard_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn"))
        )
        discard_button.click()
    except (NoSuchElementException, TimeoutException):
        print("Could not find modal dismiss or discard button.")

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(CHROME_DRIVER_LOCATION, options=chrome_options)
wait = WebDriverWait(driver, 15)  # Increased wait time

driver.get(URL)

# Click Sign in Button
try:
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/login"]')))
    sign_in_button.click()
except TimeoutException:
    print("Sign-in button not found")
    driver.quit()
    exit()

# Sign in
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

# CAPTCHA - Solve Puzzle Manually
input("Press Enter when you have solved the Captcha")

# Get Listings
try:
    all_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
except TimeoutException:
    print("No job listings found")
    driver.quit()
    exit()

# Apply for Jobs
for index in range(len(all_listings)):
    print("Opening Listing")
    try:
        # Refetch listings to avoid stale elements
        all_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
        listing = all_listings[index]
        listing.click()
        time.sleep(3)
        
        # Click Apply Button
        apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button")))
        apply_button.click()
        time.sleep(2)

        while True:
            try:
                # Click Next button
                next_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Next') or contains(@aria-label, 'Continue')]")
                if next_buttons:
                    print("Next button found")
                    next_buttons[0].click()
                    print("Clicked Next button")
                    time.sleep(2)
                    continue
                
                # Click Review button
                review_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Review')]")
                if review_buttons:
                    print("Review button found")
                    review_buttons[0].click()
                    print("Clicked Review button")
                    time.sleep(2)
                    continue

                # Click Submit application button
                submit_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Submit application')]")
                if submit_buttons:
                    print("Submit application button found")
                    submit_buttons[0].click()
                    print("Submitting job application")
                    time.sleep(2)
                    break
                
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

time.sleep(5)
driver.quit()
