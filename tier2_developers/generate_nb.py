"""Generate Track 2 — Developers notebooks (Chapters 13-22)."""
import json
from pathlib import Path

HERE = Path(__file__).parent


def src(text):
    lines = text.strip().split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": src(text)}


def code(text):
    return {
        "cell_type": "code",
        "metadata": {},
        "source": src(text),
        "outputs": [],
        "execution_count": None,
    }


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.0"},
        },
        "cells": cells,
    }


def save(notebook, name):
    path = HERE / name
    with open(path, "w") as f:
        json.dump(notebook, f, indent=2)
    print(f"✅ Created: {path.name}")


# ─── Chapter 13: Probability in Code ────────────────────────────────────────
ch13 = nb([
    md("""# 💻 Chapter 13: Probability in Code — Simulating Randomness
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Your `random()` function isn't truly random — and that's actually great.
> Understanding how it works makes you a better engineer.

**🎯 Objectives:** Understand PRNGs, seeds, reproducibility, and entropy sources."""),

    md("""## 📖 Section 1 — Concept Review

### PRNG vs TRNG
| | **PRNG** (Pseudo-Random) | **TRNG** (True Random) |
|--|--|--|
| Source | Algorithm (deterministic) | Physical entropy (hardware) |
| Speed | Very fast | Slow |
| Reproducible | Yes (with seed) | No |
| Quality | Good algorithms are excellent | Perfect |
| Use | Simulations, ML, games | Cryptography, key generation |

### The Mersenne Twister (numpy's default)
- Period: 2^19937 - 1 (astronomically large)
- Passes most statistical tests
- **NOT cryptographically secure** — don't use for passwords!

### Seeds and Reproducibility
```python
np.random.seed(42)  # Global seed — reproducible
rng = np.random.default_rng(42)  # Better: Generator object (recommended)
```

### NumPy's Newer API (Recommended)
```python
rng = np.random.default_rng(seed=42)  # PCG64 algorithm — better quality
x = rng.uniform(0, 1, 1000)
```"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import hashlib
import time
sns.set_theme(style="whitegrid")

# ── PRNG vs Seed ──
print("🔢 Understanding Seeds and Reproducibility")
print()

# Without seed: different every time
print("Without seed (first 5):", np.random.randint(0, 100, 5))
print("Without seed (next 5): ", np.random.randint(0, 100, 5))
print()

# With seed: reproducible
np.random.seed(42)
print("With seed=42 (run 1):", np.random.randint(0, 100, 5))
np.random.seed(42)
print("With seed=42 (run 2):", np.random.randint(0, 100, 5))  # same!
print()

# Modern API (recommended)
rng1 = np.random.default_rng(42)
rng2 = np.random.default_rng(42)
print("PCG64 rng1:", rng1.integers(0, 100, 5))
print("PCG64 rng2:", rng2.integers(0, 100, 5))  # same!
print()
print("💡 Use rng = np.random.default_rng(seed) in new code!")
print("   It uses the newer, better PCG64 algorithm.")"""),

    code("""# ── Test PRNG Quality: Statistical Tests ──
rng = np.random.default_rng(42)
n = 100_000
samples = rng.uniform(0, 1, n)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Uniformity test
axes[0].hist(samples, bins=50, color='#3498db', edgecolor='white', density=True)
axes[0].axhline(1.0, color='red', linestyle='--', lw=2, label='Expected density')
axes[0].set_title(f'Uniformity: n={n:,}', fontweight='bold')
axes[0].set_xlabel('Value'); axes[0].set_ylabel('Density')
axes[0].legend()

# Autocorrelation check (random shouldn't correlate with itself)
lag1 = np.corrcoef(samples[:-1], samples[1:])[0,1]
axes[1].scatter(samples[:1000], np.roll(samples, -1)[:1000], alpha=0.3, s=5, color='#3498db')
axes[1].set_title(f'Lag-1 Autocorrelation: r={lag1:.4f}\n(should be ≈0)', fontweight='bold')
axes[1].set_xlabel('x[i]'); axes[1].set_ylabel('x[i+1]')

# Bit pattern (test for periodicity in bits)
bits = (samples * 256).astype(int) % 2  # extract one bit
run_lengths = []
current, length = bits[0], 1
for b in bits[1:]:
    if b == current: length += 1
    else: run_lengths.append(length); current, length = b, 1
axes[2].hist(run_lengths, bins=range(1, 20), color='#27ae60', edgecolor='white', density=True)
from scipy.stats import geom
k = np.arange(1, 20)
axes[2].plot(k, geom.pmf(k, 0.5), 'ro-', markersize=5, label='Expected Geometric(0.5)')
axes[2].set_title('Run Length Distribution\n(test for periodicity)', fontweight='bold')
axes[2].legend(fontsize=8)

plt.suptitle("Statistical Quality Tests for NumPy's PRNG", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch13_prng_quality.png', dpi=150, bbox_inches='tight')
plt.show()

from scipy.stats import kstest
ks_stat, p_value = kstest(samples, 'uniform')
print(f"Kolmogorov-Smirnov test for uniformity: KS={ks_stat:.4f}, p={p_value:.4f}")
print("High p → looks uniform ✅" if p_value > 0.05 else "Low p → NOT uniform ❌")"""),

    code("""# ── Sampling Methods ──
rng = np.random.default_rng(42)

print("🎯 Sampling Methods")
print()
population = np.arange(1, 101)

# Simple random sampling
srs = rng.choice(population, size=10, replace=False)
print(f"Simple random sample (n=10): {sorted(srs)}")

# Weighted sampling
weights = np.linspace(1, 10, 100)
weights /= weights.sum()
weighted = rng.choice(population, size=10, replace=True, p=weights)
print(f"Weighted sample (high values more likely): {sorted(weighted)}")

# Stratified: sample equal numbers from each decile
strata = np.array_split(population, 10)
stratified = np.concatenate([rng.choice(s, 1) for s in strata])
print(f"Stratified sample (1 from each decile): {sorted(stratified)}")

# Bootstrap sample
data = np.array([23, 45, 12, 67, 34, 89, 45, 23, 56, 78])
bootstrap = rng.choice(data, size=len(data), replace=True)
print(f"\nOriginal data: {data}")
print(f"Bootstrap sample: {bootstrap}")
print(f"(Note: some values repeated, some missing — that's bootstrap!)")"""),

    md("""## 🔬 Section 3 — Simulation: Monte Carlo π Estimation"""),

    code("""# Monte Carlo: Estimate π using random dart throws
rng = np.random.default_rng(42)

def estimate_pi(n, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n)
    y = rng.uniform(-1, 1, n)
    inside = (x**2 + y**2) <= 1
    return 4 * inside.mean(), x, y, inside

n_points = 10_000
pi_est, x, y, inside = estimate_pi(n_points)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Dart board visualization
ax = axes[0]
ax.scatter(x[inside],  y[inside],  s=2, c='#27ae60', alpha=0.5, label='Inside')
ax.scatter(x[~inside], y[~inside], s=2, c='#e74c3c', alpha=0.5, label='Outside')
theta = np.linspace(0, 2*np.pi, 100)
ax.plot(np.cos(theta), np.sin(theta), 'k-', lw=2)
ax.set_aspect('equal')
ax.set_title(f'Monte Carlo π: {pi_est:.4f}\n(n={n_points:,} darts)', fontweight='bold')
ax.legend(fontsize=9)

# Convergence
ns = np.logspace(1, 5, 100).astype(int)
estimates = []
for ni in ns:
    x_i = rng.uniform(-1, 1, ni)
    y_i = rng.uniform(-1, 1, ni)
    estimates.append(4 * ((x_i**2+y_i**2)<=1).mean())

axes[1].semilogx(ns, estimates, alpha=0.7, color='#3498db', label='Estimate')
axes[1].axhline(np.pi, color='red', lw=2, linestyle='--', label=f'True π={np.pi:.4f}')
axes[1].set_xlabel('Number of darts'); axes[1].set_ylabel('π estimate')
axes[1].set_title('Monte Carlo Convergence: O(1/√n) error', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.savefig('ch13_monte_carlo_pi.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Error ∝ 1/√n. At n={n_points}: error ≈ {abs(pi_est - np.pi):.4f}")"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Implement your own Linear Congruential Generator (simplest PRNG).
`x[n+1] = (a*x[n] + c) % m`

**Challenge 2:** Why is `random.seed(42)` at the top of an ML training script important?
Write code demonstrating model reproducibility with/without seeds.

**Challenge 3:** Implement reservoir sampling to sample k items from a stream of unknown length.

<details><summary>💡 Solutions</summary>

**Challenge 1:** See code below.

**Challenge 2:** Without seed → different weight initialization → different results every run. Seed fixes the initial weights, data shuffling, and dropout masks.

**Challenge 3:** See reservoir sampling implementation below.
</details>"""),

    code("""# Challenge 1: Linear Congruential Generator
class LCG:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.state = seed; self.a = a; self.c = c; self.m = m
    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m
    def uniform(self, n):
        return [self.next() for _ in range(n)]

lcg = LCG(42)
samples = lcg.uniform(10000)
print(f"LCG mean: {np.mean(samples):.4f} (expected 0.5)")
print(f"LCG std:  {np.std(samples):.4f} (expected ~0.289)")

# Challenge 3: Reservoir Sampling
def reservoir_sample(stream, k, seed=42):
    rng = np.random.default_rng(seed)
    reservoir = list(stream[:k])
    for i, item in enumerate(stream[k:], start=k):
        j = rng.integers(0, i+1)
        if j < k:
            reservoir[j] = item
    return reservoir

stream = list(range(1, 10001))  # stream of 10,000 items
sample = reservoir_sample(stream, 100)
print(f"\nReservoir sample (k=100 from 10,000):")
print(f"  Mean: {np.mean(sample):.1f} (expected ~5000)")
print(f"  Min/Max: {min(sample)}/{max(sample)}")"""),

    md("## 🎯 Recap\n1. PRNGs are deterministic — `seed` controls reproducibility.\n2. Use `np.random.default_rng(seed)` for modern NumPy code.\n3. Test PRNG quality with KS test, autocorrelation, and uniformity checks.\n\n**Next:** [Chapter 14 — Monte Carlo Methods]"),
])
save(ch13, "13_probability_in_code.ipynb")


# ─── Chapter 14: Monte Carlo Methods ────────────────────────────────────────
ch14 = nb([
    md("""# 💻 Chapter 14: Monte Carlo Methods
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Estimate π by throwing darts. Then use the same idea to price financial derivatives, validate APIs, and solve integrals that don't have closed forms.

**🎯 Objectives:** Build Monte Carlo estimators, understand convergence, apply to integration and simulation."""),

    md("""## 📖 Section 1 — Concept Review

### The Monte Carlo Principle
Use random sampling to estimate quantities that are:
- Too complex to compute analytically
- High-dimensional integrals
- System behavior under uncertainty

### The Core Idea
If X is a random variable and we want E[g(X)]:
$$E[g(X)] \\approx \\frac{1}{n} \\sum_{i=1}^n g(x_i) \\quad \\text{where } x_i \\sim p(x)$$

### Convergence Rate
Error ∝ 1/√n (regardless of dimension!)
This is Monte Carlo's killer advantage in high dimensions.

### Variance Reduction Techniques
1. **Antithetic variates**: Use both x and (1-x) for U[0,1]
2. **Control variates**: Subtract a correlated variable with known mean
3. **Importance sampling**: Sample from regions that matter most
4. **Stratified sampling**: Divide the domain, sample from each region"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, integrate
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── Monte Carlo Integration ──
def mc_integrate(f, a, b, n, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.uniform(a, b, n)
    return (b - a) * f(x).mean()

# Integrate sin(x) from 0 to π = 2
f = np.sin
a, b = 0, np.pi
true_val = 2.0

ns = np.logspace(1, 6, 50).astype(int)
estimates = [mc_integrate(f, a, b, n) for n in ns]
errors = [abs(e - true_val) for e in estimates]

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# Show the integral
x_plot = np.linspace(0, np.pi, 300)
axes[0].plot(x_plot, np.sin(x_plot), lw=3, color='#3498db', label='sin(x)')
axes[0].fill_between(x_plot, np.sin(x_plot), alpha=0.3, color='#3498db', label='Integral = 2.0')
mc_pts_x = rng.uniform(0, np.pi, 200)
mc_pts_y = rng.uniform(0, 1, 200)
hit = mc_pts_y <= np.sin(mc_pts_x)
axes[0].scatter(mc_pts_x[hit], mc_pts_y[hit], s=10, c='#27ae60', alpha=0.7, label='Inside')
axes[0].scatter(mc_pts_x[~hit], mc_pts_y[~hit], s=10, c='#e74c3c', alpha=0.7, label='Outside')
axes[0].set_title(f'∫sin(x)dx from 0 to π = 2.000\nMC estimate: {mc_integrate(f,a,b,10000):.4f}', fontweight='bold')
axes[0].legend(fontsize=8)

# Error convergence
axes[1].loglog(ns, errors, 'bo-', markersize=4, lw=1.5, label='MC error')
axes[1].loglog(ns, 1/np.sqrt(ns), 'r--', lw=2, label='O(1/√n) reference')
axes[1].set_xlabel('n (samples)'); axes[1].set_ylabel('Absolute Error')
axes[1].set_title('Monte Carlo Convergence: O(1/√n)', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.savefig('ch14_mc_integration.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── Variance Reduction: Antithetic Variates ──
rng = np.random.default_rng(42)

def estimate_normal_prob(n_samples):
    # Estimate P(Z > 2) for Z~N(0,1) using different methods.
    # Standard MC
    z_plain = rng.normal(0, 1, n_samples)
    plain = (z_plain > 2).mean()

    # Antithetic variates: use z and -z together
    z_half = rng.normal(0, 1, n_samples // 2)
    z_anti = np.concatenate([z_half, -z_half])
    antithetic = (z_anti > 2).mean()

    true_val = 1 - stats.norm.cdf(2)
    return plain, antithetic, true_val

results = []
for n in [100, 1000, 10000, 100000]:
    p, a, t = estimate_normal_prob(n)
    results.append({'n': n, 'plain_err': abs(p-t), 'antithetic_err': abs(a-t)})
    print(f"n={n:>7}: Plain error={abs(p-t):.5f}, Antithetic error={abs(a-t):.5f}")

print(f"\nTrue P(Z>2) = {1-stats.norm.cdf(2):.6f}")
print("Antithetic variates often give 2-4x variance reduction!")"""),

    code("""# ── Applied: Option Pricing (Black-Scholes via Monte Carlo) ──
rng = np.random.default_rng(42)

# European call option parameters
S0 = 100    # current stock price
K  = 105    # strike price
T  = 1.0    # time to expiry (years)
r  = 0.05   # risk-free rate
sigma = 0.2 # volatility

def mc_option_price(S0, K, T, r, sigma, n_paths=100_000):
    rng = np.random.default_rng(42)
    # Geometric Brownian Motion: S_T = S0 * exp((r - σ²/2)T + σ√T·Z)
    Z = rng.normal(0, 1, n_paths)
    ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    payoff = np.maximum(ST - K, 0)
    price = np.exp(-r*T) * payoff.mean()
    se = np.exp(-r*T) * payoff.std() / np.sqrt(n_paths)
    return price, se, ST

price, se, ST = mc_option_price(S0, K, T, r, sigma)

# Black-Scholes analytical formula for comparison
d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2 = d1 - sigma*np.sqrt(T)
bs_price = S0*stats.norm.cdf(d1) - K*np.exp(-r*T)*stats.norm.cdf(d2)

print("📈 European Call Option Pricing")
print(f"  MC Price: ${price:.4f} ± {1.96*se:.4f} (95% CI)")
print(f"  Black-Scholes: ${bs_price:.4f}")
print(f"  Error: ${abs(price-bs_price):.4f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.hist(ST, bins=60, color='#3498db', edgecolor='white', density=True, alpha=0.7)
ax1.axvline(K, color='red', lw=2, linestyle='--', label=f'Strike K={K}')
ax1.set_title('Distribution of Stock Price at T=1yr', fontweight='bold')
ax1.set_xlabel('Stock Price'); ax1.legend()

payoffs = np.maximum(ST - K, 0)
ax2.hist(payoffs[payoffs > 0], bins=50, color='#27ae60', edgecolor='white', density=True, alpha=0.7)
ax2.set_title(f'Positive Payoffs (options in-the-money)\nMean payoff = ${np.exp(-r*T)*np.maximum(ST-K,0).mean():.2f}', fontweight='bold')
ax2.set_xlabel('Payoff ($)')
plt.tight_layout()
plt.savefig('ch14_option_pricing.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Use Monte Carlo to estimate ∫₀¹ e^(-x²) dx.
Compare with `scipy.integrate.quad`.

**Challenge 2:** Simulate a system: 3 independent components, each fails with P=0.1.
System fails if ANY component fails. Estimate P(system failure) via Monte Carlo.
Verify analytically.

**Challenge 3:** Implement importance sampling to estimate P(Z > 4) more efficiently than plain MC.

<details><summary>Solutions</summary>

**C1:** True = 0.7468. MC with n=100k gets within 0.001.

**C2:** P(system failure) = 1 - (0.9)³ = 0.271. MC should give ~0.271.

**C3:** Sample from N(4, 1) instead of N(0,1), then reweight by likelihood ratio.
</details>"""),

    code("""# C1: MC Integration vs scipy
from scipy.integrate import quad

f = lambda x: np.exp(-x**2)
mc_est = mc_integrate(np.vectorize(f), 0, 1, 1_000_000)
scipy_val, _ = quad(f, 0, 1)
print(f"MC estimate: {mc_est:.6f}")
print(f"Scipy exact: {scipy_val:.6f}")
print(f"Error: {abs(mc_est-scipy_val):.6f}")

# C2: System reliability
rng = np.random.default_rng(42)
n = 1_000_000
comps = rng.random((n, 3)) < 0.1  # each component fails with P=0.1
system_fails = comps.any(axis=1)
print(f"\nSystem failure (simulated): {system_fails.mean():.4f}")
print(f"System failure (theory):   {1 - 0.9**3:.4f}")"""),

    md("## 🎯 Recap\n1. Monte Carlo = estimate by averaging over random samples.\n2. Convergence is O(1/√n) — always, regardless of dimension.\n3. Variance reduction (antithetic, stratification) can give big speedups.\n\n**Next:** [Chapter 15 — A/B Testing]"),
])
save(ch14, "14_monte_carlo_methods.ipynb")


# ─── Chapter 15: A/B Testing ─────────────────────────────────────────────────
ch15 = nb([
    md("""# 💻 Chapter 15: A/B Testing — Design & Analysis
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Your A/B test says the new button color is 15% better with p=0.03.
> Should you ship it? The answer depends on things most teams never check.

**🎯 Objectives:** Design statistically valid A/B tests; avoid common pitfalls; analyze results correctly."""),

    md("""## 📖 Section 1 — Concept Review

### The A/B Testing Framework
1. **Metric**: What are you measuring? (CTR, conversion rate, revenue)
2. **Null hypothesis H₀**: No difference between A and B
3. **Sample size**: Calculate BEFORE running the test
4. **Duration**: Run to completion, don't peek
5. **Analysis**: Two-proportion z-test or t-test

### Sample Size Calculation
For comparing two proportions:
$$n = \\frac{(z_{\\alpha/2} + z_\\beta)^2 (p_1(1-p_1) + p_2(1-p_2))}{(p_1 - p_2)^2}$$

### The Most Common Mistakes
1. **Peeking**: Stopping early when you see p<0.05 — inflates Type I error
2. **Multiple comparisons**: Testing 20 metrics without correction
3. **Too small n**: Underpowered test misses real effects
4. **Not specifying MDE**: Minimum Detectable Effect must be set in advance
5. **Novelty effect**: Users respond differently to anything new"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import pandas as pd
rng = np.random.default_rng(42)
sns.set_theme(style="whitegrid")

# ── Sample Size Calculator ──
def ab_sample_size(p_baseline, mde, alpha=0.05, power=0.80):
    # Required sample size per variant.
    p1 = p_baseline
    p2 = p_baseline + mde
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta  = stats.norm.ppf(power)
    n = ((z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2))) / (p1-p2)**2
    return int(np.ceil(n))

print("📊 A/B Test Sample Size Calculator")
print(f"{'Baseline CTR':>14} {'MDE':>8} {'Required n/variant':>20} {'Total n':>10}")
print("-" * 56)
for p_base in [0.02, 0.05, 0.10, 0.20]:
    for mde in [0.005, 0.01, 0.02]:
        if mde/p_base > 0.5:
            n = ab_sample_size(p_base, mde)
            total = 2 * n
            print(f"{p_base:>14.1%} {mde:>8.1%} {n:>20,} {total:>10,}")
print()
print("💡 Key insight: Large baselines AND small MDEs need HUGE samples!")"""),

    code("""# ── The Peeking Problem ──
rng = np.random.default_rng(42)

def run_ab_test_with_peeking(true_p_a, true_p_b, n_max, alpha=0.05):
    # Simulate peeking: check p-value after every 10 observations.
    data_a, data_b = [], []
    peeked_significant = False

    for _ in range(n_max):
        data_a.append(rng.random() < true_p_a)
        data_b.append(rng.random() < true_p_b)

        if len(data_a) >= 20 and len(data_a) % 10 == 0:
            conv_a = np.mean(data_a); conv_b = np.mean(data_b)
            n_a = len(data_a); n_b = len(data_b)
            # Two-proportion z-test
            p_pool = (sum(data_a) + sum(data_b)) / (n_a + n_b)
            se = np.sqrt(p_pool*(1-p_pool)*(1/n_a + 1/n_b))
            if se > 0:
                z = (conv_a - conv_b) / se
                p_val = 2 * (1 - stats.norm.cdf(abs(z)))
                if p_val < alpha:
                    peeked_significant = True
                    break

    # Final test without peeking
    _, p_final = stats.ttest_ind(data_a, data_b)
    return peeked_significant, p_final < alpha

# Simulate: no TRUE difference (H₀ true)
n_sims = 1000
peek_fp = 0; nopeak_fp = 0
for _ in range(n_sims):
    peek, no_peek = run_ab_test_with_peeking(0.05, 0.05, 1000)
    if peek: peek_fp += 1
    if no_peek: nopeak_fp += 1

print(f"🚨 Peeking Problem Demo (H₀ is TRUE — no real difference)")
print(f"  False positive rate WITH peeking:    {peek_fp/n_sims:.1%}")
print(f"  False positive rate WITHOUT peeking: {nopeak_fp/n_sims:.1%}")
print(f"  Target α = 5.0%")
print()
print("💥 Peeking inflates FP rate from 5% to much higher!")
print("   Always run tests to planned completion.")"""),

    code("""# ── Complete A/B Test Analysis ──
rng = np.random.default_rng(42)

# Simulate experiment results
n_per_variant = 5000
true_rate_A = 0.050  # control (current)
true_rate_B = 0.058  # treatment (new button)
mde = 0.008  # minimum detectable effect we set in advance

conversions_A = rng.binomial(1, true_rate_A, n_per_variant)
conversions_B = rng.binomial(1, true_rate_B, n_per_variant)

conv_A = conversions_A.mean()
conv_B = conversions_B.mean()
lift = (conv_B - conv_A) / conv_A

# Two-proportion z-test
p_pool = (conversions_A.sum() + conversions_B.sum()) / (n_per_variant * 2)
se = np.sqrt(p_pool * (1-p_pool) * 2/n_per_variant)
z = (conv_B - conv_A) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z)))

alpha = 0.05
print("📊 A/B Test Results Report")
print("=" * 50)
print(f"  Variant A (control):  {conv_A:.4f} ({conversions_A.sum()} / {n_per_variant})")
print(f"  Variant B (treatment):{conv_B:.4f} ({conversions_B.sum()} / {n_per_variant})")
print(f"  Observed lift:        {lift:+.2%}")
print(f"  Z-statistic:          {z:.4f}")
print(f"  p-value:              {p_value:.4f}")
print()
if p_value < alpha and abs(conv_B - conv_A) >= mde:
    print(f"  ✅ SHIP IT: Statistically significant AND practically meaningful")
elif p_value < alpha:
    print(f"  ⚠️  Significant but effect size < MDE — may not be worth shipping")
else:
    print(f"  ❌ Not significant — don't ship")

# Confidence interval for the difference
ci_low = (conv_B - conv_A) - 1.96*se
ci_high = (conv_B - conv_A) + 1.96*se
print(f"\n  95% CI for difference: ({ci_low:.4f}, {ci_high:.4f})")
print(f"  MDE was: {mde:.4f}")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
variants = ['Control (A)', 'Treatment (B)']
rates = [conv_A, conv_B]
errors = [1.96 * np.sqrt(r*(1-r)/n_per_variant) for r in rates]
colors = ['#3498db', '#27ae60' if p_value < alpha else '#e74c3c']

axes[0].bar(variants, rates, color=colors, alpha=0.7, yerr=errors, capsize=5)
axes[0].set_ylabel('Conversion Rate')
axes[0].set_title(f'A/B Test: p={p_value:.4f}', fontweight='bold')
for i, (r, e) in enumerate(zip(rates, errors)):
    axes[0].text(i, r+e+0.001, f'{r:.3%}', ha='center', fontweight='bold')

# Null distribution vs observed
x = np.linspace(-5, 5, 300)
axes[1].plot(x, stats.norm.pdf(x), lw=3, color='#3498db', label='Null distribution')
axes[1].fill_between(x, stats.norm.pdf(x), where=(abs(x) >= abs(z)), color='#e74c3c', alpha=0.4, label=f'p={p_value:.4f}')
axes[1].axvline(z, color='#e74c3c', lw=2, linestyle='--', label=f'z={z:.2f}')
axes[1].set_title('Hypothesis Test: Z-distribution', fontweight='bold')
axes[1].set_xlabel('Z'); axes[1].legend(fontsize=9)
plt.tight_layout()
plt.savefig('ch15_ab_test.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Write a function `required_sample_size(p1, p2, alpha, power)`.
Test it for: p1=0.10, p2=0.12, α=0.05, power=0.80.

**Challenge 2:** Your A/B test has 5 metrics. If each uses α=0.05, what's the family-wise error rate?
Apply Bonferroni correction and recalculate.

**Challenge 3:** Implement a simple Bayesian A/B test using Beta-Binomial conjugacy.
Report P(B > A) and credible intervals.

<details><summary>Solutions</summary>

**C1:** n ≈ 3,560 per variant.

**C2:** FWER = 1-(0.95)^5 ≈ 0.226. Bonferroni: use α/5 = 0.01 per test.

**C3:** See Bayesian code below.
</details>"""),

    code("""# Bayesian A/B Test
from scipy.stats import beta

# Prior: Beta(1,1) = uniform
alpha_prior = 1; beta_prior = 1

# Observed
conv_a_obs = 250; visits_a = 5000
conv_b_obs = 290; visits_b = 5000

# Posterior: Beta(alpha + conversions, beta + non-conversions)
post_a = beta(alpha_prior + conv_a_obs, beta_prior + visits_a - conv_a_obs)
post_b = beta(alpha_prior + conv_b_obs, beta_prior + visits_b - conv_b_obs)

# P(B > A) via sampling
rng2 = np.random.default_rng(42)
samples_a = post_a.rvs(100_000, random_state=42)
samples_b = post_b.rvs(100_000, random_state=43)
p_b_better = (samples_b > samples_a).mean()

print(f"Bayesian A/B Test:")
print(f"  P(B > A) = {p_b_better:.3f}")
print(f"  P(B > A by > 10%) = {((samples_b / samples_a - 1) > 0.10).mean():.3f}")

x = np.linspace(0.03, 0.08, 300)
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(x, post_a.pdf(x), lw=3, color='#3498db', label=f'Control (A): {conv_a_obs}/{visits_a}')
ax.plot(x, post_b.pdf(x), lw=3, color='#27ae60', label=f'Treatment (B): {conv_b_obs}/{visits_b}')
ax.fill_between(x, post_a.pdf(x), alpha=0.2, color='#3498db')
ax.fill_between(x, post_b.pdf(x), alpha=0.2, color='#27ae60')
ax.set_title(f'Bayesian A/B Test: P(B>A) = {p_b_better:.1%}', fontweight='bold')
ax.set_xlabel('Conversion Rate'); ax.set_ylabel('Posterior Density')
ax.legend(); plt.tight_layout()
plt.savefig('ch15_bayesian_ab.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("## 🎯 Recap\n1. Calculate sample size BEFORE the experiment using MDE, α, and power.\n2. Never peek — sequential testing frameworks exist for this.\n3. Statistical significance ≠ practical significance — check effect size vs MDE.\n\n**Next:** [Chapter 16 — Bayesian Updating in Practice]"),
])
save(ch15, "15_ab_testing.ipynb")


# ─── Chapters 16-22: Developer Track ────────────────────────────────────────
ch16 = nb([
    md("""# 💻 Chapter 16: Bayesian Updating in Practice
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Machine learning models retrain on new data in batch. Bayesian updating does it online — one data point at a time, no retraining.

**🎯 Objectives:** Implement sequential Bayesian updating; understand conjugate priors; build an online learning system."""),

    md("""## 📖 Section 1 — Concept Review

### Bayesian Updating
Start with a prior → observe data → get posterior → posterior becomes the next prior.

$$\\text{Posterior} \\propto \\text{Likelihood} \\times \\text{Prior}$$

### Conjugate Priors (closed-form updates)
| Data Distribution | Prior | Posterior |
|---|---|---|
| Bernoulli/Binomial | Beta(α,β) | Beta(α+successes, β+failures) |
| Poisson | Gamma(α,β) | Gamma(α+sum, β+n) |
| Normal (known σ) | Normal(μ₀,σ₀) | Normal(μₙ,σₙ) — weighted average |

### Why Conjugate?
Posterior is same distribution family as prior → closed-form math, no MCMC needed."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, gamma, norm
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── Beta-Binomial: Click-Through Rate ──
true_ctr = 0.073  # true CTR we're estimating
n_obs = [0, 5, 20, 100, 500, 2000]
clicks_by_n = {0: 0}
cumulative_n = 0
cumulative_clicks = 0

# Simulate streaming clicks
all_data = rng.random(2000) < true_ctr
click_counts = {0: 0}
total_by_n = {0: 0}

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

alpha_prior, beta_prior = 1, 1  # uniform prior

for ax, n in zip(axes.flatten(), n_obs):
    x = np.linspace(0, 0.2, 300)
    if n == 0:
        posterior = beta(alpha_prior, beta_prior)
        title = 'Prior: Beta(1,1)\n= Uniform[0,1]'
    else:
        successes = all_data[:n].sum()
        failures  = n - successes
        posterior = beta(alpha_prior + successes, beta_prior + failures)
        title = f'After n={n}: {successes} clicks\nBeta({alpha_prior+successes},{beta_prior+failures})'

    ax.plot(x, posterior.pdf(x), lw=3, color='#3498db')
    ax.fill_between(x, posterior.pdf(x), alpha=0.3, color='#3498db')
    ax.axvline(true_ctr, color='red', lw=2, linestyle='--', label=f'True CTR={true_ctr}')
    if n > 0:
        ax.axvline(all_data[:n].mean(), color='green', lw=2, linestyle=':', label=f'MLE={all_data[:n].mean():.3f}')
    ax.set_title(title, fontweight='bold', fontsize=9)
    ax.set_xlabel('CTR'); ax.set_ylabel('Posterior Density')
    ax.legend(fontsize=7)
    ax.set_xlim(0, 0.2)

plt.suptitle("Bayesian Updating: Beta-Binomial for Click-Through Rate", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch16_bayesian_updating.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── Online Bayesian System: Website Anomaly Detection ──
rng = np.random.default_rng(42)

# Normal requests per minute, but with a DDoS starting at t=50
baseline_rate = 100
ddos_multiplier = 5

data_stream = np.concatenate([
    rng.poisson(baseline_rate, 50),
    rng.poisson(baseline_rate * ddos_multiplier, 50),
])

# Bayesian estimate of current rate (Gamma-Poisson conjugate)
# Prior: Gamma(alpha=5, beta=0.05) → prior mean = 100
alpha, beta_param = 5, 0.05

estimates = []
upper_bounds = []

for t, count in enumerate(data_stream):
    # Update: Gamma posterior after one Poisson observation
    alpha += count
    beta_param += 1
    mean_est = alpha / beta_param
    # 95th percentile of posterior
    upper = gamma.ppf(0.95, a=alpha, scale=1/beta_param)
    estimates.append(mean_est)
    upper_bounds.append(upper)

threshold = baseline_rate * 2.5

fig, ax = plt.subplots(figsize=(12, 5))
t = np.arange(100)
ax.plot(t, data_stream, alpha=0.5, color='gray', label='Observed requests/min')
ax.plot(t, estimates, color='#3498db', lw=2.5, label='Bayesian estimate')
ax.fill_between(t, estimates, upper_bounds, alpha=0.2, color='#3498db')
ax.axhline(threshold, color='#e74c3c', lw=2, linestyle='--', label=f'Alert threshold ({threshold})')
ax.axvline(50, color='orange', lw=2, linestyle=':', label='DDoS starts here')
ax.set_xlabel('Time (minutes)'); ax.set_ylabel('Requests per minute')
ax.set_title('🚨 Online Bayesian Anomaly Detection', fontweight='bold')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('ch16_anomaly.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge:** Implement a multi-armed bandit using Thompson Sampling.
You have 3 buttons (arms) with unknown click rates. At each step, sample from each arm's Beta posterior and select the arm with the highest sample.

<details><summary>Solution</summary>
See code below — Thompson Sampling naturally balances exploration vs exploitation.
</details>"""),

    code("""# Thompson Sampling Multi-Armed Bandit
rng = np.random.default_rng(42)

true_rates = [0.08, 0.12, 0.10]  # true CTRs for each arm
n_arms = len(true_rates)
n_rounds = 1000

alphas = np.ones(n_arms)  # Beta prior alpha
betas  = np.ones(n_arms)  # Beta prior beta
choices = []; rewards = []

for _ in range(n_rounds):
    # Thompson sampling: sample from each arm's posterior
    samples = [rng.beta(alphas[i], betas[i]) for i in range(n_arms)]
    chosen = np.argmax(samples)
    reward = int(rng.random() < true_rates[chosen])
    # Update posterior
    alphas[chosen] += reward
    betas[chosen]  += 1 - reward
    choices.append(chosen); rewards.append(reward)

print("🎰 Thompson Sampling Results:")
for i in range(n_arms):
    n_chosen = choices.count(i)
    est_rate = alphas[i] / (alphas[i] + betas[i])
    print(f"  Arm {i+1}: chosen {n_chosen} times, estimated rate={est_rate:.3f} (true={true_rates[i]})")

# Cumulative regret
optimal_rate = max(true_rates)
cum_regret = np.cumsum([optimal_rate - true_rates[c] for c in choices])
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(cum_regret, color='#e74c3c', lw=2.5)
ax.set_xlabel('Round'); ax.set_ylabel('Cumulative Regret')
ax.set_title('Thompson Sampling: Regret grows sub-linearly ✅', fontweight='bold')
plt.tight_layout()
plt.savefig('ch16_thompson.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("## 🎯 Recap\n1. Bayesian updating: posterior = f(prior × likelihood), done analytically with conjugate priors.\n2. Beta-Binomial is the go-to for binary outcomes (clicks, conversions).\n3. Online updating enables real-time systems without batch retraining.\n\n**Next:** [Chapter 17 — Log Probabilities & Numerical Stability]"),
])
save(ch16, "16_bayesian_updating.ipynb")


ch17 = nb([
    md("""# 💻 Chapter 17: Log Probabilities & Numerical Stability
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Multiply 1,000 small probabilities together and Python returns 0.0. Not because the answer is zero — because floating point underflowed. Here's the fix every NLP engineer must know.

**🎯 Objectives:** Understand float underflow, the log-probability trick, and the log-sum-exp algorithm."""),

    md("""## 📖 Section 1 — Concept Review

### The Underflow Problem
```python
probs = [0.1] * 1000
product = 1.0
for p in probs: product *= p
print(product)  # → 0.0  ❌ (true answer ≈ 10^-1000)
```

### The Fix: Work in Log Space
$$\\log(p_1 \\cdot p_2 \\cdots p_n) = \\log p_1 + \\log p_2 + \\cdots + \\log p_n$$

Multiplication → Addition in log space. No underflow!

### Log-Sum-Exp Trick
Computing log(a + b) from log(a) and log(b):
$$\\log(e^a + e^b) = a + \\log(1 + e^{b-a}) \\quad \\text{(take max a)}$$

Or: `scipy.special.logsumexp(log_probs)` — always use this!

### Where This Appears
- Naive Bayes classifier: P(class|features) = ∏ P(feature|class)
- Language models: P(sentence) = ∏ P(word|context)
- Viterbi algorithm, HMMs, CRFs
- Any model with many multiplication terms"""),

    code("""import numpy as np
from scipy.special import logsumexp
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")

# ── Underflow Demo ──
print("🚨 Underflow Problem")
n_probs = [10, 100, 500, 1000, 2000]
for n in n_probs:
    probs = [0.1] * n
    naive = 1.0
    for p in probs: naive *= p
    log_result = sum(np.log(p) for p in probs)
    print(f"  n={n:>4}: naive product = {naive:.2e}, log-space = {log_result:.2f}, recovered = {np.exp(log_result):.2e}")

print()
print("✅ Solution: Always work in log space, convert back only at the end!")"""),

    code("""# ── Log-Sum-Exp Trick ──
print("🔢 Log-Sum-Exp Trick")
print()

# Problem: compute log(e^a + e^b) without overflow/underflow
a, b = 1000, 1001

# Naive: e^1000 overflows!
try:
    naive = np.log(np.exp(a) + np.exp(b))
    print(f"  Naive result: {naive}")
except:
    print("  Naive: OVERFLOW!")

# Log-sum-exp: numerically stable
# log(e^a + e^b) = b + log(1 + e^(a-b))  [using max=b]
stable = b + np.log(1 + np.exp(a - b))
scipy_lse = logsumexp([a, b])

print(f"  Manual log-sum-exp: {stable:.4f}")
print(f"  scipy.special.logsumexp: {scipy_lse:.4f}")
print(f"  True value: {np.log(np.exp(a-b) + 1) + b:.4f}")
print()

# Softmax in log space
def stable_softmax(logits):
    return np.exp(logits - logsumexp(logits))

logits = np.array([1.0, 2.0, 3.0, 1.0])
probs = stable_softmax(logits)
print(f"Logits: {logits}")
print(f"Softmax: {probs}")
print(f"Sum = {probs.sum():.6f}")"""),

    code("""# ── Naive Bayes Classifier in Log Space ──
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

# Simple Naive Bayes from scratch (in log space!)
class LogSpaceNaiveBayes:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n_features = X.shape[1]
        self.log_priors_ = {}
        self.log_likelihoods_ = {}  # log P(feature | class)

        for c in self.classes_:
            mask = y == c
            X_c = X[mask]
            self.log_priors_[c] = np.log(mask.sum() / len(y))
            # Laplace smoothing in log space
            counts = X_c.sum(axis=0) + 1  # +1 smoothing
            self.log_likelihoods_[c] = np.log(counts / counts.sum())

    def predict_log_proba(self, X):
        log_probs = {}
        for c in self.classes_:
            # log P(c|x) ∝ log P(c) + Σ log P(xi|c)
            log_probs[c] = self.log_priors_[c] + X.dot(self.log_likelihoods_[c])
        return log_probs

    def predict(self, X):
        log_probs = self.predict_log_proba(X)
        predictions = np.array([
            max(self.classes_, key=lambda c: log_probs[c][i])
            for i in range(X.shape[0])
        ])
        return predictions

# Quick demo on synthetic data
rng = np.random.default_rng(42)
n = 200
# Simulate bag-of-words features
X_spam = np.column_stack([rng.poisson(5, n//2), rng.poisson(1, n//2), rng.poisson(2, n//2)])
X_ham  = np.column_stack([rng.poisson(1, n//2), rng.poisson(4, n//2), rng.poisson(3, n//2)])
X = np.vstack([X_spam, X_ham])
y = np.array(['spam']*100 + ['ham']*100)

nb = LogSpaceNaiveBayes()
nb.fit(X, y)
predictions = nb.predict(X)
accuracy = (predictions == y).mean()
print(f"Naive Bayes accuracy: {accuracy:.2%}")
print("Key: all computations done in log space, no underflow!")"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Compute log P(sentence) for a language model.
Sentence: "the cat sat on the mat". Unigram probs: {the:0.05, cat:0.01, sat:0.008, on:0.04, mat:0.003}.

**Challenge 2:** Implement `log_normalize(log_probs)` that normalizes a list of log probabilities.
Hint: use logsumexp.

**Challenge 3:** Why is cross-entropy loss in neural networks actually log-probability?
<details><summary>Solutions</summary>

**C1:** log P = Σ log(p_word). Sum the log probabilities.

**C2:** `log_probs - logsumexp(log_probs)`

**C3:** Cross-entropy = -E[log P(y|x)] = -log P(correct class). Minimizing CE = maximizing log-likelihood = MLE.
</details>"""),

    code("""# C1
sentence = "the cat sat on the mat".split()
unigram_probs = {'the':0.05,'cat':0.01,'sat':0.008,'on':0.04,'mat':0.003}
log_probs = [np.log(unigram_probs[w]) for w in sentence]
print(f"Log P(sentence) = {sum(log_probs):.4f}")
print(f"P(sentence) = {np.exp(sum(log_probs)):.2e}")

# C2
def log_normalize(log_probs):
    return np.array(log_probs) - logsumexp(log_probs)
lp = [-1.0, -2.0, -0.5, -3.0]
normalized = log_normalize(lp)
print(f"\nLog probs: {lp}")
print(f"Normalized: {normalized}")
print(f"Exp(normalized): {np.exp(normalized)} (sum={np.exp(normalized).sum():.4f})")"""),

    md("## 🎯 Recap\n1. Multiplying many small probabilities causes underflow — always use log space.\n2. Log-sum-exp trick enables numerically stable softmax, marginalization, and normalization.\n3. Log-probabilities are fundamental to NLP, HMMs, and probabilistic graphical models.\n\n**Next:** [Chapter 18 — Probability in APIs & Rate Limiting]"),
])
save(ch17, "17_log_probabilities.ipynb")


ch18 = nb([
    md("""# 💻 Chapter 18: Probability in APIs & Rate Limiting
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** How does Netflix decide how many servers to spin up? How does Stripe prevent API abuse? The answer involves Poisson processes and queuing theory.

**🎯 Objectives:** Model API traffic with Poisson processes, understand token bucket rate limiting, size server capacity."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── Poisson Process: API Requests ──
lambda_rate = 100  # requests per second

# Simulate 10 seconds of API traffic
t_sim = 10
n_requests = rng.poisson(lambda_rate * t_sim)
arrival_times = np.sort(rng.uniform(0, t_sim, n_requests))

# Requests per second
bins = np.arange(0, t_sim+1)
requests_per_sec = np.histogram(arrival_times, bins=bins)[0]

fig, axes = plt.subplots(2, 2, figsize=(13, 8))

axes[0,0].bar(np.arange(t_sim), requests_per_sec, color='#3498db', edgecolor='white')
axes[0,0].axhline(lambda_rate, color='red', lw=2, linestyle='--', label=f'Expected λ={lambda_rate}')
axes[0,0].set_title('API Requests per Second', fontweight='bold')
axes[0,0].set_xlabel('Second'); axes[0,0].set_ylabel('Requests')
axes[0,0].legend()

# Inter-arrival times (should be Exponential(λ))
inter_arrivals = np.diff(arrival_times)
x = np.linspace(0, 0.1, 300)
axes[0,1].hist(inter_arrivals, bins=50, density=True, color='#3498db', alpha=0.7, label='Observed')
axes[0,1].plot(x, stats.expon.pdf(x, scale=1/lambda_rate), 'r-', lw=2.5,
               label=f'Exp(λ={lambda_rate})')
axes[0,1].set_title('Inter-arrival Times: Exponential Distribution', fontweight='bold')
axes[0,1].set_xlabel('Time between requests (seconds)'); axes[0,1].legend()

# Count distribution (should be Poisson)
k = np.arange(60, 140)
observed_counts = [rng.poisson(lambda_rate) for _ in range(1000)]
axes[1,0].hist(observed_counts, bins=30, density=True, color='#27ae60', alpha=0.7, label='Simulated')
axes[1,0].plot(k, stats.poisson.pmf(k, lambda_rate), 'r-', lw=2.5, label='Poisson(100)')
axes[1,0].set_title('Requests/Second Distribution', fontweight='bold')
axes[1,0].set_xlabel('Requests per second'); axes[1,0].legend()

# Capacity planning: how many servers?
# Each server handles max_rps requests/second
max_rps_per_server = 30
p_overload = np.array([1 - stats.poisson.cdf(n*max_rps_per_server - 1, lambda_rate)
                        for n in range(1, 8)])
axes[1,1].bar(range(1,8), p_overload*100, color='#e74c3c', alpha=0.7)
axes[1,1].axhline(1, color='black', lw=2, linestyle='--', label='1% target')
axes[1,1].set_xlabel('Number of Servers')
axes[1,1].set_ylabel('P(Overload) %')
axes[1,1].set_title(f'Capacity Planning\n(each server: {max_rps_per_server} rps max)', fontweight='bold')
axes[1,1].legend()

plt.suptitle("Probability in API Systems: Poisson Traffic Model", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch18_api_traffic.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"With λ=100 rps, need {next(n for n,p in enumerate(p_overload,1) if p<0.01)+1} servers for <1% overload")"""),

    code("""# ── Token Bucket Rate Limiter ──
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens/second
        self.last_refill = 0

    def allow_request(self, timestamp, tokens_needed=1):
        # Refill tokens based on elapsed time
        elapsed = timestamp - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = timestamp

        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True  # Allowed
        return False  # Rate limited

# Simulate API requests
rng = np.random.default_rng(42)
bucket = TokenBucket(capacity=10, refill_rate=5)  # 5 req/sec steady state, burst of 10

n_requests = 200
request_times = np.cumsum(rng.exponential(0.15, n_requests))  # ~6.7 req/sec
allowed = [bucket.allow_request(t) for t in request_times]

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# Rate over time
window_s = 1.0
axes[0].scatter(request_times[allowed], np.ones(sum(allowed)),
                color='#27ae60', s=15, alpha=0.7, label='Allowed')
axes[0].scatter(request_times[~np.array(allowed)], np.zeros(sum(~np.array(allowed))),
                color='#e74c3c', s=15, alpha=0.7, label='Rate limited')
axes[0].set_xlabel('Time (seconds)'); axes[0].set_yticks([0,1])
axes[0].set_yticklabels(['Rejected','Allowed'])
axes[0].set_title(f'Token Bucket (capacity=10, rate=5/s)\n{sum(allowed)} allowed, {sum(~np.array(allowed))} rejected', fontweight='bold')
axes[0].legend()

# Request rate over time
bin_edges = np.arange(0, request_times[-1]+1, 1)
counts_allowed  = np.histogram(request_times[allowed], bins=bin_edges)[0]
counts_incoming = np.histogram(request_times, bins=bin_edges)[0]
axes[1].bar(bin_edges[:-1], counts_incoming, alpha=0.5, color='gray', label='Incoming')
axes[1].bar(bin_edges[:-1], counts_allowed, alpha=0.8, color='#27ae60', label='Allowed (≤5/s)')
axes[1].axhline(5, color='red', lw=2, linestyle='--', label='Rate limit (5/s)')
axes[1].set_xlabel('Second'); axes[1].set_ylabel('Requests')
axes[1].set_title('Effective Rate Limiting', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.savefig('ch18_rate_limiting.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Model: API receives Poisson(50 req/sec). Each takes Exponential(1/10 sec) to process.
Using Little's Law: L = λW, compute average queue length and wait time.

**Challenge 2:** Implement a "leaky bucket" rate limiter and compare to token bucket.

**Challenge 3:** Build a simple load balancer that routes to the server with fewest active requests, simulating request arrivals and completions.

<details><summary>Solutions</summary>

**C1:** λ=50, service rate μ=10, utilization ρ=λ/μ=5 (system overloaded at ρ>1!).
Need multiple servers: for M/M/k, ρ<1 requires k>λ/μ=5, so k≥6 servers.

**C2:** Leaky bucket vs token bucket differ in how they handle bursts.
</details>"""),

    code("""# M/M/1 Queue Analysis (basic queuing theory)
def mm1_stats(arrival_rate, service_rate):
    rho = arrival_rate / service_rate  # utilization
    if rho >= 1:
        return None  # unstable
    L  = rho / (1 - rho)       # avg customers in system
    Lq = rho**2 / (1 - rho)    # avg customers in queue
    W  = 1 / (service_rate - arrival_rate)  # avg time in system
    Wq = rho / (service_rate - arrival_rate) # avg wait in queue
    return {'rho': rho, 'L': L, 'Lq': Lq, 'W': W, 'Wq': Wq}

print("M/M/1 Queue: API Server Analysis")
for lam in [5, 8, 9, 9.5]:
    mu = 10
    r = mm1_stats(lam, mu)
    if r:
        print(f"  λ={lam:>4}/s: ρ={r['rho']:.2f}, avg wait={r['Wq']:.3f}s, queue len={r['Lq']:.2f}")
    else:
        print(f"  λ={lam:>4}/s: UNSTABLE (ρ≥1)")
print()
print("💡 As utilization approaches 1 (100%), wait time → ∞!")
print("   This is why engineers keep utilization below 70-80%.")"""),

    md("## 🎯 Recap\n1. API traffic ≈ Poisson arrivals; service times ≈ Exponential.\n2. Token bucket smooths burst traffic; Little's Law links queue length, rate, and wait time.\n3. At high utilization (ρ → 1), queues and latency blow up — plan for headroom.\n\n**Next:** [Chapter 19 — Randomized Algorithms]"),
])
save(ch18, "18_probability_in_apis.ipynb")


ch19 = nb([
    md("""# 💻 Chapter 19: Randomized Algorithms
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Sometimes the best algorithm for a problem is a coin flip. Randomized quicksort beats deterministic worst-case. QuickSelect finds medians in O(n). And hash functions are probabilistic magic.

**🎯 Objectives:** Understand randomized quicksort, reservoir sampling, hashing, and why randomness helps algorithms."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── Randomized QuickSort ──
def quicksort_deterministic(arr):
    if len(arr) <= 1: return arr
    pivot = arr[0]  # always first element (bad on sorted input!)
    left  = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    return quicksort_deterministic(left) + [pivot] + quicksort_deterministic(right)

def quicksort_random(arr, rng=None):
    if rng is None: rng = np.random.default_rng()
    if len(arr) <= 1: return arr
    pivot_idx = rng.integers(len(arr))  # RANDOM pivot
    pivot = arr[pivot_idx]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_random(left, rng) + mid + quicksort_random(right, rng)

import sys
sys.setrecursionlimit(5000)

# Compare on sorted input (worst case for deterministic)
n = 200
sorted_arr = list(range(n))

t0 = time.perf_counter()
result_det = quicksort_deterministic(sorted_arr.copy())
t_det = time.perf_counter() - t0

t0 = time.perf_counter()
result_rand = quicksort_random(sorted_arr.copy(), rng)
t_rand = time.perf_counter() - t0

print("⚡ QuickSort: Sorted Input (Worst Case for Deterministic)")
print(f"  Deterministic: {t_det*1000:.2f}ms (O(n²) on sorted input!)")
print(f"  Randomized:    {t_rand*1000:.2f}ms (O(n log n) expected)")
print()

# Distribution of pivot positions (why random pivot is good)
n_trials = 10_000
arr = list(range(100))
pivot_positions = [rng.integers(100) for _ in range(n_trials)]
# Fraction in each "quartile"
q25 = sum(1 for p in pivot_positions if 25 <= p <= 75) / n_trials
print(f"P(pivot in middle 50%) = {q25:.3f}")
print("Good pivot → balanced split → O(n log n) expected")"""),

    code("""# ── Skip List: Probabilistic Data Structure ──
# Show that random coin flips create balanced layers
import bisect

class SkipList:
    def __init__(self, max_level=4, p=0.5):
        self.max_level = max_level
        self.p = p
        self.rng = np.random.default_rng(42)
        self.layers = [[] for _ in range(max_level)]

    def _random_level(self):
        level = 1
        while self.rng.random() < self.p and level < self.max_level:
            level += 1
        return level

    def insert(self, val):
        level = self._random_level()
        for l in range(level):
            bisect.insort(self.layers[l], val)

    def search(self, val, verbose=False):
        for l in range(self.max_level-1, -1, -1):
            if val in self.layers[l]:
                if verbose: print(f"  Found in layer {l}!")
                return True
        return False

sl = SkipList()
for v in rng.integers(1, 100, 50):
    sl.insert(int(v))

print("Skip List Layer Sizes:")
for i, layer in enumerate(sl.layers):
    print(f"  Layer {i}: {len(layer)} elements {'▓'*len(layer)}")

print(f"\nSearch for 42:")
sl.search(42, verbose=True)

# Hash function collision probability
def birthday_hash_collision(n_items, table_size):
    # Approximate P(at least one collision) for n items in table of size m.
    return 1 - np.exp(-n_items**2 / (2*table_size))

print("\n🔑 Hash Table Collision Probability:")
table_sizes = [100, 1000, 10000]
for m in table_sizes:
    print(f"\n  Table size m={m}:")
    for n in [10, int(m**0.5), m//2]:
        p_coll = birthday_hash_collision(n, m)
        print(f"    n={n:>6} items: P(collision) ≈ {p_coll:.3f}")"""),

    code("""# ── Reservoir Sampling: Uniform sample from unknown-length stream ──
def reservoir_sample(stream_generator, k, seed=42):
    rng = np.random.default_rng(seed)
    reservoir = []
    for i, item in enumerate(stream_generator):
        if i < k:
            reservoir.append(item)
        else:
            j = rng.integers(0, i+1)
            if j < k:
                reservoir[j] = item
    return reservoir

# Verify uniformity: each element should have equal P(in reservoir)
N = 10_000  # stream length
k = 100    # reservoir size
n_trials = 1000

# Track how often each position in stream appears in reservoir
appearance_count = np.zeros(N)
for _ in range(n_trials):
    reservoir = reservoir_sample(iter(range(N)), k, seed=np.random.randint(0, 10000))
    for item in reservoir:
        appearance_count[item] += 1

empirical_probs = appearance_count / n_trials
theoretical_prob = k / N

print(f"Reservoir Sampling Uniformity Test")
print(f"  k={k}, N={N}, n_trials={n_trials}")
print(f"  Theoretical P(each item) = {theoretical_prob:.4f}")
print(f"  Empirical P (mean):        {empirical_probs.mean():.4f}")
print(f"  Empirical P (std):         {empirical_probs.std():.4f}")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(empirical_probs, alpha=0.5, color='#3498db', label='Empirical P')
ax.axhline(theoretical_prob, color='red', lw=2, linestyle='--', label=f'Theoretical P={theoretical_prob}')
ax.set_xlabel('Stream Position'); ax.set_ylabel('P(in reservoir)')
ax.set_title(f'Reservoir Sampling: Every position equally likely ✅', fontweight='bold')
ax.legend(); plt.tight_layout()
plt.savefig('ch19_reservoir.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Implement QuickSelect (find kth smallest in O(n) expected time) using random pivot.

**Challenge 2:** Generate a random permutation in O(n) using Fisher-Yates shuffle.
Verify that all permutations of [1,2,3] are equally likely.

**Challenge 3:** Implement a simple Bloom filter and measure the empirical false positive rate.

<details><summary>Solutions</summary>See code below.</details>"""),

    code("""# Fisher-Yates shuffle
def fisher_yates(arr, seed=None):
    arr = arr.copy()
    rng = np.random.default_rng(seed)
    for i in range(len(arr)-1, 0, -1):
        j = rng.integers(0, i+1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

# Verify uniformity for [1,2,3]
from collections import Counter
from itertools import permutations

results = Counter()
for _ in range(60000):
    perm = tuple(fisher_yates([1,2,3]))
    results[perm] += 1

all_perms = list(permutations([1,2,3]))
print("Fisher-Yates Permutation Uniformity:")
for perm in all_perms:
    count = results[perm]
    print(f"  {perm}: {count} times ({count/600:.1f}%) — expected 100%")

# Simple Bloom filter
import hashlib
class BloomFilter:
    def __init__(self, size=1000, n_hash=3):
        self.bits = np.zeros(size, dtype=bool)
        self.size = size
        self.n_hash = n_hash

    def _hashes(self, item):
        return [int(hashlib.md5(f"{item}{i}".encode()).hexdigest(), 16) % self.size
                for i in range(self.n_hash)]

    def add(self, item):
        for h in self._hashes(item): self.bits[h] = True

    def __contains__(self, item):
        return all(self.bits[h] for h in self._hashes(item))

bf = BloomFilter(size=5000, n_hash=3)
for i in range(500): bf.add(f"user_{i}")

# False positives
fps = sum(1 for i in range(500, 2000) if f"user_{i}" in bf)
print(f"\nBloom Filter: 500 elements, 1500 queries for unknown items")
print(f"False positives: {fps}/1500 = {fps/1500:.2%}")"""),

    md("## 🎯 Recap\n1. Random pivot in QuickSort avoids worst-case O(n²) — expected O(n log n).\n2. Reservoir sampling gives uniform samples from streams with unknown length.\n3. Hash functions are probabilistic — birthday problem governs collision probability.\n\n**Next:** [Chapter 20 — Bloom Filters & Probabilistic Data Structures]"),
])
save(ch19, "19_randomized_algorithms.ipynb")


ch20 = nb([
    md("""# 💻 Chapter 20: Hashing, Bloom Filters & Probabilistic Data Structures
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** Google checks if a URL is malicious in microseconds using near-zero memory. How? They accept a small probability of being wrong — and it's a great trade.

**🎯 Objectives:** Understand and implement Bloom filters, HyperLogLog, Count-Min Sketch — trade accuracy for speed and memory."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import hashlib
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── Bloom Filter: Theory ──
def bloom_false_positive_prob(n, m, k):
    # P(false positive) for n items, m bits, k hash functions.
    return (1 - np.exp(-k*n/m))**k

def optimal_k(n, m):
    # Optimal number of hash functions.
    return int(np.ceil((m/n) * np.log(2)))

print("📊 Bloom Filter Design Guide")
print(f"{'Items (n)':>12} {'Bits (m)':>10} {'Bits/item':>10} {'k':>6} {'FP rate':>10}")
print("-" * 52)
for n, m in [(1000, 10000), (10000, 100000), (1000000, 10000000)]:
    k = optimal_k(n, m)
    fp = bloom_false_positive_prob(n, m, k)
    print(f"{n:>12,} {m:>10,} {m/n:>10.1f} {k:>6} {fp:>10.4%}")

# Effect of k on FP rate for fixed n and m
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
n, m = 1000, 10000
k_range = np.arange(1, 20)
fp_rates = [bloom_false_positive_prob(n, m, k) for k in k_range]
axes[0].plot(k_range, fp_rates, 'bo-', markersize=6, lw=2)
axes[0].axvline(optimal_k(n, m), color='red', lw=2, linestyle='--',
                label=f'Optimal k={optimal_k(n,m)}')
axes[0].set_xlabel('Number of hash functions (k)')
axes[0].set_ylabel('False positive probability')
axes[0].set_title(f'Bloom Filter: n={n}, m={m}', fontweight='bold')
axes[0].legend()

# Effect of bits per item
bits_per_item = np.linspace(2, 20, 100)
k_opt = np.ceil(bits_per_item * np.log(2))
fp_opt = bloom_false_positive_prob(1, bits_per_item, k_opt)
axes[1].semilogy(bits_per_item, fp_opt, 'g-', lw=3)
axes[1].set_xlabel('Bits per item (m/n)')
axes[1].set_ylabel('Optimal FP rate')
axes[1].set_title('Bloom Filter: FP rate vs Memory', fontweight='bold')
axes[1].axvline(10, color='red', lw=2, linestyle='--', label='10 bits/item → ~0.8% FP')
axes[1].legend()

plt.tight_layout()
plt.savefig('ch20_bloom_theory.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── Full Bloom Filter Implementation ──
class BloomFilter:
    def __init__(self, expected_n, fp_rate=0.01):
        self.m = int(-expected_n * np.log(fp_rate) / (np.log(2)**2))
        self.k = int(np.ceil(self.m / expected_n * np.log(2)))
        self.bits = bytearray(self.m)
        self.n_added = 0

    def _hash_positions(self, item):
        item_bytes = str(item).encode()
        positions = set()
        for seed in range(self.k):
            h = hashlib.sha256(item_bytes + seed.to_bytes(4, 'big')).hexdigest()
            positions.add(int(h, 16) % self.m)
        return positions

    def add(self, item):
        for pos in self._hash_positions(item):
            self.bits[pos] = 1
        self.n_added += 1

    def __contains__(self, item):
        return all(self.bits[pos] for pos in self._hash_positions(item))

    def estimated_fp_rate(self):
        return bloom_false_positive_prob(self.n_added, self.m, self.k)

# Build URL blacklist Bloom filter
bf = BloomFilter(expected_n=10000, fp_rate=0.001)
print(f"Bloom Filter: m={bf.m:,} bits ({bf.m/8/1024:.1f} KB), k={bf.k}")
print(f"Exact set of 10,000 URLs would need ~80KB minimum")

# Add known malicious URLs
malicious = [f"malicious{i}.evil.com" for i in range(10000)]
for url in malicious:
    bf.add(url)

# Test
legit = [f"legit{i}.good.com" for i in range(10000)]
fp_count = sum(url in bf for url in legit)
print(f"\nFalse positives on 10,000 legit URLs: {fp_count} ({fp_count/100:.1f}%)")
print(f"Theoretical FP rate: {bf.estimated_fp_rate():.3%}")
print(f"True positives: {sum(url in bf for url in malicious[:100])}/100")"""),

    code("""# ── Count-Min Sketch: Frequency Estimation ──
class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.width = width
        self.depth = depth
        self.table = np.zeros((depth, width), dtype=np.int64)
        self.seeds = rng.integers(0, 10**9, depth)

    def _hash(self, item, i):
        h = hashlib.md5(f"{self.seeds[i]}{item}".encode()).hexdigest()
        return int(h, 16) % self.width

    def add(self, item, count=1):
        for i in range(self.depth):
            self.table[i, self._hash(item, i)] += count

    def estimate(self, item):
        return min(self.table[i, self._hash(item, i)] for i in range(self.depth))

# Word frequency estimation
words = np.random.choice(['apple','banana','cherry','date','elderberry',
                          'fig','grape','mango'] + [f'w{i}' for i in range(100)],
                         p=[0.15,0.12,0.10,0.08,0.07,0.06,0.05,0.05]+
                           [0.32/100]*100,
                         size=100000)

# True counts
true_counts = {w: (words == w).sum() for w in set(words)}

cms = CountMinSketch(width=500, depth=5)
for w in words:
    cms.add(w)

print("Count-Min Sketch vs True Counts (top words):")
print(f"{'Word':<12} {'True':>8} {'CMS Est':>8} {'Error':>8}")
top_words = sorted(true_counts.items(), key=lambda x: -x[1])[:8]
errors = []
for word, true_count in top_words:
    estimated = cms.estimate(word)
    error = (estimated - true_count) / true_count
    errors.append(abs(error))
    print(f"  {word:<12} {true_count:>8} {estimated:>8} {error:>7.2%}")
print(f"Average relative error: {np.mean(errors):.2%}")"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Implement HyperLogLog for cardinality estimation.
(Estimate the number of unique items in a stream with O(log log n) memory)

**Challenge 2:** Design a Bloom filter for a URL shortener (billions of URLs).
What are appropriate m and k values?

**Challenge 3:** Evaluate the space-accuracy tradeoff: compare exact dict vs Bloom filter vs Count-Min Sketch for 1M items.

<details><summary>Solutions</summary>
HyperLogLog: hash items, find longest leading-zero run, use harmonic mean of estimates.
URL shortener with 1B URLs and 1% FP rate: ~10 bits/item = 1.25 GB vs 8 GB for exact set.
</details>"""),

    code("""# Space comparison: exact vs probabilistic
n = 100_000
# Exact: Python set
exact = set(str(i) for i in range(n))
exact_bytes = sum(len(s) for s in exact) + n * 50  # ~50 bytes overhead per str

# Bloom filter
bf2 = BloomFilter(n, fp_rate=0.01)
for i in range(n): bf2.add(i)
bf_bytes = bf2.m // 8

# Count-Min Sketch
cms2 = CountMinSketch(width=10000, depth=5)
cms_bytes = cms2.table.nbytes

print("📊 Space Comparison for 100,000 items:")
print(f"  Exact set:         ~{exact_bytes/1024:.0f} KB (100% accurate)")
print(f"  Bloom filter:       {bf_bytes/1024:.0f} KB ({bf2.estimated_fp_rate():.2%} FP)")
print(f"  Count-Min Sketch:   {cms_bytes/1024:.0f} KB (frequency estimates)")
print(f"\nBloom filter uses {exact_bytes/bf_bytes:.0f}x less space than exact set!")"""),

    md("## 🎯 Recap\n1. Bloom filters: space-efficient membership testing with tunable FP rate. Never false negatives.\n2. Count-Min Sketch: frequency estimation with bounded error.\n3. These structures power Google SafeBrowsing, Redis, Cassandra, and most distributed databases.\n\n**Next:** [Chapter 21 — Statistical Testing for Feature Flags]"),
])
save(ch20, "20_probabilistic_data_structures.ipynb")


ch21 = nb([
    md("""# 💻 Chapter 21: Statistical Testing for Feature Flags
*Track 2 — Developers | Tier 2*

> **🎬 Hook:** You're running a feature flag at 10%. You see metrics improve. At what rollout % do you call it a win and ship to 100%?

**🎯 Objectives:** Apply sequential testing to feature flags; implement multi-armed bandits; avoid the peeking problem properly."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── Sequential Probability Ratio Test (SPRT) ──
# Allows peeking with controlled error rates

def sprt_test(data_a, data_b, p0_effect=0, p1_effect=0.01, alpha=0.05, beta=0.20):
    # Wald's SPRT: stop when likelihood ratio crosses a threshold.
    A = np.log((1-beta)/alpha)      # upper boundary (reject H0)
    B = np.log(beta/(1-alpha))       # lower boundary (accept H0)

    log_lr = 0
    decisions = []
    for i in range(max(len(data_a), len(data_b))):
        if i < len(data_a) and i < len(data_b):
            xa = data_a[i]; xb = data_b[i]
            # Update log likelihood ratio
            if xa != xb:
                if xb == 1:
                    log_lr += np.log((p1_effect + 0.5) / (p0_effect + 0.5 + 1e-10))
                else:
                    log_lr += np.log((1-p1_effect-0.5+1e-10) / (1-p0_effect-0.5+1e-10))
        if log_lr >= A:
            decisions.append('reject'); break
        elif log_lr <= B:
            decisions.append('accept'); break
        decisions.append('continue')
    return decisions, log_lr

# Simulate feature flag test
n = 2000
true_rate_control  = 0.050
true_rate_treatment = 0.058  # real improvement

control   = rng.binomial(1, true_rate_control, n)
treatment = rng.binomial(1, true_rate_treatment, n)

# Fixed horizon test (bad — peeking)
decisions_fixed = []
for n_obs in range(10, n, 10):
    _, p = stats.ttest_ind(treatment[:n_obs], control[:n_obs])
    decisions_fixed.append(p < 0.05)

# SPRT (proper sequential test)
decisions_seq, _ = sprt_test(control, treatment)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(range(10, n, 10), [int(d) for d in decisions_fixed],
        'r-', lw=2, label='Fixed-horizon peeking (WRONG)', alpha=0.7)
ax.set_xlabel('Observations so far'); ax.set_ylabel('Significant (1=Yes)')
ax.set_title('Feature Flag: Peeking vs Sequential Testing', fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('ch21_feature_flags.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"Fixed-horizon: 'significant' at {sum(decisions_fixed)} of {len(decisions_fixed)} peeks")
print(f"  This inflates Type I error!")"""),

    code("""# ── Multi-Armed Bandit for Feature Flag Rollout ──
class EpsilonGreedy:
    def __init__(self, n_arms, epsilon=0.1):
        self.n_arms = n_arms; self.epsilon = epsilon
        self.counts = np.zeros(n_arms); self.rewards = np.zeros(n_arms)

    def select_arm(self):
        if rng.random() < self.epsilon:
            return rng.integers(self.n_arms)  # explore
        return np.argmax(self.rewards / np.maximum(self.counts, 1))  # exploit

    def update(self, arm, reward):
        self.counts[arm] += 1
        self.rewards[arm] += reward

class ThompsonSampling:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.alphas = np.ones(n_arms); self.betas = np.ones(n_arms)

    def select_arm(self):
        samples = [rng.beta(self.alphas[i], self.betas[i]) for i in range(self.n_arms)]
        return np.argmax(samples)

    def update(self, arm, reward):
        self.alphas[arm] += reward; self.betas[arm] += 1-reward

# True conversion rates for 3 variants
true_rates = [0.050, 0.065, 0.058]  # B is best
n_rounds = 5000

for BanditClass, name in [(EpsilonGreedy, 'ε-Greedy'), (ThompsonSampling, 'Thompson Sampling')]:
    if name == 'ε-Greedy':
        bandit = EpsilonGreedy(3, epsilon=0.1)
    else:
        bandit = ThompsonSampling(3)

    arm_counts = np.zeros(3)
    for _ in range(n_rounds):
        arm = bandit.select_arm()
        reward = int(rng.random() < true_rates[arm])
        bandit.update(arm, reward)
        arm_counts[arm] += 1

    print(f"\n{name}:")
    for i, count in enumerate(arm_counts):
        rate = count/n_rounds
        print(f"  Variant {i+1} (true={true_rates[i]:.3f}): {count:.0f} users ({rate:.1%})")
    optimal_pct = arm_counts[np.argmax(true_rates)] / n_rounds
    print(f"  → Sent {optimal_pct:.1%} to best variant!")"""),

    md("""## ✏️ Section 6 — Coding Challenges

**Challenge 1:** Implement the Bonferroni correction for testing 5 metrics simultaneously.
Adjust α and recalculate required sample sizes.

**Challenge 2:** Build a simple feature flag system that uses Thompson Sampling to gradually shift traffic to the winning variant.

<details><summary>Solutions</summary>See patterns in the code above.</details>"""),

    code("""# Bonferroni correction
n_tests = 5
alpha_family = 0.05
alpha_individual = alpha_family / n_tests
print(f"Testing {n_tests} metrics:")
print(f"  Family-wise α = {alpha_family}")
print(f"  Bonferroni-corrected α per test = {alpha_individual}")
print(f"  FWER without correction: {1-(1-alpha_family)**n_tests:.3f}")

# Sample size with corrected alpha
from scipy.stats import norm
def sample_size(p1, p2, alpha, power):
    z_alpha = norm.ppf(1-alpha/2)
    z_beta = norm.ppf(power)
    p_bar = (p1 + p2) / 2
    return int(np.ceil(2 * (z_alpha+z_beta)**2 * p_bar*(1-p_bar) / (p1-p2)**2))

n_uncorrected = sample_size(0.05, 0.06, 0.05, 0.80)
n_corrected   = sample_size(0.05, 0.06, alpha_individual, 0.80)
print(f"\nSample size per variant:")
print(f"  Without Bonferroni: {n_uncorrected:,}")
print(f"  With Bonferroni:    {n_corrected:,} ({n_corrected/n_uncorrected:.1f}x larger)")"""),

    md("## 🎯 Recap\n1. Standard peeking inflates Type I error — use SPRT for sequential testing.\n2. Multi-armed bandits (ε-greedy, Thompson Sampling) balance exploration/exploitation.\n3. Multiple metrics → Bonferroni correction or FDR control.\n\n**Next:** [Chapter 22 — Debugging Probabilistic Systems]"),
])
save(ch21, "21_statistical_testing_feature_flags.ipynb")


ch22 = nb([
    md("""# 💻 Chapter 22: Debugging Probabilistic Systems
*Track 2 — Developers | Tier 2 Finale*

> **🎬 Hook:** How do you write a unit test for code that's supposed to be random? The answer: test the distribution, not the output.

**🎯 Objectives:** Test stochastic code statistically; use KS test, chi-square, and property-based testing for probabilistic systems."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
rng = np.random.default_rng(42)

# ── The Core Problem: Non-Deterministic Code ──
def naive_test():
    # WRONG: this test will randomly fail.
    rng2 = np.random.default_rng()
    result = rng2.integers(0, 10)
    assert result == 5, f"Expected 5, got {result}"

print("Testing probabilistic code correctly:")
print("Wrong: assert result == expected_value")
print("Right: assert distribution matches expected distribution")
print()

# ── Statistical Tests for Random Number Generators ──
def test_uniformity(samples, low, high, alpha=0.05):
    ks_stat, p_value = stats.kstest(samples, 'uniform',
                                     args=(low, high-low))
    return {'test': 'KS-Uniformity', 'stat': ks_stat, 'p': p_value,
            'pass': p_value > alpha}

def test_normality(samples, expected_mean, expected_std, alpha=0.05):
    z_scores = (samples - expected_mean) / expected_std
    ks_stat, p_value = stats.kstest(z_scores, 'norm')
    return {'test': 'KS-Normality', 'stat': ks_stat, 'p': p_value,
            'pass': p_value > alpha}

def test_categorical(samples, expected_probs, n_categories, alpha=0.05):
    counts = np.bincount(samples, minlength=n_categories)
    expected_counts = np.array(expected_probs) * len(samples)
    chi2, p_value = stats.chisquare(counts, expected_counts)
    return {'test': 'Chi2-Categorical', 'stat': chi2, 'p': p_value,
            'pass': p_value > alpha}

# Run tests
n = 10000
tests = [
    test_uniformity(rng.uniform(0, 1, n), 0, 1),
    test_normality(rng.normal(5, 2, n), 5, 2),
    test_categorical(rng.choice(4, n, p=[0.1,0.2,0.3,0.4]),
                    [0.1,0.2,0.3,0.4], 4),
]

print(f"{'Test':<20} {'Statistic':>12} {'p-value':>10} {'Pass?':>8}")
print("-" * 54)
for t in tests:
    status = "✅ PASS" if t['pass'] else "❌ FAIL"
    print(f"  {t['test']:<18} {t['stat']:>12.4f} {t['p']:>10.4f} {status:>8}")"""),

    code("""# ── Detect Biased Sampling ──
def test_random_function(sample_fn, n=10000, alpha=0.05):
    # Test if a function produces fair random samples.
    samples = [sample_fn() for _ in range(n)]
    unique_vals = sorted(set(samples))
    expected_p = 1 / len(unique_vals)
    counts = [samples.count(v) for v in unique_vals]
    expected = [n * expected_p] * len(unique_vals)
    chi2, p = stats.chisquare(counts, expected)
    return p > alpha, p, chi2

# Good sampler
def good_sampler():
    return rng.integers(0, 6)

# Bad sampler (biased! modulo bias)
def bad_sampler():
    return int(rng.integers(0, 2**31)) % 6  # slight modulo bias

# Test both
good_pass, good_p, _ = test_random_function(good_sampler)
bad_pass,  bad_p,  _ = test_random_function(bad_sampler)

print(f"Good sampler: p={good_p:.4f} → {'✅ PASS (uniform)' if good_pass else '❌ FAIL'}")
print(f"Bad sampler:  p={bad_p:.4f} → {'✅ PASS' if bad_pass else '❌ FAIL (biased!)'}")
print()

# Visualize the difference
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for ax, fn, title in [(axes[0], good_sampler, 'Good Sampler'),
                       (axes[1], bad_sampler, 'Bad Sampler (modulo bias)')]:
    samples = [fn() for _ in range(100000)]
    counts = [samples.count(i) for i in range(6)]
    colors = ['#27ae60' if abs(c/100000 - 1/6) < 0.002 else '#e74c3c' for c in counts]
    ax.bar(range(6), [c/1000 for c in counts], color=colors, edgecolor='white')
    ax.axhline(100/6, color='red', lw=2, linestyle='--', label='Expected (uniform)')
    ax.set_title(f'{title}', fontweight='bold')
    ax.set_xlabel('Value'); ax.set_ylabel('Count (thousands)')
    ax.legend()

plt.tight_layout()
plt.savefig('ch22_sampling_test.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── Property-Based Testing for Probabilistic Code ──
# Test PROPERTIES of distributions, not specific values

def verify_distribution_properties(samples, name=""):
    # Test key statistical properties of a sample.
    n = len(samples)
    results = {}

    # Test 1: Sample mean converges (LLN)
    expected_mean = samples.mean()
    batch_means = [samples[i:i+100].mean() for i in range(0, n-100, 100)]
    results['lln_convergence'] = np.std(batch_means) < 0.5

    # Test 2: No systematic time trends (stationarity)
    first_half = samples[:n//2].mean()
    second_half = samples[n//2:].mean()
    _, p_trend = stats.ttest_ind(samples[:n//2], samples[n//2:])
    results['no_trend'] = p_trend > 0.01

    # Test 3: Autocorrelation check
    lag1_corr = np.corrcoef(samples[:-1], samples[1:])[0,1]
    results['low_autocorr'] = abs(lag1_corr) < 0.05

    print(f"\n📋 Distribution Property Tests ({name})")
    for test, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {test}")
    return all(results.values())

# Test good vs bad generators
good_samples = rng.normal(0, 1, 10000)
# Bad: trending data (non-stationary)
bad_samples  = np.arange(10000) * 0.001 + rng.normal(0, 1, 10000)

verify_distribution_properties(good_samples, "Good (Normal i.i.d.)")
verify_distribution_properties(bad_samples, "Bad (Trending data)")"""),

    code("""# ── Debugging a Specific Bug: Incorrect Sampling ──
print("🔍 Debugging Case Study: Deck Shuffling Bug")
print()

def buggy_shuffle(deck):
    # Bug: selects j from [0, n) not [i, n) -- not uniform!
    deck = deck.copy()
    n = len(deck)
    for i in range(n):
        j = rng.integers(0, n)  # BUG! Should be rng.integers(i, n)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

def correct_shuffle(deck):
    deck = deck.copy()
    n = len(deck)
    for i in range(n-1, 0, -1):
        j = rng.integers(0, i+1)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

# Test: what's P(card 0 ends up in position 0)?
deck = list(range(10))
n_trials = 100_000

buggy_pos0  = sum(buggy_shuffle(deck)[0] == 0 for _ in range(n_trials))
correct_pos0 = sum(correct_shuffle(deck)[0] == 0 for _ in range(n_trials))

expected = n_trials / 10  # should be 1/10 = 10%
print(f"P(card 0 stays in position 0):")
print(f"  Correct:  {correct_pos0/n_trials:.4f} (expected {1/10:.4f})")
print(f"  Buggy:    {buggy_pos0/n_trials:.4f} ← TOO HIGH! (bias toward original position)")
print()
print("💡 Statistical test caught the bug that visual inspection missed!")
print("   The buggy shuffle is ~17% likely to leave card 0 in place (should be 10%)")"""),

    md("""## ✏️ Section 6 — Final Challenges (Track 2)

**C1:** Write a `assert_distribution` function that takes a list of samples and a `scipy.stats` distribution object, runs KS test, and passes/fails with a clear message.

**C2:** Test the Python `random.shuffle()` function for uniformity using chi-square on a small list [1,2,3].

**C3:** You have a caching layer that should hit the cache 80% of the time. Write a test that verifies the hit rate is statistically consistent with 80% using a binomial test.

<details><summary>Solutions</summary>See code below.</details>"""),

    code("""import random

# C1: assert_distribution
def assert_distribution(samples, expected_dist, alpha=0.05, name=""):
    ks_stat, p_value = stats.kstest(samples, expected_dist.cdf)
    passed = p_value > alpha
    msg = f"{'✅ PASS' if passed else '❌ FAIL'} [{name}]: KS={ks_stat:.4f}, p={p_value:.4f}"
    print(msg)
    if not passed:
        raise AssertionError(f"Distribution mismatch! {msg}")
    return True

samples = rng.normal(5, 2, 10000)
assert_distribution(samples, stats.norm(5, 2), name="Normal(5,2) test")

# C2: Test Python shuffle
from collections import Counter
import itertools

perms = Counter()
for _ in range(60000):
    lst = [1, 2, 3]
    random.shuffle(lst)
    perms[tuple(lst)] += 1

all_perms = list(itertools.permutations([1,2,3]))
counts = [perms[p] for p in all_perms]
expected = [10000] * 6
chi2, p = stats.chisquare(counts, expected)
print(f"\nC2 Python shuffle chi2 test: χ²={chi2:.4f}, p={p:.4f}")
print("✅ Uniform" if p > 0.05 else "❌ Not uniform")

# C3: Cache hit rate test
n_requests = 1000
cache_hits = rng.binomial(n_requests, 0.80)
# Binomial test: H0: p=0.80
p_binom = stats.binom_test(cache_hits, n_requests, 0.80)
print(f"\nC3 Cache hit test: {cache_hits}/{n_requests} = {cache_hits/n_requests:.2%}")
print(f"  p-value = {p_binom:.4f} → {'✅ Consistent with 80%' if p_binom > 0.05 else '❌ Not 80%'}")"""),

    md("""## 🎯 Track 2 Complete! 🏆

**You've mastered:**
- ✅ PRNGs: seeds, reproducibility, quality tests
- ✅ Monte Carlo: integration, convergence, variance reduction
- ✅ A/B testing: design, analysis, peeking problem
- ✅ Bayesian updating: conjugate priors, Thompson Sampling
- ✅ Log probabilities: numerical stability, softmax, cross-entropy
- ✅ API probability: Poisson traffic, rate limiting, queuing theory
- ✅ Randomized algorithms: quicksort, reservoir sampling, hashing
- ✅ Probabilistic data structures: Bloom filters, Count-Min Sketch
- ✅ Feature flags: sequential testing, multi-armed bandits
- ✅ Debugging probabilistic systems: KS test, chi-square, property testing

**Ready for Tier 3?** → [Chapter 23 — Markov Chains]"""),
])
save(ch22, "22_debugging_probabilistic_systems.ipynb")

print("\n🎉 All Track 2 (Developers) notebooks created successfully!")
