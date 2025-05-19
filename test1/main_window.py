from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon
from db import Session, User, Group
from add_dialog import AddDialog
from edit_dialog import EditDialog

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
        self.zag.setObjectName("zag")
        zag_layout.addWidget(self.zag)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Группа", "Дата", "ID"])
        self.table.setColumnHidden(5, True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_user)
        control_layout.addWidget(self.add_btn)
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_user)
        control_layout.addWidget(self.edit_btn)

        self.load_data()

    def load_data(self):
        session = Session()
        query = session.query(User).order_by(User.id)

        users = query.all()
        self.table.setRowCount(len(users))
        for row, u in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(u.last_name))
            self.table.setItem(row, 1, QTableWidgetItem(u.name))
            self.table.setItem(row, 2, QTableWidgetItem(u.patronymic))
            self.table.setItem(row, 3, QTableWidgetItem(u.group.name))
            self.table.setItem(row, 4, QTableWidgetItem(str(u.date)))
            self.table.setItem(row, 5, QTableWidgetItem(str(u.id)))
    
    def add_user(self):
        dialog = AddDialog(self)
        if dialog.exec():
            self.load_data()

    def edit_user(self):
        row = self.table.currentRow()
        if row <0:
            return
        us_id = self.table.item(row, 5).text()
        session = Session()
        user = session.query(User).get(us_id)
        if user:
            dialog = EditDialog(user, self)
            if dialog.exec():
                self.load_data()
