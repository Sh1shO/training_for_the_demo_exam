from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon
from db import Session, User, Group

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Пользователи")
        self.setWindowIcon(QIcon("./logo.jpg"))
        self.setMinimumSize(1024, 720)

        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        zag_container = QWidget()
        zag_layout = QHBoxLayout()
        zag_container.setLayout(zag_layout)
        main_layout.addWidget(zag_container)

        control_container = QWidget()
        control_layout = QHBoxLayout()
        control_container.setLayout(control_layout)
        main_layout.addWidget(control_container)

        self.logo = QLabel()
        logo_pixmap = QIcon("./logo.jpg").pixmap(50, 50)
        self.logo.setPixmap(logo_pixmap)
        zag_layout.addWidget(self.logo)

        self.zag = QLabel("Пользователи")
        zag_layout.addWidget(self.zag)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Группа", "Дата"])
        main_layout.addWidget(self.table)

        self.add_btn = QPushButton("Добавить")
        control_layout.addWidget(self.add_btn)
        self.edit_btn = QPushButton("Редактировать")
        control_layout.addWidget(self.edit_btn)

        self.load_data()


    def load_data(self):
        session = Session()
        query = session.query(User)

        users = query.all()
        self.table.setRowCount(len(users))
        for row, u in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(u.last_name))
            self.table.setItem(row, 1, QTableWidgetItem(u.name))
            self.table.setItem(row, 2, QTableWidgetItem(u.patronymic))
            self.table.setItem(row, 3, QTableWidgetItem(u.group.name))
            self.table.setItem(row, 4, QTableWidgetItem(str(u.date)))