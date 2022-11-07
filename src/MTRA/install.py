#  coding=ascii
import platform
import os
import zipfile
import requests
import pathlib


# Instalacion de apps necesarias!
run_in = platform.system() # Obtenemos el sistema operativo actual.


# Diccionario de plataformas.
platforms = {'Windows': 'Windows', 'Linux': 'Linux', 'Mac': 'Darwin'}  # Plataformas (Si, Mac es Darwin XD)




                                           # Comandos:
# - Windows:
apps_commands_win = {'Ombi': 'https://github.com/ombi-app/ombi/releases/download/v4.29.2/win10-x64.zip', 'Jackett': 'winget install -e --id Jackett.Jackett', 'qBitTorrent': 'winget install -e --id qBittorrent.qBittorrent', 'Plex': 'winget install -e --id Plex.Plex', 'Python 3.9': 'winget install -e --id Python.Python.3.9'} # Clave = Nombre de la app. Valor = Comando winget.

# apps_commands_linux = {'qBittorrent': 'sudo apt install qbittorrent', 'qBittorrent_next', 'sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable', 'qBittorrent_install': 'sudo apt install qbittorrent', 'Jackett Prerequisite 1': 'sudo apt install mono-devel', 'Jackett Prerequisite 2', 'sudo apt install gnupg ca-certificates' }




# INFO:
print('Tus aplicaciones se comenzaran a instalar. Una vez se comiencen a instalar le recomendamos no canelar la instalacion, esto podria conllevar serios problemas.')

# Preguntamos al usuario si queire continuar, para que una vez comenzado, se trate de evitar la mayor cantidad de errores posibles.
continue_ask = input('Seguro quiere continuar? [Y] Yes, [N] No. | ---------->  ').upper()

# Pregunt si tienen Python, ya que es util  que tambien se pueda instalar desde aca.
python_ask = input('Quiere instalar Python? [Y] Yes, [N] No. | ---------->  ').upper()




if continue_ask == 'Y':
    print('\n\nLos programas se comenzaran a instalar. No cancele nada por favor. Es probable que se pidan permisos de administrador.\n\n')
    actual_dir = os.path.abspath(os.getcwd())


    try:
        os.mkdir(f'{actual_dir}/otherApps')

    except:
        pass


    if run_in == 'Windows':

        if python_ask == 'Y':
            for command_count, command in enumerate(list(apps_commands_win.values())[::-1]): # Si se quiere instalar python, volveamos la lista e instalamos Python primero que todo.
                
                if 'http' in command: # Si es un link...
                    if 'ombi' in command:
                        print('\n\nDescargando Ombi...')
                        download_ombi = requests.get(command)
                        open(f'{actual_dir}/otherApps/ombi.zip', 'wb').write(download_ombi.content)

                        extract_ombi = zipfile.ZipFile(f'{actual_dir}/otherApps/ombi.zip', 'r')


                        try:
                            os.mkdir(f'{actual_dir}/otherApps/ombi')
                        except:
                            pass

                        try:
                            print('Extrayendo archivo zip de Ombi...\n\n')
                            extract_ombi.extractall(path = f'{actual_dir}/otherApps/ombi')
                        except:
                            pass

                        extract_ombi.close()
                        os.remove(f'{actual_dir}/otherApps/ombi.zip')

                else:
                    print(f'\n\nEjecutando el comando {command}...\n\n')


                    i = os.system(command) # Se ejecuta el comando!


                    # Manage finally.
                    if i == 0: # Si "i" devuelve 0, quiere decir que se ejecuto de manera correcta y no tiro error.
                        print(f'\n\n ======== Hemos instalado correctamente {list(apps_commands_win.keys())[command_count]} ======== \n\n')
                    else:
                        print(f'\n\nHemos tenido un error al instalar {list(apps_commands_win.keys())[command_count]}\n\n')

                    
        else:
            for command_count, command in enumerate(list(apps_commands_win.values())[:-1]):
               
                if 'http' in command: # Si es un link...
                    if 'ombi' in command:
                        print('\n\nDescargando Ombi...')
                        download_ombi = requests.get(command)
                        open(f'{actual_dir}/otherApps/ombi.zip', 'wb').write(download_ombi.content)

                        extract_ombi = zipfile.ZipFile(f'{actual_dir}/otherApps/ombi.zip', 'r')


                        try:
                            os.mkdir(f'{actual_dir}/otherApps/ombi')
                        except:
                            pass

                        try:
                            print('Extrayendo archivo zip de Ombi...\n\n')
                            extract_ombi.extractall(path = f'{actual_dir}/otherApps/ombi')
                        except:
                            pass

                        extract_ombi.close()
                        os.remove(f'{actual_dir}/otherApps/ombi.zip')


                else:
                    print(f'\n\nEjecutando el comando {command}...\n\n')


                    i = os.system(command) # Ejecutamos el comando.


                    # Manejo de la instalacion.
                    if i == 0: 
                        print(f' ======== Hemos instalado correctamente {list(apps_commands_win.keys())[command_count]} ======== ')

                    else:
                        print(f'Hemos tenido un error al instalar {list(apps_commands_win.keys())[command_count]}')





    elif run_in == 'Linux':
        print('Hola! Parece que estas corriendo el programa en Linux y aun no tenemos soporte para este sistema, te recomendamos instalar manualmente cada app o tener paciencia y esperar a que lo desarrollemos.')


    elif run_in == 'Darwin':
        print('Hola! Parece que estas corriendo el programa en Linux y aun no tenemos soporte para este sistema, te recomendamos instalar manualmente cada app o tener paciencia y esperar a que lo desarrollemos.')



else:
    print('Perfecto! Cuidate uwu.')
    exit()