
# audit.py: programma per Oriano

import sys 

def transform_date(date):
    gg = date[8:10]
    mm = date[5:7]
    aa = date[:4]
    return  gg + '/' + mm + '/' + aa

def transform_date_(date):
    gg = date[6:9]
    mm = date[4:6]
    aa = date[:4]
    return  gg + '/' + mm + '/' + aa
    
def transform_date__title(date):
    gg = date[8:10]
    mm = date[5:7]
    aa = date[:4]
    return  aa + '-' + mm + '-' + gg
    
def main(argv):

    # lancia lo script PowerShell per prendere la lista dei programmi installati
    # import subprocess
    # process=subprocess.Popen(["powershell", \
                              # "Get-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize > .\\lista.txt"], \
                              # stdout=subprocess.PIPE)
    # result=process.communicate()

    # prende le informazioni percreare il nome del file
    import socket,datetime
    hostname = socket.gethostname()
    indirizzoip = socket.gethostbyname(hostname)
    date = transform_date(str(datetime.datetime.now())[:11])
    date_title = transform_date__title(str(datetime.datetime.now())[:11])

    print(f'Data della rilevazione: {date}')
     
    intestazione = "Programma                                                                                           	Tipo         	Versione                           	Rilevato il	Ultima rilevazione\n"
    pc_str = "PC: " + hostname + "\n"

    filename = open("softwareBL-" + date_title + " (" + hostname + " " + indirizzoip + ").txt", "w")

    filename.write(intestazione)

    filename.write(pc_str)

    try:
    
        with open(argv[0], encoding="utf-16") as fp:
            line = fp.readline()
            line = fp.readline()
            line = fp.readline()
            cnt = 1
            while line:
                line = fp.readline()
                line_ = line.strip()
                print(line_)
                if len(line_) != 0:
                    if line_[-1] != '\n':
                        if len(line_) > 124:
                            date_ = transform_date_(line_[-8:])
                        else:
                            date_ = ''
                        line__ = line_[:82] + '\t'+'\t'+'\t'+'\t'+'\t'+'\t' + 'Programmi' + '\t'+'\t' + line_[82:97] + '\t'+'\t'+'\t'+'\t'+'\t'+'\t' + date + '\t' + date_
                        filename.write(line__ + '\n')
                    else:
                        filename.write(line__)
                cnt += 1
        print(f'\n\n{cnt} lines processed')
                
    except IOError:
        print(f'Error! lista.txt file not found!')
        quit()
    except EOFError:
        print(f'Error! lista.txt file is empty!')
        quit()


    filename.close()


main(sys.argv[1:])

