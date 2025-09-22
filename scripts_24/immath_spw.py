# average_spw_images.py  (run inside CASA)
import os
import re
import glob
import shutil
import traceback

# ========= USER SETTINGS =========
# mosaic_name = '03:26:24.057_+30.35.58.881'
mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'

# average_spw_images_simple.py  (run inside CASA 6)
# Runs immediately when you %run it.

BASE_CONCAT_ROOT  = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat'
SPW_LIST          = [3, 4, 5, 6, 8, 15, 16, 17]

PREFER_PB_TT0     = False   # if True and both exist for an MS, prefer .pb.tt0 over .image.tt0
OVERWRITE         = True
USE_IMREGRID      = True
# ------------------------------------------------

import os, glob, shutil, tempfile, uuid, traceback

print("\n==============================")
print("START average_spw_images_no_colons")
print("==============================\n")

# CASA tasks
from casatasks import imregrid, immath

def _safe_name(s):  # only for filenames
    return s.replace(":", "_")

base_concat = os.path.join(BASE_CONCAT_ROOT, mosaic_name)
print("mosaic_name      :", mosaic_name)
print("base_concat      :", base_concat)
print("SPWs             :", SPW_LIST)

if not os.path.isdir(base_concat):
    raise RuntimeError("[FATAL] Base concat path not found: " + base_concat)

# ensure top-level output branch
top_out = os.path.join(base_concat, "Images", "tclean")
os.makedirs(top_out, exist_ok=True)

ACCEPTED_SUFFIXES = (".image.tt0", ".pb.tt0")

for spw in SPW_LIST:
    print("\n--- SPW", spw, "---")

    # discover inputs
    inputs_root = os.path.join(base_concat, "Images", "spw")
    if not os.path.isdir(inputs_root):
        print("[WARN] Missing input root:", inputs_root, " -> skipping")
        continue

    ms_dirs = sorted([d for d in glob.glob(os.path.join(inputs_root, "*_calibrated*")) if os.path.isdir(d)])
    print("MS candidate dirs:", len(ms_dirs))
    if not ms_dirs:
        print("[stop] No *_calibrated* dirs -> skipping SPW", spw)
        continue

    chosen = []  # one picked image per MS
    for msd in ms_dirs:
        spw_dir_a = os.path.join(msd, "tclean", f"spw{spw}")
        spw_dir_b = os.path.join(msd, "tclean", f"spw{spw:02d}")
        spw_dir   = spw_dir_a if os.path.isdir(spw_dir_a) else (spw_dir_b if os.path.isdir(spw_dir_b) else spw_dir_a)

        print(" check:", spw_dir, "exists=", os.path.isdir(spw_dir))
        cands = []

        def scan_once(dd):
            if not os.path.isdir(dd): return
            for name in os.listdir(dd):
                p = os.path.join(dd, name)
                if os.path.isdir(p) and name.endswith(ACCEPTED_SUFFIXES):
                    cands.append(p)

        scan_once(spw_dir)
        if os.path.isdir(spw_dir):
            for sub in sorted([p for p in glob.glob(os.path.join(spw_dir, "*")) if os.path.isdir(p)]):
                scan_once(sub)

        if not cands:
            print("  No accepted inputs in:", os.path.basename(msd))
            continue

        def rk(p):
            nm = os.path.basename(p)
            if PREFER_PB_TT0:
                return (0 if nm.endswith(".pb.tt0") else 1, nm)
            else:
                return (0 if nm.endswith(".image.tt0") else 1, nm)

        best = sorted(cands, key=rk)[0]
        chosen.append(best)
        print("  picked:", best)

    if not chosen:
        print("[stop] No inputs picked for SPW", spw)
        continue

    # output dir (as requested)
    out_dir = os.path.join(base_concat, "Images", "tclean", f"spw{spw}")
    os.makedirs(out_dir, exist_ok=True)

    # tmp work area with NO COLONS in the path
    tmp_root = os.path.join(tempfile.gettempdir(), "casa_avg_" + uuid.uuid4().hex, f"spw{spw}")
    os.makedirs(tmp_root, exist_ok=True)
    print(" tmp_root:", tmp_root)

    try:
        # Regrid to first image (into tmp_root)
        if USE_IMREGRID:
            template_src = chosen[0]
            template_dst = os.path.join(tmp_root, "rg0.image")
            print(" copy template:", template_src, "->", template_dst)
            shutil.copytree(template_src, template_dst, symlinks=True)

            rg_paths = [template_dst]
            for i, src in enumerate(chosen[1:], start=1):
                dst = os.path.join(tmp_root, f"rg{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                print(" imregrid     :", src, "->", dst)
                imregrid(imagename=src, template=template_dst, output=dst, overwrite=True)
                rg_paths.append(dst)
        else:
            # Copy originals into tmp (avoid colons in paths)
            rg_paths = []
            for i, src in enumerate(chosen):
                dst = os.path.join(tmp_root, f"rg{i}.image")
                print(" copy input   :", src, "->", dst)
                shutil.copytree(src, dst, symlinks=True)
                rg_paths.append(dst)

        # Build immath expression using explicit varnames
        n = len(rg_paths)
        varnames  = [f"IM{i}" for i in range(n)]
        if n == 1:
            expr = "IM0"
        else:
            expr = "(" + " + ".join(varnames) + f")/{float(n)}"

        # Write final outfile in requested directory (colons OK for outfile path)
        suffix   = "pb_tt0" if (PREFER_PB_TT0 and any(os.path.basename(p).endswith(".pb.tt0") for p in chosen)) else "tt0"
        out_name = f"{_safe_name(mosaic_name)}_StokesI_spw{spw}_avg_{suffix}.image"
        outfile  = os.path.join(out_dir, out_name)

        if os.path.isdir(outfile):
            if OVERWRITE:
                print(" removing existing:", outfile)
                shutil.rmtree(outfile, ignore_errors=True)
            else:
                print(" exists and OVERWRITE=False -> skipping write:", outfile)
                continue

        print(" immath expr:", expr)
        print(" n_inputs   :", n)
        print(" writing    :", outfile)
        immath(imagename=rg_paths, varnames=varnames, expr=expr, outfile=outfile)

        if os.path.isdir(outfile):
            print(" ✅ WROTE:", outfile)
        else:
            print(" [WARN] immath returned but outfile not found:", outfile)

    finally:
        # clean tmp
        if os.path.isdir(tmp_root):
            shutil.rmtree(tmp_root, ignore_errors=True)
            print(" cleaned tmp :", tmp_root)

print("\n==============================")
print("DONE average_spw_images_no_colons")
print("==============================\n")