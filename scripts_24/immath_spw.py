# average_spw_images.py  (run inside CASA)
import os
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
    """Return a filename-safe token (remove colons for file basenames)."""
    return s.replace(':', '_')


def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def find_ms_level_spw_dirs(base_concat, spw):
    """
    Return a list of directories that might contain per-MS SPW images.
    Tries several common layouts:

      A) {base}/Images/spw/{MS}/tclean/spw{spw}
      B) {base}/Images/spw/{MS}/spw{spw}/tclean
      C) {base}/Images/spw/{MS}/spw{spw}
      D) {base}/Images/spw/tclean/spw{spw}     (mosaic-level fallback)

    Only existing directories are returned.
    """
    out = []
    root = os.path.join(base_concat, 'Images', 'spw')
    if not os.path.isdir(root):
        return out

    # Per-MS patterns
    for ms_name in sorted(os.listdir(root)):
        ms_dir = os.path.join(root, ms_name)
        if not os.path.isdir(ms_dir):
            continue

        cand = [
            os.path.join(ms_dir, 'tclean', f'spw{spw}'),
            os.path.join(ms_dir, f'spw{spw}', 'tclean'),
            os.path.join(ms_dir, f'spw{spw}'),
        ]
        for d in cand:
            if os.path.isdir(d):
                out.append(d)

    # Mosaic-level fallback
    mosaic_cand = os.path.join(root, 'tclean', f'spw{spw}')
    if os.path.isdir(mosaic_cand):
        out.append(mosaic_cand)

    # De-dup + sort
    out = sorted(list(dict.fromkeys(out)))
    return out


def _pick_one_from_dir(d, prefer_pbcor=True):
    """
    Select a single best candidate image from directory d using this priority:
      1) any *.image.pbcor.tt0 (if prefer_pbcor)
      2) any *.image.tt0
      3) any *.image.pbcor (if prefer_pbcor)
      4) any *.image
    Returns absolute path or None.
    """
    globs = []
    if prefer_pbcor:
        globs += [os.path.join(d, "*.image.pbcor.tt0")]
    globs += [os.path.join(d, "*.image.tt0")]
    if prefer_pbcor:
        globs += [os.path.join(d, "*.image.pbcor")]
    globs += [os.path.join(d, "*.image")]

    for g in globs:
        matches = [p for p in glob.glob(g) if os.path.isdir(p)]
        if matches:
            return sorted(matches)[0]
    return None


def collect_inputs_for_spw(base_concat, spw, prefer_pbcor=True):
    """
    For a given SPW, collect one input image per MS/SPW directory.
    Uses several directory layouts and a relaxed filename policy.
    Returns a sorted, de-duplicated list of absolute paths.
    """
    imagenames = []
    dirs = find_ms_level_spw_dirs(base_concat, spw)

    if not dirs:
        print(f"  [scan] No candidate SPW directories found for spw{spw}.")
        return []

    for d in dirs:
        pick = _pick_one_from_dir(d, prefer_pbcor=prefer_pbcor)
        if pick:
            imagenames.append(pick.rstrip('/'))
        else:
            print(f"  [scan] No matching images in: {d}")

    imagenames = sorted(list(dict.fromkeys(imagenames)))
    return imagenames


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


def average_spw(base_concat, mosaic_name, spw, prefer_pbcor=True, overwrite=True):
    print(f"\n=== SPW {spw} ===")
    imgs = collect_inputs_for_spw(base_concat, spw, prefer_pbcor=prefer_pbcor)

    if not imgs:
        print(f"  No inputs found for SPW {spw}. Skipping.")
        return

    print("  Inputs:")
    for p in imgs:
        print("   -", p)

    # Output directory: mosaic-level .../Images/spw/tclean/spw{spw}/
    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    ensure_dir(out_dir)

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

    for s in SPW_LIST:
        average_spw(
            base_concat=base_concat,
            mosaic_name=mosaic_name,
            spw=s,
            prefer_pbcor=PBCOR_TT0 if 'PBCOR_TT0' in globals() else PREFER_PBCOR_TT0,  # safety
            overwrite=OVERWRITE
        )

    print("\nAll done.")


# Run
if __name__ == "__main__":
    main()
