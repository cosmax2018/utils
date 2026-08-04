# QR Generator 2.0

Applicazione desktop Windows per creare, archiviare, copiare e stampare etichette
QR. Comprende un piccolo inventario e l'esportazione PDF.

## Novita della versione pulita

- nessun codice duplicato o modulo obsoleto;
- un unico database SQLite nella cartella utente;
- query con nomi di campo, non indici numerici fragili;
- inventario completamente collegato alla GUI;
- errori visibili all'utente e registrati in un file di log;
- QR ridimensionati senza sfocare i moduli;
- report multipagina con intestazione su ogni pagina;
- sorgente separato dagli artefatti di compilazione.

I dati vengono salvati in `%LOCALAPPDATA%\QRGenerator` su Windows. L'applicazione
non modifica i database della vecchia versione.

Per importare una copia dei dati precedenti, eseguire una sola volta:

```powershell
python migrate_legacy.py "C:\percorso\della\vecchia\cartella\qrcode"
```

## Installazione

Richiede Python 3.11 o successivo.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Uso essenziale

1. Inserire il contenuto e, se necessario, il seriale.
2. Premere **Crea QR**.
3. Usare **Salva PNG**, **Salva SVG**, **Copia** o **Stampa**.

Il PNG contiene QR e testo in formato etichetta. L'SVG contiene il QR vettoriale.
Il comando **Nuovo** evita di sovrascrivere un'etichetta precedentemente caricata.

Nella scheda **Inventario** si possono aggiungere asset e creare il relativo QR.
La scheda **Report** esporta tutti gli asset in PDF.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Creazione dell'eseguibile

Installare le dipendenze di sviluppo e compilare dalla cartella del progetto:

```powershell
python -m pip install -r requirements-dev.txt
pyinstaller --noconfirm --clean --windowed --name QRGenerator main.py
```

L'eseguibile viene creato in `dist\QRGenerator`. Le cartelle `build` e `dist` non
devono essere incluse nell'archivio sorgente.
