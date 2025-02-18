import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QPushButton, QInputDialog, QLineEdit, QVBoxLayout, QWidget, QFormLayout, QLabel, QDialog, QDialogButtonBox, QTableWidget, QHeaderView,QLabel
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal
import requests
from PyQt5.QtGui import QBrush, QColor, QTextDocument
import os
from requests.auth import HTTPProxyAuth
import ChromeWork
import psutil


class BrowserThread(QThread):
    browser_closed = pyqtSignal()  # Сигнал для уведомления о закрытии браузера

    def __init__(self, profile_path, proxy, parent=None):
        super().__init__(parent)
        self.profile_path = profile_path
        self.proxy = proxy
        self.driver = None


    def run(self):
        try:
            # Настройка браузера
            self.driver = ChromeWork.launch_browser_with_profile(self.profile_path, self.proxy)
            # Открываем тестовую страницу
            self.driver.get("https://nowsecure.nl")

            # Ждем закрытия браузера
            self.driver.service.process.wait()  # Ожидаем завершения процесса браузера
        except Exception as e:
            print(f"Ошибка в потоке браузера: {e}")
        finally:
            # Сигнал о закрытии браузера
            self.browser_closed.emit()


class ProxyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки прокси")

        # Разметка для формы
        self.layout = QFormLayout(self)

        # Поля для ввода данных
        self.ip_input = QLineEdit(self)
        self.port_input = QLineEdit(self)
        self.login_input = QLineEdit(self)
        self.password_input = QLineEdit(self)

        # Устанавливаем тип для пароля
        self.password_input.setEchoMode(QLineEdit.Password)

        # Добавляем поля в форму
        self.layout.addRow("IP:", self.ip_input)
        self.layout.addRow("Порт:", self.port_input)
        self.layout.addRow("Логин:", self.login_input)
        self.layout.addRow("Пароль:", self.password_input)

        # Кнопки для диалога (ОК, Отмена)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addRow(self.buttons)

        # Подключаем кнопки
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_proxy_data(self):
        """ Возвращаем данные из полей """
        return self.ip_input.text(), self.port_input.text(), self.login_input.text(), self.password_input.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем интерфейс из .ui файла
        loadUi("mainwindow.ui", self)

        # Настроим таблицу
        self.tableWidget.setRowCount(3)  # Пример: 3 строки
        self.tableWidget.setColumnCount(5)  # Пример: 5 колонок
        self.tableWidget.setHorizontalHeaderLabels(['', 'Имя', 'Прокси', 'Статус', ''])

        # Устанавливаем фиксированные размеры для столбцов
        self.set_column_widths()

        # Отключаем возможность изменения размеров строк и столбцов
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Запрещаем изменение ширины столбцов
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Запрещаем изменение высоты строк

        # Включаем отображение сетки (границ) таблицы
        self.tableWidget.setShowGrid(False)

        # Устанавливаем границы ячеек через стиль CSS

        self.setStyleSheet("""
                         QMainWindow {
                             background-color: #2E3440;
                         }
                         QPushButton {
                             background-color: #5E81AC;
                             color: white;
                             border-radius: 8px;
                             padding: 5px;
                         }
                         QPushButton:hover {
                             background-color: #81A1C1;
                         }
                         QTableWidget {
                             background-color: #3B4252;
                             color: white;
                             border: none;
                             gridline-color: #4C566A;
                         }
                         QHeaderView::section {
                             background-color: #4C566A;
                             color: white;
                             padding: 5px;
                             border: none;
                         }
                     """)
        # Заполняем таблицу
        self.fill_table("./profiles")

        # Подключаем кнопку "Новый профиль" к обработчику
        self.newProfile.clicked.connect(self.new_profile)

        # Подключаем обработчик клика на ячейки
        self.tableWidget.cellClicked.connect(self.on_cell_click)

    def set_column_widths(self):
        """ Устанавливаем фиксированную ширину для каждого столбца """
        self.tableWidget.setColumnWidth(0, 10)  # Ширина первого столбца
        self.tableWidget.setColumnWidth(1, 600)  # Ширина второго столбца
        self.tableWidget.setColumnWidth(2, 200)  # Ширина третьего столбца
        self.tableWidget.setColumnWidth(3, 200)  # Ширина четвертого столбца
        self.tableWidget.setColumnWidth(4, 150)  # Ширина пятого столбца

        # Устанавливаем фиксированную высоту строк
        self.tableWidget.setRowHeight(0, 40)
        self.tableWidget.setRowHeight(1, 40)
        self.tableWidget.setRowHeight(2, 40)

    def fill_table(self, directory_path):
        # Получаем список папок в указанной директории
        try:
            folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        except Exception as e:
            print(f"Ошибка при получении списка папок: {e}")
            return

        # Очищаем таблицу перед добавлением новых данных
        self.tableWidget.setRowCount(0)

        # Для каждой папки создаем строку в таблице
        for row, folder in enumerate(folders):
            # Добавляем новую строку в таблицу
            self.tableWidget.insertRow(row)

            # Добавляем QCheckBox в первую колонку
            checkbox = QCheckBox()
            self.tableWidget.setCellWidget(row, 0, checkbox)

            # Записываем название папки в ячейку 1
            item1 = QTableWidgetItem(folder)
            item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование текста
            self.tableWidget.setItem(row, 1, item1)

            # Чтение данных из файла ProxySettings.txt в папке
            proxy_settings_file = os.path.join(directory_path, folder, "ProxySettings.txt")
            item2 = QTableWidgetItem("Нет данных")  # Заполняем строку значением по умолчанию

            ip_port = None
            login, password = None, None

            if os.path.exists(proxy_settings_file):
                try:
                    with open(proxy_settings_file, "r") as f:
                        proxy_data = f.readlines()

                        # Инициализация переменных
                        ip = None
                        port = None
                        login = None
                        password = None

                        # Проходим по каждой строке и извлекаем нужные данные
                        for line in proxy_data:
                            line = line.strip()  # Убираем лишние пробелы

                            # Проверяем и извлекаем данные по меткам
                            if line.startswith("IP:"):
                                ip = line.split(":", 1)[1].strip()  # Получаем IP
                            elif line.startswith("Порт:"):
                                port = line.split(":", 1)[1].strip()  # Получаем порт
                            elif line.startswith("Логин:"):
                                login = line.split(":", 1)[1].strip()  # Получаем логин
                            elif line.startswith("Пароль:"):
                                password = line.split(":", 1)[1].strip()  # Получаем пароль

                        print(ip, port, login, password)
                except Exception as e:
                    print(f"Ошибка при чтении файла {proxy_settings_file}: {e}")
                    ip_port = "Ошибка при чтении файла"

            if ip_port:
                item2.setText(ip+":"+port)  # Устанавливаем только IP:Port

            item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование текста
            self.tableWidget.setItem(row, 2, item2)

            # Добавляем другие данные в ячейки (например, для 3-го столбца)
            item3 = QTableWidgetItem(f"Данные 3 для {folder}")
            item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 3, item3)

            # Добавляем QPushButton в пятую колонку
            button = QPushButton(f"Открыть")
            button.setFixedSize(120, 30)
            self.tableWidget.setCellWidget(row, 4, button)
            button.clicked.connect(lambda _, folder=folder: self.on_button_click(folder,ip+":"+port))
            # Сохраняем данные прокси
            if ip and port and login and password:
               # proxy_status = self.check_proxy_connection( ip, port, login, password)


                # Обновляем ячейку в таблице с данными прокси
                proxy_item = QTableWidgetItem(ip+":"+port)

                # Устанавливаем цвет текста в зависимости от статуса
               # if proxy_status == "success":
                #    proxy_item.setForeground(QColor("green"))  # Зеленый цвет для успешного подключения
              #  else:
                #    proxy_item.setForeground(QColor("red"))  # Красный цвет для ошибки

                # Обновляем таблицу с новой ячейкой
                self.tableWidget.setItem(row, 2, proxy_item)


    def on_cell_click(self, row, column):
        if column == 2:  # Проверяем, если это 3-й столбец
            # Получаем имя профиля из 1-го столбца (где указано имя)
            profile_name = self.tableWidget.item(row, 1).text()

            # Создаем диалог для ввода данных прокси
            dialog = ProxyDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                ip, port, login, password = dialog.get_proxy_data()

                # Формируем строку "IP:Port"
                proxy_info = f"{ip}:{port}"
                print(ip, port, login, password)

                # Проверка подключения через прокси
                proxy_status = self.check_proxy_connection(ip, port, login, password)

                # Обновляем ячейку в таблице с данными прокси
                proxy_item = QTableWidgetItem(proxy_info)

                # Устанавливаем цвет текста в зависимости от статуса
                if proxy_status == "success":
                    proxy_item.setForeground(QColor("green"))  # Зеленый цвет для успешного подключения
                else:
                    proxy_item.setForeground(QColor("red"))  # Красный цвет для ошибки

                # Обновляем таблицу с новой ячейкой
                self.tableWidget.setItem(row, 2, proxy_item)

                # Сохраняем настройки в файл (если необходимо)
                self.save_proxy_settings(profile_name, ip, port, login, password)

    def check_proxy_connection(self, ip, port, login, password):
        """ Проверка подключения через прокси с логином и паролем """

        print(ip, port, login, password)
        try:
            # Формируем строку для прокси
            proxy = {
                "http": f"http://{ip}:{port}",
                "https": f"http://{ip}:{port}",
            }

            # Настройка авторизации для прокси
            # Важно: HTTPProxyAuth использует кодировку latin-1
            auth = HTTPProxyAuth(login, password)

            # Добавляем небольшую задержку для стабильности
            time.sleep(2)

            # Проверка подключения
            response = requests.get("http://www.google.com", proxies=proxy, auth=auth, timeout=15)

            # Если ответ успешный
            if response.status_code == 200:
                print("success")
                return "success"
            else:
                print(f"failure (HTTP {response.status_code})")
                return f"failure (HTTP {response.status_code})"

        except requests.RequestException as e:
            # Выводим исключение для отладки
            print(f"Error occurred: {e}")
            return "failure"
    def save_proxy_settings(self, profile_name, ip, port, login, password):
        """ Сохраняем настройки прокси в файл ProxySettings.txt """
        directory = os.path.join(os.getcwd(),"./profiles/" +profile_name)
        proxy_file_path = os.path.join(directory, "ProxySettings.txt")

        with open(proxy_file_path, 'w') as f:
            f.write(f"IP: {ip}\n")
            f.write(f"Порт: {port}\n")
            f.write(f"Логин: {login}\n")
            f.write(f"Пароль: {password}\n")

        print(f"Настройки прокси сохранены в файл '{proxy_file_path}'.")
    def new_profile(self):

        # Появляется диалог для ввода имени
        name, ok = QInputDialog.getText(self, "Новый профиль", "Введите имя профиля:")

        if ok and name:
            # Путь для создания новой папки
            directory = f"./profiles/{name}"
            chrome_directory = os.path.join(directory, "chrome")



            # Создаем папку chrome внутри профиля

            # Создаем папку, если она не существует
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Папка '{name}' успешно создана.")
                if not os.path.exists(chrome_directory):
                    os.makedirs(chrome_directory)
                    print(f"Папка 'chrome' для профиля '{name}' успешно создана.")

                # Добавляем новую строку в таблицу
                row = self.tableWidget.rowCount()  # Получаем количество строк в таблице
                self.tableWidget.insertRow(row)  # Добавляем новую строку

                # Вставляем данные в ячейки новой строки
                checkbox = QCheckBox()
                self.tableWidget.setCellWidget(row, 0, checkbox)

                item1 = QTableWidgetItem(name)  # Используем имя для первой ячейки
                item2 = QTableWidgetItem("Не подключен")
                item3 = QTableWidgetItem("active")

                # Запрещаем редактирование текста в этих ячейках
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)

                self.tableWidget.setItem(row, 1, item1)
                self.tableWidget.setItem(row, 2, item2)
                self.tableWidget.setItem(row, 3, item3)

                button = QPushButton(f"Button")
                button.setFixedSize(120, 30)  # Размер кнопки
                self.tableWidget.setCellWidget(row, 4, button)

                print(f"Новая строка добавлена в таблицу для профиля '{name}'.")
            else:
                print(f"Папка '{name}' уже существует.")

    def on_button_click(self, folder,proxy):
        """ Обработчик нажатия на кнопку """
        print(f"Кнопка для профиля {folder} была нажата.")
        if os.path.exists("./profiles/"+ folder+"/ProxySettings.txt"):
            try:
                with open("./profiles/"+ folder+"/ProxySettings.txt", "r") as f:
                    proxy_data = f.readlines()

                    # Инициализация переменных
                    ip = None
                    port = None
                    login = None
                    password = None

                    # Проходим по каждой строке и извлекаем нужные данные
                    for line in proxy_data:
                        line = line.strip()  # Убираем лишние пробелы

                        # Проверяем и извлекаем данные по меткам
                        if line.startswith("IP:"):
                            ip = line.split(":", 1)[1].strip()  # Получаем IP
                        elif line.startswith("Порт:"):
                            port = line.split(":", 1)[1].strip()  # Получаем порт
                        elif line.startswith("Логин:"):
                            login = line.split(":", 1)[1].strip()  # Получаем логин
                        elif line.startswith("Пароль:"):
                            password = line.split(":", 1)[1].strip()  # Получаем пароль

                    print(ip, port, login, password)
            except Exception as e:
                print(f"Ошибка при чтении файла {"./profiles/"+ folder+"/ProxySettings.txt"}: {e}")
                ip_port = "Ошибка при чтении файла"
        # Тут можно добавить логику для открытия папки или выполнения других действий.
        folder_path = "./profiles/"+ folder+"/chrome"
        pr=ip+":"+port
        absolute_folder_path = os.path.abspath(folder_path)

        self.browser_thread = BrowserThread(absolute_folder_path,  pr, self)
        self.browser_thread.browser_closed.connect(self.on_browser_closed)
        self.browser_thread.start()

    def on_browser_closed(self):
        """ Обработчик завершения работы браузера """
        print("Браузер был закрыт.")