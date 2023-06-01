import sys
import qdarkstyle
from PyQt6.QtWidgets import QApplication, QPushButton

app = QApplication(sys.argv)

# Apply the dark style globally
app.setStyleSheet(qdarkstyle.load_stylesheet())

button = QPushButton("Hello, World!")
button.show()

sys.exit(app.exec())

