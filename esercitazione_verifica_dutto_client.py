import socket

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.sendall(request.encode())
        response = s.recv(1024).decode()
        return response

#Richiesta presenza file
def check_presence(nome_file):
    return send_request(f"PRESENCE:{nome_file}")

#Richiesta numero frammenti
def get_fragment_count(nome_file):
    return send_request(f"FRAG_COUNT:{nome_file}")

#Richiesta IP per un frammento specifico
def get_host_for_fragment(nome_file, n_frammento):
    return send_request(f"HOST_FOR_FRAG:{nome_file}:{n_frammento}")

#Richiesta IP di tutti gli host per i frammenti di un file
def get_all_hosts(nome_file):
    return send_request(f"ALL_HOSTS:{nome_file}")

#Test del client
if __name__ == "__main__":
    nome_file = "example.txt"
    print("Presenza file:", check_presence(nome_file))
    print("Numero frammenti:", get_fragment_count(nome_file))
    print("Host per frammento 1:", get_host_for_fragment(nome_file, 1))
    print("Tutti gli host:", get_all_hosts(nome_file))
