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

# ---------------- USER SETTINGS ----------------
mosaic_name = '03:29:12.973_+31.48.05.579'
BASE_CONCAT_ROOT = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat'
SPW_LIST = [3, 4, 5, 6, 8, 15, 16, 17]

PREFER_PB_TT0 = False
OVERWRITE = True
USE_IMREGRID = True
# ------------------------------------------------

import os, glob, shutil, traceback

print("\n==============================")
print("START average_spw_images_simple")
print("==============================\n")

# CASA tasks
try:
    from casatasks import imhead, imregrid, immath
except Exception as e:
    print("[FATAL] Could not import CASA tasks (imhead/imregrid/immath). Are you in CASA 6?")
    print("Error:", e)
    raise

# Paths
base_concat = os.path.join(BASE_CONCAT_ROOT, mosaic_name)
print("mosaic_name      :", mosaic_name)
print("base_concat      :", base_concat)
print("SPWs             :", SPW_LIST)
print("PREFER_PB_TT0    :", PREFER_PB_TT0)
print("OVERWRITE        :", OVERWRITE)
print("USE_IMREGRID     :", USE_IMREGRID)

if not os.path.isdir(base_concat):
    raise RuntimeError("[FATAL] Base concat path not found: " + base_concat)

# ensure Images/tclean exists
top_out = os.path.join(base_concat, "Images", "tclean")
if not os.path.isdir(top_out):
    print("Making:", top_out)
    os.makedirs(top_out, exist_ok=True)

# Accepted suffixes
ACCEPTED_SUFFIXES = (".image.tt0", ".pb.tt0")

def _safe_name(s): return s.replace(":", "_")

for spw in SPW_LIST:
    print("\n--- SPW", spw, "---")
    inputs_root = os.path.join(base_concat, "Images", "spw")
    if not os.path.isdir(inputs_root):
        print("[WARN] Missing input root:", inputs_root, " -> skip")
        continue

    ms_dirs = sorted([d for d in glob.glob(os.path.join(inputs_root, "*_calibrated*")) if os.path.isdir(d)])
    print("MS candidate dirs:", len(ms_dirs))
    if not ms_dirs:
        try:
            print("Contents of", inputs_root, ":", sorted(os.listdir(inputs_root))[:30])
        except Exception:
            pass
        print("No *_calibrated* dirs -> skipping SPW", spw)
        continue

    picked_images = []
    for msd in ms_dirs:
        spw_dir_a = os.path.join(msd, "tclean", f"spw{spw}")
        spw_dir_b = os.path.join(msd, "tclean", f"spw{spw:02d}")
        spw_dir = spw_dir_a if os.path.isdir(spw_dir_a) else (spw_dir_b if os.path.isdir(spw_dir_b) else spw_dir_a)

        print(" check:", spw_dir, "exists=", os.path.isdir(spw_dir))

        candidates, near_miss = [], []
        def scan_dir(dd):
            if not os.path.isdir(dd): return
            for name in os.listdir(dd):
                p = os.path.join(dd, name)
                if os.path.isdir(p):
                    if name.endswith(ACCEPTED_SUFFIXES):
                        candidates.append(p)
                    elif name.endswith((".image.pbcor.tt0", ".image.pbcor", ".image", ".pb", ".tt0")):
                        near_miss.append(p)

        scan_dir(spw_dir)
        if os.path.isdir(spw_dir):
            for sub in sorted([x for x in glob.glob(os.path.join(spw_dir, "*")) if os.path.isdir(x)]):
                scan_dir(sub)

        if not candidates and near_miss:
            print("  [hint] NEAR-MISS (excluded by strict suffix):")
            for p in near_miss[:10]:
                print("     -", p)

        if not candidates:
            print("  No accepted inputs in this MS -> skip MS:", os.path.basename(msd))
            continue

        def rank_key(path):
            nm = os.path.basename(path)
            if PREFER_PB_TT0:
                return (0 if nm.endswith(".pb.tt0") else 1, nm)
            else:
                return (0 if nm.endswith(".image.tt0") else 1, nm)

        best = sorted(candidates, key=rank_key)[0]
        picked_images.append(best)
        print("  picked:", best)

    if not picked_images:
        print("[stop] No inputs picked for SPW", spw)
        continue

    # OUTPUT DIR
    out_dir = os.path.join(base_concat, "Images", "tclean", f"spw{spw}")
    if not os.path.isdir(out_dir):
        print("Making:", out_dir)
        os.makedirs(out_dir, exist_ok=True)

    # write test
    try:
        with open(os.path.join(out_dir, "_write_test.txt"), "w") as f:
            f.write("ok\n")
        os.remove(os.path.join(out_dir, "_write_test.txt"))
        print(" write test: OK")
    except Exception as e:
        print("[SEVERE] Cannot write to:", out_dir, "Error:", e)

    # Regrid to first image (NO SYMLINKS—copy instead)
    if USE_IMREGRID:
        template = picked_images[0]
        tmp_rg = os.path.join(out_dir, f"_tmp_rg_spw{spw}")
        if os.path.isdir(tmp_rg):
            shutil.rmtree(tmp_rg, ignore_errors=True)
        os.makedirs(tmp_rg, exist_ok=True)

        rg_images = []
        for i, src in enumerate(picked_images):
            dst = os.path.join(tmp_rg, f"rg{i}.image")
            if os.path.exists(dst):
                shutil.rmtree(dst, ignore_errors=True)
            if i == 0:
                print(" copy first:", src, "->", dst)
                # **Important change**: copy the CASA image directory; do NOT symlink
                shutil.copytree(src, dst, symlinks=False)
            else:
                print(" imregrid   :", src, "->", dst)
                imregrid(imagename=src, template=template, output=dst, overwrite=True)
            rg_images.append(dst)
    else:
        rg_images = picked_images[:]

    # Average with immath (explicit varnames)
    n = len(rg_images)
    expr = "IM0" if n == 1 else "(" + " + ".join([f"IM{i}" for i in range(n)]) + f")/{float(n)}"
    varnames = [f"IM{i}" for i in range(n)]

    has_pb = any(os.path.basename(p).endswith(".pb.tt0") for p in picked_images)
    suffix = "pb_tt0" if (PREFER_PB_TT0 and has_pb) else "tt0"
    out_name = f"{_safe_name(mosaic_name)}_StokesI_spw{spw}_avg_{suffix}.image"
    outfile = os.path.join(out_dir, out_name)

    if os.path.isdir(outfile):
        if OVERWRITE:
            print(" removing existing:", outfile)
            shutil.rmtree(outfile, ignore_errors=True)
        else:
            print(" exists and OVERWRITE=False -> skip:", outfile)
            if USE_IMREGRID and os.path.isdir(os.path.join(out_dir, f"_tmp_rg_spw{spw}")):
                shutil.rmtree(os.path.join(out_dir, f"_tmp_rg_spw{spw}"), ignore_errors=True)
            continue

    print(" immath expr:", expr)
    print(" n_inputs   :", n)
    print(" writing    :", outfile)
    immath(imagename=rg_images, varnames=varnames, expr=expr, outfile=outfile)

    if os.path.isdir(outfile):
        print(" ✅ WROTE:", outfile)
    else:
        print(" [WARN] immath returned but outfile not found:", outfile)

    # Clean temp
    if USE_IMREGRID:
        tmp_rg = os.path.join(out_dir, f"_tmp_rg_spw{spw}")
        if os.path.isdir(tmp_rg):
            shutil.rmtree(tmp_rg, ignore_errors=True)
            print(" cleaned:", tmp_rg)

print("\n==============================")
print("DONE average_spw_images_simple")
print("==============================\n")
