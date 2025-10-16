# core/cad_importer.py

import ezdxf
from shapely.geometry import LineString, Polygon, MultiPolygon

class CADImporter:
    """
    Handles importing of DXF/DWG files and converts entities to Shapely geometries.
    """
    def __init__(self, path):
        self.path = path
        self.geometries = []

    def import_file(self):
        doc = ezdxf.readfile(self.path)
        msp = doc.modelspace()
        for entity in msp:
            geom = self._convert_entity(entity)
            if geom is not None:
                self.geometries.append(geom)
        return self.geometries

    def _convert_entity(self, entity):
        etype = entity.dxftype()
        if etype == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            return LineString([start, end])
        if etype == 'LWPOLYLINE':
            points = [(p[0], p[1]) for p in entity]
            return Polygon(points)
        if etype == 'CIRCLE':
            center = entity.dxf.center
            radius = entity.dxf.radius
            poly = entity.circle_approximation(64)
            return Polygon(poly)
        # ignore other types
        return None
