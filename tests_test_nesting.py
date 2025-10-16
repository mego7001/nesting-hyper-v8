# tests/test_nesting.py

import pytest
from core.genetic_algorithm import GeneticAlgorithm


def test_ga_basic():
    parts = [{'dummy': True}]
    sheets = [{'width': 100, 'height': 100}]
    ga = GeneticAlgorithm(10, 5, [0, 90])
    best = ga.run(parts, sheets)
    assert isinstance(best, list)
    assert all('part' in gene for gene in best)
