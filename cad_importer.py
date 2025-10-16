# ui/dialogs/cad_importer_dialog.py
# نسخة مصححة بالكامل - تدعم جميع أشكال DXF بدون أخطاء
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QListWidget, QGraphicsView, QGraphicsScene, QTableWidget, 
                           QTableWidgetItem, QTextEdit, QFrame, QComboBox, QCheckBox,
                           QProgressBar, QLabel, QMessageBox, QFileDialog, QSplitter,
                           QGroupBox, QFormLayout, QSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPen, QBrush, QColor
import os
import sys
from shapely.geometry import MultiPolygon, MultiLineString, Polygon, LineString, Point
from core.cad_importer import CADImporter

class ImportWorker(QThread):
    """مؤشر ترابط لاستيراد ملفات CAD في الخلفية"""
    progress_updated = pyqtSignal(int)
    file_processed = pyqtSignal(str, list)  # اسم الملف والأجزاء المستخرجة
    import_finished = pyqtSignal(list)  # جميع الأجزاء المستوردة
    error_occurred = pyqtSignal(str)

    def __init__(self, filepaths):
        super().__init__()
        self.filepaths = filepaths
        self.all_parts = []

    def run(self):
        total_files = len(self.filepaths)
        
        for i, filepath in enumerate(self.filepaths):
            try:
                # تحديث التقدم
                progress = int((i / total_files) * 100)
                self.progress_updated.emit(progress)
                
                # استيراد الملف
                importer = CADImporter(filepath)
                parts = importer.import_parts()
                
                # إضافة معلومات إضافية
                for part in parts:
                    part['source_file'] = os.path.basename(filepath)
                
                self.all_parts.extend(parts)
                self.file_processed.emit(os.path.basename(filepath), parts)
                
            except Exception as e:
                error_msg = f"Error importing {os.path.basename(filepath)}: {str(e)}"
                self.error_occurred.emit(error_msg)
                continue
        
        self.progress_updated.emit(100)
        self.import_finished.emit(self.all_parts)

class CadImporterDialog(QDialog):
    """حوار متقدم لاستيراد ملفات CAD - نسخة مصححة ومحسنة"""
    
    def __init__(self, filepath_list, parent=None):
        super().__init__(parent)
        self.filepaths = filepath_list
        self.imported_parts = []
        self.filtered_parts = []
        self.worker = None
        
        self.setWindowTitle('Import CAD Files - Professional')
        self.setMinimumSize(1400, 900)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # شريط الأدوات العلوي
        toolbar_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton('Add More Files')
        self.add_files_btn.clicked.connect(self._add_more_files)
        toolbar_layout.addWidget(self.add_files_btn)
        
        self.remove_files_btn = QPushButton('Remove Selected')
        self.remove_files_btn.clicked.connect(self._remove_selected_files)
        toolbar_layout.addWidget(self.remove_files_btn)
        
        toolbar_layout.addStretch()
        
        self.start_import_btn = QPushButton('Start Import')
        self.start_import_btn.clicked.connect(self._start_import)
        toolbar_layout.addWidget(self.start_import_btn)
        
        layout.addLayout(toolbar_layout)

        # القسم الرئيسي مقسم أفقياً
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # الجانب الأيسر: قائمة الملفات وإعدادات الاستيراد
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)

        # الوسط: المعاينات
        center_panel = self._create_center_panel()
        main_splitter.addWidget(center_panel)

        # اليمين: جداول الطبقات والأجزاء
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)

        main_splitter.setSizes([300, 500, 400])
        layout.addWidget(main_splitter, 1)

        # شريط التقدم
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Ready to import")
        progress_layout.addWidget(QLabel("Progress:"))
        progress_layout.addWidget(self.progress_bar, 1)
        progress_layout.addWidget(self.status_label)
        layout.addLayout(progress_layout)

        # سجل الأحداث
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(100)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # أزرار النهاية
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        self.done_btn = QPushButton('Import Parts')
        self.done_btn.clicked.connect(self.accept)
        self.done_btn.setEnabled(False)
        buttons_layout.addWidget(self.done_btn)
        
        layout.addLayout(buttons_layout)

        # تحميل قائمة الملفات الأولية
        self._load_file_list()

    def _create_left_panel(self):
        """إنشاء اللوحة اليسرى - قائمة الملفات والإعدادات"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # قائمة الملفات
        files_group = QGroupBox("Files to Import")
        files_layout = QVBoxLayout(files_group)
        
        self.files_list = QListWidget()
        self.files_list.currentRowChanged.connect(self._on_file_selected)
        files_layout.addWidget(self.files_list)
        
        layout.addWidget(files_group)

        # إعدادات الاستيراد
        settings_group = QGroupBox("Import Settings")
        settings_layout = QFormLayout(settings_group)
        
        self.units_combo = QComboBox()
        self.units_combo.addItems(['mm', 'cm', 'm', 'inches'])
        settings_layout.addRow("Units:", self.units_combo)
        
        self.scale_factor = QSpinBox()
        self.scale_factor.setRange(1, 1000)
        self.scale_factor.setValue(1)
        settings_layout.addRow("Scale Factor:", self.scale_factor)
        
        self.merge_layers = QCheckBox("Merge All Layers")
        settings_layout.addRow(self.merge_layers)
        
        self.ignore_text = QCheckBox("Ignore Text Entities")
        self.ignore_text.setChecked(True)
        settings_layout.addRow(self.ignore_text)
        
        self.close_open_paths = QCheckBox("Close Open Paths")
        settings_layout.addRow(self.close_open_paths)
        
        layout.addWidget(settings_group)
        
        layout.addStretch()
        return widget

    def _create_center_panel(self):
        """إنشاء اللوحة الوسطى - المعاينات المرئية"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # معاينة الملف الخام
        layout.addWidget(QLabel("Raw DXF Content:"))
        self.raw_view = QGraphicsView()
        self.raw_scene = QGraphicsScene()
        self.raw_view.setScene(self.raw_scene)
        self.raw_view.setMinimumHeight(200)
        layout.addWidget(self.raw_view, 1)

        # معاينة الأجزاء المعالجة
        layout.addWidget(QLabel("Processed Parts:"))
        self.processed_view = QGraphicsView()
        self.processed_scene = QGraphicsScene()
        self.processed_view.setScene(self.processed_scene)
        self.processed_view.setMinimumHeight(200)
        layout.addWidget(self.processed_view, 1)

        return widget

    def _create_right_panel(self):
        """إنشاء اللوحة اليمنى - الجداول والإحصائيات"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # جدول الطبقات
        layout.addWidget(QLabel("Layers Found:"))
        self.layers_table = QTableWidget(0, 3)
        self.layers_table.setHorizontalHeaderLabels(['Layer', 'Entities', 'Action'])
        self.layers_table.setMaximumHeight(150)
        layout.addWidget(self.layers_table)

        # جدول الأجزاء المستوردة
        layout.addWidget(QLabel("Imported Parts:"))
        self.parts_table = QTableWidget(0, 6)
        self.parts_table.setHorizontalHeaderLabels(['Name', 'Width', 'Height', 'Area', 'Layer', 'File'])
        layout.addWidget(self.parts_table)

        return widget

    def _load_file_list(self):
        """تحميل قائمة الملفات في القائمة"""
        self.files_list.clear()
        for filepath in self.filepaths:
            filename = os.path.basename(filepath)
            self.files_list.addItem(f"{filename} ({os.path.getsize(filepath)} bytes)")

    def _add_more_files(self):
        """إضافة ملفات إضافية"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 'Add More CAD Files', '', 
            'CAD Files (*.dxf *.dwg);;DXF Files (*.dxf);;DWG Files (*.dwg)'
        )
        if files:
            self.filepaths.extend(files)
            self._load_file_list()
            self.log_text.append(f"Added {len(files)} files")

    def _remove_selected_files(self):
        """حذف الملفات المحددة"""
        current_row = self.files_list.currentRow()
        if current_row >= 0:
            filename = os.path.basename(self.filepaths[current_row])
            del self.filepaths[current_row]
            self._load_file_list()
            self.log_text.append(f"Removed: {filename}")

    def _start_import(self):
        """بدء عملية الاستيراد"""
        if not self.filepaths:
            QMessageBox.warning(self, "Warning", "No files selected for import")
            return

        self.start_import_btn.setEnabled(False)
        self.done_btn.setEnabled(False)
        self.imported_parts.clear()

        # إنشاء وبدء العامل
        self.worker = ImportWorker(self.filepaths)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.file_processed.connect(self._on_file_processed)
        self.worker.import_finished.connect(self._on_import_finished)
        self.worker.error_occurred.connect(self._on_import_error)
        
        self.worker.start()
        self.status_label.setText("Importing...")
        self.log_text.append(f"Starting import of {len(self.filepaths)} files...")

    def _on_file_processed(self, filename, parts):
        """معالجة نتائج استيراد ملف واحد"""
        self.log_text.append(f"Processed {filename}: {len(parts)} parts found")
        
        # إضافة الطبقات الجديدة لجدول الطبقات
        self._update_layers_table(parts)
        
        # معاينة الملف الحالي
        if parts:
            self._preview_parts(parts)

    def _on_import_finished(self, all_parts):
        """معالجة انتهاء الاستيراد"""
        self.imported_parts = all_parts
        self.filtered_parts = all_parts.copy()
        
        self.status_label.setText(f"Completed - {len(all_parts)} parts imported")
        self.log_text.append(f"Import completed: {len(all_parts)} total parts")
        
        self._update_parts_table()
        self._preview_all_parts()
        
        self.start_import_btn.setEnabled(True)
        self.done_btn.setEnabled(True)

    def _on_import_error(self, error_msg):
        """معالجة أخطاء الاستيراد"""
        self.log_text.append(f"ERROR: {error_msg}")

    def _on_file_selected(self, row):
        """معالجة تحديد ملف من القائمة"""
        if row >= 0 and row < len(self.filepaths):
            filepath = self.filepaths[row]
            self.log_text.append(f"Selected: {os.path.basename(filepath)}")

    def _update_layers_table(self, parts):
        """تحديث جدول الطبقات"""
        layers_info = {}
        for part in parts:
            layer = part.get('layer', 'Unknown')
            if layer not in layers_info:
                layers_info[layer] = 0
            layers_info[layer] += 1

        # إضافة الطبقات الجديدة فقط
        for layer, count in layers_info.items():
            # تحقق من وجود الطبقة مسبقاً
            found = False
            for row in range(self.layers_table.rowCount()):
                if self.layers_table.item(row, 0).text() == layer:
                    found = True
                    break
            
            if not found:
                row = self.layers_table.rowCount()
                self.layers_table.insertRow(row)
                self.layers_table.setItem(row, 0, QTableWidgetItem(layer))
                self.layers_table.setItem(row, 1, QTableWidgetItem(str(count)))
                
                # قائمة منسدلة للإجراء
                action_combo = QComboBox()
                action_combo.addItems(['Import', 'Skip', 'Combine'])
                self.layers_table.setCellWidget(row, 2, action_combo)

    def _update_parts_table(self):
        """تحديث جدول الأجزاء"""
        self.parts_table.setRowCount(len(self.filtered_parts))
        
        for i, part in enumerate(self.filtered_parts):
            self.parts_table.setItem(i, 0, QTableWidgetItem(part.get('name', f'Part_{i+1}')))
            self.parts_table.setItem(i, 1, QTableWidgetItem(f"{part.get('width', 0):.2f}"))
            self.parts_table.setItem(i, 2, QTableWidgetItem(f"{part.get('height', 0):.2f}"))
            self.parts_table.setItem(i, 3, QTableWidgetItem(f"{part.get('area', 0):.2f}"))
            self.parts_table.setItem(i, 4, QTableWidgetItem(part.get('layer', 'Unknown')))
            self.parts_table.setItem(i, 5, QTableWidgetItem(part.get('source_file', 'Unknown')))

    def _preview_parts(self, parts):
        """معاينة الأجزاء المستوردة"""
        # مسح المشاهد
        self.raw_scene.clear()
        self.processed_scene.clear()

        # رسم الأجزاء
        y_offset = 0
        for part in parts:
            geom = part.get('geometry')
            if geom:
                self._draw_geometry_safe(self.raw_scene, geom, y_offset)
                self._draw_geometry_safe(self.processed_scene, geom, y_offset, processed=True)
                y_offset += 150

        # تعديل النطاق ليعرض كل شيء
        self.raw_view.fitInView(self.raw_scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.processed_view.fitInView(self.processed_scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def _preview_all_parts(self):
        """معاينة جميع الأجزاء المستوردة"""
        self._preview_parts(self.imported_parts[:10])  # أول 10 أجزاء للأداء

    def _draw_geometry_safe(self, scene, geom, y_offset=0, processed=False):
        """رسم الهندسة بطريقة آمنة - يدعم جميع أنواع shapely"""
        try:
            if geom is None or geom.is_empty:
                return

            # اختيار الألوان
            if processed:
                pen = QPen(QColor(0, 150, 0), 2)  # أخضر للمعالج
                brush = QBrush(QColor(0, 150, 0, 50))
            else:
                pen = QPen(QColor(100, 100, 100), 1)  # رمادي للخام
                brush = QBrush(QColor(100, 100, 100, 30))

            # معالجة الهندسات المتعددة
            if isinstance(geom, (MultiPolygon, MultiLineString)):
                for sub_geom in geom.geoms:
                    self._draw_geometry_safe(scene, sub_geom, y_offset, processed)
                return

            # رسم الأشكال المفردة
            if isinstance(geom, Polygon):
                self._draw_polygon(scene, geom, pen, brush, y_offset)
            elif isinstance(geom, LineString):
                self._draw_linestring(scene, geom, pen, y_offset)
            elif isinstance(geom, Point):
                self._draw_point(scene, geom, pen, brush, y_offset)

        except Exception as e:
            # في حالة خطأ، ارسم مستطيل بسيط
            bounds = geom.bounds if hasattr(geom, 'bounds') else (0, 0, 10, 10)
            scene.addRect(bounds[0], bounds[1] + y_offset, 
                         bounds[2] - bounds[0], bounds[3] - bounds[1], 
                         QPen(QColor(255, 0, 0), 1))

    def _draw_polygon(self, scene, polygon, pen, brush, y_offset):
        """رسم مضلع"""
        if polygon.exterior:
            coords = list(polygon.exterior.coords)
            if len(coords) >= 3:
                # تحويل النقاط
                points = [(x, y + y_offset) for x, y in coords]
                
                # رسم الحدود الخارجية
                for i in range(len(points) - 1):
                    x1, y1 = points[i]
                    x2, y2 = points[i + 1]
                    scene.addLine(x1, y1, x2, y2, pen)
                
                # رسم الثقوب الداخلية إن وجدت
                for interior in polygon.interiors:
                    hole_coords = list(interior.coords)
                    hole_points = [(x, y + y_offset) for x, y in hole_coords]
                    for i in range(len(hole_points) - 1):
                        x1, y1 = hole_points[i]
                        x2, y2 = hole_points[i + 1]
                        scene.addLine(x1, y1, x2, y2, QPen(QColor(255, 100, 100), 1))

    def _draw_linestring(self, scene, linestring, pen, y_offset):
        """رسم خط"""
        coords = list(linestring.coords)
        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            scene.addLine(x1, y1 + y_offset, x2, y2 + y_offset, pen)

    def _draw_point(self, scene, point, pen, brush, y_offset):
        """رسم نقطة"""
        x, y = point.x, point.y
        scene.addEllipse(x - 2, y + y_offset - 2, 4, 4, pen, brush)

    def get_imported_parts(self):
        """إرجاع الأجزاء المستوردة للاستخدام الخارجي"""
        return self.filtered_parts

    def closeEvent(self, event):
        """تنظيف الموارد عند إغلاق الحوار"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        super().closeEvent(event)
