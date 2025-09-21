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

SPW_LIST = [3, 4, 5, 6, 8, 15, 16, 17]

# Preference: if True, prefer .pb.tt0 when both are available for an MS; if False, prefer .image.tt0
PREFER_PB_TT0 = False

OVERWRITE = True
USE_IMREGRID = True
SMOOTH_TO_COMMON = False
# COMMON_BEAM = dict(major='45arcsec', minor='45arcsec', pa='0deg')

# Debug toggles
VERBOSE = True
PRINT_IMAGE_INFO = True
LIMIT_INPUTS = None
DRYRUN = False
# =========================================================

# --------------------- LOGGING ---------------------------
try:
    from casatasks import casalog
except Exception:
    casalog = None

def log(msg, level='INFO'):
    try:
        print(msg, flush=True)
    except Exception:
        pass
    if casalog:
        try:
            casalog.post(str(msg), priority=level)
        except Exception:
            pass

def banner(msg):
    log("\n" + "="*80)
    log(msg)
    log("="*80 + "\n")
# --------------------------------------------------------

def safe(s: str) -> str:
    """Make a filename-safe token (remove colons)."""
    return s.replace(':', '_')

def ensure_dir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def build_mean_expr(n: int, token: str = "IM") -> str:
    """Return '(IM0+IM1+...)/n' or 'IM0' for n==1."""
    if n == 1:
        return f"{token}0"
    return f"({ ' + '.join([f'{token}{i}' for i in range(n)]) })/{float(n)}"

def list_dir(path, limit=40):
    try:
        ents = sorted(os.listdir(path))
        log(f"  [ls] {path} -> {len(ents)} entries")
        for e in ents[:limit]:
            log(f"     - {e}")
        if len(ents) > limit:
            log(f"     ... and {len(ents)-limit} more")
    except Exception as e:
        log(f"  [ls] {path} -> ERROR: {e}", "WARN")

def find_casa_images_in_dir(d: str):
    """
    Return CASA image *directories* inside d with endings we accept.
    Accepted endings (ONLY):
       - .image.tt0  (Stokes-I)
       - .pb.tt0     (primary beam)
    """
    endings = [".image.tt0", ".pb.tt0"]
    out = []
    if not os.path.isdir(d):
        if VERBOSE:
            log(f"  [scan] (missing dir) {d}")
        return out
    try:
        for name in os.listdir(d):
            if any(name.endswith(suf) for suf in endings):
                p = os.path.join(d, name)
                if os.path.isdir(p):
                    out.append(p)
    except Exception as e:
        log(f"  [scan] error listing {d}: {e}", "WARN")
    return out

def imhead_summary(img):
    """Return compact imhead info."""
    try:
        out = imhead(imagename=img, mode='summary')
        if not out:
            out = imhead(imagename=img, mode='list')
        return out or {}
    except Exception as e:
        log(f"  [imhead] failed for {img}: {e}", "WARN")
        return {}

def print_image_info(img):
    if not PRINT_IMAGE_INFO:
        return
    s = imhead_summary(img)
    if not s:
        log(f"  [info] (no summary) for {img}")
        return
    shape = s.get('shape') or s.get('dimensions')
    axisnames = s.get('axisnames') or s.get('axis names')
    cell = s.get('cdelt') or s.get('incr')
    rb = s.get('restoringbeam') or {}
    if isinstance(rb, dict) and 'major' in rb:
        beam_major = rb.get('major')
        beam_minor = rb.get('minor')
        beam_pa = rb.get('positionangle') or rb.get('pa')
    else:
        beam_major = beam_minor = beam_pa = '(per-plane or unknown)'
    log(f"  [info] {os.path.basename(img)}")
    log(f"         shape: {shape}")
    log(f"         axes : {axisnames}")
    log(f"         cell : {cell}")
    log(f"         beam : major={beam_major}  minor={beam_minor}  pa={beam_pa}")

def collect_inputs_for_spw(base_concat: str, spw: int, prefer_pb: bool = False):
    """
    Expected layout:
      {base_concat}/Images/spw/
        ├─ <MSNAME>_calibrated/
        │    └─ tclean/
        │        └─ spw{spw}/
        │             ├─ *.image.tt0 / *.pb.tt0   (CASA image directories)
        │             └─ (optional subfolders like run*/ containing images)
        └─ (repeat for each MS)
    """
    root = os.path.join(base_concat, "Images", "spw")
    log(f"  [scan] root = {root}")
    if not os.path.isdir(root):
        log(f"  [scan] Missing root: {root}", "WARN")
        return []

    if VERBOSE:
        list_dir(root)

    ms_dirs = sorted([d for d in glob.glob(os.path.join(root, "*_calibrated*")) if os.path.isdir(d)])
    log(f"  [scan] *_calibrated MS folders: {len(ms_dirs)}")
    for d in ms_dirs[:20]:
        log(f"    - {os.path.basename(d)}")
    if not ms_dirs:
        return []

    spw_dirname = f"spw{spw}"
    cands = []
    for msd in ms_dirs:
        tclean_spw_dir = os.path.join(msd, "tclean", spw_dirname)
        log(f"  [scan] check: {tclean_spw_dir}")
        imgs = find_casa_images_in_dir(tclean_spw_dir)

        # also check one level deeper (e.g., run*/ or date-stamped subdirs)
        if os.path.isdir(tclean_spw_dir):
            for run_dir in glob.glob(os.path.join(tclean_spw_dir, "*")):
                if os.path.isdir(run_dir):
                    log(f"  [scan] nested: {run_dir}")
                    imgs += find_casa_images_in_dir(run_dir)

        for p in imgs:
            log(f"      [hit] {p}")

        if imgs:
            cands.extend(imgs)

    if not cands:
        log(f"  [scan] No images found for SPW {spw} under any '*_calibrated/tclean/{spw_dirname}'")
        return []

    # ranking preference
    def rank(path):
        name = os.path.basename(path)
        if name.endswith(".pb.tt0") and prefer_pb:
            return (1, name)
        if name.endswith(".image.tt0") and not prefer_pb:
            return (1, name)
        # secondary choices
        if name.endswith(".image.tt0"):
            return (2, name)
        if name.endswith(".pb.tt0"):
            return (2, name)
        return (9, name)

    # one pick per MS
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
    log(f"  [scan] SPW {spw}: picked {len(imagenames)} inputs from {len(picks_by_ms)} MS folders")
    for p in imagenames:
        log(f"    - {p}")

    if LIMIT_INPUTS and len(imagenames) > LIMIT_INPUTS:
        log(f"  [scan] LIMIT_INPUTS={LIMIT_INPUTS} -> truncating inputs")
        imagenames = imagenames[:LIMIT_INPUTS]

    for p in imagenames:
        print_image_info(p)

    return imagenames

def average_spw(base_concat: str, mosaic_name: str, spw: int, prefer_pb: bool = False, overwrite: bool = True):
    log(f"\n--- SPW {spw} ---")

    # ======= OUTPUT DIRECTORY (per your request) =======
    # /concat/{mosaic_name}/Images/tclean/spw{SPW}/
    out_dir = os.path.join(base_concat, 'Images', 'tclean', f'spw{spw}')
    log(f"  [out] out_dir = {out_dir}")
    ensure_dir(out_dir)

    # quick write-permission test
    try:
        tf = os.path.join(out_dir, "_write_test.txt")
        with open(tf, "w") as f:
            f.write("ok\n")
        os.remove(tf)
        log("  [out] write test: OK")
    except Exception as e:
        log(f"  [out] write test: FAILED -> {e}", "SEVERE")

    imgs = collect_inputs_for_spw(base_concat, spw, prefer_pb=prefer_pb)
    log(f"  [avg] inputs found: {len(imgs)}")
    for p in imgs:
        log(f"   - {p}")
    if not imgs:
        log(f"  [stop] No inputs for SPW {spw}")
        return

    # Regrid all to first image (recommended)
    workdir_rg = os.path.join(out_dir, f"_tmp_rg_spw{spw}")
    rg_imgs = []
    try:
        if USE_IMREGRID:
            log(f"  [rg] imregrid enabled; template = imgs[0]")
            ensure_dir(workdir_rg)
            template = imgs[0]
            for i, src in enumerate(imgs):
                dst = os.path.join(workdir_rg, f"rg{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                if i == 0:
                    log(f"  [rg] link first image -> {dst}")
                    try:
                        os.symlink(src, dst)
                    except Exception:
                        log("  [rg] symlink failed; copying tree")
                        shutil.copytree(src, dst, symlinks=True)
                else:
                    log(f"  [rg] imregrid {src} -> {dst}")
                    if not DRYRUN:
                        try:
                            imregrid(imagename=src, template=template, output=dst, overwrite=True)
                        except Exception as e:
                            log(f"  [rg] imregrid FAILED: {e}", "SEVERE")
                            traceback.print_exc()
                            raise
                rg_imgs.append(dst)
        else:
            log("  [rg] imregrid disabled; using originals")
            rg_imgs = imgs[:]

        # Optional: smooth to common beam
        if SMOOTH_TO_COMMON:
            log(f"  [sm] Smoothing to common beam: {COMMON_BEAM}")
            sm_dir = os.path.join(out_dir, f"_tmp_sm_spw{spw}")
            ensure_dir(sm_dir)
            sm_imgs = []
            for i, src in enumerate(rg_imgs):
                dst = os.path.join(sm_dir, f"sm{i}.image")
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                log(f"  [sm] imsmooth {src} -> {dst}")
                if not DRYRUN:
                    imsmooth(imagename=src, outfile=dst, targetres=True,
                             major=COMMON_BEAM['major'], minor=COMMON_BEAM['minor'], pa=COMMON_BEAM['pa'])
                sm_imgs.append(dst)
            rg_imgs = sm_imgs

        has_pb = any(p.endswith(".pb.tt0") for p in imgs)
        suffix = "pb_tt0" if (prefer_pb and has_pb) else "tt0"
        out_name = f"{safe(mosaic_name)}_StokesI_spw{spw}_avg_{suffix}.image"
        outfile = os.path.join(out_dir, out_name)
        log(f"  [out] outfile = {outfile}")

        if os.path.exists(outfile):
            if overwrite:
                log("  [out] removing existing outfile (OVERWRITE=True)")
                if not DRYRUN:
                    shutil.rmtree(outfile, ignore_errors=True)
            else:
                log("  [out] exists and OVERWRITE=False -> skipping")
                return

        expr = build_mean_expr(len(rg_imgs))
        log(f"  [immath] expr: {expr}")
        log(f"  [immath] n_inputs = {len(rg_imgs)}")
        log(f"  [immath] inputs  = {rg_imgs}")

        if not DRYRUN:
            try:
                immath(imagename=rg_imgs, expr=expr, outfile=outfile)
            except Exception as e:
                log(f"  [immath] FAILED: {e}", "SEVERE")
                traceback.print_exc()
                raise

        if os.path.isdir(outfile):
            banner(f"✅ WROTE: {outfile}")
        else:
            log(f"  [immath] reported but outfile not found: {outfile}", "WARN")

    except Exception as e:
        log(f"  [ERROR] while averaging SPW {spw}: {e}", "SEVERE")
        traceback.print_exc()
    finally:
        # Clean tmp dirs (comment out if you want to inspect)
        if os.path.isdir(workdir_rg):
            try:
                for p in os.listdir(workdir_rg):
                    shutil.rmtree(os.path.join(workdir_rg, p), ignore_errors=True)
                os.rmdir(workdir_rg)
                log(f"  [cleanup] removed {workdir_rg}")
            except Exception as e:
                log(f"  [cleanup] could not remove {workdir_rg} -> {e}", "WARN")
        if SMOOTH_TO_COMMON:
            sm_dir = os.path.join(out_dir, f"_tmp_sm_spw{spw}")
            if os.path.isdir(sm_dir):
                try:
                    for p in os.listdir(sm_dir):
                        shutil.rmtree(os.path.join(sm_dir, p), ignore_errors=True)
                    os.rmdir(sm_dir)
                    log(f"  [cleanup] removed {sm_dir}")
                except Exception as e:
                    log(f"  [cleanup] could not remove {sm_dir} -> {e}", "WARN")

def main():
    base_concat = os.path.join(BASE_CONCAT_ROOT, mosaic_name)
    banner("START average_spw_images")
    log(f"mosaic_name       : {mosaic_name}")
    log(f"base_concat       : {base_concat}")
    log(f"SPWs              : {SPW_LIST}")
    log(f"PREFER_PB_TT0     : {PREFER_PB_TT0}")
    log(f"OVERWRITE         : {OVERWRITE}")
    log(f"USE_IMREGRID      : {USE_IMREGRID}")
    log(f"SMOOTH_TO_COMMON  : {SMOOTH_TO_COMMON}")
    log(f"PRINT_IMAGE_INFO  : {PRINT_IMAGE_INFO}")
    log(f"LIMIT_INPUTS      : {LIMIT_INPUTS}")
    log(f"DRYRUN            : {DRYRUN}")

    if not os.path.isdir(base_concat):
        log(f"[FATAL] Base concat path not found: {base_concat}", "SEVERE")
        raise RuntimeError(f"Base concat path not found: {base_concat}")

    if VERBOSE:
        list_dir(base_concat)
        list_dir(os.path.join(base_concat, "Images"))
        list_dir(os.path.join(base_concat, "Images", "spw"))
        # also ensure the top-level Images/tclean exists
        ensure_dir(os.path.join(base_concat, "Images", "tclean"))

    for s in SPW_LIST:
        average_spw(
            base_concat=base_concat,
            mosaic_name=mosaic_name,
            spw=s,
            prefer_pb=PREFER_PB_TT0,
            overwrite=OVERWRITE
        )

    banner("DONE average_spw_images")

# Ensure it actually runs when you %run the file.
if __name__ == "__main__":
    main()
