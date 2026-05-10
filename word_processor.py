from docxtpl import DocxTemplate

def get_template_variables(docx_path):
    doc = DocxTemplate(docx_path)
    placeholders = doc.get_undeclared_template_variables(context={})
    return doc, placeholders 

# def fill_placeholders(placeholders):
#     context = {}

#     for p in placeholders:
#         value = input(f"Enter value for {p}: ")
#         context[p] = value

#     return context

def render_docx(doc_template, context):
    doc_template.render(context)
    return doc_template

# doc, placeholders = get_template_variables("template.docx")
# context = fill_placeholders(placeholders)
# render_docx(doc_template=doc, context=context)
