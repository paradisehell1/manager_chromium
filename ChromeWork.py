from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import os
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from PyQt5.QtCore import QThread, pyqtSignal
import undetected_chromedriver as uc
def launch_browser_with_profile(profile_path,proxy):
    print(profile_path)
    print(proxy)
    chrome_binary_path = "./chrome/chrome.exe"  # Укажите путь к вашему Chrome

    # Создаем объект Options для указания пути к Chrome
    options = uc.ChromeOptions()
    options.binary_location = chrome_binary_path  # Указываем путь к вашему браузеру

    # Указываем путь к профилю
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default")

    options.add_argument("--disable-popup-blocking")
    options.add_argument(f'--proxy-server={proxy}')

    driver = uc.Chrome( options=options)

    time.sleep(1)

    return driver