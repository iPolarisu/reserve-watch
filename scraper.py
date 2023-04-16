import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'https://ucampus.uchile.cl/upasaporte/adi'

# generate payload for ucampus login
def generate_payload(username, password):
    payload = {
        'servicio': 'fcfm',
        'debug': '0',
        'extras[_LB]': 'ucampus04-int',
        'extras[lang]': 'es',
        'extras[recordar]': '1',
        'username': username,
        'password': password,
        'recordar': '1',
    }
    return payload

# returns the reserves url given a certain date and space
def reserves_url(date, space):
    if not date:
        return f'https://ucampus.uchile.cl/m/fcfm_reservas/detalle?id={space}'
    else:
        return f'https://ucampus.uchile.cl/m/fcfm_reservas/detalle?fecha={date}&id={space}'

def profile_url(user_id):
    return f'https://www.u-cursos.cl/usuario/{user_id}/datos_usuario/'

# returns a list with the user_id of every reserve done in a given week
def get_reserves_id(reserves_url, payload):
    
    soup = None

    # login and getting info
    with requests.session() as s:

        # login
        post = s.post(LOGIN_URL, data=payload)
        
        # get page
        page = s.get(reserves_url)

        # parsed page
        soup = BeautifulSoup(page.content, 'html.parser')

    # get reserves div
    reserves = soup.find('div', {'id' : 'reservas'})

    # get schedule table
    schedule = reserves.find('table', {'class' : 'dhorario'})

    # get days from table
    days = schedule.findAll('td')
    days.pop(0)

    # collect ids for the week
    users_id = []

    # for each day
    for day in days:

        # for each block in a day
        block_users = day.findAll('li')
        for user in block_users:
            
            # get img data of user
            data = user.find('img')
            img_src = data['src']
            parsed_src = img_src.split('/')
            user_id = ''

            # user has picture
            try:
                user_id = parsed_src[7]

            # user only has initials
            except:
                user_id = parsed_src[6]
                user_id = user_id[:2]

            # add to weekly list
            users_id.append(user_id)
    
    return users_id

# returns a dictionary with (key) user _id -> (value) count  
def count_reserves_id(reserves_id):
    counted_reserves = {}

    # count each time id is shown in list
    for reserve_id in reserves_id:
        if reserve_id in counted_reserves:
            counted_reserves[reserve_id] += 1
        else:
            counted_reserves[reserve_id] = 1

    return counted_reserves

# filter counted_reserves by reserve_limit
def get_offenders(counted_reserves, reserve_limit):

    # remove non offenders from the given dictionary
    not_offenders = [reserve_id for reserve_id in counted_reserves if counted_reserves[reserve_id] <= reserve_limit]
    for not_offender in not_offenders:
        counted_reserves.pop(not_offender)

    return counted_reserves

# gets the offenders name given the ucursos id
def get_offenders_name(offenders_id):
    
    # offender id is not only initials
    if len(offenders_id) != 2:
        
        # get profile url
        offender_url = profile_url(offenders_id)
        
        # get page
        page = requests.get(offender_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # get offender name
        name = soup.find('div', {'class' : 'cont'})
        name = name.find('span').get_text().strip()

        return name

    # only initials
    else:
        
        return offenders_id

# creates a list with 'name - reserves number' for a given offenders list
def get_offenders_list(offenders):

    offenders_list = []
    
    # get names and add them to the 
    for offender in offenders:
        name = get_offenders_name(offender)
        name = name + ' - ' + str(offenders[offender])
        offenders_list.append(name)
    
    return offenders_list
