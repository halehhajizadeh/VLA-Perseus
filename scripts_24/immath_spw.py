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

# Limit how deep we scan under Images/spw/ for inputs
MAX_SCAN_DEPTH = 6
# =================================


def safe(s):
    """Return a filename-safe token (remove colons for file basenames)."""
    return s.replace(':', '_')


def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def build_mean_expr(n, token="IM"):
    """Return '(IM0+IM1+...)/n' or 'IM0' for n==1."""
    if n == 1:
        return f"{token}0"
    return f"({ ' + '.join([f'{token}{i}' for i in range(n)]) })/{float(n)}"


def try_immath_with_varnames(imgs, outfile):
    """
    Attempt immath using varnames so raw file paths don't appear in the expression.
    """
    n = len(imgs)
    varnames = [f"A{i}" for i in range(n)]
    expr = build_mean_expr(n, token="A")
    print("  [immath-varnames] expr:", expr)
    immath(imagename=imgs, varnames=varnames, expr=expr, outfile=outfile)


def try_immath_with_symlinks(imgs, outfile, workdir):
    """
    Create colon-free symlinks to avoid LEL ':' parsing, then immath on those.
    """
    ensure_dir(workdir)
    links = []
    try:
        for i, src in enumerate(imgs):
            # choose suffix by original type
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

        n = len(links)
        expr = build_mean_expr(n)  # uses IM0, IM1, ...
        print("  [immath-symlinks] expr:", expr)
        immath(imagename=links, expr=expr, outfile=outfile)

    finally:
        for p in links:
            try:
                os.unlink(p)
            except Exception:
                pass
        try:
            os.rmdir(workdir)
        except Exception:
            pass


def collect_inputs_for_spw(base_concat, spw, prefer_pbcor=True, max_depth=6):
    """
    Recursively search under {base_concat}/Images/spw/** for CASA images that
    look like per-MS SPW products. Accept both .tt0 and plain .image, and
    prefer pbcor when requested.

    Returns a de-duplicated list of absolute paths.
    """
    root = os.path.join(base_concat, "Images", "spw")
    if not os.path.isdir(root):
        print(f"  [scan] Missing root: {root}")
        return []

    # Accept several SPW tokens in names/paths, e.g., spw16, spw_16, spw-16 (case-insensitive)
    spw_pat = re.compile(rf"(?i)\bspw[_\-]?{spw}\b")

    start_depth = root.rstrip(os.sep).count(os.sep)
    cands = []
    for cur, dirs, files in os.walk(root):
        depth = cur.rstrip(os.sep).count(os.sep) - start_depth
        if depth > max_depth:
            # prune deeper traversal
            dirs[:] = []
            continue

        # Consider any CASA image directory inside 'dirs'
        for d in list(dirs):
            if d.endswith((".image", ".image.tt0", ".image.pbcor", ".image.pbcor.tt0")):
                p = os.path.join(cur, d)
                # Require the SPW token to appear somewhere in the path
                if spw_pat.search(p):
                    cands.append(p)

    if not cands:
        print(f"  [scan] No image dirs mentioning SPW {spw} found under {root}")
        return []

    # Rank by preference: pbcor.tt0 (if prefer), then tt0, then pbcor (if prefer), then plain .image
    def rank(path):
        name = os.path.basename(path)
        r = 100
        if name.endswith(".image.pbcor.tt0") and prefer_pbcor:
            r = 1
        elif name.endswith(".image.tt0"):
            r = 2
        elif name.endswith(".image.pbcor") and prefer_pbcor:
            r = 3
        elif name.endswith(".image"):
            r = 4
        # small bias: prefer deeper per-MS paths over mosaic-level paths
        depth_bonus = -min(3, path.count(os.sep) - root.count(os.sep))
        return (r, depth_bonus, name)

    # One pick per parent directory (to avoid grabbing multiple versions from the same place)
    picks = {}
    for p in sorted(cands):
        parent = os.path.dirname(p)
        key = parent
        if key not in picks or rank(p) < rank(picks[key]):
            picks[key] = p

    imagenames = sorted(set(picks.values()))
    print(f"  [scan] SPW {spw}: picked {len(imagenames)} inputs")
    for p in imagenames[:8]:
        print("    -", p)
    if len(imagenames) > 8:
        print(f"    ... and {len(imagenames)-8} more")

    return imagenames


def average_spw(base_concat, mosaic_name, spw, prefer_pbcor=True, overwrite=True):
    print(f"\n=== SPW {spw} ===")

    # Create output directory at the mosaic level *upfront* so you can see it even if no inputs
    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    ensure_dir(out_dir)

    imgs = collect_inputs_for_spw(base_concat, spw, prefer_pbcor=prefer_pbcor, max_depth=MAX_SCAN_DEPTH)
    if not imgs:
        print(f"  No inputs found for SPW {spw}. Created (empty) out dir: {out_dir}")
        return

    print("  Inputs to average:")
    for p in imgs:
        print("   -", p)

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

    # --- Attempt 1: varnames ---
    try:
        try_immath_with_varnames(imgs, outfile)
        if os.path.isdir(outfile):
            print("  Wrote:", outfile)
        else:
            print("  immath reported success but outfile not found:", outfile)
        return
    except Exception as e:
        print("  [immath-varnames] failed:", e)

    # --- Attempt 2: symlinks (colon-free) ---
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
    print("Max scan depth       :", MAX_SCAN_DEPTH)

    for s in SPW_LIST:
        average_spw(
            base_concat=base_concat,
            mosaic_name=mosaic_name,
            spw=s,
            prefer_pbcor=PREFER_PBCOR_TT0,
            overwrite=OVERWRITE
        )

    print("\nAll done.")


# Run
if __name__ == "__main__":
    main()
