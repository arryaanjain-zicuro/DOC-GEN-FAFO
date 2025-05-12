from openpyxl import load_workbook
from datetime import datetime, timedelta

def fill_ncd_mis_excel(term_data, template_path, output_path):
    wb = load_workbook(template_path)
    ws = wb.active

    # Example: Write Initial/Final Fixing Dates
    init_date = datetime.strptime(term_data["Initial Fixing Date"], "%B %d, %Y")
    final_date = datetime.strptime(term_data["Final Fixing Date"], "%B %d, %Y")

    ws["U2"] = init_date
    ws["W2"] = final_date
    ws["V2"] = init_date - timedelta(days=15)
    ws["X2"] = final_date - timedelta(days=15)

    # Add other mappings as needed...

    wb.save(output_path)
