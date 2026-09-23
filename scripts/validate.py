"""Validate local links, fragment targets and document structure in generated pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
import re

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    """Collect identifiers and local resource references from one HTML page."""

    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.h1_count += 1
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


pages = {}
errors = []
for path in [ROOT / 'index.html', *sorted((ROOT / 'notes').glob('*.html'))]:
    parser = PageParser()
    parser.feed(path.read_text(encoding='utf-8'))
    pages[path.resolve()] = parser
    if len(parser.ids) != len(set(parser.ids)):
        errors.append(f'Duplicate ID: {path.name}')
    if parser.h1_count != 1:
        errors.append(f'Expected one h1: {path.name}')
    html = path.read_text(encoding='utf-8')
    if 'class="term-guide"' in html:
        errors.append(f'Legacy top term guide remains: {path.name}')
    if path.name != 'index.html' and 'class="term-inline"' not in html:
        errors.append(f'Missing inline first-use term explanation: {path.name}')
    if 'equation-fallback' in html:
        errors.append(f'Unmapped plain-text equation: {path.name}')

for path, parser in pages.items():
    for link in parser.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if not target.exists():
            errors.append(f'Missing resource: {path.name} -> {link}')
        if parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
            errors.append(f'Missing anchor: {path.name} -> {link}')

extra_diagrams = sorted((ROOT / 'assets' / 'diagrams' / 'extra').glob('*.svg'))
paper_diagrams = sorted((ROOT / 'assets' / 'diagrams' / 'paper').glob('*.svg'))
reference_diagrams = sorted((ROOT / 'assets' / 'diagrams' / 'reference').glob('*.svg'))
if len(reference_diagrams) != 41:
    errors.append(f'Expected 41 CS231n/PRML reference figures, found {len(reference_diagrams)}')
if len(paper_diagrams) != 18:
    errors.append(f'Expected 18 paper-style diagrams, found {len(paper_diagrams)}')
if len(extra_diagrams) < 60:
    errors.append(f'Expected at least 60 generated extra diagrams, found {len(extra_diagrams)}')

reference_source = (ROOT / 'scripts' / 'reference_figures.py').read_text(
    encoding='utf-8'
)
if 'kind="text"' in reference_source:
    errors.append(
        'Reference figures must use visual panel kinds instead of paragraph-style '
        'text cards.'
    )

for svg_path in reference_diagrams:
    svg_text = svg_path.read_text(encoding='utf-8')
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        errors.append(f'Invalid reference SVG XML: {svg_path.name}: {exc}')
        continue

    view_box = root.attrib.get('viewBox', '').split()
    if len(view_box) != 4:
        errors.append(f'Missing/invalid viewBox: {svg_path.name}')
        continue

    _, _, width, height = map(float, view_box)
    for node in root.iter():
        if not node.tag.endswith('text'):
            continue
        raw_x = node.attrib.get('x')
        raw_y = node.attrib.get('y')
        if raw_x is None or raw_y is None:
            continue
        try:
            text_x = float(raw_x)
            text_y = float(raw_y)
        except ValueError:
            continue
        if not (0 <= text_x <= width and 0 <= text_y <= height):
            errors.append(
                f'Text anchor outside viewBox: {svg_path.name} '
                f'({text_x}, {text_y})'
            )
        text_value = ''.join(node.itertext()).strip()
        text_class = node.attrib.get('class', '')
        if text_class not in {'title', 'subtitle'} and len(text_value) > 64:
            errors.append(
                f'Overlong in-figure label ({len(text_value)} chars): '
                f'{svg_path.name} -> {text_value[:40]}...'
            )

for svg_path in [
    *sorted((ROOT / 'assets' / 'diagrams').glob('*.svg')),
    *extra_diagrams,
    *paper_diagrams,
    *reference_diagrams,
]:
    svg_text = svg_path.read_text(encoding='utf-8')
    if re.search(r'text\s*\{[^}]*fill\s*:', svg_text):
        errors.append(
            f'Generic SVG text fill can override white labels: {svg_path.name}'
        )

if errors:
    raise SystemExit('\n'.join(errors))
print(f'Validated {len(pages)} pages: local links, IDs, anchors, and headings.')
