import os
import sys
import ctypes
from typing import Union
from main import run_main
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit, QGridLayout, QPlainTextEdit, \
    QPushButton, QApplication, QWidget, QLabel


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


class App(QWidget):
    show_start_button: Union[QPushButton, QPushButton]

    def __init__(self):
        super().__init__()
        self.title = 'Программа для скачивания сигналов'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 300
        self.initialisation_ui()

    def initialisation_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.date_label = QLabel(self)
        self.date_label.setFixedSize(315, 45)
        self.date_label.setFont(QFont('Arial', 14))
        self.date_label.move(20, 10)
        self.date_label.setText('Выберите дату завершения сделки, '
                                '\nдо которой считывать сигналы:')

        self.work_progress_label = QLabel(self)
        self.work_progress_label.setFixedSize(315, 45)
        self.work_progress_label.setFont(QFont('Arial', 14))
        self.work_progress_label.move(20, 10)
        self.work_progress_label.setText('Процесс не запущен.')

        self.date_edit = QDateEdit(self)
        self.date_edit.setFixedSize(150, 35)
        self.date_edit.setFont(QFont('Arial', 14))
        default_date = QDate.currentDate()
        self.date_edit.setDate(default_date)
        self.date_edit.move(20, 70)
        self.date_edit.setCalendarPopup(True)

        self.show_start_button = QPushButton('🚀 Запуск', self)
        self.show_start_button.setFont(QFont('Arial', 14))
        self.show_start_button.setFixedSize(150, 36)
        self.show_start_button.move(20, 70)
        self.show_start_button.clicked.connect(self.main_proc)

        self.show_input_excel_button = QPushButton('   🧾 Открыть excel со ссылками', self)
        self.show_input_excel_button.setStyleSheet("text-align: left;")
        self.show_input_excel_button.setFont(QFont('Arial', 14))
        self.show_input_excel_button.setFixedSize(315, 36)
        self.show_input_excel_button.move(20, 125)
        self.show_input_excel_button.clicked.connect(lambda: open_file(
            "Открываю excel файл, где хранится список трейдеров, сигналы которых будут считываться.\n",
            rf"{current_dir}\resources\input\input hrefs.xlsx"))

        self.show_output_excel_button = QPushButton('   📁 Открыть папку с excel', self)
        self.show_output_excel_button.setFont(QFont('Arial', 14))
        self.show_output_excel_button.setStyleSheet("text-align: left;")
        self.show_output_excel_button.setFixedSize(315, 36)
        self.show_output_excel_button.move(20, 181)
        self.show_output_excel_button.clicked.connect(lambda: open_folder(
            "Открываю директорию, где хранятся сформированные файлы excel\n",
            rf"explorer.exe {current_dir}\resources\output excel"))

        self.show_output_htm_button = QPushButton('   📂 Открыть папку с htm', self)
        self.show_output_htm_button.setFont(QFont('Arial', 14))
        self.show_output_htm_button.setStyleSheet("text-align: left;")
        self.show_output_htm_button.setFixedSize(315, 36)
        self.show_output_htm_button.move(20, 237)
        self.show_output_htm_button.clicked.connect(lambda: open_folder(
            "Открываю директорию, где хранятся сформированные файлы htm\n",
            fr"explorer.exe {current_dir}\resources\output htm"))

        self.clean_output_htm_button = QPushButton('   🗑️ Очистить папку с htm', self)
        self.clean_output_htm_button.setFont(QFont('Arial', 14))
        self.clean_output_htm_button.setStyleSheet("text-align: left;")
        self.clean_output_htm_button.setFixedSize(315, 36)
        self.clean_output_htm_button.move(20, 237)
        self.clean_output_htm_button.clicked.connect(lambda: clean_folder('🗑️ Папка с htm очищена успешно\n',
                                                                          rf"{current_dir}\resources\output htm"))

        self.clean_output_excel_button = QPushButton('   🗑️ Очистить папку с excel', self)
        self.clean_output_excel_button.setFont(QFont('Arial', 14))
        self.clean_output_excel_button.setStyleSheet("text-align: left;")
        self.clean_output_excel_button.setFixedSize(315, 36)
        self.clean_output_excel_button.move(20, 237)
        self.clean_output_excel_button.clicked.connect(lambda: clean_folder('🗑️ Папка с excel очищена успешно\n',
                                                                            rf"{current_dir}\resources\output excel"))

        self.text_edit = QPlainTextEdit()
        self.text_edit.setFixedSize(650, 600)
        self.text_edit.setFont(QFont('Arial', 14))
        sys.stdout = self

        vbox1 = QGridLayout()
        vbox1.setSpacing(10)

        vbox = QGridLayout()
        vbox.setSpacing(10)
        vbox.addWidget(self.date_label, 0, 0)
        vbox.addLayout(vbox1, 0, 1, 1, 1)
        vbox1.addWidget(self.date_edit, 1, 0)
        vbox1.addWidget(self.show_start_button, 1, 1)
        vbox.addWidget(self.show_input_excel_button, 4, 0)
        vbox.addWidget(self.work_progress_label, 4, 1)
        vbox.addWidget(self.show_output_excel_button, 5, 1)
        vbox.addWidget(self.clean_output_excel_button, 5, 0)
        vbox.addWidget(self.show_output_htm_button, 6, 1)
        vbox.addWidget(self.clean_output_htm_button, 6, 0)
        vbox.addWidget(self.text_edit, 8, 0)
        self.setLayout(vbox)
        self.show()

    def write(self, text):
        self.text_edit.insertPlainText(text)

    def main_proc(self):
        date = self.date_edit.date().toString('dd.MM.yyyy')
        self.date_label.setText('Выбранная дата: ' + date)
        run_main(date)


console_window = ctypes.windll.kernel32.GetConsoleWindow()
ctypes.windll.user32.ShowWindow(console_window, 6)  # скрываем консоль при запуске из батника

current_dir = os.path.dirname(os.path.abspath(__file__))

app = QApplication(sys.argv)
app.setStyle('Fusion')
ex = App()
ex.setFixedSize(670, 860)
ex.show()
sys.exit(app.exec_())
