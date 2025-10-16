# ui/export_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QGraphicsView, QGraphicsScene, QFileDialog,
    QMessageBox, QFrame, QSplitter
)
from PyQt6.QtCore import Qt


class ExportTab(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        toolbar = QHBoxLayout()
        dxf_btn = QPushButton('DXF/DWG Export')
        dxf_btn.clicked.connect(self.export_dxf)
        summary_btn = QPushButton('Summary Report')
        summary_btn.clicked.connect(self.summary_report)
        detailed_btn = QPushButton('Detailed Report')
        detailed_btn.clicked.connect(self.detailed_report)
        toolbar.addWidget(dxf_btn)
        toolbar.addWidget(summary_btn)
        toolbar.addWidget(detailed_btn)
        layout.addLayout(toolbar)

        splitter = QSplitter(Qt.Orientation.Vertical)
        self.results_table = QTableWidget(0, 2)
        self.results_table.setHorizontalHeaderLabels(['Solution', 'Efficiency'])
        splitter.addWidget(self.results_table)
        view_frame = QFrame()
        view_layout = QVBoxLayout(view_frame)
        self.graphic_view = QGraphicsView()
        self.graphic_scene = QGraphicsScene()
        self.graphic_view.setScene(self.graphic_scene)
        view_layout.addWidget(self.graphic_view)
        splitter.addWidget(view_frame)
        layout.addWidget(splitter)

    def export_dxf(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Export DXF', '', 'DXF Files (*.dxf)')
        if path:
            # TODO: implement export logic
            QMessageBox.information(self, 'Export', f'Exported to {path}')

    def summary_report(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save Summary Report', '', 'PDF Files (*.pdf);;CSV Files (*.csv)')
        if path:
            # TODO: implement summary report generation
            QMessageBox.information(self, 'Report', f'Summary report saved to {path}')

    def detailed_report(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save Detailed Report', '', 'PDF Files (*.pdf);;CSV Files (*.csv)')
        if path:
            # TODO: implement detailed report generation
            QMessageBox.information(self, 'Report', f'Detailed report saved to {path}')
