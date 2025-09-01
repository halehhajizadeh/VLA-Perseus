import os
from glob import glob

# =========================
# User params (edit me)
# =========================
mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'



spw_list    = [3,4,5,6,8,15,16,17]
nit         = 5000                            # must match imagename you used
root = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data'

# This is where your per-MS outputs live from your run above:
#   {root}/concat/{mosaic_name}/Images/spw/{ms_name}/tclean/spw{spw}/<prefix>.image|.pb|.pbcor
per_ms_root = f'{root}/concat/{mosaic_name}/Images/spw'

# Output directory for the combined (per-SPW) mosaics
out_root = f'{root}/concat/{mosaic_name}/Images/spw_mosaics'
os.makedirs(out_root, exist_ok=True)

def build_prefix(ms_name, s):
    # Must mirror your tclean 'imagename' exactly:
    return f"{ms_name}_StokesI_spw{s}-2.5arcsec-nit{nit}-awproject"

def combine_one_spw(s, do_simple_mean_pbcor=True):
    # Find all MS subdirs that contain this SPW
    ms_dirs = sorted(glob(os.path.join(per_ms_root, '*', 'tclean', f'spw{s}')))

    if not ms_dirs:
        print(f"[SPW{s}] No inputs found.")
        return

    # Collect matching .image (uncorrected) and .pb files for PB-weighted mosaic
    image_list = []
    pb_list    = []

    for spw_dir in ms_dirs:
        ms_name = spw_dir.split(os.sep)[-3]  # .../Images/spw/{ms_name}/tclean/spw{s}
        prefix  = build_prefix(ms_name, s)
        im_path = os.path.join(spw_dir, f"{prefix}.image")
        pb_path = os.path.join(spw_dir, f"{prefix}.pb")

        if os.path.exists(im_path) and os.path.exists(pb_path):
            image_list.append(im_path)
            pb_list.append(pb_path)
        else:
            print(f"[SPW{s}] Skipping {ms_name} (missing .image or .pb)")

    if len(image_list) == 0:
        print(f"[SPW{s}] No valid image+pb pairs.")
        return

    # Interleave image/pb for immath: [IM0=img0, IM1=pb0, IM2=img1, IM3=pb1, ...]
    imath_inputs = []
    for img, pb in zip(image_list, pb_list):
        imath_inputs.extend([img, pb])

    # Build PB-weighted expression:
    # numerator = Σ_k (IM(2k) * IM(2k+1))
    # denom    = Σ_k (IM(2k+1) * IM(2k+1))
    num_terms = []
    den_terms = []
    for k in range(len(image_list)):
        im_idx = 2*k
        pb_idx = 2*k + 1
        num_terms.append(f"(IM{im_idx}*IM{pb_idx})")
        den_terms.append(f"(IM{pb_idx}*IM{pb_idx})")

    expr = f"({'+'.join(num_terms)})/({'+'.join(den_terms)})"

    out_pbw = os.path.join(out_root, f"spw{s}_StokesI_pbweighted.image")
    if os.path.exists(out_pbw):
        os.system(f"rm -rf {out_pbw}")
    print(f"[SPW{s}] PB-weighted mosaic -> {out_pbw}")
    immath(imagename=imath_inputs, expr=expr, outfile=out_pbw)

    # Optional: simple arithmetic mean of .pbcor images (quick check product)
    if do_simple_mean_pbcor:
        pbcor_list = []
        for spw_dir in ms_dirs:
            ms_name = spw_dir.split(os.sep)[-3]
            prefix  = build_prefix(ms_name, s)
            pbcor_path = os.path.join(spw_dir, f"{prefix}.pbcor")
            if os.path.exists(pbcor_path):
                pbcor_list.append(pbcor_path)

        if len(pbcor_list) >= 1:
            # Mean: (IM0 + IM1 + ...)/N
            n = len(pbcor_list)
            expr_mean = "(" + "+".join([f"IM{i}" for i in range(n)]) + f")/{float(n)}"
            out_mean = os.path.join(out_root, f"spw{s}_StokesI_mean_pbcor.image")
            if os.path.exists(out_mean):
                os.system(f"rm -rf {out_mean}")
            print(f"[SPW{s}] Mean of .pbcor -> {out_mean}")
            immath(imagename=pbcor_list, expr=expr_mean, outfile=out_mean)
        else:
            print(f"[SPW{s}] No .pbcor files found for simple mean.")

# ===== Run for all SPWs =====
for s in spw_list:
    combine_one_spw(s)
