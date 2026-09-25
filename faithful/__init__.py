"""Literal grounding gate for short generated summaries.

A pass checks tokens only; it cannot prove the meaning of a claim.
"""
import re

NUMBERS = re.compile(r'(?<![\w])\d+(?:[.,]\d+)*(?:%|[kKmMbB])?(?![\w])')
NAMES = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:[-.][A-Za-z0-9]+)*\b")
PRODUCT_IDS = re.compile(r'\b(?:[a-z]+[A-Z][A-Za-z0-9]*|[a-z][a-z0-9._/-]*\d[a-z0-9._/-]*)\b')
KNOWN_LOWERCASE_PRODUCTS = {'claude', 'codex', 'deepseek', 'gemini', 'gradio', 'llama',
                            'ollama', 'pytorch', 'qwen', 'vllm'}
GENERIC = {'A', 'An', 'The', 'This', 'These', 'Those', 'It', 'Its', 'They', 'Their',
           'For', 'With', 'Using', 'Users', 'Builders', 'Developers', 'Researchers',
           'Source', 'Project', 'Model', 'Models', 'Paper', 'Results', 'However', 'In',
           'On', 'By', 'To', 'As', 'And', 'If', 'There', 'Here'}


def faithful(result, source):
    summary = result.get('summary')
    why = result.get('why_builder_cares')
    if not isinstance(summary, str) or not isinstance(why, str) or not summary.strip() or not why.strip():
        return 'missing summary or builder line'
    sentences = [part for part in re.split(r'(?<=[.!?])\s+', summary.strip()) if part]
    if len(sentences) != 2 or not all(part[-1] in '.!?' for part in sentences):
        return 'summary must have exactly two sentences'
    if '\n' in why:
        return 'builder reason must be one line'
    combined = summary + ' ' + why
    missing = []
    for token in NUMBERS.findall(combined):
        if not re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', source, re.I):
            missing.append(f'number {token}')
    for token in NAMES.findall(combined):
        if token in GENERIC:
            continue
        if not re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', source, re.I):
            missing.append(f'name {token}')
    for token in PRODUCT_IDS.findall(combined):
        if not re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', source, re.I):
            missing.append(f'product {token}')
    for token in re.findall(r'\b[a-z]+\b', combined):
        if token in KNOWN_LOWERCASE_PRODUCTS and not re.search(
                r'(?<!\w)' + re.escape(token) + r'(?!\w)', source, re.I):
            missing.append(f'product {token}')
    return 'absent from fetched text: ' + ', '.join(dict.fromkeys(missing)) if missing else ''
