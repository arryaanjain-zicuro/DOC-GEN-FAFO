from docxtpl import DocxTemplate
import pandas as pd
import os

def generate_document(term_sheet_file, template_name):
    df = pd.read_excel(term_sheet_file)
    data = df.iloc[0].to_dict()  # Use the first row for now

    template_path = f"app/templates/{template_name}"
    doc = DocxTemplate(template_path)
    doc.render(data)

    output_path = f"app/data/output/generated_doc.docx"
    doc.save(output_path)
    return output_path
