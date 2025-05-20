from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QMessageBox
from PySide6.QtGui import QIcon
from db import Session, Product, Product_type, Material_type

class EditDialog(QDialog):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить")
        self.setWindowIcon(QIcon("./logo.jpg"))
        self.product = product
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

        self.type_product_i.setCurrentIndex(self.type_product_i.findData(product.type_product_id))
        self.name_i.setText(product.name)
        self.articul_i.setText(product.articul)
        self.min_price_i.setText(str(product.min_price))
        self.type_material_i.setCurrentIndex(self.type_material_i.findData(product.material_type_id))

        self.add_btn = QPushButton("Сохранить")
        self.add_btn.clicked.connect(self.edit_product)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        for w in [self.type_material_i, self.name_i, self.articul_i, self.min_price_i, self.type_material_i, self.add_btn, self.cancel_btn]:
            layout.addWidget(w)

        self.setLayout(layout)

    def edit_product(self):
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите изменить данные?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        try:
            session = Session()
            product = session.query(Product).get(self.product.id)

            product.type_product_id = self.type_product_i.currentData()
            product.name = self.name_i.text()
            product.articul = self.articul_i.text()
            product.min_price = float(self.min_price_i.text())
            product.material_type_id = self.type_material_i.currentData()

            session.commit()
            self.accept()
            QMessageBox.information(self, "Успех!", "Данные успешно изменены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"{e}")


        

        
