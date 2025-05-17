from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtGui import QIcon
from db1 import Session, Product, Product_type, Material_type

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add")
        self.setMinimumSize(600, 700)
        self.setWindowIcon(QIcon("./logo.svg"))

        layout = QVBoxLayout()

        self.name_i = QLineEdit(placeholderText="Name")
        layout.addWidget(self.name_i)
        self.type_i = QComboBox()
        session = Session()
        for t in session.query(Product_type).all():
            self.type_i.addItem(t.type, t.id)
        layout.addWidget(self.type_i)
        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.add_product)
        layout.addWidget(self.btn_add)
        self.btn_cancel = QPushButton("Cancel")
        layout.addWidget(self.btn_cancel)
        self.btn_cancel.clicked.connect(self.reject)

        self.setLayout(layout)
        
    def add_product(self):
        session = Session()
        prod = Product(
            name = self.name_i.text(),
            type_product_id = self.type_i.currentData()
        )
        session.add(prod)
        session.commit()
        self.accept()




        