from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
def start_parse_harpie(driver):
    driver.get(f"chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/popup.html")
    time.sleep(2)
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

    # ¬вести пароль
    password_input.send_keys("Azaza345")
    password_input.send_keys(Keys.RETURN)
    time.sleep(2)

    driver.get(f"https://harpie.io/onboarding/basic/")
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/button").click()