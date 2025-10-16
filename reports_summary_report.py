# reports/summary_report.py

import csv
from datetime import datetime

class SummaryReport:
    """
    Generates summary reports for nesting results in CSV or plain-text format.
    """
    def __init__(self, results, sheets, output_path):
        self.results = results
        self.sheets = sheets
        self.output_path = output_path

    def generate_csv(self):
        with open(self.output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Report','Generated', datetime.now().isoformat()])
            writer.writerow(['Total Solutions', len(self.results)])
            writer.writerow(['Sheets Used', len(self.sheets)])
            writer.writerow([])
            writer.writerow(['Solution', 'Efficiency'])
            for i, sol in enumerate(self.results, start=1):
                writer.writerow([f'Solution {i}', f"{sol['efficiency']:.2f}"])

    def generate_text(self):
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(f"Summary Report\nGenerated: {datetime.now().isoformat()}\n")
            f.write(f"Total Solutions: {len(self.results)}\n")
            f.write(f"Sheets Used: {len(self.sheets)}\n\n")
            for i, sol in enumerate(self.results, start=1):
                f.write(f"Solution {i}: Efficiency = {sol['efficiency']:.2f}\n")
