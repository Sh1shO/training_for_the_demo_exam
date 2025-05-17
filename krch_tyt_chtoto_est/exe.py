from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from styles import STYLESHEET

app = QApplication([])
app.setStyleSheet(STYLESHEET)
w = MainWindow()
w.show()
app.exec()