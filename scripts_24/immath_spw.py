import os
import glob
import shutil

# ========= USER SETTINGS =========
mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'


base_concat = f'/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}'

# SPWs you want to average (match what you imaged)
spw_list = [3, 4, 5, 6, 8, 15, 16, 17]

# Part of the imagename you used in tclean (before CASA suffixes)
# Example from your script:
#   imagename = f"{ms_name}_StokesI_spw{s}-2.5arcsec-nit{nit}-awproject"
# We'll match robustly with wildcards in case nit/threshold changes (as long as "-awproject" is present)
imagename_contains = '_StokesI_spw{spw}-'
imagename_trailer   = '-awproject'

# Prefer pbcor if available?
prefer_pbcor = True

# Overwrite existing averaged images?
overwrite = True
# =================================

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def find_ms_level_spw_dirs(base_concat, spw):
    """
    Return list of directories like:
      .../Images/spw/{ms_name}/tclean/spw{spw}
    """
    root = os.path.join(base_concat, 'Images', 'spw')
    if not os.path.isdir(root):
        return []
    ms_dirs = []
    for ms_name in sorted(os.listdir(root)):
        ms_root = os.path.join(root, ms_name, 'tclean', f'spw{spw}')
        if os.path.isdir(ms_root):
            ms_dirs.append(ms_root)
    return ms_dirs

def collect_images_in_dir(d, spw):
    """
    In a given tclean/spw{spw} dir, collect candidate images.
    Prefer *.image.pbcor if available (when prefer_pbcor=True), else *.image.
    We try both the exact pattern you used and a wildcard fallback.
    """
    # exact-ish pattern
    pbcor_candidates = glob.glob(os.path.join(d, f"*{imagename_contains.format(spw=spw)}*{imagename_trailer}.image.pbcor"))
    image_candidates = glob.glob(os.path.join(d, f"*{imagename_contains.format(spw=spw)}*{imagename_trailer}.image"))

    # fallback (any pbcor/image in case naming varied slightly)
    if prefer_pbcor and not pbcor_candidates:
        pbcor_candidates = glob.glob(os.path.join(d, "*.image.pbcor"))
    if not image_candidates:
        image_candidates = glob.glob(os.path.join(d, "*.image"))

    if prefer_pbcor and pbcor_candidates:
        return sorted(pbcor_candidates)
    elif image_candidates:
        # Filter out .image.pbcor if both patterns matched
        image_only = [p for p in image_candidates if not p.endswith(".image.pbcor")]
        return sorted(image_only)
    else:
        return []

def build_average_expr(n):
    if n == 1:
        return 'IM0'
    # (IM0 + IM1 + ... + IM{n-1})/n
    s = " + ".join([f"IM{i}" for i in range(n)])
    return f"({s})/{float(n)}"

def average_spw(base_concat, mosaic_name, spw):
    ms_spw_dirs = find_ms_level_spw_dirs(base_concat, spw)
    imagenames = []
    for d in ms_spw_dirs:
        imgs = collect_images_in_dir(d, spw)
        if imgs:
            # choose the principal cube if both .image and .image.tt0 exist, prefer the multi-term full .image
            # (If you want tt0 specifically, filter here accordingly.)
            imagenames.append(imgs[0])

    # De-duplicate in case the same path was found twice
    imagenames = sorted(list(dict.fromkeys(imagenames)))

    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    ensure_dir(out_dir)

    # Suffix shows whether we averaged pbcor or not
    suffix = '_pbcor' if (prefer_pbcor and any(p.endswith('.image.pbcor') for p in imagenames)) else ''
    outfile = os.path.join(out_dir, f"{mosaic_name}_StokesI_spw{spw}_avg{suffix}.image")

    print(f"\n=== SPW {spw} ===")
    if not imagenames:
        print(f"No input images found for SPW {spw}. Skipping.")
        return

    print("Input images:")
    for p in imagenames:
        print("  -", p)
    print("Output:", outfile)

    if os.path.exists(outfile):
        if overwrite:
            shutil.rmtree(outfile, ignore_errors=True)
        else:
            print("Output exists and overwrite=False. Skipping.")
            return

    expr = build_average_expr(len(imagenames))
    print("Expression:", expr)

    # Run CASA immath
    immath(imagename=imagenames, expr=expr, outfile=outfile)
    print(f"Averaged {len(imagenames)} image(s) into:\n  {outfile}")

# ---- Run for all requested SPWs ----
for s in spw_list:
    average_spw(base_concat, mosaic_name, s)

print("\nAll done.")
