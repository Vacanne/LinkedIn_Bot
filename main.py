from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

URL = LINKED IN JOB LINK (MUST BE EASY APPLY)
YOUR_EMAIL = YOUR_EMAIL
YOUR_PASSWORD = YOUR_PASSWORD
CHROME_DRIVER_LOCATION = YOUR CHROME DRIVER LOCATION


def abort_application():
    # Click Close Button
    close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard Button
    discard_button = driver.find_elements(By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[0]
    discard_button.click()


# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(CHROME_DRIVER_LOCATION, options=chrome_options)

driver.get(URL)

# Click Sign in Button
time.sleep(2)
sign_in_button = driver.find_element(By.XPATH, value='/html/body/div[1]/header/nav/div/a[2]')
sign_in_button.click()

# Sign in
time.sleep(3)
email_field = driver.find_element(By.ID, value="username")
email_field.send_keys(YOUR_EMAIL)
password_field = driver.find_element(By.ID, value="password")
password_field.send_keys(YOUR_PASSWORD)
password_field.send_keys(Keys.ENTER)


# CAPTCHA - Solve Puzzle Manually
input("Press Enter when you have solved the Captcha")

# Get Listings
time.sleep(3)
all_listings = driver.find_elements(By.CSS_SELECTOR, value=".job-card-container--clickable")

# Apply for Jobs
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(5)
    try:
        # Click Apply Button
        apply_button = driver.find_element(By.CSS_SELECTOR, value=".jobs-s-apply button")
        apply_button.click()
        time.sleep(2)
        # Press Next Button
        next_buttonish = driver.find_element(By.CLASS_NAME, value="artdeco-button artdeco-button--2 artdeco-button--primary ember-view")

        next_button = next_buttonish.find_element(By.LINK_TEXT, value='Next')
        next_button.click()
        time.sleep(1)
        second_next_button = driver.find_element(By.CLASS_NAME, value='artdeco-button artdeco-button--2 artdeco-button--primary ember-view')
        second_next_button.click()
        time.sleep(1)
        review_button = driver.find_element(By.CLASS_NAME, value='artdeco-button artdeco-button--2 artdeco-button--primary ember-view')
        review_button.click()
        time.sleep(1)
        # Check the Submit Button
        submit_button = driver.find_element(By.CLASS_NAME, value='artdeco-button__text')
        if submit_button.text != "Submit application":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            # Click Submit Button
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        # Click Close Button
        close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__icon")
        close_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()



# #ember362 //*[@id="ember362"]
# class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view" text = next
