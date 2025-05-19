STYLESHEET="""
QMainWindow, QDialog, QWidget{
    background-color: white;
    font-family: Arial;
}

QLabel#zag {
    font-size: 20px;
}

QPushButton, QLineEdit, QDateEdit, QComboBox{
    background-color: green;
    color: white;
}

QPushButton:hover {
    background-color: yellow;
    color: black;
}

QHeaderView::section{
    background-color: blue;
    color: white;
}
"""