import time
import ctypes

# Структура для получения данных от Windows
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_system_idle_time():
    """Возвращает время бездействия системы в секундах"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    # Вызываем системную функцию Windows
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        # Получаем время работы системы и время последнего ввода (в миллисекундах)
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    return 0

class IdleManager:
    def __init__(self, root, timeout, on_idle_callback, on_resume_callback):
        self.root = root
        self.timeout = timeout
        self.on_idle_callback = on_idle_callback
        self.on_resume_callback = on_resume_callback
        self.is_idle = False

    def check_idle(self):
        # Получаем реальное время простоя системы (независимо от окна)
        idle_time = get_system_idle_time()
        
        if idle_time > self.timeout:
            if not self.is_idle:
                self.is_idle = True
                self.on_idle_callback()
        else:
            if self.is_idle:
                self.is_idle = False
                self.on_resume_callback()

        # Проверяем достаточно часто (например, раз в секунду)
        self.root.after(1000, self.check_idle)

    def update_timeout(self, new_timeout):
        self.timeout = new_timeout