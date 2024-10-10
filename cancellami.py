from pynput import keyboard

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
