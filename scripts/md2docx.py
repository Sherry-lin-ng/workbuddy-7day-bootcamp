# -*- coding: utf-8 -*-
"""极简 Markdown -> DOCX 生成器（仅用 Python 标准库，零依赖）。

支持：# ~ ### 标题、- 列表、1. 列表、> 引用、简单表格、**粗体**、普通段落。
用法：python scripts/md2docx.py <input.md> <output.docx> [标题]
"""
import datetime
import re
import sys
import zipfile
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
FONT_RUN = (
    '<w:rPr><w:rFonts w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei" '
    'w:eastAsia="Microsoft YaHei"/>%s</w:rPr>'
)
HEAD_STYLE = {1: 'Heading1', 2: 'Heading2', 3: 'Heading3'}


def rich_text(text):
    """把 **粗体** 切成若干 run。"""
    out = ''
    for part in re.split(r'(\*\*.+?\*\*)', text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            out += (
                '<w:r>' + (FONT_RUN % '<w:b/>') +
                '<w:t xml:space="preserve">%s</w:t></w:r>' % escape(part[2:-2])
            )
        else:
            out += '<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % escape(part)
    return out


def para(text='', style=None, indent=0):
    pr = '<w:pPr>'
    if style:
        pr += '<w:pStyle w:val="%s"/>' % style
    if indent:
        pr += '<w:ind w:left="%d"/>' % indent
    pr += '</w:pPr>'
    return '<w:p>%s%s</w:p>' % (pr, rich_text(text))


def table(rows):
    borders = ('<w:tcBorders>' + ''.join(
        '<w:%s w:val="single" w:sz="4" w:color="BFBFBF"/>' % s
        for s in ('top', 'left', 'bottom', 'right')) + '</w:tcBorders>')
    trs = ''.join(
        '<w:tr>%s</w:tr>' % ''.join(
            '<w:tc><w:tcPr>%s%s</w:tcPr>%s</w:tc>' % (
                '<w:shd w:fill="F2F2F2"/>' if ri == 0 else '',
                borders, para(c or ' '))
            for c in row)
        for ri, row in enumerate(rows))
    tbl_borders = ''.join(
        '<w:%s w:val="single" w:sz="4" w:color="BFBFBF"/>' % s
        for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    return (
        '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>'
        '<w:tblBorders>%s</w:tblBorders></w:tblPr>%s</w:tbl>'
        % (tbl_borders, trs)
    )


def convert(md_text):
    body = ''
    in_code = False
    rows = []
    for raw in md_text.splitlines() + ['']:
        line = raw.strip()

        # 表格行进行缓冲，连续的行合并成同一个表格
        if not in_code and line.startswith('|') and line.endswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(re.fullmatch(r':?-+=?:?', c) for c in cells):
                continue  # 分隔行
            rows.append(cells)
            continue
        if rows:
            body += table(rows) + para('')
            rows = []

        if line.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            body += para(line, indent=360)
            continue
        if not line:
            continue

        m = re.match(r'^(#{1,3})\s+(.*)$', line)
        if m:
            body += para(m.group(2).strip(), HEAD_STYLE[len(m.group(1))])
            continue

        if line.startswith('>'):
            body += para(line.lstrip('> ').strip(), indent=360)
            continue

        m = re.match(r'^[-*]\s+(.*)$', line)
        if m:
            body += para(m.group(1).strip(), indent=420)
            continue

        m = re.match(r'^(\d+)\.\s+(.*)$', line)
        if m:
            body += para('%s. %s' % (m.group(1), m.group(2).strip()), indent=420)
            continue

        body += para(line)
    return body


STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles %s>
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei" w:eastAsia="Microsoft YaHei" w:cs="Microsoft YaHei"/>
<w:sz w:val="21"/><w:szCs w:val="21"/>
</w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
<w:pPr><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:color w:val="1F3864"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
<w:pPr><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="2E5496"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
<w:pPr><w:outlineLvl w:val="2"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>
</w:styles>""" % W

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>WorkBuddy 7-Day Bootcamp</Application>
</Properties>"""


def build(md_path, docx_path, title):
    with open(md_path, 'r', encoding='utf-8') as f:
        body = convert(f.read())

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>%s</dc:title><dc:creator>WorkBuddy</dc:creator>'
        '<cp:lastModifiedBy>WorkBuddy</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>'
        '</cp:coreProperties>' % (escape(title), now, now)
    )

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document %s><w:body>%s<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>' % (W, body)
    )

    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('docProps/core.xml', core)
        z.writestr('docProps/app.xml', APP)
        z.writestr('word/document.xml', document)
        z.writestr('word/_rels/document.xml.rels', DOC_RELS)
        z.writestr('word/styles.xml', STYLES)


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    build(src, dst, sys.argv[3] if len(sys.argv) > 3 else 'Document')
    print('generated:', dst)
