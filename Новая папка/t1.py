from PySide6.QtWidgets import QMainWindow, QWidget, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from addDialog import AddDialog
from editDialog import EditDialog
from db import Session, Employee, JobName
from sqlalchemy import or_

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("t1")
        self.setMinimumSize(600, 700)
        self.setWindowIcon(QIcon("./logo.svg"))

        container = QWidget()
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


        self.filter_job = QComboBox()
        self.filter_job.addItem("All")
        control_layout.addWidget(self.filter_job)
        self.filter_job.currentIndexChanged.connect(self.load_data)

        self.search_line = QLineEdit(placeholderText="Search...")
        control_layout.addWidget(self.search_line)
        self.search_line.textChanged.connect(self.load_data)

        main_layout.addLayout(control_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Должность"])
        main_layout.addWidget(self.table)

        self.btn_add = QPushButton("add Employee")
        buttons_layout.addWidget(self.btn_add)
        self.btn_add.clicked.connect(self.add_employee)

        self.btn_edit = QPushButton("edit Employee")
        buttons_layout.addWidget(self.btn_edit)
        self.btn_edit.clicked.connect(self.edit_employee)

        self.btn_delete = QPushButton("delete Employee")
        buttons_layout.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self.delete_employee)

        main_layout.addLayout(buttons_layout)

        self.filter_jobname()
        self.load_data()

    def filter_jobname(self):
        session = Session()
        for job in session.query(JobName).all():
            self.filter_job.addItem(job.name, job.id)

    def load_data(self):
        session = Session()
        query = session.query(Employee)

        search = self.search_line.text().lower()
        if search:
            query = query.filter(or_(
                Employee.last_name.ilike(f"%{search}%"),
                Employee.name.ilike(f"%{search}%"),
                Employee.middlename.ilike(f"%{search}%")
            ))

        selected_job_id = self.filter_job.currentData()
        if selected_job_id:
            query = query.filter(Employee.jobname_id == selected_job_id)

        employees = query.all()
        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            last_name_item = QTableWidgetItem(emp.last_name)
            last_name_item.setData(Qt.UserRole, emp.id)
            self.table.setItem(row, 0, last_name_item)
            self.table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row, 2, QTableWidgetItem(emp.middlename))
            self.table.setItem(row, 3, QTableWidgetItem(emp.jobname.name))

    def add_employee(self):
        dialog = AddDialog(self)
        if dialog.exec():
            self.load_data()

    def edit_employee(self):
        row = self.table.currentRow()
        if row < 0:
            return
        emp_id = self.table.item(row, 0).data(Qt.UserRole)
        session = Session()
        employee = session.query(Employee).get(emp_id)
        if employee:
            dialog = EditDialog(employee, self)
            if dialog.exec():
                self.load_data()

    def delete_employee(self):
        row = self.table.currentRow()
        if row < 0:
            return
        emp_id = self.table.item(row, 0).data(Qt.UserRole)
        session = Session()
        employee = session.query(Employee).get(emp_id)
        if employee:
            session.delete(employee)
            session.commit()
            self.load_data()
