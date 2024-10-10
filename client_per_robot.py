import socket
#lista e fai elif x vane 
SERVER_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
from pynput import keyboard

def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.IN1,GPIO.HIGH)
			GPIO.output(self.IN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.IN1,GPIO.LOW)
			GPIO.output(self.IN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.IN3,GPIO.HIGH)
			GPIO.output(self.IN4,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.IN3,GPIO.LOW)
			GPIO.output(self.IN4,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)

#funzione chiamata quando un tasto viene premuto 
def on_press(key):
    #try
    if key.char == "w":
        print("press w")
# expect AttributeError:
# ignora tasti speciali come Shift, Crel, etc
#pass
#funzione chiamata quando un tasto viene rilasciato 
def on_release(key):
    #try:
    if key.char == "w":
        print("release w")
#except AttributeError:
#       pass
def start_listener():
    #Listener per intercettare gli eventi da tastiera 
    with keyboard.listener(on_press = on_press, on_release = on_release) as listener:
            listener.join()

start_listener()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    while True:
        command = input("inserisci che cosa vuoi che il robot faccia: forward per andare dritto, backward per andare indietro, left per andare a sinistra, right per andare a destra: ")
        value = input("inserisci un valore: ")
        message = f"{command}|{value}" #valore che mando al server
        s.sendall(message.encode()) #per trasmettere stringhe binarie
        stringa= s.recv(BUFFER_SIZE) #ritorna i dati e l'indirizzo
        x = stringa.decode().split("|")
        print(x)#stampa il messagio del server

        s.close()

if __name__ == "__main__":
    main()