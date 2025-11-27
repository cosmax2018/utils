
#  estract_audio_from_video.py  : estrae l'audioo da un video .mp4

import os
from seleziona_file import seleziona
from moviepy.editor import VideoFileClip

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

def cambia_estensione(nome_file, nuova_estensione):
    nome_base, _ = os.path.splitext(nome_file)
    nuovo_nome_file = f"{nome_base}.{nuova_estensione}"
    return nuovo_nome_file
    
def extract_audio(video_file_path, output_audio_file_path):
    """
    Estrae l'audio da un file video e lo salva in un file audio.
    
    :param video_file_path: Percorso del file video da cui estrarre l'audio.
    :param output_audio_file_path: Percorso del file audio di output (con estensione .mp3 o .wav).
    """
    # Carica il file video
    video = VideoFileClip(video_file_path)
    
    # Estrai l'audio e salvalo
    video.audio.write_audiofile(output_audio_file_path)

def main():

    file_video,tipo = seleziona() # apre una finestra di selezione del file
    
    if file_video:
    
        print("File selezionato:  ",file_video," -- Tipo:  ",tipo)

        cartella = ottieni_cartella_da_percorso(file_video)
        nome_file_audio = ottieni_nome_file(file_video)
        
        output_audio_file = cartella + '/' + cambia_estensione(nome_file_audio,'mp3')  # Cambia in .wav se preferisci quel formato

        extract_audio(file_video, output_audio_file)
        
if __name__ == "__main__":
    main()