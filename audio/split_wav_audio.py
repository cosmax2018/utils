
#
# split_wav_audio.py : divide il file audio .wav in pezzetti di durata inferiore.
#

import os
from seleziona_file import seleziona

from pydub import AudioSegment

def ottieni_nome_file(percorso_completo,senza_estensione=None):        
    nome_file = os.path.basename(percorso_completo)
    if senza_estensione:
        if senza_estensione == True:
            return os.path.splitext(nome_file)[0]
        else:
            return nome_file
    else:
        return nome_file            
    
def ottieni_cartella_da_percorso(percorso_completo):
    cartella = os.path.dirname(percorso_completo)
    return cartella
    
def divide_file_audio(file_input, durata_segmento, cartella_output, nome_file_output):
    audio = AudioSegment.from_file(file_input, format="wav")
    durata_totale = len(audio)

    try:
        for i, inizio in enumerate(range(0, durata_totale, durata_segmento)):
            fine = min(inizio + durata_segmento, durata_totale)
            segmento = audio[inizio:fine]

            file_output = f"{cartella_output}/{nome_file_output}_{str(i+1).zfill(3)}.wav"
            segmento.export(file_output, format="wav")
            print(f"Segmento {i + 1} salvato in {file_output}")
            
        return True
        
    except:
        return False

def split_wav(file_audio_wav=None):

    if not file_audio_wav:
        file_audio_wav = seleziona()            # apre una finestra di selezione del file da splittare.
    
    if file_audio_wav:
    
        print(file_audio_wav)                                           # percorso_del_tuo_file_audio .wav
        cartella_output = ottieni_cartella_da_percorso(file_audio_wav)  # percorso_della cartella di output
        nome_file_output = ottieni_nome_file(file_audio_wav, True)      # nome del file di output
        durata_segmento_secondi = 60                                    # Durata di ciascun segmento in secondi

        if divide_file_audio(file_audio_wav, durata_segmento_secondi * 1000, cartella_output, nome_file_output):
            return True
        else:
            return False
            
    return False

if __name__ == "__main__":
    split_wav()
    