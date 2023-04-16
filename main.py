from os import system, name
import sys
import json
import getpass
import constants
import scraper
import re

BANNER = """

╭━━━━╮╱╱╱╱╱╱╭╮╭╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮
┃╭╮╭╮┃╱╱╱╱╱╱┃┃┃┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
╰╯┃┃┣┻━╮╭━━┳┫┃┃┃╭━━┳╮╭┳━━┳━━╮╭━━┳━━╮╭━━┳━━┳╮╭┳━━┳━━┳━╯┣━┳━━╮
╱╱┃┃┃┃━┫┃╭╮┣┫┃┃┃┃╭╮┃╰╯┃╭╮┃━━┫┃╭╮┃╭╮┃┃╭━┫╭╮┃╰╯┃╭╮┃╭╮┃╭╮┃╭┫┃━┫
╱╱┃┃┃┃━┫┃╰╯┃┃╰┫╰┫╭╮┃┃┃┃╰╯┣━━┃┃╰╯┃╰╯┃┃╰━┫╰╯┃┃┃┃╰╯┃╭╮┃╰╯┃┃┃┃━┫
╱╱╰╯╰━━╯┃╭━┻┻━┻━┻╯╰┻┻┻┻━━┻━━╯┃╭━┻━━╯╰━━┻━━┻┻┻┫╭━┻╯╰┻━━┻╯╰━━╯
╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
╱╱╱╱╱╱╱╱╰╯╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯

"""

POLARIS = "Polaris™"

INFORMATION = """
    Esta herramienta permite detectar usuarios que superen el límite de reservas semanales para determinados espacios de la FCFM (UCH) analizando el html que proporciona U-Campus a estudiantes que revisan la reserva de espacios. Esto ya que U-Campus no limita el número de reservas y por ende debe ser revisado manualmente.
"""

DISCLAIMER = """
    Para utilizar esta herramienta necesitas entregar credenciales de U-Campus para poder acceder a los datos de las reservas, esto es necesario para acceder al código fuente de la página y las credenciales no son enviadas a ningún otro lado (revisa el código para más detalles). De todas formas no me hago responsable por el uso que hagas de este código. 

    Lo mismo aplica para las acciones o consecuencias derivadas de la información obtenida, es meramente referencial y puede estar sujeta a errores (leer el README para detalles).

    Es posible que para algunos usuarios no obtengas nombres sino iniciales, a pesar de que es improbable, no es imposible que personas con las mismas iniciales hayan reservado durante la misma semana, por tanto recomiendo darle una vuelta si llegase a pasar.
    
    (sí sí ya te entendí solo quiero saber quién me anda robando horarios)
"""

def clear():
 
    if name == 'nt':
        _ = system('cls')
 
    else:
        _ = system('clear')


if __name__ == "__main__":
    
    print(BANNER)
    print(POLARIS)
    print("")
    print("- INFORMACIÓN -")
    print(INFORMATION)
    input('Presiona ENTER para continuar')
    clear()

    print('- DISCLAIMER - ')
    print(DISCLAIMER)
    input('Presiona ENTER si aceptas continuar')
    clear()
    
    space = ""
    while True:
        print('Indica el espacio que quieres revisar (piscina, gimnasio o squash):')
        space = input()
        if space in constants.SPACES:
            print("")
            break
        print("Espacio inválido, por favor indica un espacio válido")

    space = constants.SPACES[space]

    limit = ""
    while True:
        print("Indica el límite de reservas para este espacio (usualmente 2):")
        limit = input("")
        try:
            limit = int(limit)
            print("")
            break
        except:
            print("Indica un límite válido")

    print("Indica una fecha para revisar la respectiva semana (MM-DD)")
    print("Ejemplo para el 15 de abril: 04-15")
    print("También puedes omitir para revisar la semana actual:")
    date = input()
    if date:
        date = constants.YEAR + '-' + date
    print("")

    print("Indica tus credenciales de U-Campus")
    username = input('username: ')
    password = getpass.getpass('password: ')
    payload = scraper.generate_payload(username, password)
    print("")
    
    print("Iniciando análisis")
    print("")

    reserves_url = scraper.reserves_url(date, space)
    print("Revisando la siguiente URL: " + reserves_url)
    print("")

    reserves_id = []
    try:
        reserves_id = scraper.get_reserves_id(reserves_url, payload)
        print("Reservas obtenidas con éxito")
        print("")
    except:
        print("Ocurrió un error obteniendo la información de la página, revisa tus credenciales, fecha o la conexión a internet")
        exit(1)
    
    print("Contando reservas")
    counted_reserves = scraper.count_reserves_id(reserves_id)
    print("")

    print("Obteniendo lista de infractores")
    offenders = scraper.get_offenders(counted_reserves, limit)
    offenders_list = scraper.get_offenders_list(offenders)
    print("")

    print("Todo listo, estos son los resultados:")
    for offender in offenders_list:
        print(offender)