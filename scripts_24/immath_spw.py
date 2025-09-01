import os
from glob import glob

def _pick_first_existing(*candidates):
    """Return the first existing path from candidates, else None."""
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None

def combine_one_spw(s, do_simple_mean_pbcor=True):
    ms_dirs = sorted(glob(os.path.join(per_ms_root, '*', 'tclean', f'spw{s}')))
    if not ms_dirs:
        print(f"[SPW{s}] No per-MS directories found under {per_ms_root}")
        return

    image_list = []
    pb_list    = []

    for spw_dir in ms_dirs:
        ms_name = spw_dir.split(os.sep)[-3]  # .../Images/spw/{ms_name}/tclean/spw{s}
        prefix  = build_prefix(ms_name, s)

        img = _pick_first_existing(
            os.path.join(spw_dir, f"{prefix}.image.tt0"),
            os.path.join(spw_dir, f"{prefix}.image"),
        )
        pb  = _pick_first_existing(
            os.path.join(spw_dir, f"{prefix}.pb"),
            os.path.join(spw_dir, f"{prefix}.pb.tt0"),
        )

        if img and pb:
            image_list.append(img)
            pb_list.append(pb)
        else:
            print(f"[SPW{s}] Skipping {ms_name} (found image={bool(img)}, pb={bool(pb)})")

    if len(image_list) == 0:
        print(f"[SPW{s}] No valid image+pb pairs after MT-MFS checks.")
        return

    # Interleave image/pb for immath
    imath_inputs = []
    for img, pb in zip(image_list, pb_list):
        imath_inputs.extend([img, pb])

    # Build PB-weighted expression
    num_terms = []
    den_terms = []
    for k in range(len(image_list)):
        im_idx = 2*k
        pb_idx = 2*k + 1
        num_terms.append(f"(IM{im_idx}*IM{pb_idx})")
        den_terms.append(f"(IM{pb_idx}*IM{pb_idx})")
    expr = f"({'+'.join(num_terms)})/({'+'.join(den_terms)})"

    out_pbw = os.path.join(out_root, f"spw{s}_StokesI_pbweighted.image")
    os.system(f"rm -rf {out_pbw}")
    print(f"[SPW{s}] PB-weighted mosaic from {len(image_list)} inputs -> {out_pbw}")
    immath(imagename=imath_inputs, expr=expr, outfile=out_pbw)

    # Optional: simple mean of pbcor maps
    if do_simple_mean_pbcor:
        pbcor_list = []
        for spw_dir in ms_dirs:
            ms_name = spw_dir.split(os.sep)[-3]
            prefix  = build_prefix(ms_name, s)
            pbcor = _pick_first_existing(
                os.path.join(spw_dir, f"{prefix}.pbcor"),
                os.path.join(spw_dir, f"{prefix}.pbcor.tt0"),
            )
            if pbcor:
                pbcor_list.append(pbcor)

        if pbcor_list:
            n = len(pbcor_list)
            expr_mean = "(" + "+".join([f"IM{i}" for i in range(n)]) + f")/{float(n)}"
            out_mean = os.path.join(out_root, f"spw{s}_StokesI_mean_pbcor.image")
            os.system(f"rm -rf {out_mean}")
            print(f"[SPW{s}] Mean of {n} .pbcor images -> {out_mean}")
            immath(imagename=pbcor_list, expr=expr_mean, outfile=out_mean)
        else:
            print(f"[SPW{s}] No .pbcor(.tt0) files found for simple mean.")
