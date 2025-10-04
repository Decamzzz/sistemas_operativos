import random
from queue import PriorityQueue

class Process:
    def __init__(self, name):
        self.name = name
        self.quantum = None
        self.priority =  None
        self.pid = 0
        self.state = "inactivo"
        
    def generate_random_values(self):
        self.quantum = random.randint(1, 10)
        self.priority = random.randint(1, 10)
    
    def organize_processes(self, processes):
        queue_processes = PriorityQueue()
        for process in processes:
            queue_processes.put((process.quantum, process.priority, process.pid))
        return queue_processes

if __name__ == "__main__":
    p = Process("process_1")
    print(p.quantum, p.priority)
    p.generate_random_values()
    print(p.quantum, p.priority)

