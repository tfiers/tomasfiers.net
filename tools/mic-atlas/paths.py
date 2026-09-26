"""Where the Mic Atlas tools find their inputs and write their outputs.

SRC    the manufacturers' PDFs and images (not in the repository; see README.md), default ./sources/
PAGES  images extracted from those PDFs by extract_images.py, default ./sources/pages/
STATIC the website's static/ folder, where mics-library.js and the image folders live
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('MIC_ATLAS_SOURCES', os.path.join(HERE, 'sources')).rstrip('/') + '/'
PAGES = SRC + 'pages/'
STATIC = os.path.normpath(os.path.join(HERE, '..', '..', 'static')) + '/'
