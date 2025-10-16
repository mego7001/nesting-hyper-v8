# tests/test_sheets.py

import pytest
from ui.sheets_tab import AddSheetDialog, SheetsTab
from PyQt6.QtWidgets import QApplication
import sys

@pytest.fixture(scope='session')
def app():
    return QApplication(sys.argv)


def test_add_sheet(app, qtbot):
    tab = SheetsTab({'spacing': {}, 'genetic_algorithm': {}})
    qtbot.addWidget(tab)
    # simulate add
    dialog = AddSheetDialog()
    dialog.name_input.setText('Sheet1')
    dialog.width_input.setText('100')
    dialog.height_input.setText('200')
    dialog.qty_input.setValue(2)
    qtbot.keyClick(dialog, 'Return')  # accept
    tab.add_sheet()
    assert tab.table.rowCount() == 1
    assert tab.sheets[0]['name'] == 'Sheet1'
