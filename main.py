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
        # Click Close Button
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()
        time.sleep(2)
        # Click Discard Button
        discard_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
        discard_button.click()
    except NoSuchElementException:
        pass

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(CHROME_DRIVER_LOCATION, options=chrome_options)
wait = WebDriverWait(driver, 10)

driver.get(URL)

# Click Sign in Button
try:
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/nav/div/a[2]')))
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
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(3)
    try:
        # Click Apply Button
        apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button")))
        apply_button.click()
        time.sleep(2)

        while True:
            try:
                # Click Next or Submit button
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next')]")))
                next_button.click()
                time.sleep(2)

                review_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Review')]")))
                review_button.click()
                time.sleep(2)

                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Submit application')]")))
                print("Submitting job application")
                submit_button.click()
                break

            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                print(f"Exception occurred: {str(e)}")
                abort_application(driver)
                break

        time.sleep(2)
        # Click Close Button
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Exception occurred: {str(e)}")
        abort_application(driver)
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()
