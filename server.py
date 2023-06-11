import socket, time, random

localIP             = "127.0.0.1"
localPort           = 20001
bufferSize          = 32                        # Tamanho total da mensagem enviada e recebida (header+msg)
headerSize          = 16                        # Tamanho do cabecalho
messageSize         = bufferSize - headerSize   # Tamanho dos dados
ackDict             = {}                         # Ultimo ack para msg do cliente, so atualizando se for maior

UDPServerSocket     = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

# Faz alteracoes na string recebida
def changeStr(message):
    return message.upper();


# Envia resposta para cliente
def sendResponse(recSeq, recAck, address, recMsg):
    global ackDict
    if (recAck >= ackDict[address]):                                         # Encaixa o ACK no header
        ackStr = str(recSeq+messageSize).rjust(             # Se ACK da msg recebida for maior que armazenado,
                round(headerSize/2), '0')                   # servidor envia ACK para a mensagem recebida,
        ackDict[address] = recAck                                
    else: ackStr = str(ackDict[address]).rjust(round(headerSize/2), '0') # se nao, envia o ack armazenado (maior)
    seqStr = str(recSeq).rjust((round(headerSize/2)), '0')      # Encaixa o SEQ no header
    msg = changeStr(recMsg)
    #msg = str(msgFromServer[recSeq:recSeq + messageSize])       # Extrai proximo segmento da mensagem
    print(f"Enviado:{msg}")
    print("---------------------------")
    UDPServerSocket.sendto(str.encode(seqStr + ackStr + msg), address)  # Envia resposta para cliente

def readMsg(bytesAddressPair):
    message = bytesAddressPair[0]                               # Extrai msg da tupla recebida
    address = bytesAddressPair[1]                               # Extrai informacoes do remetente da tupla
    if (message.decode() == 'ini'):
        ackDict[address] = 0
        UDPServerSocket.sendto(str.encode("ini"), address)
        print(f"Nova Conexao: {address}")
        print("---------------------------")
        return
    print(f"Address Client:{format(address)}")
    print(f"Recebido:{format(message)}")
    recSeq = int(str(format(message))[2:2+round(headerSize/2)])             # Extrai SEQ da msg recebida
    recAck = int(str(format(message))[2+round(headerSize/2):2+headerSize])  # Extrai ACK da msg recebida
    recMsg = str(format(message)[2+headerSize:])
    sendResponse(recSeq, recAck, address, recMsg)                            # Envia resposta

# Caso normal do servidor, sem falhas
def loopNormal():
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     # Recebe msg do cliente (nao usa timeout)
        readMsg(bytesAddressPair)

# Teste de perda de pacotes
def loopPacketLoss():
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     # Recebe msg do cliente (nao usa timeout)
        rng = random.randint(1, 10)
        if (rng != 1):
            readMsg(bytesAddressPair)

# Teste simulando tempo de espera de diversos fatores
def loopDelay():
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     # Recebe msg do cliente (nao usa timeout)
        rng = random.random()                                       # Retorna valor entre 0 e 1
        time.sleep(0.5 + rng)
        readMsg(bytesAddressPair)

input = input("insira 'n' para servidor normal, 'p' para perda de pacote ou 'd' para atrasado: ")
if (input == 'p'):
    loopPacketLoss()
elif (input == 'd'):
    loopDelay()
elif (input == 'n'):
    loopNormal()
