from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from pathlib import Path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._load_ui()
        self._connect_signals()

    def _load_ui(self):
        ui_path = (
            Path(__file__).parent.parent
            / "views"
            / "main_window.ui"
        )

        loader = QUiLoader()
        ui_file = QFile(str(ui_path))
        ui_file.open(QFile.ReadOnly)

        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(self.ui)

    def _connect_signals(self):
        # пример подключения кнопки
        if hasattr(self.ui, "pushButton"):
            self.ui.pushButton.clicked.connect(self.on_click)

    def on_click(self):
        print("Button clicked")