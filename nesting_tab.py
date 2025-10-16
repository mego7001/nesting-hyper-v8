# ui/nesting_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
    QLabel, QGroupBox, QFormLayout, QDoubleSpinBox, QComboBox,
    QSpinBox, QMessageBox, QProgressBar, QSplitter, QTableWidget,
    QTableWidgetItem, QGraphicsView, QGraphicsScene
)
from PyQt6.QtCore import Qt, QRunnable, QThreadPool, pyqtSignal, QObject
from core.nesting_engine import NestingEngine


class NestingWorker(QObject, QRunnable):
    progress = pyqtSignal(int)
    result_ready = pyqtSignal(object)

    def __init__(self, parts, sheets, settings):
        super().__init__()
        self.parts = parts
        self.sheets = sheets
        self.settings = settings

    def run(self):
        engine = NestingEngine(self.settings)
        result = engine.nest(self.parts, self.sheets)
        self.result_ready.emit(result)


class NestingTab(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.threadpool = QThreadPool()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        # Toolbar
        toolbar = QHBoxLayout()
        start_btn = QPushButton('Start')
        start_btn.clicked.connect(self.start_nesting)
        stop_btn = QPushButton('Stop')
        stop_btn.clicked.connect(self.stop_nesting)
        self.spacing_input = QDoubleSpinBox()
        self.spacing_input.setValue(self.settings['spacing']['part_to_part'])
        self.margin_input = QDoubleSpinBox()
        self.margin_input.setValue(self.settings['spacing']['margin'])
        strategy_combo = QComboBox()
        strategy_combo.addItems(['Max Efficiency', 'Balanced', 'Repeat Preferences'])
        toolbar.addWidget(start_btn)
        toolbar.addWidget(stop_btn)
        toolbar.addWidget(QLabel('Part to Part:'))
        toolbar.addWidget(self.spacing_input)
        toolbar.addWidget(QLabel('Margin:'))
        toolbar.addWidget(self.margin_input)
        toolbar.addWidget(QLabel('Strategy:'))
        toolbar.addWidget(strategy_combo)
        layout.addLayout(toolbar)

        # Splitter for results and preview
        splitter = QSplitter(Qt.Orientation.Vertical)
        # Results table
        self.results_table = QTableWidget(0, 2)
        self.results_table.setHorizontalHeaderLabels(['Solution', 'Efficiency'])
        splitter.addWidget(self.results_table)
        # Layout preview
        view_frame = QFrame()
        view_layout = QVBoxLayout(view_frame)
        self.graphic_view = QGraphicsView()
        self.graphic_scene = QGraphicsScene()
        self.graphic_view.setScene(self.graphic_scene)
        view_layout.addWidget(self.graphic_view)
        splitter.addWidget(view_frame)
        layout.addWidget(splitter)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

    def start_nesting(self):
        # Dummy parts and sheets
        parts = []  # to be loaded from previous tabs
        sheets = []
        worker = NestingWorker(parts, sheets, self.settings)
        worker.result_ready.connect(self.on_result)
        self.threadpool.start(worker)

    def stop_nesting(self):
        self.threadpool.clear()
        QMessageBox.information(self, 'Stop', 'Nesting stopped.')

    def on_result(self, result):
        # Display result in table and preview
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        self.results_table.setItem(row, 0, QTableWidgetItem('Solution 1'))
        self.results_table.setItem(row, 1, QTableWidgetItem(str(round( result,2))))
        # TODO: draw layout
        QMessageBox.information(self, 'Done', 'Nesting completed.')
