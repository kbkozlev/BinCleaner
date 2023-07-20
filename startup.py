import pywintypes
from win32api import (GetModuleFileName, RegCloseKey, RegDeleteValue,
                      RegOpenKeyEx, RegSetValueEx, RegEnumValue)
from win32con import (HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, KEY_WRITE,
                      KEY_QUERY_VALUE, REG_SZ)
from winerror import ERROR_NO_MORE_ITEMS


class RunAtStartup:
    STARTUP_KEY_PATH = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"

    def __init__(self, appname, path=None, user=False):
        self.appname = appname
        self.path = path
        self.user = user

    def _open_registry_key(self):
        return RegOpenKeyEx(
            HKEY_CURRENT_USER if self.user else HKEY_LOCAL_MACHINE,
            RunAtStartup.STARTUP_KEY_PATH,
            0,
            KEY_WRITE | KEY_QUERY_VALUE
        )

    def _entry_exists(self, key):
        i = 0
        while True:
            try:
                name, _, _ = RegEnumValue(key, i)
            except pywintypes.error as e:
                if e.winerror == ERROR_NO_MORE_ITEMS:
                    break
                else:
                    raise
            if name == self.appname:
                return True
            i += 1
        return False

    def add_to_startup(self):
        key = self._open_registry_key()
        if not self._entry_exists(key):
            RegSetValueEx(key, self.appname, 0, REG_SZ, self.path or GetModuleFileName(0))
        RegCloseKey(key)

    def add_script_to_startup(self, script_path):
        self.path = '{} "{}"'.format(GetModuleFileName(0), script_path)
        self.add_to_startup()

    def remove_from_startup(self):
        key = self._open_registry_key()
        try:
            if self._entry_exists(key):
                RegDeleteValue(key, self.appname)
        except Exception as e:
            print(e)
        finally:
            RegCloseKey(key)
