from PySide6.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
from PySide6.QtGui import QIcon
from sqlalchemy import or_
from add_dialog import AddDialog
from edit_dialog import EditDialog
from db import Session, Order

class MainWindow(QMainWindow):
    # Метод для интерфейса основного окна
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тут должно быть НАЗВАНИЕ")
        self.setWindowIcon(QIcon("./Мастер пол.ico"))
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
        logo_pixmap = QIcon("./000.jpg").pixmap(50, 50)
        self.logo.setPixmap(logo_pixmap)
        self.zag = QLabel("Zagolovok")
        self.zag.setObjectName("zag")
        zag_layout.addWidget(self.logo)
        zag_layout.addWidget(self.zag)
        

        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Дата", "Оборудование", "Неисправность", "Описание", "Фамилия", "Имя", "Отчество", "Статус"])
        main_layout.addWidget(self.table)
        
        
        self.search = QLineEdit(placeholderText="Поиск по клиенту...")
        self.search.textChanged.connect(self.load_data)
        control_layout.addWidget(self.search)
        
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_dialog)
        control_layout.addWidget(self.btn_add)
        
        self.btn_edit = QPushButton("Редактировать")
        self.btn_edit.clicked.connect(self.edit_dialog)
        control_layout.addWidget(self.btn_edit)
        
        
        self.load_data()
    
    # Метод для отображения таблицы
    def load_data(self):
        session = Session()
        query = session.query(Order)
        
        search_i = self.search.text().lower()
        if search_i:
            query = query.filter(or_(
                Order.last_name.ilike(f"%{search_i}%"),
                Order.name.ilike(f"%{search_i}%"),
                Order.patronymic.ilike(f"%{search_i}%")
            ))
        
        orders = query.all()
        self.table.setRowCount(len(orders))
        for row, ord in enumerate(orders):
            self.table.setItem(row, 0, QTableWidgetItem(str(ord.date)))
            self.table.setItem(row, 1, QTableWidgetItem(ord.oboryd.name))
            self.table.setItem(row, 2, QTableWidgetItem(ord.neisprav.name))
            self.table.setItem(row, 3, QTableWidgetItem(ord.description))
            self.table.setItem(row, 4, QTableWidgetItem(ord.last_name))
            self.table.setItem(row, 5, QTableWidgetItem(ord.name))
            self.table.setItem(row, 6, QTableWidgetItem(ord.patronymic))
            self.table.setItem(row, 7, QTableWidgetItem(ord.status.name))
            
    # Метод для вызова диалога добавления
    def add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec():
            self.load_data()
            
    # Метод для вызова диалога редактирования   
    def edit_dialog(self):
        dialog = EditDialog(self)
        if dialog.exec():
            self.load_data()

        