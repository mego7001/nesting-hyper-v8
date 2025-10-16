# ui/sheets_tab.py

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QDialogButtonBox, QFormLayout,
    QLineEdit, QSpinBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt


def resource_path(relative):
    return os.path.join(os.path.dirname(__file__), '..', 'resources', relative)


class AddSheetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Sheet')
        self.layout = QFormLayout(self)
        self.name_input = QLineEdit()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Width:', self.width_input)
        self.layout.addRow('Height:', self.height_input)
        self.layout.addRow('Quantity:', self.qty_input)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'width': float(self.width_input.text()),
            'height': float(self.height_input.text()),
            'quantity': self.qty_input.value()
        }


class SheetsTab(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.sheets = []
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        toolbar = QHBoxLayout()
        add_btn = QPushButton('Create Sheet')
        add_btn.clicked.connect(self.add_sheet)
        import_btn = QPushButton('DXF/DWG Create')
        import_btn.clicked.connect(self.import_sheet)
        remove_btn = QPushButton('Remove Selected Sheets')
        remove_btn.clicked.connect(self.remove_selected)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(import_btn)
        toolbar.addWidget(remove_btn)
        main_layout.addLayout(toolbar)

        # Table of sheets
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Name', 'Width', 'Height', 'Quantity'])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table)

    def add_sheet(self):
        dialog = AddSheetDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.sheets.append(data)
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(data['name']))
            self.table.setItem(row, 1, QTableWidgetItem(str(data['width'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(data['height'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(data['quantity'])))

    def import_sheet(self):
        QMessageBox.information(self, 'Import', 'DXF/DWG import not yet implemented.')

    def remove_selected(self):
        selected = self.table.selectionModel().selectedRows()
        for index in sorted(selected, reverse=True):
            self.table.removeRow(index.row())
            del self.sheets[index.row()]
