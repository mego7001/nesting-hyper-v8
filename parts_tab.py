# ui/parts_tab.py

import os
import ezdxf
import math
from shapely.geometry import MultiPoint
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView,
    QGraphicsScene, QTableWidget, QTableWidgetItem, QTextEdit,
    QFrame, QFileDialog, QSplitter, QLabel
)
from PyQt6.QtCore import Qt

class PartsTab(QWidget):
    def __init__(self, settings, mainwindow):
        super().__init__()
        self.settings = settings
        self.mainwindow = mainwindow
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()
        import_btn = QPushButton('Import CAD')
        import_btn.clicked.connect(self.opencadimporter)
        toolbar.addWidget(import_btn)
        layout.addLayout(toolbar)

        # Split view
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Upper: raw and imported preview
        preview_frame = QFrame()
        preview_layout = QHBoxLayout(preview_frame)
        self.raw_view = QGraphicsView()
        self.raw_scene = QGraphicsScene()
        self.raw_view.setScene(self.raw_scene)
        self.imported_view = QGraphicsView()
        self.imported_scene = QGraphicsScene()
        self.imported_view.setScene(self.imported_scene)
        preview_layout.addWidget(self.raw_view)
        preview_layout.addWidget(self.imported_view)
        splitter.addWidget(preview_frame)

        # Lower: parts table and log
        lower_frame = QFrame()
        lower_layout = QHBoxLayout(lower_frame)
        self.parts_table = QTableWidget(0, 4)
        self.parts_table.setHorizontalHeaderLabels(['Name', 'Width', 'Height', 'Qty'])
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        lower_layout.addWidget(self.parts_table)
        lower_layout.addWidget(self.log_text)
        splitter.addWidget(lower_frame)

        layout.addWidget(splitter)

    def opencadimporter(self):
        filepaths, _ = QFileDialog.getOpenFileNames(
            self, 'Import DXF/DWG Files', '', 'CAD Files (*.dxf *.dwg)'
        )
        if not filepaths:
            return

        # clear previous
        self.raw_scene.clear()
        self.imported_scene.clear()
        self.parts_table.setRowCount(0)
        self.log_text.clear()

        for filepath in filepaths:
            try:
                doc = ezdxf.readfile(filepath)
                msp = doc.modelspace()

                # draw raw lines
                for e in msp.query('LINE'):
                    x1, y1 = e.dxf.start
                    x2, y2 = e.dxf.end
                    self.raw_scene.addLine(x1, -y1, x2, -y2)

                coords = []
                for entity in msp:
                    et = entity.dxftype()
                    if et == 'LINE':
                        s = entity.dxf.start
                        e = entity.dxf.end
                        coords.extend([(s.x, s.y), (e.x, e.y)])
                    elif et == 'LWPOLYLINE':
                        coords.extend([(p[0], p[1]) for p in entity])
                    elif et == 'CIRCLE':
                        c = entity.dxf.center
                        r = entity.dxf.radius
                        for i in range(32):
                            a = 2*math.pi*i/32
                            coords.append((c.x+ r*math.cos(a), c.y+ r*math.sin(a)))

                if len(coords) < 3:
                    self.log_text.append(f'Warning: {os.path.basename(filepath)} insufficient geometry')
                    continue

                hull = MultiPoint(coords).convex_hull
                # draw imported hull
                pts = hull.exterior.coords
                prev = pts[0]
                for pt in pts[1:]:
                    self.imported_scene.addLine(prev[0], -prev[1], pt[0], -pt[1])
                    prev = pt

                name = os.path.splitext(os.path.basename(filepath))[0]
                minx, miny, maxx, maxy = hull.bounds
                width = round(maxx-minx,3)
                height = round(maxy-miny,3)
                qty = 1

                row = self.parts_table.rowCount()
                self.parts_table.insertRow(row)
                self.parts_table.setItem(row,0,QTableWidgetItem(name))
                self.parts_table.setItem(row,1,QTableWidgetItem(str(width)))
                self.parts_table.setItem(row,2,QTableWidgetItem(str(height)))
                self.parts_table.setItem(row,3,QTableWidgetItem(str(qty)))

                self.log_text.append(f'Success: Imported {name}')
            except Exception as e:
                self.log_text.append(f'Error importing {os.path.basename(filepath)}: {e}')
