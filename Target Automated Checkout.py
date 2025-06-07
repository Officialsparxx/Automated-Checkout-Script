import traceback
import setuptools
import sys
# Workaround for Python 3.12 missing distutils
sys.modules['distutils'] = setuptools._distutils

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

# === Helper to keep console open on crash ===
def main():
    # === CONFIG ===
    URL      = "https://www.target.com/p/pok-233-mon-scarlet-violet-s10-5-booster-bundle-box-trading-cards/-/A-94681770"
    EMAIL    = "your-email"
    PASSWORD = "your-password"

    # === SETUP ===
    options = uc.ChromeOptions()
    # standard args
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # proper way to exclude the automation switch
    options.exclude_switches = ["enable-automation"]
    # remove Chrome extension fingerprinting
    options.add_argument("--disable-extensions")

    driver = uc.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(URL)

    # === WAIT FOR MANUAL LOGIN ===
    print("Please log in to Target within 30 seconds...")
    time.sleep(30)
    in_cart = False

    # === WATCH & ADD TO CART ===
    while True:
        # 0) Check for throttled banner
        try:
            driver.find_element(
                By.XPATH,
                "//h3[contains(normalize-space(.),'This item is not available')]"
            )
            print("🚫 Throttled—backing off…")
            time.sleep(random.uniform(10, 15))
            driver.refresh()
            continue
        except NoSuchElementException:
            pass

        # 1) Locate live Add-to-Cart
        buttons = driver.find_elements(
            By.CSS_SELECTOR,
            'button[data-test="add-to-cart-button"]:not([disabled])'
        )

        if buttons:
            btn = buttons[0]
            print("🟢 Clicking real Add-to-Cart…")
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", btn)
            btn.click()

            # 2) Verify cart badge
            try:
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR,
                         "button[data-test=cart-button] .vzw-icon__badge"),
                        "1"
                    )
                )
                print("✅ Item added to cart.")
                in_cart = True
                break
            except TimeoutException:
                print("⚠️ Click didn't stick—retrying…")

        # 3) If nothing, pause & refresh
        print("🔴 Still out of stock—refreshing…")
        time.sleep(random.uniform(2.5, 4.0))
        driver.refresh()

    # === PROCEED TO CHECKOUT ===
    if in_cart:
        driver.get("https://www.target.com/co-cart")
        time.sleep(3)
        try:
            checkout = driver.find_element(
                By.XPATH, "//button[normalize-space()='Check out']"
            )
            checkout.click()
            print("✔️ Proceeded to checkout.")
        except NoSuchElementException:
            print("❌ Checkout button not found.")

    # === OPTIONAL LOGIN DURING CHECKOUT ===
    try:
        driver.find_element(By.ID, "username").send_keys(EMAIL)
        driver.find_element(By.ID, "continue").click()
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login").click()
        print("🔑 Logged in at checkout.")
    except NoSuchElementException:
        pass

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print("\nAn error occurred:")
        traceback.print_exc()
        input("Press Enter to exit...")
