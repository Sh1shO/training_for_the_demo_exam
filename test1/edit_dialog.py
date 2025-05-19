from PySide6.QtWidgets import QDialog, QLineEdit, QComboBox, QDateEdit, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from db import Session, User, Group

class EditDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование")
        self.setWindowIcon(QIcon("./logo.jpg"))
        self.user = user
        session = Session()

        layout = QVBoxLayout()

        self.last_name_i = QLineEdit()
        self.name_i = QLineEdit()
        self.patronymic_i = QLineEdit()
        self.group_i = QComboBox()
        for g in session.query(Group).all():
            self.group_i.addItem(g.name, g.id)
        self.date_i = QDateEdit()
        self.date_i.setCalendarPopup(True)

        self.last_name_i.setText(user.last_name)
        self.name_i.setText(user.name)
        self.patronymic_i.setText(user.patronymic)
        self.group_i.setCurrentIndex(self.group_i.findData(user.group_id))
        self.date_i.setDate(QDate(self.user.date.year, self.user.date.month, self.user.date.day))

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.save_data)
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)

        for w in [self.last_name_i, self.name_i, self.patronymic_i, self.group_i, self.date_i, self.btn_save, self.btn_cancel]:
            layout.addWidget(w)

        self.setLayout(layout)

    def save_data(self):
        session = Session()
        us = session.query(User).get(self.user.id)

        us.last_name = self.last_name_i.text()
        us.name = self.name_i.text()
        us.patronymic = self.patronymic_i.text()
        us.group_id = self.group_i.currentData()
        us.date = self.date_i.date().toPython()

        session.commit()
        self.accept()
        QMessageBox.information(self, "Уведомление", "Данные изменены")
