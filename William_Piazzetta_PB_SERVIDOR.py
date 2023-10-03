import socket, pickle, psutil, platform, cpuinfo, os, time, tabulate, nmap, subprocess

# Definir funções

# TP4 - Capturas das informações dos diretórios, como nome, tamanho, localização, data de criação, data de modificação, tipo, etc.
def info_arquivos(): 
    lista = os.listdir()
    dic = {}
    for i in lista:
        if os.path.isfile(i):
            dic[i] = []
            dic[i].append(os.stat(i).st_size)
            dic[i].append(os.stat(i).st_atime)
            dic[i].append(os.stat(i).st_mtime)
    tabela = [["Nome", "Tamanho", "Data criação", "Data modificação"]]
    for arq in dic:
        linha = [arq]
        linha.append(dic[arq][0])
        linha.append(time.ctime(dic[arq][1]))
        linha.append(time.ctime(dic[arq][2]))
        tabela.append(linha)
    return tabela

# TP4 - Capturas das informações dos processos do sistema, como PID, nome do executável, consumo de processamento, consumo de memória.
def exibir_pids():
    def exibir_titulo(tabela):
        titulo = []
        titulo.append("PID")
        titulo.append("# threads")
        titulo.append("Criação")
        titulo.append("T. Usu")
        titulo.append("T. Sis")
        titulo.append("Mem. (%)")
        titulo.append("RSS")
        titulo.append("VMS")
        titulo.append("Executável")
        tabela.append(titulo)
        return tabela

    def mostra_info(pid):
        try:
            p = psutil.Process(pid)
            texto = []
            texto.append(pid)
            texto.append(p.num_threads())
            texto.append(time.ctime(p.create_time()))
            texto.append(round(p.cpu_times().user, 2))
            texto.append(round(p.cpu_times().system, 2))
            texto.append(round(p.memory_percent(), 2))
            rss = round((p.memory_info().rss / (2 ** 20)), 2)
            texto.append(rss)
            vms = round((p.memory_info().vms / (2 ** 20)), 2)
            texto.append(vms)
            exe = p.exe()
            exe = exe.split("\\")
            exe = exe[-1]
            texto.append(exe)
            #print(texto)
            return texto
        except:
            pass

    tabela = []
    tabela = exibir_titulo(tabela)
    lista_pids = psutil.pids()
    cont = 0
    for pid in lista_pids:
        texto = mostra_info(pid)
        if (texto != None):
            tabela.append(texto)
            if (cont == 20):
                break
        cont += 1
    return tabela

# TP6 - Informações sobre as máquinas pertencentes à sub-rede do IP específico
def subredes_e_portas():
    def retorna_codigo_ping(host):
        plataforma = platform.system()
        if (plataforma == "Windows"):
            args = ["ping", "-n", "1", "-l", "1", "-w", "100", host]
            #args = ["ping", host]
        else:
            args = ["ping", "-c", "1", "-W", "1", host]
            #args = ["ping", HOST]
        retorno = subprocess.call(args, stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))
        return retorno

    def verifica_hosts(base_ip):
        #print("Verificando...", end="", flush=True)
        host_validos = []
        for i in range(1, 255):
            #if (i % 5) == 0:
                #print(".", end="", flush=True)
            ip = base_ip + str(i)
            retorno = retorna_codigo_ping(ip)
            if (retorno == 0):
                host_validos.append(ip)
        #host_validos.append("")
        return host_validos

    def obter_hostnames(host_validos):
        resultado_obter_hostnames = []
        nm = nmap.PortScanner()
        try:
            nm.scan(host)
            resultado_obter_hostnames.append(f"IP {host} possui o nome {nm[host].hostname()}")
        except:
            #pass
            resultado_obter_hostnames.append(f"Erro {host}")
        return resultado_obter_hostnames

    # TP6 - Informações sobre as portas dos diferentes IPs obtidos nessa sub-rede.
    def scan_host(host):
        resultado_scan_host = []
        nm = nmap.PortScanner()
        nm.scan(host)
        resultado_scan_host.append(f"{nm[host].hostname()}")
        for proto in nm[host].all_protocols():
            resultado_scan_host.append("..................")
            resultado_scan_host.append(f"Protocolo: {proto}")
            lport = nm[host][proto].keys()
            for port in lport:
                resultado_scan_host.append(f"Porta {port} Estado {nm[host][proto][port]['state']}")
        return resultado_scan_host

    #parte_1 = []
    result = []

    ip_string = "192.168.1.103"
    ip_lista = ip_string.split(".") # 192 168 1 103
    base_ip = ".".join(ip_lista[0:3]) +  "." # 192.168.1.
    #parte_1.append(f"Testar os IPs da subrede: {base_ip}.0")
    host_validos = verifica_hosts(base_ip)
    #parte_1.append(f"Hosts válidos: {host_validos}")
    #result.append(parte_1)
    for host in host_validos:
        result.append(obter_hostnames(host))
        result.append(scan_host(host))
    return result

# TP7 - Ao menos 3 informações de interfaces de redes (exemplos: interfaces disponíveis, IP, gateway, máscara de subrede, etc.)
def infos_interfaces():
    interfaces = psutil.net_if_addrs()
    nomes_interfaces = []
    for i in interfaces.keys():
        # Lista com nomes das interfaces disponíveis
        nomes_interfaces.append(i)
    # IPv4 da máquina
    ipv4 = interfaces["enp2s0"][0].address
    # Netmask
    netmask = interfaces["enp2s0"][0].netmask
    #ipv6Slice = ipv6[0:24]
    #print(interfaces)
    dic_infos_interfaces = {
        "Interfaces disponíveis": nomes_interfaces,
        "IPv4 da máquina": ipv4,
        "Máscara de subrede": netmask
    }
    return dic_infos_interfaces

def infos_cpu():
    info = cpuinfo.get_cpu_info()
    nome = str(platform.node())
    versao = str(platform.platform())
    so = str(platform.system())
    arq = info["arch"]
    marca_processador = info["brand_raw"]
    bits = str(info['bits'])
    #frequencia_processador = (psutil.cpu_freq().current, "MHz")
    frequencia_processador = round(psutil.cpu_freq().current, 2)
    nucleos_fisicos = str(psutil.cpu_count(logical=False))
    nucleos_logicos = str(psutil.cpu_count(logical=True))

    dados_cpu = [nome, versao, so, arq, marca_processador, bits, frequencia_processador, nucleos_fisicos, nucleos_logicos]
    return dados_cpu

def infos_memoria():
    mem = psutil.virtual_memory()
    mem_total = round(mem.total / pow(2, 30), 2)
    porcent_memoria = mem.percent
    texto_memoria = "Memória total: " + str(mem_total) + "GB / " + str(porcent_memoria) + "% em uso"
    return texto_memoria

def infos_disco():
    disco = psutil.disk_usage(".")
    disco_total = round(disco.total / pow(2, 30), 2)
    texto_uso_disco = "Espaço total do disco: " + str(disco_total) + "GB / " + str(disco.percent) + "% utilizado"
    return texto_uso_disco

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Obtém o nome da máquina
HOST = socket.gethostname()
PORTA = 9999

# Associa a porta
socket_servidor.bind((HOST, PORTA))

# Escutando...
socket_servidor.listen()

print("Servidor de nome", HOST, "esperando conexão na porta", PORTA)
# Aceita alguma conexão
(socket_cliente, addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

while True:
    msg = socket_cliente.recv(1024)
    opcao = msg.decode('utf-8')

    if opcao == '1':
        resultado = info_arquivos()
    elif opcao == '2':
        resultado = exibir_pids()
    elif opcao == '3':
        resultado = subredes_e_portas()
    elif opcao == '4':
        resultado = infos_interfaces()
    elif opcao == '5':
        resultado = infos_cpu()
    elif opcao == '6':
        resultado = infos_memoria()
    elif opcao == '7':
        resultado = infos_disco()
    elif opcao == '8':
        resultado = 'Conexão encerrada'
        # Converte o resultado para bytes
        bytes = pickle.dumps(resultado)
        # Envia os bytes
        socket_cliente.send(bytes)
        # Fecha a conexão com o cliente
        socket_cliente.close()
        socket_servidor.close()
    else:
        resultado = "Opção inválida. Tente novamente."

    # Converte o resultado para bytes
    bytes = pickle.dumps(resultado)
    # Envia os bytes
    socket_cliente.send(bytes)


