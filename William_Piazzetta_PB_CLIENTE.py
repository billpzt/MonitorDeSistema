import socket, sys, pickle, time
#from tabulate import tabulate

def tabulador(lista):
    return(tabulate(lista, headers='firstrow'))

def imprimir_resultados_opcao_3(resultado):
    for i in resultado:
        for j in i:
            print(j)

def imprimir_resultados_opcao_4(resultado):
    for key, value in resultado.items():
        if key == 'Interfaces disponíveis':
            print(key,":")
            for interface in resultado[key]:
                print("---",interface)
        else:
            print(key,":")
            print("---",value)

def imprimir_resultados_opcao_5(resultado):
    print("Nome da máquina:")
    print(f"--- {resultado[0]}")
    print("Versão do SO:")
    print(f"--- {resultado[1]}")
    print("SO:")
    print(f"--- {resultado[2]}")
    print("Arquitetura:")
    print(f"--- {resultado[3]}")
    print("Modelo do CPU:")
    print(f"--- {resultado[4]}")
    print("Palavra do processador:")
    print(f"--- {resultado[5]}")
    print("Frequência do processador:")
    print(f"--- {resultado[6]}")
    print("Núcleos físicos:")
    print(f"--- {resultado[7]}")
    print("Núcleos lógicos:")
    print(f"--- {resultado[8]}")

def imprimir_menu():
    print('Escolha uma opção para obter mais informações do servidor:')
    print()

    menu = [
        "[1] - Informações de Diretórios", 
        "[2] - Processos do Sistema", 
        "[3] - Subredes e Portas", 
        "[4] - Interfaces Disponíveis, IPv4 do Servidor, Máscara de Subrede", 
        "[5] - CPU", 
        "[6] - Memória", 
        "[7] - Disco Rígido",
        "[8] - Encerrar"
        ]

    for i in menu:
        print(i)
    print()

# cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostname()
PORT = 9999

'''msg = opcao'''

try:
    # Tenta se conectar ao servidor que fica na mesma máquina
    s.connect((HOST, PORT))
except Exception as erro:
    print(str(erro))
    sys.exit(1) # Termina o programa

opcao = ''

while opcao != '8':
    imprimir_menu()

    # Obtém a opção do menu:
    opcao = input("Digite um número: ")
    print()

    msg = opcao

    # Envia mensagem codificada em bytes ao servidor
    s.send(msg.encode('utf-8'))
    # Marca o início da contagem de tempo que leva o pedido
    inicio = time.time()
    # Recebe até 100000 bytes do servidor
    bytes = s.recv(10000000)
    # Marca o fim da contagem de tempo que leva o pedido
    fim = time.time()
    # Converte os bytes recebidos do servidor para o formato que o cliente pode usar
    resultado = pickle.loads(bytes)
    # Calcula o tempo total de execução do pedido
    tempo_execucao = fim - inicio

    # Apresenta o resultado:
    if opcao == '1':
        print(tabulador(resultado))
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '2':
        print(tabulador(resultado))
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '3':
        imprimir_resultados_opcao_3(resultado)
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '4':
        imprimir_resultados_opcao_4(resultado)
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '5':
        imprimir_resultados_opcao_5(resultado)
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '6':
        print(resultado)
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '7':
        print(resultado)
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
    elif opcao == '8':
        print(resultado)
        input("Pressione qualquer tecla para sair...")
        # Fecha conexão com o servidor
        s.close()
    else:
        print(resultado)
        print("\nTempo de execução: ",round(tempo_execucao, 2), "segundos")
