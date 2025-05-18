from PySide6.QtWidgets import QMainWindow, QDateEdit, QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QComboBox, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from sqlalchemy import or_
from db import Session, Order, Type_oboryd, Type_neispravnosti, Status

class AddDialog(QDialog):
    #Метод для создания интерфейса
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Добавление заявки")
        self.setMinimumSize(600, 700)
        self.setWindowIcon(QIcon("./Мастер пол.ico"))
        session = Session()
        
        layout = QVBoxLayout()


        self.date_i = QDateEdit()
        self.date_i.setCalendarPopup(True)
        self.date_i.setDate(QDate.currentDate())


        self.oboryd_i = QComboBox()
        for o in session.query(Type_oboryd).all():
            self.oboryd_i.addItem(o.name, o.id)
        self.neisprav_i = QComboBox()
        for n in session.query(Type_neispravnosti):
            self.neisprav_i.addItem(n.name, n.id)
        self.description_i = QLineEdit(placeholderText="Описание")
        self.last_name_i = QLineEdit(placeholderText="Фамилия")
        self.name_i = QLineEdit(placeholderText="Имя")
        self.patronymic_i = QLineEdit(placeholderText="Отчество")
        self.status_i = QComboBox()
        for s in session.query(Status).all():
            self.status_i.addItem(s.name, s.id)
            
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_order)
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
            
        for w in [self.date_i, self.oboryd_i, self.neisprav_i, self.description_i, self.last_name_i, self.name_i, self.patronymic_i, self.status_i, self.btn_add, self.btn_cancel]:
            layout.addWidget(w)
            
        self.setLayout(layout)
        
        
# Метод для добавления
    def add_order(self):
        try:
            session = Session()
            order = Order(
                date = self.date_i.date().toPython(),
                oboryd_id = self.oboryd_i.currentData(),
                type_neisprav_id = self.neisprav_i.currentData(),
                description = self.description_i.text(),
                last_name = self.last_name_i.text(),
                name = self.name_i.text(),
                patronymic = self.patronymic_i.text(),
                status_id = self.status_i.currentData()
            )
            session.add(order)
            session.commit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {e}")