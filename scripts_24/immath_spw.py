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

BASE_CONCAT_ROOT = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat'

SPW_LIST = [15]  # start with one SPW for debugging
PREFER_PBCOR_TT0 = False
OVERWRITE = True
USE_IMREGRID = True
SMOOTH_TO_COMMON = False
# COMMON_BEAM = dict(major='45arcsec', minor='45arcsec', pa='0deg')

# ---- Debug toggles ----
VERBOSE = True
PRINT_IMAGE_INFO = True   # print imhead summary for each input
LIMIT_INPUTS = 3          # None or small int to limit #images averaged
DRYRUN = False            # True => do not write outputs; only log what would happen
# =======================


def banner(msg):
    print("\n" + "="*80)
    print(msg)
    print("="*80 + "\n")


def safe(s: str) -> str:
    return s.replace(':', '_')


def ensure_dir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def build_mean_expr(n: int, token: str = "IM") -> str:
    if n == 1:
        return f"{token}0"
    return f"({ ' + '.join([f'{token}{i}' for i in range(n)]) })/{float(n)}"


def list_dir(path):
    try:
        ents = sorted(os.listdir(path))
        print(f"  [ls] {path}  -> {len(ents)} entries")
        for e in ents[:20]:
            print("     -", e)
        if len(ents) > 20:
            print(f"     ... and {len(ents)-20} more")
    except Exception as e:
        print(f"  [ls] {path}  -> ERROR:", e)


def find_casa_images_in_dir(d: str):
    endings = [".image.pbcor.tt0", ".image.tt0", ".image.pbcor", ".image"]
    results = []
    if not os.path.isdir(d):
        if VERBOSE:
            print(f"  [scan] (missing dir) {d}")
        return results
    try:
        for name in os.listdir(d):
            if any(name.endswith(suf) for suf in endings):
                p = os.path.join(d, name)
                if os.path.isdir(p):
                    results.append(p)
    except Exception as e:
        print("  [scan] error listing", d, ":", e)
    return results


def imhead_summary(img):
    """Return a tiny summary dict robustly; print on failure."""
    try:
        # CASA 6: summary mode is most compact; fall back to list
        out = imhead(imagename=img, mode='summary')
        if not out:
            out = imhead(imagename=img, mode='list')
        return out or {}
    except Exception as e:
        print("  [imhead] failed for", img, ":", e)
        return {}


def print_image_info(img):
    s = imhead_summary(img)
    if not s:
        print("  [info] (no summary) for", img)
        return
    # Try to extract common bits, being defensive about keys
    shape = s.get('shape') or s.get('dimensions')
    axisnames = s.get('axisnames') or s.get('axis names')
    cell = s.get('cdelt') or s.get('incr')
    rb = s.get('restoringbeam') or {}
    if isinstance(rb, dict) and 'major' in rb:
        beam_major = rb.get('major')
        beam_minor = rb.get('minor')
        beam_pa = rb.get('positionangle') or rb.get('pa')
    else:
        # per-plane beams? print top-level key only
        beam_major = beam_minor = beam_pa = '(per-plane or unknown)'
    print(f"  [info] {os.path.basename(img)}")
    print(f"         shape: {shape}")
    print(f"         axes : {axisnames}")
    print(f"         cell : {cell}")
    print(f"         beam : major={beam_major}  minor={beam_minor}  pa={beam_pa}")


def collect_inputs_for_spw(base_concat: str, spw: int, prefer_pbcor: bool = True):
    root = os.path.join(base_concat, "Images", "spw")
    print(f"  [scan] root = {root}")
    if not os.path.isdir(root):
        print(f"  [scan] Missing root: {root}")
        return []

    # show immediate listing to confirm structure
    list_dir(root)

    ms_dirs = sorted([d for d in glob.glob(os.path.join(root, "*_calibrated*")) if os.path.isdir(d)])
    print(f"  [scan] *_calibrated MS folders found: {len(ms_dirs)}")
    for d in ms_dirs[:10]:
        print("    -", os.path.basename(d))
    if not ms_dirs:
        return []

    spw_dirname = f"spw{spw}"
    cands = []
    for msd in ms_dirs:
        tclean_spw_dir = os.path.join(msd, "tclean", spw_dirname)
        print(f"  [scan] checking: {tclean_spw_dir}")
        imgs = find_casa_images_in_dir(tclean_spw_dir)

        # also check one level deeper (e.g., run*/ or date-stamped subdirs)
        if os.path.isdir(tclean_spw_dir):
            for run_dir in glob.glob(os.path.join(tclean_spw_dir, "*")):
                if os.path.isdir(run_dir):
                    print(f"  [scan] checking nested: {run_dir}")
                    imgs += find_casa_images_in_dir(run_dir)

        if imgs:
            for p in imgs:
                print("      [hit] ", p)
            cands.extend(imgs)

    if not cands:
        print(f"  [scan] No images found for SPW {spw} under any '*_calibrated/tclean/{spw_dirname}'")
        return []

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

    picks_by_ms = {}
    for p in sorted(cands):
        parts = p.split(os.sep)
        ms_key = None
        for seg in parts:
            if seg.endswith("_calibrated") or "_calibrated" in seg:
                ms_key = seg
                break
        if ms_key is None:
            ms_key = os.path.basename(os.path.dirname(os.path.dirname(p)))
        if (ms_key not in picks_by_ms) or (rank(p) < rank(picks_by_ms[ms_key])):
            picks_by_ms[ms_key] = p

    imagenames = sorted(set(picks_by_ms.values()))
    print(f"  [scan] SPW {spw}: picked {len(imagenames)} inputs from {len(picks_by_ms)} MS folders")
    for p in imagenames:
        print("    -", p)

    if LIMIT_INPUTS and len(imagenames) > LIMIT_INPUTS:
        print(f"  [scan] LIMIT_INPUTS={LIMIT_INPUTS} -> truncating inputs")
        imagenames = imagenames[:LIMIT_INPUTS]

    if PRINT_IMAGE_INFO:
        for p in imagenames:
            print_image_info(p)

    return imagenames


def average_spw(base_concat: str, mosaic_name: str, spw: int, prefer_pbcor: bool = True, overwrite: bool = True):
    print(f"\n--- SPW {spw} ---")

    out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
    print(f"  [out] out_dir = {out_dir}")
    ensure_dir(out_dir)

    # quick write-permission test
    try:
        test_file = os.path.join(out_dir, "_write_test.txt")
        with open(test_file, "w") as f:
            f.write("ok\n")
        os.remove(test_file)
        print("  [out] write test: OK")
    except Exception as e:
        print("  [out] write test: FAILED ->", e)

    imgs = collect_inputs_for_spw(base_concat, spw, prefer_pbcor=prefer_pbcor)
    if not imgs:
        print(f"  [stop] No inputs found for SPW {spw}.")
        return

    print("  [avg] Inputs ({}):".format(len(imgs)))
    for p in imgs:
        print("   -", p)

    workdir_rg = os.path.join(out_dir, f"_tmp_rg_spw{spw}")
    rg_imgs = []
    try:
        if USE_IMREGRID:
            print(f"  [rg] Using imregrid -> template = imgs[0]")
            ensure_dir(workdir_rg)
            template = imgs[0]
            for i, src in enumerate(imgs):
                dst = os.path.join(workdir_rg, f"rg{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                if i == 0:
                    print(f"  [rg] link first image -> {dst}")
                    try:
                        os.symlink(src, dst)
                    except Exception:
                        print("  [rg] symlink failed; copying tree")
                        shutil.copytree(src, dst, symlinks=True)
                else:
                    print(f"  [rg] imregrid {src} -> {dst}")
                    try:
                        if not DRYRUN:
                            imregrid(imagename=src, template=template, output=dst, overwrite=True)
                    except Exception as e:
                        print("  [rg] imregrid FAILED:", e)
                        traceback.print_exc()
                        raise
                rg_imgs.append(dst)
        else:
            print("  [rg] Skipping imregrid; using originals")
            rg_imgs = imgs[:]

        if SMOOTH_TO_COMMON:
            print("  [sm] Smoothing to common beam:", COMMON_BEAM)
            sm_dir = os.path.join(out_dir, f"_tmp_sm_spw{spw}")
            ensure_dir(sm_dir)
            sm_imgs = []
            for i, src in enumerate(rg_imgs):
                dst = os.path.join(sm_dir, f"sm{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                print(f"  [sm] imsmooth {src} -> {dst}")
                if not DRYRUN:
                    imsmooth(imagename=src, outfile=dst, targetres=True,
                             major=COMMON_BEAM['major'], minor=COMMON_BEAM['minor'], pa=COMMON_BEAM['pa'])
                sm_imgs.append(dst)
            rg_imgs = sm_imgs

        has_pb = any(p.endswith(".image.pbcor.tt0") or p.endswith(".image.pbcor") for p in imgs)
        suffix = "_pbcor_tt0" if (prefer_pbcor and has_pb) else "_tt0"
        out_name = f"{safe(mosaic_name)}_StokesI_spw{spw}_avg{suffix}.image"
        outfile = os.path.join(out_dir, out_name)
        print(f"  [out] outfile = {outfile}")

        if os.path.exists(outfile):
            if overwrite:
                print("  [out] removing existing outfile (OVERWRITE=True)")
                if not DRYRUN:
                    shutil.rmtree(outfile, ignore_errors=True)
            else:
                print("  [out] exists and OVERWRITE=False -> skipping")
                return

        expr = build_mean_expr(len(rg_imgs))
        print("  [immath] expr:", expr)
        print("  [immath] inputs:", rg_imgs)

        if not DRYRUN:
            try:
                immath(imagename=rg_imgs, expr=expr, outfile=outfile)
            except Exception as e:
                print("  [immath] FAILED:", e)
                traceback.print_exc()
                raise

        if os.path.isdir(outfile):
            banner(f"✅ WROTE: {outfile}")
        else:
            print("  [immath] reported but outfile not found:", outfile)

    except Exception as e:
        print("  [ERROR] while averaging SPW", spw, ":", e)
        traceback.print_exc()
    finally:
        # clean tmp dirs (comment these out if you want to inspect tmp results)
        if os.path.isdir(workdir_rg):
            try:
                for p in os.listdir(workdir_rg):
                    q = os.path.join(workdir_rg, p)
                    shutil.rmtree(q, ignore_errors=True)
                os.rmdir(workdir_rg)
                print("  [cleanup] removed", workdir_rg)
            except Exception as e:
                print("  [cleanup] could not remove", workdir_rg, "->", e)
        if SMOOTH_TO_COMMON:
            sm_dir = os.path.join(out_dir, f"_tmp_sm_spw{spw}")
            if os.path.isdir(sm_dir):
                try:
                    for p in os.listdir(sm_dir):
                        q = os.path.join(sm_dir, p)
                        shutil.rmtree(q, ignore_errors=True)
                    os.rmdir(sm_dir)
                    print("  [cleanup] removed", sm_dir)
                except Exception as e:
                    print("  [cleanup] could not remove", sm_dir, "->", e)


def main():
    base_concat = os.path.join(BASE_CONCAT_ROOT, mosaic_name)
    banner("START average_spw_images_debug")
    print("Phase center (mosaic):", mosaic_name)
    print("Base concat path     :", base_concat)
    print("SPWs                 :", SPW_LIST)
    print("Prefer pbcor tt0     :", PREFER_PBCOR_TT0)
    print("Overwrite outputs    :", OVERWRITE)
    print("Use imregrid         :", USE_IMREGRID)
    print("Smooth to common     :", SMOOTH_TO_COMMON)
    print("Verbose              :", VERBOSE)
    print("Print image info     :", PRINT_IMAGE_INFO)
    print("Limit inputs         :", LIMIT_INPUTS)
    print("Dry-run              :", DRYRUN)

    if not os.path.isdir(base_concat):
        raise RuntimeError(f"Base concat path not found: {base_concat}")

    # top-level listing to confirm tree
    list_dir(base_concat)
    list_dir(os.path.join(base_concat, "Images"))
    list_dir(os.path.join(base_concat, "Images", "spw"))

    for s in SPW_LIST:
        average_spw(
            base_concat=base_concat,
            mosaic_name=mosaic_name,
            spw=s,
            prefer_pbcor=PBCOR_TT0 if 'PBCOR_TT0' in globals() else PREFER_PBCOR_TT0,
            overwrite=OVERWRITE
        )

    banner("DONE")


# Run
if __name__ == "__main__":
    main()
