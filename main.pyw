import datetime
import PySimpleGUI as sg
from psgtray import SystemTray
from configurator import Configurator
from startup import RunAtStartup
import winshell as ws
import time_calculator as tc
import threading


def background_process():
    while True:
        days = conf.get_value('days')
        hours = conf.get_value('hours')
        minutes = conf.get_value('minutes')
        old_time = conf.get_value('latest_time')

        if old_time <= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            clean(old_time, days, hours, minutes)


def clean(old_time, days, hours, minutes):
    try:
        ws.recycle_bin().empty(confirm=False, show_progress=False)

    except Exception as e:
        print('Recycle bin is already empty')

    finally:
        new_time = tc.time_difference(old_time, days, hours, minutes)
        conf.latest_time = new_time.strftime('%Y-%m-%d %H:%M:%S')
        conf.save_config_file()


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

    window = sg.Window(WINDOW_TITLE, layout, icon=ICON, font=(FONT_FAMILY, FONT_SIZE), finalize=True,
                       enable_close_attempted_event=True)
    tray = SystemTray(tray_menu, single_click_events=False, window=window, tooltip='BinCleaner', icon=ICON)

    while True:
        event, values = window.read()

        if event == 'Exit':
            break

        # Event selections for Tray
        if event == tray.key:
            event = values[event]

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()

        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_message('BinCleaner', 'BinCleaner minimized to tray!')
            tray.show_icon()

        # Event selections for Buttons
        if event == 'Apply':
            conf.days = values['-D-']
            conf.hours = values['-H-']
            conf.minutes = values['-M-']
            conf.on_boot = values['-ONBOOT-']
            conf.save_config_file()

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

    sg.theme("Reddit")
    sg.set_options(font=(FONT_FAMILY, FONT_SIZE), force_modal_windows=True, dpi_awareness=True,
                   auto_size_buttons=True, auto_size_text=True)

    DAYS = list(range(0, 31))
    HOURS = list(range(0, 24))
    MINUTES = list(range(0, 60))

    conf = Configurator()
    conf.create_on_start()

    conf.latest_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conf.save_config_file()

    startup_app = RunAtStartup('BinCleaner', user=True)

    main = threading.Thread(target=main_window(), args=(1,))
    bgp = threading.Thread(target=background_process(), args=(1,))
    main.start()
    bgp.start()
