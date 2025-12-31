import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
from scipy.stats import norm

# SPW → frequency (GHz)
SPW_FREQ = {
    2: 1.591, 3: 1.655, 4: 1.719, 5: 1.783, 6: 1.847, 8: 1.975,
    15: 1.283, 16: 1.347, 17: 1.411
}

df = pd.read_csv("combined_sources_all_spw.csv")

# Reshape wide → long
rows = []
for spw, freq in SPW_FREQ.items():
    rows.append(pd.DataFrame({
        "source": df["Source_ID"],
        "spw": spw,
        "freq": freq,
        "flux": df[f"Total_S_SPW{spw}"],
        "err":  df[f"E_Total_S_SPW{spw}"],
    }))

long = pd.concat(rows, ignore_index=True)
long = long.dropna()

def fit_alpha(group):
    if len(group) < 4:
        return np.nan

    x = np.log10(group["freq"].values)
    y = np.log10(group["flux"].values)

    # Proper log-space errors
    sigma_y = group["err"].values / (group["flux"].values * np.log(10))
    w = 1.0 / sigma_y**2

    A = np.vstack([x, np.ones_like(x)]).T
    C = np.diag(w)

    cov = np.linalg.inv(A.T @ C @ A)
    beta = cov @ A.T @ C @ y

    return beta[0]   # alpha

alpha = (
    long.groupby("source")
        .apply(fit_alpha)
        .dropna()
        .reset_index(name="alpha")
)

# Add alpha to long dataframe
long = pd.merge(long, alpha, on='source')

print("Alpha:", alpha)

# Normalize flux per source
long["norm_flux"] = (
    long.groupby("source")["flux"]
        .transform(lambda x: x / np.median(x))
)

plt.figure(figsize=(7,5))

for spw, g in long.groupby("spw"):
    plt.scatter(
        np.full(len(g), SPW_FREQ[spw]),
        g["norm_flux"],
        alpha=0.25,
        label=f"SPW {spw}"
    )

plt.axhline(1.0, color="k", linestyle="--")
plt.xlabel("Frequency (GHz)")
plt.ylabel("Flux / median(flux per source)")
plt.title("Per-SPW Flux Normalization Diagnostic")

plt.savefig('bias.png')

spw_bias = (
    long.groupby("spw")["norm_flux"]
        .median()
        .sort_index()
)

print(spw_bias)

# Histogram and Gaussian fit for alpha
plt.figure(figsize=(7,5))
n, bins, patches = plt.hist(alpha['alpha'], bins=20, density=True, alpha=0.6, color='g')

# Fit a Gaussian
g_init = models.Gaussian1D(amplitude=1, mean=np.mean(alpha['alpha']), stddev=np.std(alpha['alpha']))
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, (bins[1:]+bins[:-1])/2, n)

# Evaluate Gaussian at more points for a smoother curve
x = np.linspace(bins[0], bins[-1], 200)
plt.plot(x, g(x), 'r-', label='Gaussian fit')

plt.xlabel('Alpha')
plt.ylabel('Probability Density')
plt.title('Alpha Distribution')
plt.legend()
plt.savefig('alpha_hist.png')


print(f"Gaussian fit: mean = {g.mean.value:.2f}, stddev = {g.stddev.value:.2f}")

# Power law fit
for source, group in long.groupby('source'):
    y = group['flux'].values
    y_err = group['err'].values
    x_val = group['freq'].values
    
    # Filter out non-positive fluxes and non-finite values
    mask = (y > 0) & (y_err > 0) & np.isfinite(x_val) & np.isfinite(y) & np.isfinite(y_err)
    y = y[mask]
    y_err = y_err[mask]
    x_val = x_val[mask]
    
    if len(x_val) < 2:  # Need at least 2 points for fit
        continue
    
    # Initial guess
    init = models.PowerLaw1D(amplitude=1, x_0=1, alpha=-1)
    fitter = fitting.LevMarLSQFitter()
    try:
        fit = fitter(init, x_val, y, weights=1/y_err, filter_non_finite=True)
    except Exception as e:
        print(f"Fit failed for source {source}: {e}")
        continue
    
#    plt.figure(figsize=(7,5))
#    plt.errorbar(x_val, y, yerr=y_err, fmt='bo', label='Data')
#    plt.plot(x_val, fit(x_val), 'r-', label='Power law fit')
#    plt.xscale('log')
#    plt.yscale('log')
#    plt.xlabel('Frequency (GHz)')
#    plt.ylabel('Flux')
#    plt.title(f'Power Law Fit for Source {source}')
#    plt.legend()
#    plt.savefig(f'powerlaw_{source}.png')

# Write out CSV with alpha
long.to_csv('long_with_alpha.csv', index=False)
print(f"Gaussian fit: mean = {g.mean.value:.2f}, stddev = {g.stddev.value:.2f}")
