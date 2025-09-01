# average_spw_images.py  (run inside CASA)
import os
import glob
import shutil
import traceback

# ========= USER SETTINGS =========
mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
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
    Return list of directories like:
      {base_concat}/Images/spw/{ms_name}/tclean/spw{spw}
    """
    root = os.path.join(base_concat, 'Images', 'spw')
    if not os.path.isdir(root):
        return []
    out = []
    for ms_name in sorted(os.listdir(root)):
        d = os.path.join(root, ms_name, 'tclean', f'spw{spw}')
        if os.path.isdir(d):
            out.append(d)
    return out


def collect_inputs_for_spw(base_concat, spw, prefer_pbcor=True):
    """
    For a given SPW, collect one input image per MS directory.
    Priority:
      1) *_*.image.pbcor.tt0 (if prefer_pbcor=True)
      2) *_*.image.tt0
    Fallbacks:
      any *.image.pbcor.tt0, else any *.image.tt0
    Returns a sorted de-duplicated list of absolute paths (no trailing slashes).
    """
    imagenames = []
    for d in find_ms_level_spw_dirs(base_concat, spw):
        # First try matching your naming pattern explicitly
        pat_pbcor = os.path.join(d, f"*_StokesI_spw{spw}-*awproject.image.pbcor.tt0")
        pat_tt0   = os.path.join(d, f"*_StokesI_spw{spw}-*awproject.image.tt0")

        pb_list = glob.glob(pat_pbcor)
        tt_list = glob.glob(pat_tt0)

        # Fallbacks (any tt0 in the folder)
        if prefer_pbcor and not pb_list:
            pb_list = glob.glob(os.path.join(d, "*.image.pbcor.tt0"))
        if not tt_list:
            tt_list = glob.glob(os.path.join(d, "*.image.tt0"))

        pick = None
        if prefer_pbcor and pb_list:
            pick = sorted(pb_list)[0]
        elif tt_list:
            # avoid accidentally picking a pbcor file here
            cand = [p for p in tt_list if not p.endswith(".image.pbcor.tt0")]
            pick = sorted(cand)[0] if cand else sorted(tt_list)[0]

        if pick:
            imagenames.append(pick.rstrip('/'))

    # De-dup + sort
    imagenames = sorted(list(dict.fromkeys(imagenames)))
    return imagenames


def build_mean_expr(n, token="IM"):
    """Return '(IM0+IM1+...)/n' or 'IM0' for n==1."""
    if n == 1:
        return f"{token}0"
    return f"({ ' + '.join([f'{token}{i}' for i in range(n)]) })/{float(n)}"


def try_immath_with_varnames(imgs, outfile):
    """
    Attempt immath using varnames so raw file paths don't appear
    in the parsed expression.
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
        # Make deterministic colon-free link names
        for i, src in enumerate(imgs):
            # choose suffix by original type
            suffix = ".image.pbcor.tt0" if src.endswith(".image.pbcor.tt0") else ".image.tt0"
            dst = os.path.join(workdir, f"im{i}{suffix}")
            if os.path.islink(dst) or os.path.exists(dst):
                # remove any stale link/dir
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
        # Best-effort cleanup of symlinks
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

    # Output directory: .../Images/spw/tclean/spw{spw}/
    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    ensure_dir(out_dir)

    suffix = "_pbcor_tt0" if prefer_pbcor and any(p.endswith(".image.pbcor.tt0") for p in imgs) else "_tt0"
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
        print("  Wrote:", outfile)
        return
    except Exception as e:
        msg = f"{e}"
        print("  [immath-varnames] failed:", msg)
        # Fall through to symlink method

    # --- Attempt 2: symlinks (colon-free) ---
    workdir = os.path.join(out_dir, f"_tmp_symlinks_spw{spw}")
    try:
        try_immath_with_symlinks(imgs, outfile, workdir)
        print("  Wrote:", outfile)
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

# Run
if __name__ == "__main__":
    main()
