from PySide6.QtWidgets import QMainWindow, QDialog, QWidget, QStackedWidget

from tp_vdgo.gui.views.main_window_ui import Ui_MainWindow
from tp_vdgo.gui.views.radio_window_ui import Ui_Form
from tp_vdgo.gui.views.dialog_window_ui import Ui_Dialog


class DialogWindow(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # Сохраняем главный виджет ДО замены на QStackedWidget
        self._main_widget = self.centralwidget
        self._main_widget.setParent(None)

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)
        self._stack.addWidget(self._main_widget)

        self._radio_widget = QWidget()
        self._radio_ui = Ui_Form()
        self._radio_ui.setupUi(self._radio_widget)
        self._stack.addWidget(self._radio_widget)

        self._dialog = DialogWindow(self)

        self._connect_signals()

    def _connect_signals(self):
        self.pushButton.clicked.connect(self.on_click)
        self.DialogButton.clicked.connect(self.on_dialog_click)
        self._radio_ui.pushButton.clicked.connect(self.on_return_click)

    def on_click(self):
        self.pushButton.setEnabled(False)
        self._stack.setCurrentWidget(self._radio_widget)

    def on_dialog_click(self):
        self._dialog.exec()

    def on_return_click(self):
        self._stack.setCurrentWidget(self._main_widget)
        self.pushButton.setEnabled(True)