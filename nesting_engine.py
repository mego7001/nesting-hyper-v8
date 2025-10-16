# core/nesting_engine.py

from core.genetic_algorithm import GeneticAlgorithm

class NestingEngine:
    """
    High-level interface for nesting parts onto sheets.
    """
    def __init__(self, settings):
        ga_cfg = settings['genetic_algorithm']
        self.ga = GeneticAlgorithm(
            ga_cfg['population_size'],
            ga_cfg['generations'],
            ga_cfg['rotation_angles']
        )

    def nest(self, parts, sheets):
        # parts: list of geometries
        # sheets: list of dicts {width, height, name}
        result = self.ga.run(parts, sheets)
        return result
