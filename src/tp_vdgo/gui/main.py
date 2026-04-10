from tp_vdgo.gui.app import Application
from tp_vdgo.gui.widgets.main_window import MainWindow


def run():
    """
    Запуск GUI приложения.
    """

    app = Application()

    window = MainWindow()
    window.show()

    return app.exec()