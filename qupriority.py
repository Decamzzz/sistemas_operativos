from queue import PriorityQueue

# Inicializa la cola de prioridad
cola_prioridad_obj = PriorityQueue()

cola_prioridad_obj.put((1, 7, 1))
cola_prioridad_obj.put((2, 4, 3))
cola_prioridad_obj.put((4, 4, 2))
cola_prioridad_obj.put((7, 2, 4))
cola_prioridad_obj.put((1, 1, 5))

# Saca elementos de la cola
while not cola_prioridad_obj.empty():
    quantum, prioridad, pid = cola_prioridad_obj.get()
    print(f"Quantum:{quantum}/Prioridad:{prioridad}/PID:{pid}")


