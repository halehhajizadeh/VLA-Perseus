import os, glob, shutil

mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'


base_concat = f'/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}'
spw = 15
prefer_pbcor = False   # set True if you want *.image.pbcor.tt0

def find_ms_spw_dirs(base_concat, spw):
    root = os.path.join(base_concat, 'Images', 'spw')
    if not os.path.isdir(root):
        return []
    out = []
    for ms_name in sorted(os.listdir(root)):
        d = os.path.join(root, ms_name, 'tclean', f'spw{spw}')
        if os.path.isdir(d):
            out.append(d)
    return out

def list_tt0_inputs(base_concat, spw, prefer_pbcor=True):
    inputs = []
    for d in find_ms_spw_dirs(base_concat, spw):
        # try the exact pattern first (matches your example naming)
        pb = glob.glob(os.path.join(d, f'*_StokesI_spw{spw}-* -awproject.image.pbcor.tt0'.replace(' ', '')))
        tt = glob.glob(os.path.join(d, f'*_StokesI_spw{spw}-* -awproject.image.tt0'.replace(' ', '')))

        # fallback (any tt0)
        if prefer_pbcor and not pb:
            pb = glob.glob(os.path.join(d, '*.image.pbcor.tt0'))
        if not tt:
            tt = glob.glob(os.path.join(d, '*.image.tt0'))

        if prefer_pbcor and pb:
            inputs.append(pb[0].rstrip('/'))
        elif tt:
            inputs.append(tt[0].rstrip('/'))
    # de-dup + sort
    return sorted(list(dict.fromkeys(inputs)))

def build_expr(n):
    return 'IM0' if n == 1 else f"({ ' + '.join([f'IM{i}' for i in range(n)]) })/{float(n)}"

# collect inputs (your sample fits this list)
imgs = list_tt0_inputs(base_concat, spw, prefer_pbcor=prefer_pbcor)

print('Inputs for SPW', spw)
for p in imgs: print('  -', p)

if not imgs:
    raise RuntimeError(f'No tt0 images found for SPW {spw}')

# choose an output folder like .../Images/spw/tclean/spw15/
out_dir = os.path.join(base_concat, 'Images', 'spw', 'tclean', f'spw{spw}')
os.makedirs(out_dir, exist_ok=True)
suffix = '_pbcor_tt0' if prefer_pbcor else '_tt0'
outfile = os.path.join(out_dir, f'{mosaic_name}_StokesI_spw{spw}_avg{suffix}.image')

# overwrite safely
if os.path.exists(outfile):
    shutil.rmtree(outfile, ignore_errors=True)

expr = build_expr(len(imgs))
print('immath expr:', expr)

immath(imagename=imgs, expr=expr, outfile=outfile)
print('Wrote:', outfile)
