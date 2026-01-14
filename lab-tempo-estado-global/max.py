import threading
import time
import random
import queue

# Filas para rede
canais = [queue.Queue() for _ in range(3)]
num_processos = 3

def max_vetor(v1, v2):
    """Retorna o max elemento a elemento entre dois vetores"""
    return [max(v1[i], v2[i]) for i in range(len(v1))]

def processo_vetorial(pid):
    # Inicializa vetor zerado [0, 0, 0]
    vetor = [0] * num_processos
    
    for i in range(3):
        time.sleep(random.uniform(0.5, 1.5))
        
        # Verifica mensagem chegando antes de agir
        try:
            # Tenta pegar mensagem sem bloquear muito
            vetor_msg, remetente = canais[pid].get(timeout=0.1)
            
            # Atualiza vetor: max(local, recebido)
            vetor = max_vetor(vetor, vetor_msg)
            # Incrementa o seu próprio relógio após receber
            vetor[pid] += 1
            print(f"[P{pid}] RECEBEU de P{remetente}. Vetor atualizado: {vetor}")
            
        except queue.Empty:
            pass
            
        # Ação: Enviar mensagem
        vetor[pid] += 1
        dest = (pid + 1) % 3
        
        # Envia CÓPIA do vetor
        canais[dest].put((list(vetor), pid))
        print(f"[P{pid}] ENVIOU para P{dest}. Vetor enviado: {vetor}")

print("--- INICIANDO RELÓGIO VETORIAL ---")
threads = []
for i in range(3):
    t = threading.Thread(target=processo_vetorial, args=(i,))
    threads.append(t)
    t.start()