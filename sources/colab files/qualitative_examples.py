"""
Qualitative Examples Extraction Script
CLEF 2026 SimpleText Task 1 — Tokatrons Team

Purpose: Extract representative simplification examples for §8 (Error Analysis).
Run on the LLaMA-8B validation output or any system outputs.

Usage:
  python qualitative_examples.py

Expected data format: JSONL with fields:
  source, reference, bart_v2_output, llama8b_output, llama4_output

Output: LaTeX-ready table rows.
"""

import json
import random
import argparse

random.seed(42)


def load_data(path: str) -> list[dict]:
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def pick_examples(data: list[dict], n: int = 3) -> list[dict]:
    """Pick n representative examples showing clear differences."""
    scored = []
    for item in data:
        src_len = len(item['source'].split())
        ref_len = len(item['reference'].split())
        bart_len = len(item.get('bart_v2_output', '').split())
        llama_len = len(item.get('llama8b_output', '').split())

        # Score examples where outputs diverge significantly
        divergence = abs(bart_len - llama_len)
        scored.append((divergence, item))

    scored.sort(key=lambda x: -x[0])
    # Pick from top-divergence examples, but spread across different lengths
    short = [s for s in scored if len(s[1]['source'].split()) < 30]
    medium = [s for s in scored if 30 <= len(s[1]['source'].split()) <= 60]
    long = [s for s in scored if len(s[1]['source'].split()) > 60]

    examples = []
    for pool in [short, medium, long]:
        if pool:
            examples.append(pool[0][1])

    return examples[:n]


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
        '_': r'\_', '{': r'\{', '}': r'\}',
        '~': r'\textasciitilde{}', '^': r'\^{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_table(examples: list[dict]) -> str:
    lines = []
    lines.append(r"\begin{table*}[t]")
    lines.append(r"\centering")
    lines.append(r"\caption{Qualitative comparison of system outputs.}")
    lines.append(r"\label{tab:qualitative}")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{p{0.12\textwidth}p{0.25\textwidth}p{0.25\textwidth}p{0.25\textwidth}}")
    lines.append(r"\toprule")
    lines.append(r"Source & Reference & BART v2 & LLaMA-3.1-8B \\")
    lines.append(r"\midrule")

    for i, ex in enumerate(examples):
        src = escape_latex(ex['source'])
        ref = escape_latex(ex.get('reference', ''))
        bart = escape_latex(ex.get('bart_v2_output', ''))
        llama = escape_latex(ex.get('llama8b_output', ''))

        if len(src) > 300:
            src = src[:297] + '...'
        if len(ref) > 300:
            ref = ref[:297] + '...'
        if len(bart) > 300:
            bart = bart[:297] + '...'
        if len(llama) > 300:
            llama = llama[:297] + '...'

        lines.append(f"{src} & {ref} & {bart} & {llama} \\\\")
        if i < len(examples) - 1:
            lines.append(r"\midrule")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table*}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True,
                        help='Path to JSONL file with all system outputs')
    parser.add_argument('--output', default='qualitative_table.tex',
                        help='Output LaTeX file path')
    parser.add_argument('--n', type=int, default=3,
                        help='Number of examples')
    args = parser.parse_args()

    data = load_data(args.input)
    examples = pick_examples(data, n=args.n)
    latex_table = format_table(examples)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(latex_table)

    print(f"Written {len(examples)} examples to {args.output}")
    print()
    print("LaTeX table:")
    print(latex_table)


if __name__ == '__main__':
    main()
