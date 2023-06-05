from PySide6.QtWidgets import QMainWindow, QPushButton
from Tasty_Api_Result import Tasty_App
class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tasty App")
        button = QPushButton("Press Me!")
        button.setCheckable(False)
        self.setCentralWidget(button)
        button.clicked.connect(lambda: Tasty_App.get_recipies_auto_complete("chicken"))