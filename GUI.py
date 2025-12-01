from process_object import Process, organize_processes
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

        self.timer_suspended = QTimer(self)
        self.timer_suspended.timeout.connect(self.resume_suspended_processes)

        # --- nuevos estados de control ---
        self.current_process = None
        self.suspended_queue = []  # procesos en espera para reingresar a preparados
        self.cycle_counter = 0
        
        self.layout_root = QVBoxLayout()
        
        self.about = QHBoxLayout()
        self.label_about = QLabel("Creadores: Deiby Camilo Botina - Juan Diego Juaginoy - Jeison Camilo Diaz - Dario Narvaez © 2025")
        self.about.addWidget(self.label_about)
        
        self.layout_main = QHBoxLayout()
        
        self.layout_add_process = QVBoxLayout()
        self.layout_main_processes = QVBoxLayout()
        self.layout_extra_processes = QHBoxLayout()
        
        self.add_process_button = QPushButton("Agregar proceso")
        self.add_process_button.clicked.connect(self.open_dialog_add_process)
        
        self.choose_process_button = QPushButton("Añadir a preparados")
        self.choose_process_button.setEnabled(False)
        self.choose_process_button.clicked.connect(self.update_bcp_prepared_process)
        
        self.start_simulation_button = QPushButton("Iniciar simulacion")
        # self.start_simulation_button.setEnabled(False)
        self.start_simulation_button.clicked.connect(self.start_simulation)
        
        self.list_inactive_processes = QListWidget()
        self.list_inactive_processes.currentItemChanged.connect(lambda e: self.choose_process_button.setEnabled(True))
        self.inactive_processes = []
        self.prepared_processes = []
        self.processes_with_cpu = []
        
        self.list_running_processes = QListWidget()
        self.list_prepared_processes = QListWidget()
        self.list_suspended_processes = QListWidget()
        
        self.table_bcp = QTableWidget(0, 6)
        self.table_bcp.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_bcp.setHorizontalHeaderLabels(["Nombre", "Quantum", "Prioridad", "PID", "Estado", "Tiempo CPU"])
        
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
        
        self.layout_root.addLayout(self.layout_main)
        self.layout_root.addLayout(self.about)
        self.setLayout(self.layout_root)
    
    def start_simulation(self):
        if not self.prepared_processes:
            QMessageBox.information(self, "Simulador", "No hay procesos preparados.")
            return
        self.timer.start(1000)
        self.timer_suspended.start(3000)  
    
    def simulation_tick(self):
        if not self.current_process:
            remaining = [p for p in self.processes_with_cpu if p.cpu_time > 0]

            if not remaining:
                self.timer.stop()
                QMessageBox.information(self, "Simulación", "Todos los procesos han terminado.")
                return

            if self.prepared_processes:
                self.current_process = self.prepared_processes.pop(0)
                self.current_process.state = "Ejecución"
                self.update_process_lists()
            else:
                return  

        p = self.current_process
        p.cpu_time -= 1
        p.quantum -= 1

        self.update_bcp_table(p)
        
        if p.cpu_time <= 0:
            p.state = "Inactivo"
            p.quantum = 0
            p.cpu_time = 0
            p.priority = 0
            p.pid = 0
            self.inactive_processes.append(p)
            self.current_process = None
            self.update_process_lists()
            self.update_bcp_table(p)
            return
        
        if p.quantum <= 0:
            p.state = "Suspendido"
            self.suspended_queue.append(p)
            self.current_process = None
            self.update_process_lists()
            self.update_bcp_table(p)
            return

        self.update_process_lists()
        
    def resume_suspended_processes(self):
        if not self.suspended_queue:
            return

        for p in list(self.suspended_queue):
            p.state = "Preparado"
            p.quantum = p.original_quantum
            self.prepared_processes.append(p)
            self.suspended_queue.remove(p)
            self.update_bcp_table(p)

        self.update_process_lists()

    def update_process_lists(self):
        self.list_running_processes.clear()
        self.list_prepared_processes.clear()
        self.list_suspended_processes.clear()
        self.list_inactive_processes.clear()

        if self.current_process:
            self.list_running_processes.addItem(QListWidgetItem(self.current_process.name))

        for p in self.prepared_processes:
            self.list_prepared_processes.addItem(QListWidgetItem(p.name))
        for p in self.suspended_queue:
            self.list_suspended_processes.addItem(QListWidgetItem(p.name))
        for p in self.inactive_processes:
            self.list_inactive_processes.addItem(QListWidgetItem(p.name))
        
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
            self.table_bcp.setItem(i, 5, QTableWidgetItem(f"{self.inactive_processes[i].cpu_time}"))
    
    def update_bcp_prepared_process(self):
        if self.list_inactive_processes.currentRow() < 0:
            return
        
        index = self.list_inactive_processes.currentRow()
        
        if index >= len(self.inactive_processes):
            return
        
        process = self.inactive_processes[index]
        
        new_pid = len(self.prepared_processes) + 101
        process.pid = new_pid
        process.state = "Preparado"
        process.get_values()
        
        self.update_bcp_table(process)
        
        self.prepared_processes.append(process)
        self.inactive_processes.pop(index)
        
        self.list_inactive_processes.takeItem(index)
        #self.choose_process_button.setEnabled(False)
        self.list_inactive_processes.clearSelection()
        
        self.update_list_prepared_processes()

    def update_bcp_table(self, process):
        for row in range(self.table_bcp.rowCount()):
            item = self.table_bcp.item(row, 0)
            if item and item.text() == process.name:
                self.table_bcp.setItem(row, 1, QTableWidgetItem(f"{process.quantum}"))
                self.table_bcp.setItem(row, 2, QTableWidgetItem(f"{process.priority}"))
                self.table_bcp.setItem(row, 3, QTableWidgetItem(f"{process.pid}"))
                self.table_bcp.setItem(row, 4, QTableWidgetItem(f"{process.state}"))
                self.table_bcp.setItem(row, 5, QTableWidgetItem(f"{process.cpu_time}"))
                break

    def update_list_prepared_processes(self):
        self.list_prepared_processes.clear()
        queue = organize_processes(self.prepared_processes)
        
        ordered_processes = []
        while not queue.empty():
            quantum, priority, pid = queue.get()
            for process in self.prepared_processes:
                if process.pid == pid:
                    ordered_processes.append(process)
                    break
                
        self.prepared_processes = ordered_processes.copy()
        self.processes_with_cpu = self.prepared_processes.copy()
        for process in self.prepared_processes:
            self.list_prepared_processes.addItem(QListWidgetItem(process.name))