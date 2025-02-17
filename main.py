from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QPushButton, QVBoxLayout, QWidget,QHeaderView
from PyQt5.uic import loadUi
import QtForms



if __name__ == "__main__":
    app = QApplication([])
    window = QtForms.MainWindow()
    window.show()
    app.exec_()

    '''
    profile_path = r"D:\incognitonv2\config\02c9cb7f-2863-48d9-9c5f-a5c3a303b085"  # Путь к профилю
    extension_base_path = r"D:\incognitonv2\config\02c9cb7f-2863-48d9-9c5f-a5c3a303b085\Default\Extensions"  # Путь к каталогу с расширениями

    # Находим все расширения в каталоге
    extension_dirs = find_all_extensions(extension_base_path)

    # Список для хранения путей к последним версиям расширений
    latest_extension_paths = []

    for extension_path in extension_dirs:
        # Для каждого расширения ищем последнюю версию
        latest_version_path = find_latest_version(extension_path)
        if latest_version_path:
            latest_extension_paths.append(latest_version_path)

    if latest_extension_paths:
        print(f"Найдено {len(latest_extension_paths)} расширений. Запуск браузера с ними...")

        # Загружаем расширения партиями
        for extension_chunk in load_extensions_in_chunks(latest_extension_paths,
                                                         max_chunk_size=5):  # Пробуем 5 расширений за раз
            print(f"Загружаем {len(extension_chunk)} расширений.")
            driver = launch_browser_with_profile(profile_path, extension_chunk)

            if driver is not None:
                # Ожидаем некоторое время, чтобы браузер загрузил расширения
                time.sleep(5)  # Задержка для стабилизации процесса загрузки расширений

                # Открываем страницу для проверки
                driver.get("https://example.com")
                input("Нажмите Enter для выхода...")
                driver.quit()
            else:
                print("Не удалось запустить браузер с расширениями.")
    else:
        print("Не удалось найти расширения с актуальными версиями.")
        '''
