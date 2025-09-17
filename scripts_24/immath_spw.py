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

# Root that contains the "concat/{mosaic_name}" tree
BASE_CONCAT_ROOT = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat'

# SPWs to average
SPW_LIST = [3, 4, 5, 6, 8, 15, 16, 17]

# Prefer pb-corrected tt0 inputs? If True, use *.image.pbcor.tt0 when available
PREFER_PBCOR_TT0 = False

# Overwrite existing averaged images?
OVERWRITE = True
# =================================


def safe(s):
    return s.replace(':', '_')


def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def build_mean_expr(n, token="IM"):
    if n == 1:
        return f"{token}0"
    return f"({ ' + '.join([f'{token}{i}' for i in range(n)]) })/{float(n)}"


def try_immath_with_varnames(imgs, outfile):
    n = len(imgs)
    varnames = [f"A{i}" for i in range(n)]
    expr = build_mean_expr(n, token="A")
    print("  [immath-varnames] expr:", expr)
    immath(imagename=imgs, varnames=varnames, expr=expr, outfile=outfile)


def try_immath_with_symlinks(imgs, outfile, workdir):
    ensure_dir(workdir)
    links = []
    try:
        for i, src in enumerate(imgs):
            if src.endswith(".image.pbcor.tt0"):
                suffix = ".image.pbcor.tt0"
            elif src.endswith(".image.tt0"):
                suffix = ".image.tt0"
            elif src.endswith(".image.pbcor"):
                suffix = ".image.pbcor"
            else:
                suffix = ".image"
            dst = os.path.join(workdir, f"im{i}{suffix}")
            if os.path.islink(dst) or os.path.exists(dst):
                try:
                    if os.path.islink(dst):
                        os.unlink(dst)
                    else:
                        shutil.rmtree(dst)
                except Exception:
                    pass
            os.symlink(src, dst)
            links.append(dst)

        expr = build_mean_expr(len(links))  # IM0 + IM1 + ...
        print("  [immath-symlinks] expr:", expr)
        immath(imagename=links, expr=expr, outfile=outfile)
    finally:
        for p in links:
            try: os.unlink(p)
            except Exception: pass
        try: os.rmdir(workdir)
        except Exception: pass


def find_casa_images_in_dir(d):
    """
    Return CASA image *directories* inside d with endings we accept.
    """
    endings = [".image.pbcor.tt0", ".image.tt0", ".image.pbcor", ".image"]
    results = []
    try:
        for name in os.listdir(d):
            if any(name.endswith(suf) for suf in endings):
                p = os.path.join(d, name)
                if os.path.isdir(p):
                    results.append(p)
    except FileNotFoundError:
        pass
    return results


def collect_inputs_for_spw(base_concat, spw, prefer_pbcor=True):
    """
    Expected layout (your spec):
      {base_concat}/Images/spw/
        ├─ <MSNAME>_calibrated/
        │    └─ tclean/
        │        └─ spw{spw}/
        │             ├─ <...>.image.tt0 / .image.pbcor.tt0 / .image.pbcor / .image
        └─ (repeat for each MS)
    """
    root = os.path.join(base_concat, "Images", "spw")
    if not os.path.isdir(root):
        print(f"  [scan] Missing root: {root}")
        return []

    # all *_calibrated dirs directly under Images/spw/
    ms_dirs = sorted([d for d in glob.glob(os.path.join(root, "*_calibrated*")) if os.path.isdir(d)])
    if not ms_dirs:
        print(f"  [scan] No '*_calibrated' MS folders found under {root}")
        return []

    # gather images from each MS’s tclean/spw{spw} directory
    spw_dirname = f"spw{spw}"
    cands = []
    for msd in ms_dirs:
        tclean_spw_dir = os.path.join(msd, "tclean", spw_dirname)
        imgs = find_casa_images_in_dir(tclean_spw_dir)
        # also accept nested per-run subdirs like .../tclean/spw{spw}/runX/<images>
        for run_dir in glob.glob(os.path.join(tclean_spw_dir, "*")):
            if os.path.isdir(run_dir):
                imgs += find_casa_images_in_dir(run_dir)
        if imgs:
            cands.extend(imgs)

    if not cands:
        print(f"  [scan] No images found for SPW {spw} under any '*_calibrated/tclean/{spw_dirname}'")
        return []

    # ranking preference
    def rank(path):
        name = os.path.basename(path)
        if name.endswith(".image.pbcor.tt0") and prefer_pbcor:
            return (1, name)
        if name.endswith(".image.tt0"):
            return (2, name)
        if name.endswith(".image.pbcor") and prefer_pbcor:
            return (3, name)
        if name.endswith(".image"):
            return (4, name)
        return (9, name)

    # one pick per MS to avoid duplicates from multiple runs of the same MS
    picks_by_ms = {}
    for p in sorted(cands):
        # ms key is the *_calibrated folder name
        parts = p.split(os.sep)
        try:
            ms_idx = parts.index("spw") + 1  # "spw" then "<MSNAME>_calibrated"
        except ValueError:
            # fall back: find the *_calibrated segment
            ms_idx = next((i for i, s in enumerate(parts) if s.endswith("_calibrated")), None)
        if ms_idx is None or ms_idx >= len(parts):
            ms_key = os.path.dirname(os.path.dirname(p))  # coarse fallback
        else:
            ms_key = parts[ms_idx]

        if (ms_key not in picks_by_ms) or (rank(p) < rank(picks_by_ms[ms_key])):
            picks_by_ms[ms_key] = p

    imagenames = sorted(set(picks_by_ms.values()))
    print(f"  [scan] SPW {spw}: picked {len(imagenames)} inputs from {len(picks_by_ms)} MS folders")
    for p in imagenames[:10]:
        print("    -", p)
    if len(imagenames) > 10:
        print(f"    ... and {len(imagenames)-10} more")

    return imagenames


def average_spw(base_concat, mosaic_name, spw, prefer_pbcor=True, overwrite=True):
    print(f"\n=== SPW {spw} ===")

    # Output: concat/{mosaic}/Images/spw/tclean/spw{spw}/<mosaic_safe>_StokesI_spw{spw}_avg_*.image
    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    ensure_dir(out_dir)

    imgs = collect_inputs_for_spw(base_concat, spw, prefer_pbcor=prefer_pbcor)
    if not imgs:
        print(f"  No inputs found for SPW {spw}. Created (empty) out dir: {out_dir}")
        return

    has_pb = any(p.endswith(".image.pbcor.tt0") or p.endswith(".image.pbcor") for p in imgs)
    suffix = "_pbcor_tt0" if (prefer_pbcor and has_pb) else "_tt0"
    out_name = f"{safe(mosaic_name)}_StokesI_spw{spw}_avg{suffix}.image"
    outfile = os.path.join(out_dir, out_name)

    if os.path.exists(outfile):
        if overwrite:
            print("  Removing existing:", outfile)
            shutil.rmtree(outfile, ignore_errors=True)
        else:
            print("  Output exists and OVERWRITE=False. Skipping.")
            return

    print("  Inputs to average ({}):".format(len(imgs)))
    for p in imgs:
        print("   -", p)

    # Attempt 1: varnames
    try:
        try_immath_with_varnames(imgs, outfile)
        if os.path.isdir(outfile):
            print("  Wrote:", outfile)
            return
        else:
            print("  immath reported success but outfile not found:", outfile)
    except Exception as e:
        print("  [immath-varnames] failed:", e)

    # Attempt 2: symlinks
    workdir = os.path.join(out_dir, f"_tmp_symlinks_spw{spw}")
    try:
        try_immath_with_symlinks(imgs, outfile, workdir)
        if os.path.isdir(outfile):
            print("  Wrote:", outfile)
        else:
            print("  immath reported success but outfile not found:", outfile)
    except Exception as e2:
        print("  [immath-symlinks] failed:", e2)
        traceback.print_exc()
        print("  ERROR: Could not average SPW", spw)


def main():
    base_concat = os.path.join(BASE_CONCAT_ROOT, mosaic_name)
    if not os.path.isdir(base_concat):
        raise RuntimeError(f"Base concat path not found: {base_concat}")

    print("Phase center (mosaic):", mosaic_name)
    print("Base concat path     :", base_concat)
    print("SPWs                 :", SPW_LIST)
    print("Prefer pbcor tt0     :", PREFER_PBCOR_TT0)
    print("Overwrite outputs    :", OVERWRITE)

    for s in SPW_LIST:
        average_spw(
            base_concat=base_concat,
            mosaic_name=mosaic_name,
            spw=s,
            prefer_pbcor=PREFER_PBCOR_TT0,
            overwrite=OVERWRITE
        )

    print("\nAll done.")


if __name__ == "__main__":
    main()
