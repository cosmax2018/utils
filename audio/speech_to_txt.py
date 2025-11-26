
#
# speech_to_txt.py : trasforma il parlato registrato (.m4a/.mp3/.3ga/.wav) in file di testo.
#
#                     n.b.: installare :
#
#                               ffmpeg da https://www.gyan.dev/ffmpeg/builds/
#                               pip install audioop-lts
#                               pip install SpeechRecognition
#
#

import os,shutil,time,calendar
from split_wav_audio import split_wav

import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

def get_timestamp():
    utc_time_tuple = time.gmtime()
    utc_timestamp = calendar.timegm(utc_time_tuple)
    return str(utc_timestamp)

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

def cambia_estensione(nome_file, nuova_estensione, timestamp=None):
    nome_base, _ = os.path.splitext(nome_file)
    if timestamp:
        nuovo_nome_file = f"{nome_base}_{timestamp}.{nuova_estensione}"
    else:
        nuovo_nome_file = f"{nome_base}.{nuova_estensione}"
    
    return nuovo_nome_file
    
def converti_m4a_in_wav(file_m4a, file_wav):
    audio = AudioSegment.from_file(file_m4a, format="m4a")
    audio.export(file_wav, format="wav")

def converti_mp3_in_wav(file_mp3, file_wav):
    audio = AudioSegment.from_file(file_mp3, format="mp3")
    audio.export(file_wav, format="wav")
    
def converti_3ga_in_wav(file_3ga, file_wav):
    # Rinomina temporaneamente il file .3ga in .mp4 per la compatibilità con FFmpeg
    percorso_temp = file_3ga + ".mp4"
    os.rename(file_3ga, percorso_temp)
    
    try:
        # Carica il file (ora .mp4)
        audio = AudioSegment.from_file(percorso_temp, format="mp4")
    
        # Esporta il file come wav
        audio.export(file_wav, format="wav")
    finally:
        # Rinomina il file al suo nome originale
        os.rename(percorso_temp, file_3ga)    
    
def estrai_testo_da_audio(file_audio):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_audio) as source:
        audio = recognizer.record(source)
        
    try:
        testo = recognizer.recognize_google(audio, language="it-IT")
        return testo
    except sr.UnknownValueError:
        print(f"Impossibile riconoscere il parlato in {file_audio}")
        return None
    except sr.RequestError as e:
        print(f"Errore nella richiesta a Google: {e}")
        return None

def salva_testo_su_file(testo, nome_file):
    with open(nome_file, 'w', encoding='utf-8') as file:
        file.write(testo)

def estrai_testo(cartella_wav,nome_file_testo):

    testo_estratto = ''
    
    for file_wav in [file for file in os.listdir(cartella_wav) if file.lower().endswith(".wav")]:
        print(f"...processing {file_wav}")
        testo = estrai_testo_da_audio(cartella_wav + '/' + file_wav)# estrai il testo da tutti i files .wav splittati
        if testo:
            testo_estratto += testo
        else:
            testo_estratto += '\n[ Nel blocco ' + file_wav + ' impossibile riconoscere il parlato ]\n'
            
    if testo_estratto:
        salva_testo_su_file(testo_estratto, nome_file_testo)
        print(f"\nTesto estratto con successo e salvato in {nome_file_testo}.")  
        return True
    else:
        print("Errore nell'estrazione del testo.")
        
    return False
            
def converti_in_testo(file_audio,tipo):

    if file_audio:
    
        print("File selezionato:\t",file_audio," -- Tipo:\t",tipo)
        
        cartella_wav = os.path.join(ottieni_cartella_da_percorso(file_audio), ottieni_nome_file(file_audio,True))    
        file_audio_wav = cartella_wav  + '/' + cambia_estensione(ottieni_nome_file(file_audio),"wav")
        
        os.makedirs(cartella_wav, exist_ok=True)
        
        if tipo == 'm4a':
            converti_m4a_in_wav(file_audio, file_audio_wav)                             # converte nel formato .wav i files .m4a / .mp3 / .3ga
            
        elif tipo == 'mp3':
            converti_mp3_in_wav(file_audio, file_audio_wav)
            
        elif tipo == '3ga':
            converti_3ga_in_wav(file_audio, file_audio_wav)
            
        elif tipo == 'wav':
            file_audio_wav = cartella_wav  + '/' + ottieni_nome_file(file_audio)
            shutil.copy(file_audio,file_audio_wav)
            
        else:
            print('ERROR! : audio-file type unknown')
            
        if split_wav(file_audio_wav):
        
            os.remove(file_audio_wav)
        
        nome_file_testo =  ottieni_cartella_da_percorso(file_audio) + '/' + cambia_estensione(ottieni_nome_file(file_audio),"txt",get_timestamp())
        
        if estrai_testo(cartella_wav,nome_file_testo):
            
            shutil.rmtree(cartella_wav)
        
    else:
        print("Nessun file selezionato!")        

if __name__ == "__main__":
    
    file_audio,tipo = seleziona() # apre una finestra di selezione del file
    
    converti_in_testo(file_audio,tipo)
    