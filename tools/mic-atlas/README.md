# Mic Atlas tools

The scripts that produced the data behind [Mic Atlas](https://tomasfiers.net/mics.html) (`static/mics.html`):
the frequency responses, polar data, specs and images of the built-in microphones in `static/mics-library.js`.

They were written with Claude Code while building the page. They're research scripts rather than a polished
package: each one records exactly how one manufacturer's graph was read (which PDF drawing, which pixel colours,
where the axes are). Running them again reproduces the committed data exactly.

Requirements: Python 3 with `numpy`, `Pillow` and (for reading PDFs) `pymupdf`.

## Rebuild the data file

```sh
python3 build_library.py
```

This writes `static/mics-library.js` from the extracted data in `response/` and `polar/`. It needs no PDFs.
Everything that isn't a curve lives in `build_library.py` itself: specs, descriptions, manufacturer and price,
links, which images go with which mic, and the order of the library. The top of `mics-library.js` explains every
field of an entry.

## How the curves were extracted

- **`response/`**: on-axis frequency responses. One script per source, each writing a `.json` (or `.csv`)
  with `[frequency, dB]` points:
  - `vec.py`, `u87.py`, `dpa.py`, `dpa_prox.py`, `shure.py`, `vector_extras.py`: where the PDF contains the graph
    as vector paths, the curve is read exactly (`pymupdf`'s `get_drawings()`). The axes are calibrated from the
    gridlines or axis labels in the same PDF.
  - `trace.py`, `setrace2.py`, `c414.py`, `ovid.py`, `mk4.py`, `mk5.py`: where the graph is an image, the curve
    is traced by its colour, column by column, and calibrated from the gridlines (roughly ±0.5 dB).
  - `ovid_join.py`: joins the Ovid's near-field and far-field measurements.
- **`polar/`**: polar data, as dB at 0°, 5°, …, 180° for each plotted frequency. Shared helpers are in
  `common.py`: reading vector paths, tracing coloured or dark curves around a centre, and overlay images for
  checking. `rings.py` finds the ring radii of a polar grid.
- **`images/`**: how the first set of product photos, polar diagrams and source-graph crops were cut out of the
  PDFs. They were later converted to WebP. A few images, such as the Schoeps and Shure ones, were made with
  one-off commands in the same way.

To run the extraction scripts, put the source files (below) in `sources/`, or point `MIC_ATLAS_SOURCES` to
where they are. Then:

```sh
python3 extract_images.py      # the images embedded in the PDFs, into sources/pages/
cd response && python3 vec.py  # etc.: run each script from its own folder
```

Most scripts also save a `chk_*.png` with the traced points drawn over the source graph, to check the trace.

## Source files

The manufacturers' documents aren't redistributed here. File names are as they were uploaded while building
the page. The prefix is just an upload ID; keep it, since the scripts use these exact names.

| File in `sources/` | What | From |
|---|---|---|
| `2009385d-at2020_english.pdf` | AT2020 spec sheet | [audio-technica.com](https://docs.audio-technica.com/us/at2020_english.pdf) |
| `c982d482-8849953521694.pdf` | Behringer C-2 manual | behringer.com |
| `364a6e63-V7V3UserManualv1.0-2.pdf` | sE V7 manual | [seelectronics.com](https://seelectronics.com/wp-content/uploads/2021/11/V7V3UserManualv1.0-2.pdf) |
| `68ef680f-V7XUserManualv1-1.pdf` | sE V7 X manual | [seelectronics.com](https://seelectronics.com/wp-content/uploads/2021/11/V7XUserManualv1-1.pdf) |
| `440f0c59-se8usermanualv1-9-2.pdf` | sE8 manual | [seelectronics.com](https://seelectronics.com/wp-content/uploads/2021/11/sE8UserManualv1-9-2.pdf) |
| `8ac76b35-sE4400-sE4100-T2-T1-user-manual-v1-2.pdf` | sE4400 manual | seelectronics.com |
| `5e265249-datasheet_ovid_system_cc-100_uk_web.pdf` | the t.bone Ovid CC 100 data sheet | thomann.de |
| `c2844ec7-19-1-4099_manual.pdf` | DPA 4099 manual | [dpamicrophones.com](https://dpa.cloud14.structpim.com/media/4bknjkkj/4099-manual.pdf) |
| `5bd4da93-462001-01U.pdf` | Neumann U 87 Ai manual | [neumann.com](https://www.neumann.com/globalassets/digizuite/16474-en-opin0134_u87ai_06-10.pdf) |
| `8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf` | AKG C414 XLS / XLII manual | [akg.com](https://www.akg.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dwaabcd3f2/pdfs/AKG_C414XLS_C414XLII_Manual.pdf) |
| `bea4129c-us_pro_sm57_specsheet.pdf` | Shure SM57 spec sheet | shure.com |
| `9402a691-us_pro_sm58_specsheet.pdf` | Shure SM58 spec sheet | shure.com |
| `a53d1e0f-image.jpg` | sE V7 response and polar graphs (screenshot of the manual) | seelectronics.com |
| `fa1198f6-image.jpg` | AT2020 response graph (screenshot) | audio-technica.com |
| `a58ba6db-image.jpg`, `99afab08-image.jpg` | Schoeps MK 4 response and polar graphs | schoeps.de |
| `0d42ac95-image.jpg`, `3768500a-image.jpg` | Schoeps MK 5 response graphs (omni, cardioid) | schoeps.de |
| `3c1c18f7-image.jpg`, `0baabca9-image.jpg` | Schoeps MK 5 polar graphs (omni, cardioid) | schoeps.de |
| `556bd71e-image.png`, `ff7026b8-image.png` | Schoeps MK 4 graph (an earlier screenshot) and photo | schoeps.de |

## Adding a mic

The quickest way is how these were done: give an AI coding assistant such as Claude Code the manufacturer's
data sheet or manual (PDF), and ask it to add the mic to Mic Atlas along these lines:

1. Find the response graph in the PDF. If it's vector data, read the curve's path and calibrate the axes from
   the gridlines or labels. If it's an image, trace the curve's colour.
2. Do the same for the polar plot, if there is one. Rings and angles give dB per 5° from 0° to 180°.
3. Save both as data files in `response/` and `polar/`. Add the mic (specs, description, links, images) to
   `build_library.py`, then run it.
4. Check the traced points against the original graph (the `chk_*.png` overlays) before trusting them.

For a one-off comparison, no code is needed: the page's "Add Microphone" section takes pasted or dropped
`[frequency, dB]` data.
