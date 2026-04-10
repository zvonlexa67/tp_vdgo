# tp_vdgo/gui/app.py

import sys
from PySide6.QtWidgets import QApplication


class Application:
    """
    Обёртка над QApplication.
    Здесь настраиваются:
    - стиль
    - тема
    - DI контейнер
    - глобальные сервисы
    """

    def __init__(self):
        self.qt_app = QApplication.instance() or QApplication(sys.argv)

        self._configure()

    def _configure(self):
        self.qt_app.setApplicationName("TP_VDGO")
        self.qt_app.setOrganizationName("tp_vdgo")

        # пример:
        # self.qt_app.setStyle("Fusion")

    def exec(self):
        return self.qt_app.exec()