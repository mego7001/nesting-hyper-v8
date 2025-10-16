# tests/test_export.py

import pytest
from reports.summary_report import SummaryReport
from reports.detailed_report import DetailedReport

def test_summary_csv(tmp_path):
    results = [{'efficiency': 0.75}, {'efficiency': 0.85}]
    sheets = [{'name':'S1'}, {'name':'S2'}]
    path = tmp_path / 'sum.csv'
    report = SummaryReport(results, sheets, str(path))
    report.generate_csv()
    assert path.exists()
    content = path.read_text()
    assert 'Total Solutions' in content


def test_detailed_csv(tmp_path):
    results = [[{'part': {'name':'P1'}, 'efficiency':0.9}]]
    sheets = [{'name':'S1'}]
    parts = [{'name':'P1'}]
    path = tmp_path / 'det.csv'
    report = DetailedReport(results, sheets, parts, str(path))
    report.generate_csv()
    assert path.exists()
    content = path.read_text()
    assert 'Detailed Report' in content
