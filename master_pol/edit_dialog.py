from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from PySide6.QtGui import QIcon
from db import Session, Product, Material_type

class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Edit")
        self.setMinimumSize(500, 500)
        self.setWindowIcon(QIcon("./logo.png"))
        
        layout = QVBoxLayout()
        
        self.name_i = QLineEdit(placeholderText="Name")
        layout.addWidget(self.name_i)
        self.min_price_i = QLineEdit(placeholderText="Min price")
        layout.addWidget(self.min_price_i)
        
        self.material_i = QComboBox()
        session = Session()
        for m in session.query(Material_type).all():
            self.material_i.addItem(m.type, m.id)
        layout.addWidget(self.material_i)
        
        self.btn_add = QPushButton("Edit")
        self.btn_add.clicked.connect(self.save_product)
        layout.addWidget(self.btn_add)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        layout.addWidget(self.btn_cancel)
        
        layout.addWidget
        self.setLayout(layout)
        
    def save_product(self):
        session = Session()
        
        prod = Product(
            name = self.name_i.text(),
            min_price = self.min_price_i.text(),
            material_type_id = self.material_i.currentData()
        )
        session.commit()
        self.accept()


        
    