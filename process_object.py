import random
from queue import PriorityQueue

def organize_processes(processes):
    queue_processes = PriorityQueue()
    for process in processes:
        queue_processes.put((process.quantum, -process.priority, process.pid))
    return queue_processes

class Process:
    def __init__(self, name):
        self.name = name
        self.quantum = 0
        self.priority = 0
        self.pid = 0
        self.state = "inactivo"
        self.cpu_time = 0
        self.original_quantum = 0

    def get_values(self):
        quantum_rate = 5
        self.cpu_time = random.randint(15, 50)
        self.quantum = self.cpu_time // quantum_rate
        self.original_quantum = self.quantum
        self.priority = random.randint(1, 10)

if __name__ == "__main__":
    p = Process("process_1")
    print(p.quantum, p.priority)
    p.generate_random_values()
    print(p.quantum, p.priority)
    

