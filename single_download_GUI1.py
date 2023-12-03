import os
import sys
import ctypes
import logging
from selenium import webdriver
from main import run_main
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QVBoxLayout, QLabel, QWidget, QProgressBar, QGridLayout, QStyleFactory, \
    QPlainTextEdit
from PyQt5.QtGui import QFont


class WorkerThread(QThread):
    # Указываем сигналу имя для использования при соединении с методом
    progress_update = pyqtSignal(int, bool, name='progressUpdate')
    def __init__(self, max_iterations, run_type):
        super().__init__()
        self.max_iterations = max_iterations
        self.ex = False
        self.run_type = run_type

    def run(self):
        try:
            if self.run_type == 'all':
                for site in input_lists:
                    for href in site:
                        if href is None:
                            continue
                        elif 'forex4you' in href.value:
                            forex4you = Forex4you(
                                current_dir,
                                bd_dir,
                                driver,
                                href,
                                'forex4you',
                                forex4you_xpathes
                            )
                            forex4you.scrap_all()
                        elif 'litefinance' in href.value:
                            litefinance = Lifefinance(
                                current_dir,
                                bd_dir,
                                driver,
                                href,
                                'litefinance',
                                lifefinance_xpathes
                            )
                            litefinance.scrap_all()
                        i = i + 1
                        self.progress_update.emit(i + 1, self.ex)
            elif self.run_type == 'lifefinance':
                for href in litefinance_list:
                    if href is None:
                        continue
                    elif 'litefinance' in href.value:
                        litefinance = Lifefinance(
                            current_dir,
                            bd_dir,
                            driver,
                            href,
                            'litefinance',
                            lifefinance_xpathes
                        )
                        litefinance.scrap_all()
                    i = i + 1
                    self.progress_update.emit(i + 1, self.ex)
            elif self.run_type == 'forex4you':
                for href in forex4you_list:
                    if href is None:
                        continue
                    elif 'forex4you' in href.value:
                        forex4you = Forex4you(
                            current_dir,
                            bd_dir,
                            driver,
                            href,
                            'forex4you',
                            forex4you_xpathes
                        )
                        forex4you.scrap_all()
                    i = i + 1
                    self.progress_update.emit(i + 1, self.ex)
            driver.quit()
        except Exception as error:
            driver.quit()
            self.ex = True
            logging.error(error)
        self.progress_update.emit(0, self.ex)  # Завершаем выполнение операции


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Скачивание сигналов')
        self.setGeometry(300, 300, 200, 300)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        self.show_input_excel_button = QPushButton(
            '   🧾 Открыть excel lifefinance', self)
        self.show_input_excel_button.setStyleSheet("text-align: left;")
        self.show_input_excel_button.setFont(QFont('Arial', 14))
        self.show_input_excel_button.clicked.connect(lambda: open_file(
            "Открываю excel файл, где хранится список ссылок для lifefinance\n",
            rf"{current_dir}\resources\БАЗА ДАННЫХ\litefinance hrefs.xlsx"))
        layout.addWidget(self.show_input_excel_button)

        self.show_input_excel_button1 = QPushButton(
            '   🧾 Открыть excel forex4you', self)
        self.show_input_excel_button1.setStyleSheet("text-align: left;")
        self.show_input_excel_button1.setFont(QFont('Arial', 14))
        self.show_input_excel_button1.clicked.connect(lambda: open_file(
            "Открываю excel файл, где хранится список ссылок для forex4you\n",
            rf"{current_dir}\resources\БАЗА ДАННЫХ\forex4you hrefs.xlsx"))
        layout.addWidget(self.show_input_excel_button1)

        self.show_log_button = QPushButton('   🧾 Открыть логи', self)
        self.show_log_button.setStyleSheet("text-align: left;")
        self.show_log_button.setFont(QFont('Arial', 14))
        self.show_log_button.clicked.connect(lambda: open_file(
            "Открываю log файл, где хранятся ошибки работы робота",
            rf"{current_dir}\main.log"))
        layout.addWidget(self.show_log_button)

        self.show_output_excel_button = QPushButton(
            '   📁 Открыть папку lifefinance', self)
        self.show_output_excel_button.setFont(QFont('Arial', 14))
        self.show_output_excel_button.setStyleSheet("text-align: left;")
        self.show_output_excel_button.clicked.connect(lambda: open_folder(
            "Открываю директорию, где хранятся сформированные файлы excel\n",
            rf"explorer.exe {current_dir}\resources\БАЗА ДАННЫХ\litefinance"))
        layout.addWidget(self.show_output_excel_button)

        self.show_output_htm_button = QPushButton(
            '   📂 Открыть папку forex4you', self)
        self.show_output_htm_button.setFont(QFont('Arial', 14))
        self.show_output_htm_button.setStyleSheet("text-align: left;")
        self.show_output_htm_button.clicked.connect(lambda: open_folder(
            "Открываю директорию, где хранятся сформированные файлы htm\n",
            fr"explorer.exe {current_dir}\resources\БАЗА ДАННЫХ\forex4you"))
        layout.addWidget(self.show_output_htm_button)

        self.label = QLabel('Ожидаю запуск')
        self.label.setFont(QFont('Arial', 14))
        layout.addWidget(self.label)

        self.progress_bar_loading = QProgressBar(self)
        self.progress_bar_loading.setFont(QFont('Arial', 14))
        self.progress_bar_loading.setVisible(False)
        layout.addWidget(self.progress_bar_loading)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton('🚀 Общий запуск', self)
        self.start_button.setFont(QFont('Arial', 14))
        self.start_button.clicked.connect(self.run_all)
        layout.addWidget(self.start_button)

        self.start_button_lifefanance = QPushButton('🚀 Запуск только lifefinance', self)
        self.start_button_lifefanance.setFont(QFont('Arial', 14))
        self.start_button_lifefanance.clicked.connect(self.run_lifefinance)
        layout.addWidget(self.start_button_lifefanance)

        self.start_button_forex4you = QPushButton(
            '🚀 Запуск только forex4you', self)
        self.start_button_forex4you.setFont(QFont('Arial', 14))
        self.start_button_forex4you.clicked.connect(self.run_forex4you)
        layout.addWidget(self.start_button_forex4you)

        self.setCentralWidget(self.widget)

    def run_all(self):
        max_iterations = len(litefinance_list) + len(forex4you_list)
        self.progress_bar.setMaximum(max_iterations)
        self.start_operation(max_iterations, 'all')

    def run_lifefinance(self):
        max_iterations = len(litefinance_list)
        self.progress_bar.setMaximum(max_iterations)
        self.start_operation(max_iterations, 'lifefinance')

    def run_forex4you(self):
        max_iterations = len(forex4you_list)
        self.progress_bar.setMaximum(max_iterations)
        self.start_operation(max_iterations, 'forex4you')

    def start_operation(self, max_iterations, run_type):
        self.label.setText('Процесс выполняется...')
        self.progress_bar_loading.setVisible(True)
        self.progress_bar_loading.setRange(0, 0)
        self.widget.setEnabled(False)  # Блокируем кнопки
        self.worker_thread = WorkerThread(max_iterations, run_type)
        self.worker_thread.progressUpdate.connect(
        self.update_progress)  # Соединяем сигнал с обработчиком
        self.worker_thread.finished.connect(
        self.operation_completed)  # Соединяем сигнал о завершении с методом
        self.worker_thread.start()


    def update_progress(self, value, ex):
        self.progress_bar.setValue(value)
        self.progress_bar_loading.setVisible(False)
        if value == 0 and ex is False:
            self.label.setText('✅ Процесс завершен успешно')
        elif value == 0 and ex is True:
            self.label.setText('Процесс завершен с ошибкой. \nПроверьте логи!')

    def operation_completed(self):
        self.widget.setEnabled(True)  # Разблокируем кнопки


def open_file(msg, path):
    print(msg)
    os.startfile(path)


def open_folder(msg, path):
    print(msg)
    os.system(path)


def clean_folder(msg, folder_path):
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)
    print(msg)


console_window = ctypes.windll.kernel32.GetConsoleWindow()
ctypes.windll.user32.ShowWindow(console_window, 6)  # скрываем консоль при запуске из батника

current_dir = os.path.dirname(os.path.abspath(__file__))

app = QApplication(sys.argv)
app.setStyle('Fusion')
ex = App()
ex.setFixedSize(670, 860)
ex.show()
sys.exit(app.exec_())