from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon
from sqlalchemy import or_
from db1 import Session, Product_type, Product
from add_dialog import AddDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мастер пол")
        self.setMinimumSize(1024, 720)
        self.setWindowIcon(QIcon("./logo.png"))

        main_container = QWidget()
        main_container.setObjectName("main_container")
        main_layout = QVBoxLayout()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        control_container = QWidget()
        control_container.setObjectName("control_container")
        control_layout = QHBoxLayout()
        control_container.setLayout(control_layout)
        main_layout.addWidget(control_container)

        self.search_line = QLineEdit(placeholderText="Search...")
        self.search_line.textChanged.connect(self.load_data)
        self.filter = QComboBox()
        self.filter.addItem("All products")
        self.filter.currentIndexChanged.connect(self.load_data)

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.load_add_dialog)
        self.edit_btn = QPushButton("Edit")
        self.del_btn = QPushButton("Delete")

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Название", "Тип продукта"])
        main_layout.addWidget(self.table)

        for widgets in [self.search_line, self.filter, self.add_btn, self.del_btn, self.edit_btn]:
            control_layout.addWidget(widgets)

        self.load_data()
        self.filter_product_type()

    def filter_product_type(self):
        session = Session()
        for p in session.query(Product_type).all():
            self.filter.addItem(p.type, p.id)
        
    def load_data(self):
        session = Session()
        query = session.query(Product)

        selected_product_type_id = self.filter.currentData()
        if selected_product_type_id:
            query = query.filter(Product.type_product_id == selected_product_type_id)

        search_i = self.search_line.text().lower()
        if search_i:
            query = query.filter(or_(
                Product.name.ilike(f"%{search_i}%")
            ))


        products = query.all()
        self.table.setRowCount(len(products))
        for row, p in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(p.name))
            self.table.setItem(row, 1, QTableWidgetItem(p.type.type))
        

    def load_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec():
            self.load_data()




