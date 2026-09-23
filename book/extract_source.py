#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pull a chapter out of hard.pdf as a cleaned, OCR'd reference.

    python3 book/extract_source.py ch02-in-the-canteen 32 45

Arguments: chapter folder, first and last BOOK page (as printed in the book).
Writes <chapter>/source/scan-cleaned.pdf and <chapter>/source/scan-text.txt —
the reference you transcribe content.py from.

Needs: PyMuPDF, Pillow, numpy, tesseract (with the nld language pack).
    brew install tesseract tesseract-lang
    python3 -m pip install --break-system-packages numpy   (or use a venv)

About hard.pdf: book page = PDF page + 1. Every PDF page carries a CropBox that
selects ONE book page out of the scanned spread, so rendering with PyMuPDF gives
a single page. (The Read tool ignores CropBox and shows the spread twice — that
is not duplication in the file.)

The scan is MRC-compressed: crisp 200 dpi bitonal text over a blurry 100 dpi grey
background. So text is sharp, but the tinted boxes carry bleed-through from the
facing page. The cleanup below rebuilds those tints instead of filtering them.
"""
import os, subprocess, sys, tempfile

def need(mod):
    try: return __import__(mod)
    except ImportError: sys.exit(f"missing dependency: {mod} — see the docstring at the top of this file")

fitz = need("fitz"); np = need("numpy")
from PIL import Image, ImageFilter
from numpy.lib.stride_tricks import sliding_window_view

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(os.path.dirname(ROOT), "hard.pdf")
DPI, BLOCK = 400, 24
SCALE = DPI / 200.0

def _coarse_max(a, block=BLOCK):
    h, w = a.shape
    H, W = -(-h//block)*block, -(-w//block)*block
    pad = np.full((H, W), 255, np.uint8); pad[:h, :w] = a
    return pad.reshape(H//block, block, W//block, block).max(axis=(1, 3)), (H, W)

def background(a, block=BLOCK):
    """Local paper/tint value with the text removed."""
    b, (H, W) = _coarse_max(a, block)
    b3 = sliding_window_view(np.pad(b, 2, mode="edge"), (5, 5)).max(axis=(2, 3))
    im = Image.fromarray(b3).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(block*1.2))
    return np.asarray(im, dtype=np.float32)[:a.shape[0], :a.shape[1]]

def _components(mask):
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32); cur = 0
    for sy in range(h):
        for sx in range(w):
            if mask[sy, sx] and lab[sy, sx] == 0:
                cur += 1; stack = [(sy, sx)]; lab[sy, sx] = cur
                while stack:
                    y, x = stack.pop()
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; stack.append((ny, nx))
    return lab, cur

def tint_mask(a, block=BLOCK, thresh=244.0, min_cells=25, fill_ratio=0.45):
    """The design tints are rectangles. Detect them coarsely, then snap each to its
    bounding box so bleed-through cannot eat holes out of the fill."""
    b, (H, W) = _coarse_max(a, block)
    lab, n = _components(b < thresh)
    out = np.zeros_like(b, dtype=bool)
    for k in range(1, n+1):
        ys, xs = np.where(lab == k)
        if len(ys) < min_cells: continue
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        if len(ys)/((y1-y0+1)*(x1-x0+1)) >= fill_ratio: out[y0:y1+1, x0:x1+1] = True
        else: out[ys, xs] = True
    im = Image.fromarray((out*255).astype(np.uint8)).resize((W, H), Image.NEAREST)
    im = im.filter(ImageFilter.GaussianBlur(3.0))
    return np.asarray(im, dtype=np.float32)[:a.shape[0], :a.shape[1]]/255.0

def restore(a, tint=232.0, ink=16.0, dead=30.0, floor=55.0):
    """Rebuild the page as flat design tints plus crisp ink. The dead zone erases
    bleed-through (a few levels below local paper) and leaves real ink alone."""
    af = a.astype(np.float32)
    B = np.clip(background(a), 60, 255)
    paper = 255.0 - (255.0-tint)*tint_mask(a)
    alpha = np.clip((B - af - dead)/np.maximum(B - floor - dead, 1.0), 0, 1)
    return np.clip(paper*(1-alpha) + ink*alpha, 0, 255).astype(np.uint8)

def photo_curve():
    pts = [(0,0),(40,25),(200,205),(250,252),(254,255),(255,255)]
    x = np.arange(256, dtype=np.float32)
    return np.clip(np.interp(x, [p[0] for p in pts], [p[1] for p in pts]), 0, 255).astype(np.uint8)

def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    chapter, first, last = sys.argv[1].rstrip("/"), int(sys.argv[2]), int(sys.argv[3])
    cdir = os.path.join(ROOT, chapter)
    if not os.path.isdir(cdir): sys.exit(f"no such directory: {cdir}")
    outdir = os.path.join(cdir, "source"); os.makedirs(outdir, exist_ok=True)

    doc = fitz.open(BOOK)
    LP = photo_curve()
    tmp = tempfile.mkdtemp()
    pdfs, texts = [], []
    print(f"{chapter}: book pages {first}-{last}  (PDF pages {first-1}-{last-1})")

    for book_page in range(first, last+1):
        page = doc[book_page - 2]            # book page = PDF page + 1, and fitz is 0-based
        pm = page.get_pixmap(dpi=DPI, colorspace=fitz.csGRAY)
        a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width).copy()
        is_opener = book_page == first       # chapter openers are a full-bleed photo
        if is_opener:
            a[:806, :200] = 255; a[806:, :76] = 255
            a = LP[a]
        else:
            a[:, :int(115*SCALE)] = 255      # binding streak in the left margin
            a[:int(50*SCALE), :] = 255       # dark line along the top edge
            a[:, int(1252*SCALE):] = 255     # right margin
            a = restore(a)
        png = os.path.join(tmp, f"p{book_page:03d}.png")
        Image.fromarray(a).save(png, optimize=True)
        base = os.path.join(tmp, f"p{book_page:03d}")
        subprocess.run(["tesseract", png, base, "-l", "nld+eng", "--psm", "6",
                        "--dpi", str(DPI), "pdf", "txt"],
                       check=True, stderr=subprocess.DEVNULL)
        pdfs.append(base + ".pdf"); texts.append((book_page, base + ".txt"))
        print(f"  p{book_page}  {'photo' if is_opener else 'text '}  "
              f"{len(open(base+'.txt',encoding='utf-8').read().split()):>4} words")

    out = fitz.open()
    for p in pdfs: out.insert_pdf(fitz.open(p))
    out.set_page_labels([{"startpage": 0, "prefix": "", "style": "D", "firstpagenum": first}])
    out.set_metadata({"title": f"Nederlands in gang — book pages {first}-{last} (cleaned scan)"})
    pdf_out = os.path.join(outdir, "scan-cleaned.pdf")
    out.save(pdf_out, deflate=True, garbage=4)

    txt_out = os.path.join(outdir, "scan-text.txt")
    with open(txt_out, "w", encoding="utf-8") as fh:
        for n, t in texts:
            fh.write(f"════ blz. {n} ════\n" + open(t, encoding="utf-8").read() + "\n")
    print(f"  -> {pdf_out}  ({out.page_count} pages, {os.path.getsize(pdf_out)//1024} KB)")
    print(f"  -> {txt_out}")

if __name__ == "__main__":
    main()
