#!/usr/bin/env python3
"""Extract published Nepal-Wang SI Tables S10-S17; no Tc calculation.

Run: python extract_stable_tables.py > stable_epc_published.csv
Dependencies: requests, pypdf. Downloads only the ~4 MB supplementary PDF.
Columns preserve the authors' formula and reported values; FE is NOT hull energy.
Source DOI: 10.1038/s41524-026-01962-w (2026).
"""
import csv
import io
import re
import sys

import requests
from pypdf import PdfReader

URL = (
    'https://media.springernature.com/original/springer-static/esm/'
    'art%3A10.1038%2Fs41524-026-01962-w/MediaObjects/'
    '41524_2026_1962_MOESM1_ESM.pdf'
)
ROW = re.compile(
    r'^(mp-\d+)\s+(\S+)\s+(\d+)\s+(-?[\d.]+)\s+'
    r'([\d.]+)\s+([\d.]+)\s+([\d.]+)$'
)


def main():
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    reader = PdfReader(io.BytesIO(response.content))
    rows = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        table = re.search(r'TABLE\s+S(1[0-7])\.', text)
        if not table:
            continue
        for line in text.splitlines():
            match = ROW.fullmatch(line.strip())
            if match:
                rows.append((*match.groups(), 'S' + table.group(1), page_number))
    if len(rows) != 381:
        raise RuntimeError(
            f'Expected 381 published stable-table rows; obtained {len(rows)}. '
            'Inspect PDF/version/parser before using this output.'
        )
    writer = csv.writer(sys.stdout)
    writer.writerow([
        'mp_id', 'formula_as_published', 'spacegroup',
        'formation_energy_eV_per_atom', 'lambda', 'omega_log_K',
        'Tc_K_as_published', 'source_table', 'pdf_page_1_based',
    ])
    writer.writerows(rows)
    print(
        f'Extracted {len(rows)} rows from {len(response.content)} PDF bytes. '
        'These are published predictions, not measurements or new calculations.',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
