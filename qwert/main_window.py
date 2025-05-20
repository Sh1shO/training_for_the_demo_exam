from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QWidget, QTabWidget, QMessageBox
from PySide6.QtGui import QIcon
from db import Session, Partner_product, Product, Material_type
from sqlalchemy.sql import func
from add_dialog import AddDialog
from edit_dialog import EditDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заказ")
        self.setWindowIcon(QIcon("./logo.jpg"))
        self.setMinimumSize(1024, 720)

        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        zag_container = QWidget()
        zag_layout = QHBoxLayout()
        zag_container.setLayout(zag_layout)
        main_layout.addWidget(zag_container)

        self.logo = QLabel()
        logo_pixmap = QIcon("./logo.jpg").pixmap(50, 50)
        self.logo.setPixmap(logo_pixmap)
        zag_layout.addWidget(self.logo)
        self.zag = QLabel("Заказ")
        zag_layout.addWidget(self.zag)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Тип продукта", "Название", "Артикул", "мин стоимость", "Тип материала", "ID", "Сумма"])
        self.table.setColumnHidden(5, True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.table2 = QTableWidget()
        self.table2.setColumnCount(2)
        self.table2.setHorizontalHeaderLabels(["Тип", "Процент брака"])
        self.table2.setEditTriggers(QTableWidget.NoEditTriggers)

        tab_widget.addTab(self.table, "Продукты")
        tab_widget.addTab(self.table2, "Материалы")

        self.control_container = QWidget()
        control_layout = QHBoxLayout()
        self.control_container.setLayout(control_layout)
        main_layout.addWidget(self.control_container)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_product)

        for w in [self.add_btn, self.edit_btn]:
            control_layout.addWidget(w)

        tab_widget.currentChanged.connect(self.update_visible)

        self.load_data()

    def update_visible(self, index):
        self.control_container.setVisible(index == 0)
        
    def load_data(self):
        session = Session()
        query = session.query(Product).order_by(Product.id)
        product = query.all()
        self.table.setRowCount(len(product))
        for row, p in enumerate(product):
            self.table.setItem(row, 0, QTableWidgetItem(p.type_product.type))
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            self.table.setItem(row, 2, QTableWidgetItem(p.articul))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.min_price)))
            self.table.setItem(row, 4, QTableWidgetItem(p.type_material.type))
            self.table.setItem(row, 5, QTableWidgetItem(str(p.id)))

            count = session.query(func.sum(Partner_product.count)).filter(Partner_product.name_product_id == p.id).scalar() or 0
            price = p.min_price
            self.table.setItem(row, 6, QTableWidgetItem(str(price * count)))

        query2 = session.query(Material_type).order_by(Material_type.id)
        material = query2.all()
        self.table2.setRowCount(len(material))
        for row, m in enumerate(material):
            self.table2.setItem(row, 0, QTableWidgetItem(m.type))
            self.table2.setItem(row, 1, QTableWidgetItem(str(m.percent_brak)))

    def add_product(self):
        try:
            dialog = AddDialog(self)
            if dialog.exec():
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"{e}")

    def edit_product(self):
        try:
            row = self.table.currentRow()
            if row < 0:
                return
            product_id = self.table.item(row, 5).text()
            session = Session()
            product = session.query(Product).get(product_id)
            if product:
                dialog = EditDialog(product, self)
                if dialog.exec():
                    self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"{e}")