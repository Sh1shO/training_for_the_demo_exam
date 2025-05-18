from PySide6.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QComboBox, QMessageBox
from PySide6.QtGui import QIcon
from sqlalchemy import or_
from db import Session, Order, Type_oboryd, Type_neispravnosti, Status, Employee

class EditDialog(QDialog):
    # Метод для интерфейса окна диалога
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Добавление заявки")
        self.setMinimumSize(600, 700)
        self.setWindowIcon(QIcon("./Мастер пол.ico"))
        session = Session()
        
        layout = QVBoxLayout()
        
        self.description_i = QLineEdit(placeholderText="Описание")
        self.last_name_i = QLineEdit(placeholderText="Фамилия")
        self.name_i = QLineEdit(placeholderText="Имя")
        self.patronymic_i = QLineEdit(placeholderText="Отчество")
        self.status_i = QComboBox()
        for s in session.query(Status).all():
            self.status_i.addItem(s.name, s.id)
            
        self.btn_add = QPushButton("Сохранить")
        self.btn_add.clicked.connect(self.edit_order)
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
            
        for w in [self.description_i, self.last_name_i, self.name_i, self.patronymic_i, self.status_i, self.btn_add, self.btn_cancel]:
            layout.addWidget(w)
            
        self.setLayout(layout)
        
        
    # Метод для сохранения при редактировании
    def edit_order(self):
        try:
            session = Session()
            order = Order(
                description = self.description_i.text(),
                status_id = self.status_i.currentData()
            )
            employee = Employee(
                last_name = self.last_name_i.text(),
                name = self.name_i.text(),
                patronymic = self.patronymic_i.text(),
            )
            session.commit()
            self.accept()
        except Exception as e:
            QMessageBox(self, "Ошибка" f"Ошибка при сохранении: {e}")