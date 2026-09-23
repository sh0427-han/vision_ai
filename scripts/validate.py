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
    is_legacy_redirect = 'data-legacy-redirect="true"' in html
    if (
        path.name != 'index.html'
        and not is_legacy_redirect
        and 'class="term-inline"' not in html
    ):
        errors.append(f'Missing inline first-use term explanation: {path.name}')
    if 'equation-fallback' in html:
        errors.append(f'Unmapped plain-text equation: {path.name}')

index_html = (ROOT / 'index.html').read_text(encoding='utf-8')
if '논문 해설' in index_html:
    errors.append('Legacy paper-review top-level category remains in index.html')
for required_group in [
    '이미지·CNN',
    'Transformer·Attention',
    'Vision Tasks·Segmentation',
    '학습·평가',
    'Anomaly Detection',
    '종합 이론',
]:
    if f'>{required_group}<' not in index_html:
        errors.append(f'Missing topic-first category in index.html: {required_group}')
for forbidden_link in ['notes/resnet.html', 'notes/unet.html']:
    if forbidden_link in index_html:
        errors.append(f'Legacy standalone topic card remains: {forbidden_link}')

required_topic_anchors = {
    ROOT / 'notes' / 'cnn.html': [
        'architectures',
        'resnet_problem',
        'residual_block',
        'residual_shape',
        'resnet_bottleneck',
        'resnet_scope',
    ],
    ROOT / 'notes' / 'tasks.html': [
        'segmentation_context',
        'unet_architecture',
        'unet_original',
        'unet_scope',
    ],
}
for topic_path, anchors in required_topic_anchors.items():
    parser = pages.get(topic_path.resolve())
    if parser is None:
        errors.append(f'Missing topic page: {topic_path.name}')
        continue
    for anchor in anchors:
        if anchor not in parser.ids:
            errors.append(f'Missing merged topic anchor: {topic_path.name}#{anchor}')

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
if len(reference_diagrams) != 68:
    errors.append(f'Expected 68 CS231n/PRML reference figures, found {len(reference_diagrams)}')
if len(paper_diagrams) != 18:
    errors.append(f'Expected 18 paper-style diagrams, found {len(paper_diagrams)}')
if len(extra_diagrams) < 60:
    errors.append(f'Expected at least 60 generated extra diagrams, found {len(extra_diagrams)}')

reference_source = (ROOT / 'scripts' / 'reference_figures.py').read_text(
    encoding='utf-8'
)

paper_source = (ROOT / 'scripts' / 'paper_figures.py').read_text(encoding='utf-8')
extra_source = (ROOT / 'scripts' / 'extra_diagrams.py').read_text(encoding='utf-8')
build_source = (ROOT / 'scripts' / 'build.py').read_text(encoding='utf-8')

chapter1_photo_assets = [
    ROOT / 'assets' / 'diagrams' / 'illustrations' / 'ch01' / 'apple-real.webp',
    ROOT / 'assets' / 'diagrams' / 'illustrations' / 'ch01' / 'apple-r.webp',
    ROOT / 'assets' / 'diagrams' / 'illustrations' / 'ch01' / 'apple-g.webp',
    ROOT / 'assets' / 'diagrams' / 'illustrations' / 'ch01' / 'apple-b.webp',
]
for asset in chapter1_photo_assets:
    if not asset.exists():
        errors.append(f'Missing Chapter 01 realistic photo asset: {asset.relative_to(ROOT)}')

for obsolete in [
    'illustrations/ch01/image-to-pixels.svg',
    'illustrations/ch01/rgb-channel-decomposition.svg',
    'illustrations/ch01/resize-effects.svg',
    'illustrations/ch01/lighting-conditions.svg',
]:
    if obsolete in build_source:
        errors.append(f'Obsolete crude Chapter 01 SVG is still referenced: {obsolete}')


for source_name, source_text in [
    ('reference_figures.py', reference_source),
    ('paper_figures.py', paper_source),
    ('extra_diagrams.py', extra_source),
]:
    if "'NanumGothic'" not in source_text or "'Noto Sans CJK KR'" not in source_text:
        errors.append(
            f'Missing Korean SVG font fallback in {source_name}'
        )

if 'automatic two-line labels for narrow boxes' not in reference_source:
    errors.append('Missing wrapped pipeline labels in reference figures')

for forbidden in [
    '"pixels-channels.svg": ("flow"',
    '"cnn-multichannel.svg": ("flow"',
    '"vit-attention.svg": ("flow"',
    '"vit-multihead.svg": ("flow"',
    '"tasks-output-types.svg": ("flow"',
    '"tasks-label-box-mask.svg": ("flow"',
    '"unet-mask-triplet.svg": ("flow"',
    '"prml-variational.svg": ("flow"',
    '"prml-ensemble.svg": ("flow"',
    '"train-curves.svg": ("compare"',
    '"resnet-function.svg": ("flow"',
    '"resnet-gradient.svg": ("flow"',
]:
    if forbidden in extra_source:
        errors.append(
            f'Extra-diagram structural regression remains: {forbidden}'
        )

for required in [
    'def _pixels_channels(',
    'def _parallel_conv_channels(',
    'def _attention_qkv_visual(',
    'def _multihead_visual(',
    'def _mask_compare_visual(',
    'def _roc_pr_visual(',
    'def _residual_function_visual(',
    'def _ensemble_visual(',
]:
    if required not in extra_source:
        errors.append(f'Missing visual-QA corrected extra diagram: {required}')

for forbidden in [
    '"train-overfit.svg": ("curve"',
    '"train-threshold.svg": ("curve"',
    '"cs-optimization.svg": ("curve"',
]:
    if forbidden in extra_source:
        errors.append(
            f'Extra-diagram semantic regression remains: generic curve used for {forbidden}'
        )

for required in [
    'def _overfit_curve(',
    'def _threshold_curve(',
    'def _optimization_curve(',
    'validation loss rises',
    'False-positive rate',
]:
    if required not in extra_source:
        errors.append(f'Missing audited extra-diagram safeguard: {required}')

for forbidden_note in ["note('resnet'", "note('unet'"]:
    if forbidden_note in build_source:
        errors.append(
            f'Legacy standalone paper page remains in build source: {forbidden_note}'
        )

for forbidden_group in ["'논문 해설'", "'핵심 주제'"]:
    if forbidden_group in build_source:
        errors.append(
            f'Legacy source-type/top-level grouping remains: {forbidden_group}'
        )


for forbidden in [
    'v=3 if c==1 else 0',
    'Layer 1: local edge',
    'Head 1","nearby shape',
]:
    if forbidden in paper_source:
        errors.append(f'Paper figure semantic regression remains: {forbidden}')

for required in [
    'output = [[3,3,0],[3,3,0],[3,3,0]]',
    '실제 모델에서 측정한 attention이 아닙니다',
]:
    if required not in paper_source:
        errors.append(f'Missing audited paper-figure safeguard: {required}')

for forbidden in [
    'maximizing ELBO closes the KL gap',
    'MCMC reaches a target distribution',
]:
    if forbidden in reference_source:
        errors.append(f'Reference wording regression remains: {forbidden}')

for forbidden in [
    'values=[0.02,0.2,0.65,1.0]',
    'steps=["model A","model B","model C","average"]',
    'steps=["input","gating","experts","weighted output"]',
    'dict(title="decision regions",kind="scatter_curve")',
]:
    if forbidden in reference_source:
        errors.append(
            f'Reference figure semantic regression remains in source: {forbidden}'
        )

for required in [
    'cs-conv-channels-rf.svg',
    'cs-attention.svg',
    'cs-gradient-stability.svg',
    'cs-dropout-fit.svg',
    'cs-vgg-transfer.svg',
    'cs-interpretability.svg',
    'prml-discrete-map.svg',
    'prml-generative-discriminative.svg',
    'prml-kernel-gp.svg',
    'prml-graph-inference.svg',
    'prml-vi-meanfield.svg',
    'prml-sampling-diagnostics.svg',
    'prml-state-space.svg',
    'prml-ensemble-boosting.svg',
    'cs-regularization-objective.svg',
    'cs-conv-sliding-response.svg',
    'prml-posterior-predictive.svg',
    'prml-dirichlet-multinomial.svg',
    'prml-svm-c-rvm.svg',
    'prml-em-evolution.svg',
    'prml-rejection-sampling.svg',
    'prml-pca-spectrum.svg',
    'prml-nn-regularization.svg',
    'prml-polynomial-kernel.svg',
    'prml-ep-vi.svg',
    'prml-factor-ica.svg',
    'prml-tree-ensemble.svg',
]:
    if required not in reference_source:
        errors.append(f'Missing required corrected reference figure: {required}')

if 'kind="text"' in reference_source:
    errors.append(
        'Reference figures must use visual panel kinds instead of paragraph-style '
        'text cards.'
    )

for svg_path in [*paper_diagrams, *reference_diagrams]:
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
        if text_class == 'title' and len(text_value) > 68:
            errors.append(
                f'Overlong figure title ({len(text_value)} chars): '
                f'{svg_path.name} -> {text_value[:48]}...'
            )
        elif text_class == 'subtitle' and len(text_value) > 120:
            errors.append(
                f'Overlong figure subtitle ({len(text_value)} chars): '
                f'{svg_path.name} -> {text_value[:56]}...'
            )
        elif text_class not in {'title', 'subtitle'} and len(text_value) > 64:
            errors.append(
                f'Overlong in-figure label ({len(text_value)} chars): '
                f'{svg_path.name} -> {text_value[:40]}...'
            )

for svg_path in sorted((ROOT / 'assets' / 'diagrams').glob('*.svg')):
    svg_text = svg_path.read_text(encoding='utf-8')
    if "font-family:Arial,'Noto Sans KR',sans-serif" in svg_text:
        errors.append(
            f'Core SVG puts Latin font before Korean fallback: {svg_path.name}'
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
print(
    f'Validated {len(pages)} pages plus '
    f'{len(paper_diagrams)} paper and {len(reference_diagrams)} reference SVGs.'
)
