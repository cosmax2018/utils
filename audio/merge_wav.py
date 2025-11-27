
# merge_wav.py : crea un unico file audio .wav con tanti files audio .wav

from pydub import AudioSegment
import os

# Sostituisci questo percorso con il percorso della tua cartella contenente i file .wav
cartella = "W:\mie-registrazioni-audio\computazione epifenomenale 2020\Mia registrazione 1" #"percorso/alla/tua/cartella"

# Ottieni un elenco di tutti i file .wav nella cartella
files_wav = [f for f in os.listdir(cartella) if f.endswith('.wav')]
files_wav.sort()  # Assicurati che l'ordine dei file sia corretto

# Crea un segmento audio vuoto per iniziare l'unione
audio_totale = AudioSegment.empty()

# Unisci i file .wav
for file in files_wav:
    print(f"...processing {file}")
    percorso_completo = os.path.join(cartella, file)
    segmento_audio = AudioSegment.from_wav(percorso_completo)
    audio_totale += segmento_audio

# Esporta l'audio unito in un nuovo file .wav
audio_totale.export(cartella+"/audio_unito.wav", format="wav")
