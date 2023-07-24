import datetime
import time
import webbrowser
import re
import PySimpleGUI as sg
import winshell as ws
import functions as fn
import multiprocessing as mp
import threading as th
from psgtray import SystemTray
from configurator import Configurator
from startup import RunAtStartup


def background_process(conf, initial):
    while True:
        days = conf.get_value('days')
        hours = conf.get_value('hours')
        minutes = conf.get_value('minutes')
        old_time = conf.get_value('latest_time')

        if old_time <= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            if not initial:
                clean(conf, old_time, days, hours, minutes)


def clean(conf, old_time, days, hours, minutes):
    if conf.get_value('on_start'):
        new_time = fn.time_difference(old_time, days, hours, minutes)
        conf.latest_time = new_time.strftime('%Y-%m-%d %H:%M:%S')
        conf.on_start = False
        conf.save_config_file()

    else:
        try:
            ws.recycle_bin().empty(confirm=False, show_progress=False)

        except Exception as e:
            print('Recycle bin is already empty')

        finally:
            new_time = fn.time_difference(old_time, days, hours, minutes)
            conf.latest_time = new_time.strftime('%Y-%m-%d %H:%M:%S')
            conf.save_config_file()


def re_start_window():
    layout = [[sg.Push(), sg.T('The application will now exit'), sg.Push()],
              [sg.Push(), sg.T('Re-start is needed for the changes to apply!'), sg.Push()],
              [sg.Push(), sg.Button('OK'), sg.Push()]]

    window = sg.Window('Apply changes', layout, icon=ICON, keep_on_top=True)
    while True:
        event, values = window.read()

        if event in ('OK', sg.WINDOW_CLOSED):
            window.close()
            break


def about_window():
    layout = [[sg.Push(), sg.T(str(WINDOW_TITLE), font=(FONT_FAMILY, 12, "bold")), sg.Push()],
              [sg.T(s=40)],
              [sg.Push(), sg.T(github_url['name'], enable_events=True, font=(FONT_FAMILY, FONT_SIZE, "underline"),
                               justification='l', text_color='#0066CC',
                               auto_size_text=True, key='download'), sg.Push()],
              [sg.Push(), sg.T("License: GPL-3.0", justification='c'), sg.Push()],
              [sg.T()],
              [sg.Push(), sg.T("Copyright © 2023 Kaloian Kozlev", text_color='light grey'), sg.Push()]]

    window = sg.Window("About", layout, icon=ICON)

    while True:
        event, values = window.read()

        match event:

            case sg.WIN_CLOSED:
                break

            case 'download':
                webbrowser.open(github_url['url'])
                window.close()


def updates_window(current_release):
    latest_release, download_url = fn.get_latest_version()
    layout = [[sg.Push(), sg.T('Version Info', font=(FONT_FAMILY, 12, 'bold')), sg.Push()],
              [sg.T()],
              [sg.T('Current Version:', s=13), sg.T(f'{current_release}', font=(FONT_FAMILY, 10, 'bold'))],
              [sg.T(f'Latest Version:', s=13), sg.T(f'{latest_release}', font=(FONT_FAMILY, 10, 'bold'))],
              [sg.T(s=40, justification="c", key="-INFO-")],
              [sg.Push(), sg.B('Download', key='download', button_color=BT_COLOR, s=16), sg.Push()]]

    window = sg.Window("Check for Updates", layout, icon=ICON)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        match event:

            case 'download':
                if latest_release is not None:
                    current_release = re.sub(r'[^0-9]', '', current_release)
                    latest_release = re.sub(r'[^0-9]', '', latest_release)

                    if int(latest_release) > int(current_release):
                        webbrowser.open(download_url)
                        window.close()

                    else:
                        window['-INFO-'].update("You have the latest version", text_color='green')

                else:
                    window['-INFO-'].update("Cannot fetch version data", text_color='red')

        window.refresh()
        time.sleep(1)
        window["-INFO-"].update(" ")


def main_window():

    tray_menu = ['', ['Show Window', 'Hide Window', '---', 'Exit']]
    app_menu = [['Help', ['About', 'Check for Updates']]]

    layout = [[sg.Menubar(app_menu)],
              [sg.T('Delete Frequency:'), sg.T('D:'),
               sg.DropDown(DAYS, default_value=str(conf.days), key='-D-'), sg.T('H:'),
               sg.DropDown(HOURS, default_value=str(conf.hours), key='-H-'), sg.T('M:'),
               sg.DropDown(MINUTES, default_value=str(conf.minutes), key='-M-')],
              [sg.HSeparator()],
              [sg.Checkbox('Start on boot', key='-ONBOOT-', default=conf.on_boot)],
              [sg.Button('Apply'), sg.Button('Exit')]
              ]

    window = sg.Window(WINDOW_TITLE, layout, icon=ICON, finalize=True,
                       enable_close_attempted_event=True)
    tray = SystemTray(tray_menu, single_click_events=False, window=window, tooltip='BinCleaner', icon=ICON)
    tray.show_message('BinCleaner', 'BinCleaner running!', )

    while True:
        event, values = window.read()

        # Event selections for Tray
        if event == tray.key:
            event = values[event]

        if event in ('Exit', sg.WINDOW_CLOSED):
            break

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()

        if event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_message('BinCleaner', 'BinCleaner minimized to tray!')
            tray.show_icon()

        # Event selections for Buttons
        if event == 'Apply':
            if not conf.get_value('initial'):
                bgp.terminate()
            conf.days = values['-D-']
            conf.hours = values['-H-']
            conf.minutes = values['-M-']
            conf.on_boot = values['-ONBOOT-']
            conf.initial = False
            conf.save_config_file()
            re_start_window()
            break

        if event == 'About':
            about_window()

        if event == 'Check for Updates':
            updates_window(RELEASE)

        # Check for on-boot
        if conf.on_boot:
            # startup_app.add_to_startup()
            """If you are running this app from sourcecode uncomment the line below and comment the one above"""
            startup_app.add_script_to_startup(__file__)
        else:
            startup_app.remove_from_startup()

    tray.close()
    window.close()


if __name__ == "__main__":
    RELEASE = '1.0.0'
    WINDOW_TITLE = f"BinCleaner v{RELEASE}"
    FONT_FAMILY = "Arial"
    FONT_SIZE = 10
    BT_COLOR = "#015FB8"
    ICON = "BinCleaner.ico"

    theme = sg.theme("Reddit")
    sg.set_options(font=(FONT_FAMILY, FONT_SIZE), force_modal_windows=True, dpi_awareness=True,
                   auto_size_buttons=True, auto_size_text=True)

    DAYS = list(range(0, 31))
    HOURS = list(range(0, 24))
    MINUTES = list(range(0, 60))

    github_url = {'name': 'Official GitHub Page',
                  'url': 'https://github.com/kbkozlev/BinCleaner'}

    # Services and configurations
    conf = Configurator()
    conf.create_on_start()

    conf.latest_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conf.on_start = True
    conf.save_config_file()
    initial = conf.get_value('initial')

    startup_app = RunAtStartup('BinCleaner', user=True)

    main = th.Thread(target=main_window)
    bgp = mp.Process(target=background_process, args=(conf, initial))
    bgp.daemon = True
    if not initial:
        bgp.start()
    main.start()
