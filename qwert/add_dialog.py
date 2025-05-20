from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QMessageBox
from PySide6.QtGui import QIcon
from db import Session, Product, Product_type, Material_type

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить")
        self.setWindowIcon(QIcon("./logo.jpg"))
        session = Session()

        layout = QVBoxLayout()

        self.type_product_i = QComboBox()
        for tp in session.query(Product_type).all():
            self.type_product_i.addItem(tp.type, tp.id)
        self.name_i = QLineEdit(placeholderText="Название")
        self.articul_i = QLineEdit(placeholderText="Артикул")
        self.min_price_i = QLineEdit(placeholderText="Мин цена")
        self.type_material_i = QComboBox()
        for tm in session.query(Material_type).all():
            self.type_material_i.addItem(tm.type, tm.id)
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_product)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        for w in [self.type_material_i, self.name_i, self.articul_i, self.min_price_i, self.type_material_i, self.add_btn, self.cancel_btn]:
            layout.addWidget(w)

        self.setLayout(layout)

    def add_product(self):
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите добавить?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        try:
            session = Session()
            product = Product(
                type_product_id = self.type_product_i.currentData(),
                name = self.name_i.text(),
                articul = self.articul_i.text(),
                min_price = self.min_price_i.text(),
                material_type_id = self.type_material_i.currentData()
            )
            session.add(product)
            session.commit()
            self.accept()
            QMessageBox.information(self, "Успех!", "Данные успешно добавлены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"{e}")
