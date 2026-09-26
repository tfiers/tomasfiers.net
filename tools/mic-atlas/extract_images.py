"""Extracts the images embedded in the manufacturers' PDFs that the tracing and image scripts use,
into sources/pages/ (see paths.py). Names: <short name>_<xref>.png, or <file prefix>_p0_x<xref>.png."""
import os, pymupdf
from paths import SRC, PAGES

JOBS = [  # (output name, PDF in sources/, xref of the embedded image)
    *[(f'se4400_{x}', '8ac76b35-sE4400-sE4100-T2-T1-user-manual-v1-2.pdf', x) for x in range(198, 206)],
    ('se8_35', '440f0c59-se8usermanualv1-9-2.pdf', 35),
    ('ovid_131', '5e265249-datasheet_ovid_system_cc-100_uk_web.pdf', 131),
    ('ovid_134', '5e265249-datasheet_ovid_system_cc-100_uk_web.pdf', 134),
    *[(f'c414_{x}', '8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf', x) for x in range(643, 656)],
    # product photos
    ('2009385d_p0_x1', '2009385d-at2020_english.pdf', 1),
    ('364a6e63_p0_x13', '364a6e63-V7V3UserManualv1.0-2.pdf', 13),
    ('68ef680f_p0_x13', '68ef680f-V7XUserManualv1-1.pdf', 13),
    ('5e265249_p0_x138', '5e265249-datasheet_ovid_system_cc-100_uk_web.pdf', 138),
    ('440f0c59_p0_x13', '440f0c59-se8usermanualv1-9-2.pdf', 13),
    ('8ac76b35_p0_x11', '8ac76b35-sE4400-sE4100-T2-T1-user-manual-v1-2.pdf', 11),
    ('8bb1a74e_p0_x765', '8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf', 765),
    ('8bb1a74e_p0_x767', '8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf', 767),
    ('dpa_p8_76', 'c2844ec7-19-1-4099_manual.pdf', 76),
    ('5bd4da93_p0_x85', '5bd4da93-462001-01U.pdf', 85),
]

os.makedirs(PAGES, exist_ok=True)
for name, pdf, xref in JOBS:
    pix = pymupdf.Pixmap(pymupdf.open(SRC + pdf), xref)
    if pix.alpha: pix = pymupdf.Pixmap(pix, 0)                       # drop the alpha channel
    if pix.colorspace.name != pymupdf.csRGB.name:                     # CMYK, DeviceN, gray, … -> RGB
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    pix.save(PAGES + name + '.png')
    print(name, pix.width, 'x', pix.height)
