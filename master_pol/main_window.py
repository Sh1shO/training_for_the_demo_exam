from sqlalchemy import or_
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import Qt
from db import Session, Product, Material_type
from add_dialog import AddDialog
from edit_dialog import EditDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Master pol")
        self.setMinimumSize(1024, 720)
        self.setWindowIcon(QIcon("./logo.png"))
        
        container = QWidget()
        container.setStyleSheet("background: #FFFFFF;")
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        zag_layout = QHBoxLayout()
        main_layout.addLayout(zag_layout)
        main_layout.addLayout(control_layout)
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.logo = QLabel()
        logo_pixmap = QIcon("./logo.png").pixmap(50,50)
        self.logo.setAlignment(Qt.AlignRight)
        self.logo.setPixmap(logo_pixmap)
        zag_layout.addWidget(self.logo)
        self.zag = QLabel("Products")
        font = QFont("Segoe UI", 20)
        self.zag.setFont(font)
        zag_layout.addWidget(self.zag)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "min price", "material_type"])
        main_layout.addWidget(self.table)
        
        self.search = QLineEdit(placeholderText="Search...")
        self.search.textChanged.connect(self.load_data)
        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add_dialog)

        self.button_edit = QPushButton("Edit")
        self.button_edit.clicked.connect(self.edit_dialog)
        self.button_delete = QPushButton("Delete")
        
        self.material = QComboBox()
        self.material.addItem("All materials")
        self.material.currentIndexChanged.connect(self.load_data)
        session = Session()
        for m in session.query(Material_type).all():
            self.material.addItem(m.type, m.id)

        for w in [self.material, self.search, self.button_delete, self.button_add, self.button_edit]:
            w.setStyleSheet('background-color: #F4E8D3;padding:10 15; color: white')
            control_layout.addWidget(w)
            
      
        
        self.load_data()

    def load_data(self):
        session = Session()
        query = session.query(Product)
        
        search_i = self.search.text().lower()
        if search_i:
            query = query.filter(or_(
                Product.name.ilike(f"%{search_i}%")
            ))
        
        material_filter = self.material.currentData()
        if material_filter:
            query = query.filter(Product.material_type_id == material_filter)
        
        products = query.all()
        self.table.setRowCount(len(products))
        for row, p in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(p.name))
            self.table.setItem(row, 1, QTableWidgetItem(p.min_price))
            self.table.setItem(row, 2, QTableWidgetItem(p.material.type))
            
    def add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec():
            self.load_data()
            
    def edit_dialog(self):
        product_id = self,
        
    
