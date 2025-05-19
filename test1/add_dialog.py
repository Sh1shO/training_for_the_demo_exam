from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLineEdit, QComboBox, QDateEdit, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from db import Session, Group, User

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        session = Session()

        self.setWindowTitle("Добавление")

        self.setWindowIcon(QIcon("./logo.jpg"))

        layout = QVBoxLayout()

        self.last_name_i = QLineEdit(placeholderText="Фамилия")
        self.name_i = QLineEdit(placeholderText="Имя")
        self.patronymic_i = QLineEdit(placeholderText="Отчество")

        self.group_c_i = QComboBox()
        for g in session.query(Group).all():
            self.group_c_i.addItem(g.name, g.id)
        
        self.date_i = QDateEdit()
        self.date_i.setCalendarPopup(True)
        self.date_i.setDate(QDate.currentDate())

        
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_user)
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)

        for w in [self.last_name_i, self.name_i, self.patronymic_i, self.group_c_i, self.date_i, self.btn_add, self.btn_cancel]:
            layout.addWidget(w)
        
        self.setLayout(layout)

    def add_user(self):
        session = Session()
        user = User(
            last_name = self.last_name_i.text(),
            name = self.name_i.text(),
            patronymic = self.patronymic_i.text(),
            group_id = self.group_c_i.currentData(),
            date = self.date_i.date().toPython()
        )
        session.add(user)
        session.commit()
        self.accept()
        QMessageBox.information(self, "Успешно", "Пользователь успешно добавлен!")
        

