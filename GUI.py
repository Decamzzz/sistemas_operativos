from process_object import Process
from PySide6.QtWidgets import (
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QDialog,
    QMessageBox,
    QTableWidget, 
    QTableWidgetItem,
    QLabel)
from PySide6.QtCore import Qt
from PySide6.QtCore import QItemSelectionModel, QTimer

class Simulador(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de procesos")
        #self.setFixedSize(800, 600)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simulation_tick)
        self.counter_test = 0
        
        self.layout_main = QHBoxLayout()
        
        self.layout_add_process = QVBoxLayout()
        self.layout_main_processes = QVBoxLayout()
        self.layout_extra_processes = QHBoxLayout()
        
        self.add_process_button = QPushButton("Agregar proceso")
        self.add_process_button.clicked.connect(self.open_dialog_add_process)
        
        self.choose_process_button = QPushButton("Añadir a preparados")
        self.choose_process_button.setEnabled(False)
        self.choose_process_button.clicked.connect(self.add_prepared_process)
        
        self.start_simulation_button = QPushButton("Iniciar simulacion")
        # self.start_simulation_button.setEnabled(False)
        self.start_simulation_button.clicked.connect(self.start_simulation)
        
        self.list_inactive_processes = QListWidget()
        self.list_inactive_processes.currentItemChanged.connect(lambda e: self.choose_process_button.setEnabled(True))
        self.inactive_processes = []
        
        self.list_running_processes = QListWidget()
        self.list_prepared_processes = QListWidget()
        self.list_suspended_processes = QListWidget()
        
        self.table_bcp = QTableWidget(0, 5)
        self.table_bcp.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_bcp.setHorizontalHeaderLabels(["Nombre", "Quantum", "Prioridad", "PID", "Estado"])
        
        self.layout_add_process.addWidget(self.add_process_button)
        self.layout_add_process.addWidget(self.choose_process_button)
        self.layout_add_process.addWidget(self.start_simulation_button)
        self.layout_add_process.addWidget(QLabel("PROCESOS INACTIVOS", alignment=Qt.AlignmentFlag.AlignHCenter))
        self.layout_add_process.addWidget(self.list_inactive_processes)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("PROCESOS PREPARADOS", alignment=Qt.AlignmentFlag.AlignHCenter))
        layout.addWidget(self.list_prepared_processes)

        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("PROCESOS SUSPENDIDOS", alignment=Qt.AlignmentFlag.AlignHCenter))
        layout1.addWidget(self.list_suspended_processes)

        self.layout_extra_processes.addLayout(layout)
        self.layout_extra_processes.addLayout(layout1)

        self.layout_main_processes.addWidget(QLabel("PROCESOS EN EJECUCION", alignment=Qt.AlignmentFlag.AlignHCenter))
        self.layout_main_processes.addWidget(self.list_running_processes)
        
        self.layout_main_processes.addLayout(self.layout_extra_processes)
        
        self.layout_main.addLayout(self.layout_add_process)
        self.layout_main.addLayout(self.layout_main_processes)
        self.layout_main.addWidget(self.table_bcp)
        
        self.setLayout(self.layout_main)
    
    def start_simulation(self):
        self.timer.start(1000)
    
    def simulation_tick(self):
        self.counter_test += 1
        print(self.counter_test)
        
    def open_dialog_add_process(self):
        dialog = QDialog()
        dialog.setWindowTitle("Simulador de procesos")
        dialog.setFixedSize(350, 75)
        
        self.process_name = QLineEdit()
        self.process_name.setPlaceholderText("Ingrese el nombre del proceso a añadir")
        
        button_accept = QPushButton("Aceptar")
        button_accept.clicked.connect(self.validate_add_process_in_list)
        button_reject = QPushButton("Cancelar")
        button_reject.clicked.connect(lambda e: dialog.close())
        
        layout_main = QVBoxLayout()
        layout_buttons = QHBoxLayout()
        
        layout_buttons.addWidget(button_accept)
        layout_buttons.addWidget(button_reject)
        
        layout_main.addWidget(self.process_name)
        layout_main.addLayout(layout_buttons)
        
        dialog.setLayout(layout_main)
        dialog.open()
        
    def validate_add_process_in_list(self):
        if not self.process_name.text():
            message = QMessageBox(text="Nombre de proceso invalido\nPor favor intente de nuevo")
            message.setWindowTitle("Simulador de procesos")
            message.exec()
        else:
            if self.list_inactive_processes.findItems(self.process_name.text(), Qt.MatchFlag.MatchExactly)!= []:
                message = QMessageBox(text="Nombre de proceso ya asignado\nPor favor intente de nuevo")
                message.setWindowTitle("Simulador de procesos")
                message.exec()
            else:
                p = Process(self.process_name.text())
                p.generate_random_values()
                self.list_inactive_processes.addItem(QListWidgetItem(p.name))
                self.inactive_processes.append(p)
                self.add_process_in_table()
                self.process_name.clear()

    def add_process_in_table(self):
        self.table_bcp.setRowCount(self.list_inactive_processes.count())
        
        for i in range(self.list_inactive_processes.count()):
            self.table_bcp.setItem(i, 0, QTableWidgetItem(self.inactive_processes[i].name))
            self.table_bcp.setItem(i, 1, QTableWidgetItem(f"{self.inactive_processes[i].quantum}"))
            self.table_bcp.setItem(i, 2, QTableWidgetItem(f"{self.inactive_processes[i].priority}"))
            self.table_bcp.setItem(i, 3, QTableWidgetItem(f"{self.inactive_processes[i].pid}"))
            self.table_bcp.setItem(i, 4, QTableWidgetItem(self.inactive_processes[i].state))
    
    def add_prepared_process(self):
        process = self.list_inactive_processes.currentItem()
        index = self.list_inactive_processes.currentRow()
        self.list_prepared_processes.addItem(process.text())
        self.inactive_processes[index].pid += self.list_prepared_processes.count()+100
        self.inactive_processes[index].state = "Preparado"
        self.table_bcp.setItem(index, 3, QTableWidgetItem(f"{self.inactive_processes[index].pid}"))
        self.table_bcp.setItem(index, 4, QTableWidgetItem(self.inactive_processes[index].state))
        self.choose_process_button.setEnabled(False)
        self.list_inactive_processes.setCurrentItem(self.list_inactive_processes.currentItem(), QItemSelectionModel.SelectionFlag.Deselect)
        