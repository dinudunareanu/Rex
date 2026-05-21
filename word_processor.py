from docxtpl import DocxTemplate
from docx import Document
from docx.opc.oxml import parse_xml
from jinja2 import Environment, nodes
from jinja2.meta import find_undeclared_variables


def get_template_variables(docx_path):
    """Extract template variables in document order (first-occurrence order)."""
    doc_template = DocxTemplate(docx_path)
    temp_doc = Document(docx_path)

    xml = doc_template.xml_to_string(temp_doc._element.body)
    xml = doc_template.patch_xml(xml)

    for uri in [doc_template.HEADER_URI, doc_template.FOOTER_URI]:
        for relKey, val in temp_doc._part.rels.items():
            if (val.reltype == uri) and (val.target_part.blob):
                _xml = doc_template.xml_to_string(parse_xml(val.target_part.blob))
                xml += doc_template.patch_xml(_xml)

    env = Environment()
    ast = env.parse(xml)

    undeclared_set = find_undeclared_variables(ast)
    ordered = []
    seen = set()
    for n in ast.find_all(nodes.Name):
        if n.name in undeclared_set and n.name not in seen:
            ordered.append(n.name)
            seen.add(n.name)

    return doc_template, ordered

def render_docx(doc_template, context):
    doc_template.render(context)
    return doc_template
