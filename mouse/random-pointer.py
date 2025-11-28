import pyautogui
import random
import time

def movimento_casuale(interval=1):
    # Ottieni la dimensione dello schermo
    screen_width, screen_height = pyautogui.size()
    
    print("Inizio movimento casuale del mouse. Premi CTRL+C per fermare.")

    try:
        while True:
            # Genera una posizione casuale
            x = random.randint(0, screen_width - 1)
            y = random.randint(0, screen_height - 1)

            # Muove il mouse lentamente verso la posizione
            pyautogui.moveTo(x, y, duration=0.5)

            # Attendi prima di un altro movimento
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Movimento interrotto.")

if __name__ == "__main__":
    movimento_casuale(interval=2)   # muove il mouse ogni 2 secondi
