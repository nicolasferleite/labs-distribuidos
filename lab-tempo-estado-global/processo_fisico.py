import threading
import time
import random

def processo_fisico(pid):
    for i in range(5):
        # Simula processamento
        time.sleep(random.uniform(0.1, 0.5))
        
        # Pega relógio físico
        tempo_fisico = time.time()
        
        # Formata para ficar legível (apenas os segundos finais)
        tempo_formatado = f"{tempo_fisico:.4f}"
        
        print(f"[Processo {pid}] Tempo: {tempo_formatado} - Evento {i} realizado")

# Criando e iniciando as threads
threads = []
print("--- INICIANDO SIMULAÇÃO RELÓGIO FÍSICO ---")
for i in range(3):
    t = threading.Thread(target=processo_fisico, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()