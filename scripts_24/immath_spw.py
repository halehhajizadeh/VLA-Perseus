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

# average_spw_images.py  (run inside CASA)


# Root that contains the "concat/{mosaic_name}" tree
BASE_CONCAT_ROOT = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat'

# SPWs to average
SPW_LIST = [3, 4, 5, 6, 8, 15, 16, 17]

# Prefer pb-corrected tt0 inputs? If True, use *.image.pbcor.tt0 when available
PREFER_PBCOR_TT0 = False

# Overwrite existing averaged images?
OVERWRITE = True

# Regrid all inputs to a common grid (recommended to avoid immath shape/coords errors)
USE_IMREGRID = True

# Smooth to a common beam (disabled by default; enable only if beams differ and you know the target beam)
SMOOTH_TO_COMMON = False
# COMMON_BEAM = dict(major='45arcsec', minor='45arcsec', pa='0deg')  # example
# =================================


def safe(s: str) -> str:
    """Return a filename-safe token (remove colons for file basenames)."""
    return s.replace(':', '_')


def ensure_dir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def build_mean_expr(n: int, token: str = "IM") -> str:
    """Return '(IM0+IM1+...)/n' or 'IM0' for n==1."""
    if n == 1:
        return f"{token}0"
    return f"({ ' + '.join([f'{token}{i}' for i in range(n)]) })/{float(n)}"


def find_casa_images_in_dir(d: str):
    """
    Return CASA image *directories* inside d with endings we accept.
    """
    endings = [".image.pbcor.tt0", ".image.tt0", ".image.pbcor", ".image"]
    results = []
    if not os.path.isdir(d):
        return results
    try:
        for name in os.listdir(d):
            if any(name.endswith(suf) for suf in endings):
                p = os.path.join(d, name)
                if os.path.isdir(p):
                    results.append(p)
    except FileNotFoundError:
        pass
    return results


def collect_inputs_for_spw(base_concat: str, spw: int, prefer_pbcor: bool = True):
    """
    Expected layout:
      {base_concat}/Images/spw/
        ├─ <MSNAME>_calibrated/
        │    └─ tclean/
        │        └─ spw{spw}/
        │             ├─ <...>.image.tt0 / .image.pbcor.tt0 / .image.pbcor / .image
        │             └─ (optional subfolders like run*/ containing images)
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

    spw_dirname = f"spw{spw}"
    cands = []
    for msd in ms_dirs:
        tclean_spw_dir = os.path.join(msd, "tclean", spw_dirname)
        imgs = find_casa_images_in_dir(tclean_spw_dir)

        # also accept nested per-run subdirs like .../tclean/spw{spw}/runX/<images>
        if os.path.isdir(tclean_spw_dir):
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
        # ms_key is the *_calibrated folder name
        parts = p.split(os.sep)
        ms_key = None
        for seg in parts:
            if seg.endswith("_calibrated") or "_calibrated" in seg:
                ms_key = seg
                break
        if ms_key is None:
            ms_key = os.path.basename(os.path.dirname(os.path.dirname(p)))  # fallback to parent of 'spw{N}'
        if (ms_key not in picks_by_ms) or (rank(p) < rank(picks_by_ms[ms_key])):
            picks_by_ms[ms_key] = p

    imagenames = sorted(set(picks_by_ms.values()))
    print(f"  [scan] SPW {spw}: picked {len(imagenames)} inputs from {len(picks_by_ms)} MS folders")
    for p in imagenames[:12]:
        print("    -", p)
    if len(imagenames) > 12:
        print(f"    ... and {len(imagenames)-12} more")

    return imagenames


def average_spw(base_concat: str, mosaic_name: str, spw: int, prefer_pbcor: bool = True, overwrite: bool = True):
    print(f"\n=== SPW {spw} ===")

    # Output: concat/{mosaic}/Images/spw/tclean/spw{spw}/<mosaic_safe>_StokesI_spw{spw}_avg_*.image
    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    ensure_dir(out_dir)

    imgs = collect_inputs_for_spw(base_concat, spw, prefer_pbcor=prefer_pbcor)
    if not imgs:
        print(f"  No inputs found for SPW {spw}. Created (empty) out dir: {out_dir}")
        return

    print("  Inputs to average ({}):".format(len(imgs)))
    for p in imgs:
        print("   -", p)

    # optionally regrid all to the first image
    workdir_rg = os.path.join(out_dir, f"_tmp_rg_spw{spw}")
    rg_imgs = []
    try:
        if USE_IMREGRID:
            ensure_dir(workdir_rg)
            template = imgs[0]
            for i, src in enumerate(imgs):
                dst = os.path.join(workdir_rg, f"rg{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                if i == 0:
                    # link/copy first image as-is to avoid tiny resample drift
                    try:
                        os.symlink(src, dst)
                    except Exception:
                        # if symlink across filesystems not allowed, copy tree
                        shutil.copytree(src, dst, symlinks=True)
                else:
                    imregrid(imagename=src, template=template, output=dst, overwrite=True)
                rg_imgs.append(dst)
        else:
            rg_imgs = imgs[:]

        # (optional) smooth to a common beam here if needed
        if SMOOTH_TO_COMMON:
            sm_dir = os.path.join(out_dir, f"_tmp_sm_spw{spw}")
            ensure_dir(sm_dir)
            sm_imgs = []
            for i, src in enumerate(rg_imgs):
                dst = os.path.join(sm_dir, f"sm{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                imsmooth(imagename=src, outfile=dst, targetres=True,
                         major=COMMON_BEAM['major'], minor=COMMON_BEAM['minor'], pa=COMMON_BEAM['pa'])
                sm_imgs.append(dst)
            rg_imgs = sm_imgs

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

        # Use immath with positional list (IM0, IM1, ...)
        expr = build_mean_expr(len(rg_imgs))
        print("  [immath] expr:", expr)
        immath(imagename=rg_imgs, expr=expr, outfile=outfile)

        if os.path.isdir(outfile):
            print("\n✅ Wrote:", outfile, "\n")
        else:
            print("  immath reported success but outfile not found:", outfile)

    except Exception as e:
        print("  ERROR while averaging SPW", spw, ":", e)
        traceback.print_exc()
    finally:
        # clean tmp regrids/smoothed
        if os.path.isdir(workdir_rg):
            for p in os.listdir(workdir_rg):
                q = os.path.join(workdir_rg, p)
                try:
                    shutil.rmtree(q, ignore_errors=True)
                except Exception:
                    pass
            try:
                os.rmdir(workdir_rg)
            except Exception:
                pass
        if SMOOTH_TO_COMMON:
            sm_dir = os.path.join(out_dir, f"_tmp_sm_spw{spw}")
            if os.path.isdir(sm_dir):
                for p in os.listdir(sm_dir):
                    q = os.path.join(sm_dir, p)
                    try:
                        shutil.rmtree(q, ignore_errors=True)
                    except Exception:
                        pass
                try:
                    os.rmdir(sm_dir)
                except Exception:
                    pass


def main():
    base_concat = os.path.join(BASE_CONCAT_ROOT, mosaic_name)
    if not os.path.isdir(base_concat):
        raise RuntimeError(f"Base concat path not found: {base_concat}")

    print("Phase center (mosaic):", mosaic_name)
    print("Base concat path     :", base_concat)
    print("SPWs                 :", SPW_LIST)
    print("Prefer pbcor tt0     :", PREFER_PBCOR_TT0)
    print("Overwrite outputs    :", OVERWRITE)
    print("Use imregrid         :", USE_IMREGRID)
    print("Smooth to common     :", SMOOTH_TO_COMMON)

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
