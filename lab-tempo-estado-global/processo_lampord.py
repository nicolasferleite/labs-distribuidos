import threading
import time
import random
import queue

# Filas para simular a rede entre processos (P0, P1, P2)
canais = [queue.Queue() for _ in range(3)]

def processo_lamport(pid):
    relogio = 0
    
    for i in range(3):
        time.sleep(random.uniform(0.5, 1.5))
        
        # Decide aleatoriamente se vai enviar mensagem ou fazer evento interno
        acao = random.choice(['interno', 'enviar'])
        
        # Verifica se tem mensagem para receber
        if not canais[pid].empty():
            msg_relogio, remetente = canais[pid].get()
            relogio = max(relogio, msg_relogio) + 1
            print(f"[P{pid}] RECEBEU de P{remetente}. Ajustou relógio para: {relogio}")
        
        if acao == 'interno':
            relogio += 1
            print(f"[P{pid}] Evento INTERNO. Relógio: {relogio}")
            
        elif acao == 'enviar':
            relogio += 1
            # Envia para um destinatário aleatório (diferente de si mesmo)
            dest = (pid + 1) % 3 
            canais[dest].put((relogio, pid))
            print(f"[P{pid}] ENVIOU para P{dest} com timestamp: {relogio}")

print("--- INICIANDO RELÓGIO DE LAMPORT ---")
threads = []
for i in range(3):
    t = threading.Thread(target=processo_lamport, args=(i,))
    threads.append(t)
    t.start()