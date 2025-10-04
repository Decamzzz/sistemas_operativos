import sys
from GUI import Simulador
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Simulador()
    ventana.show()
    sys.exit(app.exec())