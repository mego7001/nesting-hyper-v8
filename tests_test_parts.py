# tests/test_parts.py

import pytest
from core.cad_importer import CADImporter


def test_import_line(tmp_path):
    # create a minimal DXF file with one LINE entity
    dxf_path = tmp_path / "test.dxf"
    from ezdxf import new
    doc = new()
    msp = doc.modelspace()
    msp.add_line((0, 0), (10, 0))
    doc.saveas(str(dxf_path))

    importer = CADImporter(str(dxf_path))
    geoms = importer.import_file()
    assert len(geoms) == 1
    from shapely.geometry import LineString
    assert isinstance(geoms[0], LineString)
