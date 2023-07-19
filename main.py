import PySimpleGUI as sg
from psgtray import SystemTray
import winshell as ws


def main_window():
    tray_menu = ['', ['Show Window', 'Hide Window', '---', 'Exit']]
    app_menu = [['Help', ['About', 'Check for Updates']]]

    layout = [[sg.Menubar(app_menu)],
              [sg.T('Delete Frequency:'), sg.T('M:'),
               sg.DropDown(months, default_value='0', key='-M-'), sg.T('D:'),
               sg.DropDown(days, default_value='0', key='-D-'), sg.T('H:'),
               sg.DropDown(hours, default_value='0', key='-H-'), sg.T('M:'),
               sg.DropDown(minutes, default_value='0', key='-M-')],
              [sg.HSeparator()],
              [sg.Checkbox('Start on boot', key='-ONBOOT-')],
              [sg.Button('Apply'), sg.Button('Exit')]
              ]

    window = sg.Window(window_title, layout, icon=icon, font=(font_family, font_size), finalize=True,
                       enable_close_attempted_event=True)
    tray = SystemTray(tray_menu, single_click_events=False, window=window, tooltip='BinCleaner', icon=icon)

    while True:
        event, values = window.read()

        if event == tray.key:
            event = values[event]

        if event == 'Exit':
            break

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()

        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_message('BinCleaner', 'BinCleaner minimized to tray!')
            tray.show_icon()

        if event == 'Apply':
            try:
                ws.recycle_bin().empty(confirm=True, show_progress=False)

            except:
                print('Recycle bin is already empty')

    tray.close()
    window.close()


if __name__ == "__main__":
    release = '1.0.0'
    window_title = f"BinCleaner v{release}"
    font_family = "Arial"
    font_size = 10
    bt_color = "#015FB8"
    icon = "BinCleaner.ico"

    sg.theme("Reddit")
    sg.set_options(font=(font_family, font_size), force_modal_windows=True, dpi_awareness=True,
                   auto_size_buttons=True, auto_size_text=True)

    months = list(range(0, 13))
    days = list(range(0, 31))
    hours = list(range(0, 24))
    minutes = list(range(0, 60))

    main_window()
