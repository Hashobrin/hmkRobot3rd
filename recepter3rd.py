import PySimpleGUI as sg
import cv2
import numpy as np
import datetime

from user import User
from dbController import authenticate, setReserve, addUser, getUser, getOrder 
import qrcode_generator, qrcode_read
import sendEmail

def loginPage():
    signup_btn = sg.Button('Sign Up', size=(30, 3), key='-signup-')
    login_btn = sg.Button('Login', size=(30, 3), key='-login-')

    layout = [
        [sg.Text('ID:', size=(30, 3)), sg.Input(key='-id-')],
        [
            sg.Text('Password:', size=(30, 3)),
            sg.Input(key='-pw-', password_char='*'),
        ],
        [signup_btn, login_btn],
    ]

    window = sg.Window(title='Recepter', layout=layout)

    while True:
        event, values = window.read()

        if event in ('Quit', 'Exit', sg.WIN_CLOSED):
            break
        elif event == '-signup-':
            window.Hide()
            main_return = signupPage()
            if main_return is None:
                break
            window.UnHide()
        elif event == '-login-':
            if authenticate(values['-id-'], values['-pw-']):
                window.Hide()
                main_return = homePage(values['-id-'])
                window['-id-'].update('')
                window['-pw-'].update('')
                if main_return is None:
                    break
                window.UnHide()
            else:
                window['-id-'].update('')
                window['-pw-'].update('')
            
    window.close()

def signupPage():
    login_btn = sg.Button('Login', size=(30, 3), key='-login-')
    submit_btn = sg.Button('Submit', size=(30, 3), key='-submit-')
    this_year = datetime.datetime.now().year
    
    year_list = []
    for i in range(1900, this_year+1):
        year_list.insert(0, str(i))
    year_tuple = tuple(year_list)
    month_list = []
    for i in range(1, 12+1):
        month_list.append(str(i))
    month_tuple = tuple(month_list)
    date_list = []
    for i in range(1, 31+1):
        date_list.append(str(i))
    date_tuple = tuple(date_list)

    male_radio = sg.Radio(
        'male', size=(30, 3), group_id='gender', key='-male-', default=True
        )
    female_radio = sg.Radio(
        'female', size=(30, 3), group_id='gender', key='-female-', default=False
        )
    etc_radio = sg.Radio(
        'etc', size=(30, 3), group_id='gender', key='-etc-', default=False
        )
    gender_combo = sg.Combo(
        ('male', 'female', 'etc'),
        size=(30, 3),
        key='-gender-',
        default_value='male',
    )
    
    year_combo = sg.Combo(
        year_tuple, size=(30, 10), key='-year-', default_value=this_year
    )
    month_combo = sg.Combo(
        month_tuple, size=(30, len(month_tuple)), key='-month-', default_value=month_tuple[0]
    )
    date_combo = sg.Combo(
        date_tuple, size=(30, len(date_tuple)), key='-date-', default_value=date_tuple[0]
    )

    layout = [
        [sg.Text('Email:', size=(30, 3)), sg.Input(key='-email-')],
        [
            sg.Text('Password:', size=(30, 3)),
            sg.Input(key='-pw-', password_char='*'),
        ],
        [
            sg.Text('Retype Password:',size=(30, 3)),
            sg.Input(key='-retype-', password_char='*'),
        ],
        [sg.Text('Name:', size=(30, 3)), sg.Input(key='-name-')],
        [sg.Text('Gender:', size=(30, 3))],
        # [male_radio, female_radio, etc_radio,],
        [gender_combo],
        [sg.Text('BirthDay:', size=(30, 3))],
        [
            sg.Text('Year:', size=(30, 3)),year_combo,
            sg.Text('Month:', size=(30, 3)),month_combo,
            sg.Text('Date:', size=(30, 3)),date_combo,
        ],
        [login_btn, submit_btn],
    ]

    window = sg.Window(title='Recepter', layout=layout)
    ret = None

    while True:
        event, values = window.read()

        # if values['-male-'] == True:
        #     gender = 0
        # if values['-female-'] == True:
        #     gender = 1
        # if values['-etc-'] == True:
        #     gender = 2
        
        if event in ('Quit', 'Exit', sg.WIN_CLOSED):
            break
        elif event == '-login-':
            ret = True
            break
        elif event == '-submit-':
            if values['-pw-'] == values['-retype-']:
                user = User(
                    values['-email-'],
                    values['-pw-'],
                    values['-name-'],
                    values['-gender-'],
                    int(values['-year-']),
                    int(values['-month-']),
                    int(values['-date-']),
                )
                addUser(user)
                ret = True
                break
            else:
                window['-pw-'].update('')
                window['-retype-'].update('')

    window.close()
    return ret

def homePage(id):
    size = (30, 3)
    email = sg.Text(getUser(id)['email'], size=size)
    pw = sg.Text(getUser(id)['pw'], size=size)
    name = sg.Text(getUser(id)['name'], size=size)
    gender = sg.Text(getUser(id)['gender'], size=size)
    birth_year = getUser(id)['birth_year']
    birth_month = getUser(id)['birth_month']
    birth_date = getUser(id)['birth_date']
    birthday = sg.Text(
        str(birth_year) + '/' + str(birth_month) + '/' + str(birth_date),
        size=size,
    )

    frame1 = sg.Frame(
        title='Infomation',
        layout = [
            [sg.Text('Email:', size=size), email],
            [sg.Text('Password:', size=size), pw],
            [sg.Text('Your name:', size=size), name],
            [sg.Text('Gender:', size=size), gender],
            [sg.Text('Birth day:', size=size), birthday],
            [
                sg.Button('Logout', size=size, key='-logout-'),
            ],
        ]
    )

    hour_list = []
    for i in range(0, 24):
        hour_list.append(i)
    hour_tuple = tuple(hour_list)

    min_list = []
    for i in range(0, 60):
        min_list.append(i)
    min_tuple = tuple(min_list)

    frame2 = sg.Frame(
        title='Reserve',
        layout=[
            [sg.Text('Room number:', size=size), sg.Input(key='-room-')],
            [
                sg.Text('Check in at:', size=size),
                sg.Combo(hour_tuple, key='-checkin_hour-', default_value=hour_tuple[0]),
                sg.Text(':'),
                sg.Combo(min_tuple, key='-checkin_min-', default_value=min_tuple[0]),
            ],
            [
                sg.Text('Check out at:', size=size),
                sg.Combo(
                    hour_tuple, key='-checkout_hour-', default_value=hour_tuple[0]
                ),
                sg.Text(':'),
                sg.Combo(
                    min_tuple, key='-checkout_min-', default_value=min_tuple[0]
                ),
            ],
            [sg.Button('Submit', size=size, key='-submit-')],
        ]
    )

    frame3 = sg.Frame(
        title='result',
        layout=[
            [
                sg.Text('Room number:', size=size),
                sg.Text('', size=size, key='-show_room-'),
            ],
            [
                sg.Text('Check in at:', size=size),
                sg.Text('', size=size, key='-show_checkin-'),
            ],
            [
                sg.Text('Check out at:', size=size),
                sg.Text('', size=size, key='-show_checkout-'),
            ],
            [sg.Button('show QRCode',size=size, key='-qr-'),],
        ]
    )

    layout = [
        [frame1, frame2],
        [frame3,],
    ]

    window = sg.Window('My Home', layout=layout)
    ret = None
    recording = False

    while True:
        event, values = window.read()

        if event in ('Quit', 'Exit', sg.WIN_CLOSED):
            break
        if event == '-logout-':
            ret = True
            break
        elif event == '-qr-':
            qr = int(qrcode_read.detect())
            window['-show_room-'].update(getOrder(qr)['room'])
            in_hour = str(getOrder(qr)['checkin_hour'])
            in_min = str(getOrder(qr)['checkin_min'])
            show_checkin = in_hour + ':' + in_min
            out_hour = str(getOrder(qr)['checkout_hour'])
            out_min = str(getOrder(qr)['checkout_min'])
            show_checkout = out_hour + ':' + out_min
            window['-show_checkin-'].update(show_checkin)
            window['-show_checkout-'].update(show_checkout)
            
        elif event == '-submit-':
            setReserve(
                values['-room-'],
                values['-checkin_hour-'],
                values['-checkin_min-'],
                values['-checkout_hour-'],
                values['-checkout_min-'],
            )
            qrcode_generator.generate()
            sendEmail.main(id)
            window['-room-'].update('')
            window['-checkin_hour-'].update('')
            window['-checkin_min-'].update('')
            window['-checkout_hour-'].update('')
            window['-checkout_min-'].update('')

    window.close()
    return ret

if __name__ == '__main__':
    loginPage()