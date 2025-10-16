# ui/components.py

import os
import json

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox, QMenu, QMenuBar
from PyQt6.QtGui import QAction

from PyQt6.QtGui import QIcon
from ui.parts_tab import PartsTab
from ui.sheets_tab import SheetsTab
from ui.nesting_tab import NestingTab
from ui.export_tab import ExportTab


class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle('HyperNesting')
        self.resize(1200, 800)
        self._create_menu()
        self._create_tabs()

    def _create_menu(self):
        menubar = self.menuBar()
        # File menu
        file_menu = menubar.addMenu('File')
        new_action = QAction('New', self)
        open_action = QAction('Open', self)
        save_action = QAction('Save', self)
        save_as_action = QAction('Save As', self)
        recent_menu = QMenu('Recent Files', self)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addMenu(recent_menu)

        # Preferences
        pref_action = QAction('Preferences', self)
        file_menu.addAction(pref_action)

        # About
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        help_menu.addAction(about_action)

    def _create_tabs(self):
        tabs_widget = QTabWidget()
        tabs_widget.addTab(PartsTab(self.settings, self), 'Parts')
        tabs_widget.addTab(SheetsTab(self.settings), 'Sheets')
        tabs_widget.addTab(NestingTab(self.settings), 'Nesting')
        tabs_widget.addTab(ExportTab(self.settings), 'Export')
        self.setCentralWidget(tabs_widget)
