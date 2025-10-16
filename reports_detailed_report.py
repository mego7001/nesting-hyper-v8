# reports/detailed_report.py

import csv
from datetime import datetime

class DetailedReport:
    """
    Generates detailed nesting reports with per-sheet and per-part info.
    """
    def __init__(self, results, sheets, parts, output_path):
        self.results = results
        self.sheets = sheets
        self.parts = parts
        self.output_path = output_path

    def generate_csv(self):
        with open(self.output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Detailed Report', datetime.now().isoformat()])
            for i, sol in enumerate(self.results, start=1):
                writer.writerow([])
                writer.writerow([f'Solution {i}', f"Efficiency: {sol['efficiency']:.2f}"])
                for sheet in self.sheets:
                    writer.writerow([f"Sheet: {sheet['name']}", f"Used: {sheet.get('used', 0):.2f}%"])  # placeholder
                writer.writerow([])
                writer.writerow(['Part', 'Quantity', 'Position', 'Rotation'])
                for gene in sol:
                    part = gene['part']
                    writer.writerow([
                        part.get('name', 'N/A'),
                        gene.get('quantity', 1),
                        f"{gene['pos']}",
                        gene['angle']
                    ])

    def generate_text(self):
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(f"Detailed Report\nGenerated: {datetime.now().isoformat()}\n")
            for i, sol in enumerate(self.results, start=1):
                f.write(f"\nSolution {i}: Efficiency = {sol['efficiency']:.2f}\n")
                for sheet in self.sheets:
                    f.write(f"Sheet {sheet['name']}: Used {sheet.get('used', 0):.2f}%\n")
                f.write("\nParts:\n")
                for gene in sol:
                    part = gene['part']
                    f.write(f" - {part.get('name','N/A')} x{gene.get('quantity',1)} @ {gene['pos']} rotated {gene['angle']}°\n")
