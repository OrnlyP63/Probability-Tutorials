"""Generate Tier 2 — Engineers track notebooks (chapters 13-22)."""
import json
from pathlib import Path

HERE = Path(__file__).parent


def src(text):
    lines = text.strip().split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": src(text)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "source": src(text),
            "outputs": [], "execution_count": None}


def nb(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
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
    print(f"  ✅ {name}")


# ── Chapter 13 ────────────────────────────────────────────────────────────────
ch13 = nb([
    md("""# Chapter 13 — Reliability & Failure Probability
*Track 4: Engineers*

## 🎯 Learning Objectives
- Model component failure using probability distributions
- Compute system reliability for series and parallel configurations
- Understand MTTF, MTBF, and failure rate functions"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Reliability Function

The **reliability function** $R(t)$ is the probability that a component
survives past time $t$:
$$R(t) = P(T > t) = 1 - F(t)$$

The **failure rate** (hazard rate):
$$h(t) = \\frac{f(t)}{R(t)}$$

**Bathtub curve** — three phases:
1. **Infant mortality** (decreasing h): early defects
2. **Useful life** (constant h): random failures → Exponential distribution
3. **Wear-out** (increasing h): aging → Weibull distribution"""),

    code("""t = np.linspace(0, 100, 500)

# Bathtub curve (sum of decreasing + constant + increasing hazard)
h_infant   = 0.05 * np.exp(-0.08 * t)
h_useful   = 0.005 * np.ones_like(t)
h_wearout  = 0.002 * np.exp(0.03 * (t - 60)) * (t > 60)
h_bathtub  = h_infant + h_useful + h_wearout

plt.figure(figsize=(10, 4))
plt.plot(t, h_bathtub, lw=2)
plt.fill_between(t[:100], h_bathtub[:100], alpha=0.3, color="red",   label="Infant mortality")
plt.fill_between(t[100:300], h_bathtub[100:300], alpha=0.3, color="green", label="Useful life")
plt.fill_between(t[300:], h_bathtub[300:], alpha=0.3, color="orange", label="Wear-out")
plt.xlabel("Time"); plt.ylabel("Hazard rate h(t)")
plt.title("Bathtub Curve — System Failure Rate over Time")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Exponential & Weibull

**Exponential** (constant hazard, memoryless):
$$R(t) = e^{-\\lambda t}, \\quad \\text{MTTF} = \\frac{1}{\\lambda}$$

**Weibull** (generalised — shape $k$, scale $\\lambda$):
$$R(t) = e^{-(t/\\lambda)^k}$$
- $k < 1$: decreasing hazard (infant mortality)
- $k = 1$: constant hazard (exponential)
- $k > 1$: increasing hazard (wear-out)"""),

    code("""t_range = np.linspace(0, 5, 300)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Weibull reliability
for k in [0.5, 1.0, 2.0, 3.5]:
    R = np.exp(-(t_range)**k)
    axes[0].plot(t_range, R, label=f"k={k}")
axes[0].set_xlabel("t/λ"); axes[0].set_ylabel("R(t)")
axes[0].set_title("Weibull Reliability Function"); axes[0].legend()

# Weibull hazard
for k in [0.5, 1.0, 2.0, 3.5]:
    dist = stats.weibull_min(k)
    h = dist.pdf(t_range) / (dist.sf(t_range) + 1e-10)
    axes[1].plot(t_range, h, label=f"k={k}")
axes[1].set_ylim(0, 5); axes[1].set_xlabel("t/λ")
axes[1].set_ylabel("h(t)"); axes[1].set_title("Weibull Hazard Function")
axes[1].legend()
plt.tight_layout(); plt.show()"""),

    md("""## 3. Simulation — Series vs Parallel System Reliability"""),

    code("""# Series: system fails if ANY component fails
# Parallel: system fails only if ALL components fail

def series_reliability(component_reliabilities):
    return np.prod(component_reliabilities)

def parallel_reliability(component_reliabilities):
    return 1 - np.prod(1 - np.array(component_reliabilities))

R_comp = 0.95  # individual component reliability
n_range = range(1, 11)

series  = [series_reliability([R_comp]*n) for n in n_range]
parallel = [parallel_reliability([R_comp]*n) for n in n_range]

plt.figure(figsize=(9, 5))
plt.plot(list(n_range), series,   "r-o", label="Series (fails if any fails)")
plt.plot(list(n_range), parallel, "b-o", label="Parallel (fails only if all fail)")
plt.axhline(R_comp, ls="--", color="gray", label=f"Single component R={R_comp}")
plt.xlabel("Number of components"); plt.ylabel("System Reliability")
plt.title("Series vs Parallel System Reliability (R=0.95 per component)")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 4–6. Monte Carlo Simulation, Real Analysis & Practice"""),

    code("""# Monte Carlo life testing simulation
n_components = 1000
mttf = 1000  # hours
failure_times = rng.exponential(mttf, n_components)

print(f"Simulated MTTF: {failure_times.mean():.1f} hours (true={mttf})")
print(f"R(500): simulated={np.mean(failure_times > 500):.4f}, analytic={np.exp(-500/mttf):.4f}")
print(f"R(1000): simulated={np.mean(failure_times > 1000):.4f}, analytic={np.exp(-1):.4f}")

# Fit Weibull to failure data (with wear-out)
failure_wearout = rng.weibull(2.5, n_components) * 800 + 200
shape, loc, scale = stats.weibull_min.fit(failure_wearout, floc=0)
print(f"\nWeibull fit: shape={shape:.2f}, scale={scale:.0f}")
print(f"MTTF estimate: {scale * stats.gamma(1 + 1/shape):.0f} hours")"""),

    code("""# Practice P1: Compute MTTF and B10 life for a pump
lam_pump = 1/2000  # failure rate: 1 failure per 2000 hours
MTTF = 1/lam_pump
B10_life = -np.log(0.90) / lam_pump  # time when 10% have failed
print(f"Pump MTTF: {MTTF:.0f} hours")
print(f"B10 life (10% failure): {B10_life:.0f} hours")

# Practice P2: 4-component series system
R_each = np.array([0.99, 0.97, 0.98, 0.995])
R_series = series_reliability(R_each)
print(f"\n4-component series reliability: {R_series:.4f}")
print(f"System unreliability: {1-R_series:.4f}")"""),
])
save(ch13, "13_reliability_failure_probability.ipynb")


# ── Chapter 14 ────────────────────────────────────────────────────────────────
ch14 = nb([
    md("""# Chapter 14 — Poisson Processes in Systems
*Track 4: Engineers*

## 🎯 Learning Objectives
- Model random event arrivals with the Poisson process
- Derive inter-arrival times and their exponential distribution
- Apply to server requests, hardware failures, and network packets"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — The Poisson Process

A **Poisson process** with rate $\\lambda$ satisfies:
1. **Independence**: events in non-overlapping intervals are independent
2. **Stationarity**: rate is constant over time
3. **Singularity**: no two events at the same instant

**Key results:**
- Number of events in time $t$: $N(t) \\sim \\text{Poisson}(\\lambda t)$
- Inter-arrival time: $T \\sim \\text{Exp}(\\lambda)$ (memoryless!)
- Merging two Poisson processes ($\\lambda_1$, $\\lambda_2$) → $\\text{Poisson}(\\lambda_1 + \\lambda_2)$"""),

    code("""# Simulate a Poisson process
lambda_rate = 3  # events per unit time
T_max = 20

inter_arrivals = rng.exponential(1/lambda_rate, 200)
arrival_times = np.cumsum(inter_arrivals)
arrival_times = arrival_times[arrival_times <= T_max]

# Count process N(t)
t_grid = np.linspace(0, T_max, 1000)
N_t = np.array([np.sum(arrival_times <= t) for t in t_grid])

fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].step(t_grid, N_t, where="post")
axes[0].set_xlabel("Time"); axes[0].set_ylabel("N(t)")
axes[0].set_title(f"Poisson Process (λ={lambda_rate})")

axes[1].hist(inter_arrivals[:50], bins=20, density=True, alpha=0.6)
t_range = np.linspace(0, 2, 200)
axes[1].plot(t_range, stats.expon.pdf(t_range, scale=1/lambda_rate), "r-", lw=2,
             label=f"Exp(λ={lambda_rate})")
axes[1].set_title("Inter-arrival Times"); axes[1].legend()
plt.tight_layout(); plt.show()

print(f"Expected arrivals in T={T_max}: {lambda_rate*T_max:.0f}")
print(f"Simulated arrivals: {len(arrival_times)}")"""),

    md("""## 2. Math Walkthrough — Poisson PMF Derivation

Starting from the binomial: divide $[0,t]$ into $n$ tiny intervals of size $\\Delta t = t/n$.

$$P(N(t) = k) = \\binom{n}{k}(\\lambda\\Delta t)^k (1-\\lambda\\Delta t)^{n-k}$$

As $n \\to \\infty$:
$$P(N(t) = k) = \\frac{(\\lambda t)^k e^{-\\lambda t}}{k!}$$"""),

    code("""# Verify: Poisson counts in windows
lambda_rate = 5
window_size = 1.0
n_windows = 5000
counts = rng.poisson(lambda_rate * window_size, n_windows)

k_range = range(0, 15)
empirical = [np.mean(counts == k) for k in k_range]
theoretical = [stats.poisson.pmf(k, lambda_rate) for k in k_range]

plt.bar([k-0.2 for k in k_range], empirical, width=0.4, alpha=0.7, label="Simulated")
plt.bar([k+0.2 for k in k_range], theoretical, width=0.4, alpha=0.7, label="Theoretical")
plt.xlabel("Count"); plt.ylabel("Probability")
plt.title(f"Poisson(λ={lambda_rate}) — Empirical vs Theoretical")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 3–6. Applications in Engineering"""),

    code("""# Server failure events — non-homogeneous Poisson process (time-varying rate)
T_hours = 24
t_fine = np.linspace(0, T_hours, 1000)

# Rate varies with time of day (peak at 9am and 9pm)
def lambda_t(t):
    return 2 + 5*np.exp(-0.5*(t-9)**2/4) + 3*np.exp(-0.5*(t-21)**2/4)

plt.figure(figsize=(10, 4))
plt.plot(t_fine, lambda_t(t_fine), lw=2)
plt.fill_between(t_fine, lambda_t(t_fine), alpha=0.3)
plt.xlabel("Hour of day"); plt.ylabel("Event rate λ(t)")
plt.title("Non-Homogeneous Poisson Process — Server Events Over 24 Hours")
plt.tight_layout(); plt.show()

# Total expected events
from scipy.integrate import quad
total_expected, _ = quad(lambda_t, 0, T_hours)
print(f"Total expected events in 24h: {total_expected:.0f}")"""),

    code("""# Network packet arrivals — test if Poisson assumption holds
packet_gaps = rng.exponential(0.001, 2000)  # 1ms mean inter-arrival (1000 pps)

# Test: Poisson requires exponential inter-arrivals
D_stat, p_val = stats.kstest(packet_gaps, "expon",
                              args=(packet_gaps.min(), packet_gaps.mean() - packet_gaps.min()))
print(f"KS test for exponential inter-arrivals: D={D_stat:.4f}, p={p_val:.4f}")
print("Poisson assumption ✅ plausible" if p_val > 0.05 else "Poisson assumption ❌ rejected")

# Compound Poisson: burst packets (each arrival brings a batch)
batch_sizes = rng.geometric(0.3, 500)
total_packets = batch_sizes.sum()
print(f"\nBurst traffic: {len(batch_sizes)} arrivals, {total_packets} total packets")
print(f"Mean batch size: {batch_sizes.mean():.2f}")"""),

    code("""# Practice
lambda_sys = 0.5  # failures per day
# P(zero failures in a week)
p_zero = stats.poisson.pmf(0, lambda_sys*7)
print(f"P(0 failures in 7 days): {p_zero:.4f}")
# Expected wait for 3rd failure
from scipy.stats import erlang
mttf_3rd = 3 / lambda_sys
print(f"Expected time to 3rd failure: {mttf_3rd:.1f} days")
# Inter-arrival 90th percentile
p90 = stats.expon.ppf(0.90, scale=1/lambda_sys)
print(f"90th percentile inter-arrival time: {p90:.2f} days")"""),
])
save(ch14, "14_poisson_processes.ipynb")


# ── Chapter 15 ────────────────────────────────────────────────────────────────
ch15 = nb([
    md("""# Chapter 15 — Queuing Theory Basics
*Track 4: Engineers*

## 🎯 Learning Objectives
- Understand the M/M/1 queue and Little's Law
- Compute average queue length, wait time, and utilisation
- Model real engineering bottlenecks"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — The M/M/1 Queue

**Kendall notation:** M/M/1
- First M: Markovian (Poisson) arrivals with rate $\\lambda$
- Second M: Markovian (Exponential) service with rate $\\mu$
- 1: single server

**Steady-state results (valid when ρ = λ/μ < 1):**

| Metric | Formula |
|--------|---------|
| Utilisation | $\\rho = \\lambda/\\mu$ |
| Avg. customers in system | $L = \\rho/(1-\\rho)$ |
| Avg. customers in queue | $L_q = \\rho^2/(1-\\rho)$ |
| Avg. time in system | $W = 1/(\\mu - \\lambda)$ |
| Avg. wait in queue | $W_q = \\lambda/[\\mu(\\mu-\\lambda)]$ |

**Little's Law** (works for any stable queue): $L = \\lambda W$"""),

    code("""# M/M/1 metrics as a function of utilisation
rho_values = np.linspace(0.01, 0.99, 200)

L  = rho_values / (1 - rho_values)       # avg customers in system
Lq = rho_values**2 / (1 - rho_values)    # avg queue length

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(rho_values, L,  lw=2, label="L (in system)")
axes[0].plot(rho_values, Lq, lw=2, label="Lq (in queue)")
axes[0].axvline(0.8, color="red", linestyle="--", label="ρ=0.8")
axes[0].set_xlabel("Utilisation ρ"); axes[0].set_ylabel("Average customers")
axes[0].set_ylim(0, 20); axes[0].legend()
axes[0].set_title("M/M/1: Average Queue vs Utilisation")

# Service time = 1/mu = 1, vary lambda
mu = 1.0
lambdas = np.linspace(0.01, 0.99, 200)
W = 1 / (mu - lambdas)
axes[1].plot(lambdas, W, lw=2)
axes[1].set_xlabel("Arrival rate λ"); axes[1].set_ylabel("Avg. time in system W")
axes[1].set_ylim(0, 30); axes[1].set_title("M/M/1: Sojourn Time vs Arrival Rate (μ=1)")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Deriving L from Balance Equations

For M/M/1 with $\\rho < 1$, steady-state probabilities:
$$\\pi_n = (1-\\rho)\\rho^n$$

Then:
$$L = \\sum_{n=0}^\\infty n \\pi_n = (1-\\rho)\\rho \\frac{d}{d\\rho}\\left(\\sum_{n=0}^\\infty \\rho^n\\right) = \\frac{\\rho}{1-\\rho}$$"""),

    code("""# Verify analytically
rho = 0.7
pi_n = [(1-rho)*rho**n for n in range(1000)]
L_direct = sum(n*p for n, p in enumerate(pi_n))
L_formula = rho / (1 - rho)
print(f"L from summation: {L_direct:.4f}")
print(f"L from formula:   {L_formula:.4f}")"""),

    code("""# Discrete-event simulation of M/M/1 queue
def simulate_mm1(lam, mu, n_customers=5000):
    arrivals = np.cumsum(rng.exponential(1/lam, n_customers))
    services = rng.exponential(1/mu, n_customers)
    start = np.zeros(n_customers)
    finish = np.zeros(n_customers)
    for i in range(n_customers):
        start[i] = max(arrivals[i], finish[i-1]) if i > 0 else arrivals[i]
        finish[i] = start[i] + services[i]
    wait = start - arrivals
    sojourn = finish - arrivals
    return wait.mean(), sojourn.mean()

lam, mu = 0.7, 1.0
rho = lam/mu
w_q_sim, w_sim = simulate_mm1(lam, mu)
print(f"ρ={rho:.1f}")
print(f"Simulated Wq={w_q_sim:.3f}, theory={lam/(mu*(mu-lam)):.3f}")
print(f"Simulated W={w_sim:.3f},  theory={1/(mu-lam):.3f}")"""),

    code("""# Real-world: web server capacity planning
def capacity_plan(lam_peak, mu, sla_wait):
    # Find min servers needed to meet SLA (avg wait < sla_wait).
    for c in range(1, 20):
        rho_c = lam_peak / (c * mu)
        if rho_c >= 1:
            continue
        # M/M/c Erlang-C approximation
        # P0 calculation
        erlang_c_num = (c*rho_c)**c / (np.math.factorial(c) * (1 - rho_c))
        denom = sum((c*rho_c)**k / np.math.factorial(k) for k in range(c)) + erlang_c_num
        P0 = 1 / denom
        Pc = erlang_c_num * P0
        Wq = Pc / (c * mu * (1 - rho_c))
        if Wq < sla_wait:
            return c, rho_c, Wq
    return None

import math
result = capacity_plan(lam_peak=8, mu=3, sla_wait=0.1)
if result:
    c, rho, wq = result
    print(f"Need {c} servers: ρ={rho:.2f}, avg wait={wq:.4f}s (SLA<0.1s)")"""),
])
save(ch15, "15_queuing_theory.ipynb")


# ── Chapter 16 ────────────────────────────────────────────────────────────────
ch16 = nb([
    md("""# Chapter 16 — Statistical Process Control (SPC)
*Track 4: Engineers*

## 🎯 Learning Objectives
- Build Shewhart control charts (X̄, R, p charts)
- Detect out-of-control signals using Western Electric rules
- Distinguish common-cause from special-cause variation"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Control Charts

A **control chart** monitors a process statistic over time.
Control limits are set at ±3σ of the statistic (not of the data).

**X̄ chart (mean chart):**
- UCL = $\\bar{\\bar X} + 3\\frac{\\hat\\sigma}{\\sqrt n}$
- LCL = $\\bar{\\bar X} - 3\\frac{\\hat\\sigma}{\\sqrt n}$

The **false alarm rate** with ±3σ limits ≈ 0.27% per point (assuming normality)."""),

    code("""# Simulate a manufacturing process
n_subgroups = 30
subgroup_size = 5
true_mean = 50.0
true_std = 2.0

# First 20 groups in-control, last 10 with shift
data = np.vstack([
    rng.normal(true_mean, true_std, (20, subgroup_size)),
    rng.normal(true_mean + 2.5, true_std, (10, subgroup_size)),
])
xbar = data.mean(axis=1)
R    = data.max(axis=1) - data.min(axis=1)

# Control limits (using first 20 in-control groups)
xbar_bar = xbar[:20].mean()
R_bar = R[:20].mean()
A2 = 0.577  # for subgroup size 5
D3, D4 = 0, 2.114

UCL_x = xbar_bar + A2 * R_bar
LCL_x = xbar_bar - A2 * R_bar

fig, axes = plt.subplots(2, 1, figsize=(12, 7))
ax = axes[0]
ax.plot(range(1, n_subgroups+1), xbar, "b-o", markersize=4)
ax.axhline(xbar_bar, color="green", linewidth=1.5, label="CL")
ax.axhline(UCL_x, color="red", linewidth=1.5, linestyle="--", label="UCL")
ax.axhline(LCL_x, color="red", linewidth=1.5, linestyle="--", label="LCL")
out_of_control = np.where((xbar > UCL_x) | (xbar < LCL_x))[0]
ax.scatter(out_of_control+1, xbar[out_of_control], color="red", zorder=5, s=80, label="OOC")
ax.set_title("X̄ Chart"); ax.legend(fontsize=9)
ax.set_xlabel("Subgroup"); ax.set_ylabel("X̄")

ax = axes[1]
UCL_r = D4 * R_bar
LCL_r = D3 * R_bar
ax.plot(range(1, n_subgroups+1), R, "b-o", markersize=4)
ax.axhline(R_bar, color="green", linewidth=1.5, label="CL")
ax.axhline(UCL_r, color="red", linewidth=1.5, linestyle="--", label="UCL")
ax.axhline(LCL_r, color="red", linewidth=1.5, linestyle="--", label="LCL")
ax.set_title("R Chart"); ax.legend(fontsize=9)
ax.set_xlabel("Subgroup"); ax.set_ylabel("Range R")
plt.tight_layout(); plt.show()
print(f"Out-of-control subgroups (X̄ chart): {out_of_control + 1}")"""),

    md("""## 2. Math Walkthrough — Process Capability

**Cp** measures potential capability (spread only):
$$C_p = \\frac{USL - LSL}{6\\hat\\sigma}$$

**Cpk** measures actual capability (includes centering):
$$C_{pk} = \\min\\left(\\frac{USL - \\bar x}{3\\hat\\sigma},\\; \\frac{\\bar x - LSL}{3\\hat\\sigma}\\right)$$

Rule of thumb: $C_{pk} \\geq 1.33$ for a capable process."""),

    code("""# Process capability analysis
USL, LSL = 56, 44
process_data = rng.normal(50.5, 1.8, 500)  # slightly off-center

sigma_hat = process_data.std(ddof=1)
xbar_est  = process_data.mean()
Cp  = (USL - LSL) / (6 * sigma_hat)
Cpk = min((USL - xbar_est) / (3*sigma_hat), (xbar_est - LSL) / (3*sigma_hat))
ppm_defects = (stats.norm.sf(USL, xbar_est, sigma_hat) +
               stats.norm.cdf(LSL, xbar_est, sigma_hat)) * 1e6

print(f"Process mean: {xbar_est:.2f}, σ: {sigma_hat:.2f}")
print(f"Cp={Cp:.3f}, Cpk={Cpk:.3f}")
print(f"Estimated defects: {ppm_defects:.0f} ppm")
print("Capable ✅" if Cpk >= 1.33 else "NOT capable ❌")

x_range = np.linspace(40, 60, 300)
plt.figure(figsize=(9, 4))
plt.hist(process_data, bins=40, density=True, alpha=0.5, label="Process data")
plt.plot(x_range, stats.norm.pdf(x_range, xbar_est, sigma_hat), "b-", lw=2)
plt.axvline(USL, color="red", lw=2, linestyle="--", label=f"USL={USL}")
plt.axvline(LSL, color="red", lw=2, linestyle="--", label=f"LSL={LSL}")
plt.fill_between(x_range[x_range>USL], stats.norm.pdf(x_range[x_range>USL], xbar_est, sigma_hat), alpha=0.4, color="red", label="Defects")
plt.fill_between(x_range[x_range<LSL], stats.norm.pdf(x_range[x_range<LSL], xbar_est, sigma_hat), alpha=0.4, color="red")
plt.title(f"Process Capability: Cp={Cp:.2f}, Cpk={Cpk:.2f}")
plt.legend(); plt.tight_layout(); plt.show()"""),

    code("""# p-chart for attribute data (proportion defective)
n_inspected = 100
p_true_in  = 0.03  # first 20 batches
p_true_out = 0.08  # last 10 batches
defects = np.concatenate([rng.binomial(n_inspected, p_true_in, 20),
                           rng.binomial(n_inspected, p_true_out, 10)])
p_i = defects / n_inspected
pbar = p_i[:20].mean()
UCL_p = pbar + 3*np.sqrt(pbar*(1-pbar)/n_inspected)
LCL_p = max(0, pbar - 3*np.sqrt(pbar*(1-pbar)/n_inspected))

plt.figure(figsize=(12, 4))
plt.plot(range(1, 31), p_i, "b-o", markersize=4)
plt.axhline(pbar, color="green", lw=1.5, label=f"p̄={pbar:.3f}")
plt.axhline(UCL_p, color="red", lw=1.5, linestyle="--", label=f"UCL={UCL_p:.3f}")
plt.axhline(LCL_p, color="red", lw=1.5, linestyle="--", label=f"LCL={LCL_p:.3f}")
ooc = np.where((p_i > UCL_p) | (p_i < LCL_p))[0]
plt.scatter(ooc+1, p_i[ooc], color="red", s=80, zorder=5)
plt.title("p-Chart — Proportion Defective"); plt.legend()
plt.xlabel("Batch"); plt.ylabel("p"); plt.tight_layout(); plt.show()"""),
])
save(ch16, "16_statistical_process_control.ipynb")


# ── Chapter 17 ────────────────────────────────────────────────────────────────
ch17 = nb([
    md("""# Chapter 17 — Signal vs Noise: SNR & Filtering
*Track 4: Engineers*

## 🎯 Learning Objectives
- Quantify signal-to-noise ratio and its probabilistic interpretation
- Implement moving average and exponential smoothing filters
- Apply Kalman filter concepts for state estimation"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.signal as signal

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Signal and Noise

A measurement is:
$$y[t] = s[t] + n[t]$$

where $s[t]$ is the true signal and $n[t] \\sim N(0, \\sigma_n^2)$ is noise.

**Signal-to-Noise Ratio (SNR):**
$$\\text{SNR} = \\frac{P_{signal}}{P_{noise}} = \\frac{\\sigma_s^2}{\\sigma_n^2}$$

$$\\text{SNR}_{dB} = 10\\log_{10}\\left(\\frac{P_{signal}}{P_{noise}}\\right)$$"""),

    code("""# Simulate noisy signal
t = np.linspace(0, 10, 500)
signal_true = np.sin(2*np.pi*0.5*t) + 0.3*np.sin(2*np.pi*2.0*t)
noise_levels = [0.1, 0.5, 1.5]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, sigma_n in zip(axes, noise_levels):
    noise = rng.normal(0, sigma_n, len(t))
    y = signal_true + noise
    snr_linear = signal_true.var() / noise.var()
    snr_db = 10 * np.log10(snr_linear)
    ax.plot(t, y, alpha=0.7, lw=0.8, label="Noisy")
    ax.plot(t, signal_true, "r-", lw=2, label="True signal")
    ax.set_title(f"σ_noise={sigma_n}\nSNR={snr_db:.1f} dB")
    ax.legend(fontsize=8)
plt.suptitle("Effect of Noise on Signal Quality", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Moving Average as Low-Pass Filter

An order-$M$ moving average:
$$\\hat s[t] = \\frac{1}{M}\\sum_{k=0}^{M-1} y[t-k]$$

The variance of the MA estimate:
$$\\text{Var}(\\hat s[t]) = \\frac{\\sigma_n^2}{M}$$

→ SNR improves by factor $M$."""),

    code("""sigma_n = 0.8
noise = rng.normal(0, sigma_n, len(t))
y_noisy = signal_true + noise

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
for ax, M in zip(axes.flat, [1, 5, 20, 50]):
    if M == 1:
        y_filt = y_noisy
    else:
        kernel = np.ones(M) / M
        y_filt = np.convolve(y_noisy, kernel, mode="same")
    residual_var = np.var(y_filt - signal_true)
    snr_improvement = sigma_n**2 / residual_var
    ax.plot(t, y_noisy, alpha=0.4, lw=0.8, label="Noisy")
    ax.plot(t, signal_true, "g-", lw=1.5, label="True")
    ax.plot(t, y_filt, "r-", lw=2, label=f"MA(M={M})")
    ax.set_title(f"M={M}, SNR gain={snr_improvement:.1f}x")
    ax.legend(fontsize=8)
plt.suptitle("Moving Average Filtering — Variance Reduction", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 3–6. Exponential Smoothing, Kalman Filter, Practice"""),

    code("""# Exponential smoothing (EMA)
def ema(y, alpha):
    s = np.zeros_like(y)
    s[0] = y[0]
    for i in range(1, len(y)):
        s[i] = alpha * y[i] + (1-alpha) * s[i-1]
    return s

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, alpha in zip(axes, [0.1, 0.3, 0.8]):
    y_smooth = ema(y_noisy, alpha)
    ax.plot(t, y_noisy, alpha=0.4, lw=0.8)
    ax.plot(t, signal_true, "g-", lw=1.5, label="True")
    ax.plot(t, y_smooth, "r-", lw=2, label=f"EMA α={alpha}")
    ax.set_title(f"α={alpha}")
    ax.legend(fontsize=9)
plt.suptitle("Exponential Moving Average Smoothing")
plt.tight_layout(); plt.show()"""),

    code("""# Kalman filter: 1D constant velocity model
# State: [position, velocity], Measurement: position only
dt = t[1] - t[0]
F = np.array([[1, dt], [0, 1]])  # state transition
H = np.array([[1, 0]])           # measurement matrix
Q = np.diag([1e-4, 1e-4])       # process noise covariance
R_kf = np.array([[sigma_n**2]]) # measurement noise covariance

x_est = np.zeros((len(t), 2))
P_est = np.eye(2) * 1.0
x_est[0] = [y_noisy[0], 0]

for k in range(1, len(t)):
    # Predict
    x_pred = F @ x_est[k-1]
    P_pred = F @ P_est @ F.T + Q
    # Update
    S = H @ P_pred @ H.T + R_kf
    K = P_pred @ H.T @ np.linalg.inv(S)
    x_est[k] = x_pred + K @ (y_noisy[k:k+1] - H @ x_pred)
    P_est = (np.eye(2) - K @ H) @ P_pred

plt.figure(figsize=(10, 4))
plt.plot(t, y_noisy, alpha=0.4, lw=0.8, label="Noisy")
plt.plot(t, signal_true, "g-", lw=1.5, label="True signal")
plt.plot(t, x_est[:, 0], "r-", lw=2, label="Kalman filter")
plt.title("Kalman Filter — 1D State Estimation")
plt.legend(); plt.tight_layout(); plt.show()

kf_mse = np.mean((x_est[:, 0] - signal_true)**2)
noisy_mse = np.mean((y_noisy - signal_true)**2)
print(f"Noisy MSE: {noisy_mse:.4f}  →  Kalman MSE: {kf_mse:.4f}")"""),
])
save(ch17, "17_signal_noise_snr_filtering.ipynb")


# ── Chapter 18 ────────────────────────────────────────────────────────────────
ch18 = nb([
    md("""# Chapter 18 — Failure Mode Analysis with Probability
*Track 4: Engineers*

## 🎯 Learning Objectives
- Perform FMEA with probability-based Risk Priority Number (RPN)
- Build fault trees and compute top-event probability
- Apply event tree analysis for consequence modeling"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — FMEA

**FMEA** (Failure Mode and Effects Analysis) ranks failure modes by:

$$\\text{RPN} = \\text{Severity} \\times \\text{Occurrence} \\times \\text{Detection}$$

Each factor is rated 1–10:
- **Severity**: how bad is the effect? (1=minor, 10=catastrophic)
- **Occurrence**: how often does it happen? (1=rare, 10=almost certain)
- **Detection**: how easy is it to detect before reaching customer? (1=easy to detect, 10=undetectable)"""),

    code("""# FMEA analysis for a pump system
fmea_data = {
    "Failure Mode": [
        "Seal leak", "Bearing failure", "Impeller wear",
        "Motor overload", "Cavitation", "Corrosion"
    ],
    "Severity":    [8, 7, 5, 9, 6, 7],
    "Occurrence":  [4, 5, 6, 3, 4, 5],
    "Detection":   [3, 4, 6, 2, 5, 7],
}
df = pd.DataFrame(fmea_data)
df["RPN"] = df["Severity"] * df["Occurrence"] * df["Detection"]
df = df.sort_values("RPN", ascending=False)
print(df.to_string(index=False))

colors = ["red" if r > 200 else "orange" if r > 100 else "green" for r in df["RPN"]]
plt.barh(df["Failure Mode"], df["RPN"], color=colors)
plt.axvline(200, color="red", linestyle="--", label="High risk (RPN>200)")
plt.axvline(100, color="orange", linestyle="--", label="Medium risk (RPN>100)")
plt.xlabel("Risk Priority Number (RPN)")
plt.title("FMEA — Pump System Risk Ranking")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Fault Tree Analysis

**AND gate**: all inputs must fail for output to fail:
$$P(\\text{top}) = \\prod_i P(\\text{input}_i)$$

**OR gate**: any input failing causes output:
$$P(\\text{top}) = 1 - \\prod_i (1 - P(\\text{input}_i))$$"""),

    code("""# Fault tree calculation
def and_gate(probs):
    return np.prod(probs)

def or_gate(probs):
    return 1 - np.prod(1 - np.array(probs))

# System failure tree
p_sensor_A = 0.02   # sensor A failure rate
p_sensor_B = 0.015  # sensor B
p_power_A  = 0.005
p_power_B  = 0.005

# Sensor subsystem: both must fail (AND)
p_sensor_subsystem = and_gate([p_sensor_A, p_sensor_B])

# Power subsystem: either fails (OR)
p_power_subsystem = or_gate([p_power_A, p_power_B])

# Top event: either subsystem fails (OR)
p_top = or_gate([p_sensor_subsystem, p_power_subsystem])

print(f"Sensor subsystem failure (AND): {p_sensor_subsystem:.6f}")
print(f"Power subsystem failure (OR):   {p_power_subsystem:.6f}")
print(f"Top event probability (OR):     {p_top:.6f}")
print(f"Top event per year (1e6 hours): {p_top*8760:.4f}")"""),

    md("""## 3–6. Monte Carlo Fault Tree, Event Tree, Practice"""),

    code("""# Monte Carlo fault tree simulation
n_sim = 100_000
sensor_A_fail = rng.random(n_sim) < p_sensor_A
sensor_B_fail = rng.random(n_sim) < p_sensor_B
power_A_fail  = rng.random(n_sim) < p_power_A
power_B_fail  = rng.random(n_sim) < p_power_B

sensor_sub_fail = sensor_A_fail & sensor_B_fail
power_sub_fail  = power_A_fail | power_B_fail
top_event_fail  = sensor_sub_fail | power_sub_fail

mc_prob = top_event_fail.mean()
print(f"Monte Carlo top event probability: {mc_prob:.6f}")
print(f"Analytic:                          {p_top:.6f}")"""),

    code("""# Event tree: consequences given initiating event
# Initiating event: pressure release (IE)
p_IE = 0.01  # per year

# Safety barriers (independent)
p_detection  = 0.95  # probability detector works
p_isolation  = 0.90  # probability valve closes
p_mitigation = 0.80  # probability mitigation system works

# Consequence paths
paths = {
    "Near miss (all barriers)":      p_IE * p_detection * p_isolation * p_mitigation,
    "Minor incident (no mitigation)": p_IE * p_detection * p_isolation * (1-p_mitigation),
    "Moderate (no isolation)":        p_IE * p_detection * (1-p_isolation),
    "Major incident (no detection)":  p_IE * (1-p_detection),
}
print("Event Tree — Annual Frequencies:")
for outcome, freq in paths.items():
    print(f"  {outcome:<40}: {freq:.2e}")

plt.barh(list(paths.keys()), list(paths.values()), color=["green","yellow","orange","red"])
plt.xscale("log"); plt.xlabel("Annual frequency")
plt.title("Event Tree Analysis — Pressure Release Scenario")
plt.tight_layout(); plt.show()"""),
])
save(ch18, "18_failure_mode_analysis.ipynb")


# ── Chapter 19 ────────────────────────────────────────────────────────────────
ch19 = nb([
    md("""# Chapter 19 — Monte Carlo Simulation for Engineering
*Track 4: Engineers*

## 🎯 Learning Objectives
- Apply Monte Carlo to structural and tolerance analysis
- Propagate uncertainty through engineering calculations
- Estimate probabilities of failure for complex systems"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Monte Carlo for Uncertainty Propagation

When $Y = g(X_1, X_2, \\ldots, X_n)$ and the $X_i$ are random:

1. Sample $N$ realisations of each $X_i$
2. Compute $Y^{(j)} = g(X_1^{(j)}, \\ldots, X_n^{(j)})$ for each $j$
3. Estimate $P(Y > \\text{limit})$, $E[Y]$, $\\text{Var}[Y]$

Advantages: handles **any** distribution, **any** functional form,
correlations, discrete + continuous mixing."""),

    code("""# Structural example: beam deflection
# δ = P*L³ / (48*E*I) — all inputs are uncertain
N = 100_000
P = rng.normal(10_000, 1_000, N)   # Load [N]: mean=10kN, COV=10%
L = rng.normal(3.0, 0.05, N)       # Length [m]: mean=3m, COV=1.7%
E = rng.normal(2e11, 1e10, N)      # Elastic modulus [Pa]: steel
I = rng.normal(8.3e-6, 5e-7, N)    # Second moment [m⁴]

delta = P * L**3 / (48 * E * I)

limit = 0.010  # 10mm deflection limit
p_exceed = np.mean(delta > limit)

print(f"Mean deflection:     {delta.mean()*1000:.2f} mm")
print(f"Std deflection:      {delta.std()*1000:.2f} mm")
print(f"P(δ > {limit*1000:.0f}mm): {p_exceed:.4f}")

plt.figure(figsize=(9, 4))
plt.hist(delta*1000, bins=80, density=True, alpha=0.7, edgecolor="k", linewidth=0.2)
plt.axvline(limit*1000, color="red", lw=2, linestyle="--", label=f"Limit={limit*1000:.0f}mm")
plt.xlabel("Deflection (mm)"); plt.ylabel("Density")
plt.title(f"Monte Carlo Beam Deflection — P(exceed limit)={p_exceed:.4f}")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Tolerance Stackup

For linear stacking of $n$ dimensions:
$$Y = \\sum_{i=1}^n X_i$$

If $X_i \\sim N(\\mu_i, \\sigma_i^2)$ independently:
$$Y \\sim N\\left(\\sum \\mu_i, \\sum \\sigma_i^2\\right)$$

**Worst-case analysis** assumes all at extreme:
$$\\text{Total tolerance} = \\sum_i t_i$$

**RSS (Root Sum of Squares):**
$$\\text{Total tolerance}_{RSS} = \\sqrt{\\sum_i t_i^2}$$"""),

    code("""# Tolerance stackup: shaft in housing
n_parts = 6
means = np.array([50.0, 30.0, 20.0, 15.0, 10.0, 5.0])  # nominal dimensions
tolerances = np.array([0.05, 0.04, 0.03, 0.03, 0.02, 0.02])  # ±tolerance (3σ)
sigmas = tolerances / 3

# Monte Carlo stackup
N = 200_000
dims = rng.normal(means, sigmas, (N, n_parts))
total = dims.sum(axis=1)

worst_case_tol = tolerances.sum()
rss_tol = np.sqrt((tolerances**2).sum())

print(f"Nominal total:     {means.sum():.1f}")
print(f"Worst-case ±:      {worst_case_tol:.4f}")
print(f"RSS ±:             {rss_tol:.4f}")
print(f"MC std:            {total.std():.4f}")
print(f"MC ±3σ:            {3*total.std():.4f}")

clearance_limit = means.sum() + rss_tol * 1.5
p_exceed = np.mean(total > clearance_limit)
print(f"\nP(total > clearance {clearance_limit:.2f}): {p_exceed:.6f}")"""),

    code("""# Sensitivity analysis: which input drives the most variance?
from scipy.stats import spearmanr
for i, name in enumerate(["P", "L", "E", "I"]):
    inputs = [P, L, E, I]
    rho, p_val = spearmanr(inputs[i], delta)
    print(f"Rank correlation of {name} with deflection: {rho:.4f}")"""),

    code("""# Reliability index β (First-Order Reliability Method approximation)
# For linear limit state g = R - S (resistance minus stress)
mu_R, sig_R = 150_000, 15_000   # Resistance
mu_S, sig_S = 100_000, 20_000   # Stress (load)

beta = (mu_R - mu_S) / np.sqrt(sig_R**2 + sig_S**2)
pf_approx = stats.norm.sf(beta)

# Monte Carlo verification
R_mc = rng.normal(mu_R, sig_R, 500_000)
S_mc = rng.normal(mu_S, sig_S, 500_000)
pf_mc = np.mean(R_mc < S_mc)

print(f"Reliability index β = {beta:.3f}")
print(f"FORM P(failure) = {pf_approx:.6f}")
print(f"MC   P(failure) = {pf_mc:.6f}")"""),
])
save(ch19, "19_monte_carlo_engineering.ipynb")


# ── Chapter 20 ────────────────────────────────────────────────────────────────
ch20 = nb([
    md("""# Chapter 20 — Risk Assessment & Safety Factors
*Track 4: Engineers*

## 🎯 Learning Objectives
- Quantify risk as probability × consequence
- Design safety factors using probabilistic methods
- Build risk matrices and F-N curves"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Risk = Probability × Consequence

$$\\text{Risk} = P(\\text{hazard}) \\times C(\\text{consequence})$$

**Risk matrix** qualitatively ranks scenarios by:
- Likelihood (1–5 scale)
- Severity (1–5 scale)

**F-N curves** (Frequency-Number): cumulative frequency of events
causing N or more fatalities — used in nuclear/offshore industries."""),

    code("""# Risk matrix
fig, ax = plt.subplots(figsize=(8, 6))
severity_labels   = ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"]
likelihood_labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]

risk_colors = np.array([
    [1, 1, 2, 3, 3],
    [1, 2, 2, 3, 4],
    [1, 2, 3, 4, 4],
    [2, 3, 3, 4, 5],
    [2, 3, 4, 5, 5],
])[::-1]  # flip for display (low likelihood at bottom)

color_map = {1: "#2ecc71", 2: "#f1c40f", 3: "#e67e22", 4: "#e74c3c", 5: "#8e44ad"}
risk_labels = {1: "Low", 2: "Medium", 3: "High", 4: "Very High", 5: "Extreme"}

for i in range(5):
    for j in range(5):
        val = risk_colors[i, j]
        rect = plt.Rectangle([j, i], 1, 1, color=color_map[val], alpha=0.8)
        ax.add_patch(rect)
        ax.text(j+0.5, i+0.5, risk_labels[val], ha="center", va="center", fontsize=9, fontweight="bold")

ax.set_xticks(np.arange(5)+0.5); ax.set_xticklabels(severity_labels, fontsize=9)
ax.set_yticks(np.arange(5)+0.5); ax.set_yticklabels(likelihood_labels[::-1], fontsize=9)
ax.set_xlim(0,5); ax.set_ylim(0,5)
ax.set_xlabel("Severity →"); ax.set_ylabel("Likelihood →")
ax.set_title("5×5 Risk Matrix")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Probabilistic Safety Factor

The **safety factor** $SF = R/S$. If $R$ and $S$ are lognormal:
$$\\ln SF \\sim N(\\mu_{\\ln R} - \\mu_{\\ln S},\\; \\sigma_{\\ln R}^2 + \\sigma_{\\ln S}^2)$$

The probability of failure:
$$P_f = P(SF < 1) = \\Phi\\left(\\frac{\\mu_{\\ln S} - \\mu_{\\ln R}}{\\sqrt{\\sigma_{\\ln R}^2 + \\sigma_{\\ln S}^2}}\\right)$$"""),

    code("""# Probabilistic safety factor for a structural connection
# Resistance R ~ Lognormal, Demand S ~ Lognormal
mu_R, cov_R = 100, 0.10   # kN
mu_S, cov_S =  60, 0.20   # kN

# Lognormal parameters
sig_lnR = np.sqrt(np.log(1 + cov_R**2))
mu_lnR  = np.log(mu_R) - 0.5*sig_lnR**2
sig_lnS = np.sqrt(np.log(1 + cov_S**2))
mu_lnS  = np.log(mu_S) - 0.5*sig_lnS**2

beta_lognormal = (mu_lnR - mu_lnS) / np.sqrt(sig_lnR**2 + sig_lnS**2)
pf = stats.norm.cdf(-beta_lognormal)
nominal_sf = mu_R / mu_S

print(f"Nominal safety factor: {nominal_sf:.2f}")
print(f"Reliability index β:   {beta_lognormal:.3f}")
print(f"Probability of failure: {pf:.6f}")
print(f"Return period:          {1/pf:.0f} cycles")

N = 100_000
R_mc = rng.lognormal(mu_lnR, sig_lnR, N)
S_mc = rng.lognormal(mu_lnS, sig_lnS, N)
print(f"\nMC P(failure): {np.mean(R_mc < S_mc):.6f}")"""),

    code("""# F-N Curve
import matplotlib.ticker as ticker
fatalities = [1, 5, 10, 50, 100, 500, 1000]
freq       = [1e-2, 5e-3, 2e-3, 4e-4, 1e-4, 2e-5, 5e-6]  # per year

plt.figure(figsize=(8, 6))
plt.loglog(fatalities, freq, "ro-", lw=2, markersize=8)
# ALARP regions
n_range = np.array([1, 10000])
plt.fill_between(n_range, 1e-3/n_range, 1e-1/n_range, alpha=0.3, color="red", label="Intolerable")
plt.fill_between(n_range, 1e-5/n_range, 1e-3/n_range, alpha=0.2, color="yellow", label="ALARP")
plt.fill_between(n_range, 1e-7/n_range, 1e-5/n_range, alpha=0.2, color="green", label="Broadly acceptable")
plt.xlabel("Number of fatalities N"); plt.ylabel("Frequency F(N) [per year]")
plt.title("F-N Curve with ALARP Regions")
plt.legend(); plt.xlim(1, 1e4); plt.ylim(1e-8, 1e-1)
plt.tight_layout(); plt.show()"""),
])
save(ch20, "20_risk_assessment_safety_factors.ipynb")


# ── Chapter 21 ────────────────────────────────────────────────────────────────
ch21 = nb([
    md("""# Chapter 21 — Regression for Engineers
*Track 4: Engineers*

## 🎯 Learning Objectives
- Apply linear and polynomial regression to engineering data
- Check OLS assumptions (residual diagnostics)
- Use regression for calibration, degradation, and load prediction"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — OLS Regression

$$Y = \\beta_0 + \\beta_1 X + \\varepsilon, \\quad \\varepsilon \\sim N(0, \\sigma^2)$$

OLS estimators:
$$\\hat\\beta = (X^T X)^{-1} X^T y$$

**Gauss-Markov theorem**: OLS is BLUE (Best Linear Unbiased Estimator)
under: linearity, independence, homoscedasticity, zero-mean errors."""),

    code("""# Sensor calibration: true vs measured temperature
T_true = rng.uniform(0, 100, 60)
T_meas = 1.05 * T_true - 2.3 + rng.normal(0, 1.5, 60)  # gain error + offset + noise

X_mat = sm.add_constant(T_meas)
model = sm.OLS(T_true, X_mat).fit()
print(model.summary().tables[1])

plt.figure(figsize=(8, 5))
plt.scatter(T_meas, T_true, alpha=0.6, s=30)
x_range = np.linspace(T_meas.min(), T_meas.max(), 100)
plt.plot(x_range, model.predict(sm.add_constant(x_range)), "r-", lw=2, label="Calibration curve")
plt.plot([0,110], [0,110], "k--", alpha=0.5, label="Ideal (y=x)")
plt.xlabel("Measured Temperature"); plt.ylabel("True Temperature")
plt.title("Sensor Calibration Regression")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Residual Diagnostics

For OLS to be valid, check:
1. **Residuals vs. fitted**: should show no pattern (homoscedasticity)
2. **QQ plot**: residuals should be normal
3. **Scale-location**: sqrt(|residuals|) should be flat
4. **Leverage**: influential points should not dominate"""),

    code("""residuals = model.resid
fitted = model.fittedvalues

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
# 1. Residuals vs fitted
axes[0,0].scatter(fitted, residuals, alpha=0.5, s=20)
axes[0,0].axhline(0, color="red"); axes[0,0].set_title("Residuals vs Fitted")
axes[0,0].set_xlabel("Fitted"); axes[0,0].set_ylabel("Residuals")

# 2. QQ plot
stats.probplot(residuals, plot=axes[0,1])
axes[0,1].set_title("Q-Q Plot of Residuals")

# 3. Scale-location
axes[1,0].scatter(fitted, np.sqrt(np.abs(residuals)), alpha=0.5, s=20)
axes[1,0].set_title("Scale-Location"); axes[1,0].set_xlabel("Fitted")
axes[1,0].set_ylabel("√|Residuals|")

# 4. Residuals histogram
axes[1,1].hist(residuals, bins=20, density=True, alpha=0.7)
xr = np.linspace(residuals.min(), residuals.max(), 100)
axes[1,1].plot(xr, stats.norm.pdf(xr, residuals.mean(), residuals.std()), "r-")
axes[1,1].set_title("Residuals Histogram")
plt.tight_layout(); plt.show()

sw_stat, sw_p = stats.shapiro(residuals)
print(f"Shapiro-Wilk normality test: W={sw_stat:.4f}, p={sw_p:.4f}")"""),

    code("""# Degradation modelling: component wear over time
time_hours = np.arange(0, 1001, 50, dtype=float)
wear = 0.0005 * time_hours + 0.000002 * time_hours**2 + rng.normal(0, 0.02, len(time_hours))

# Polynomial regression
poly = make_pipeline(PolynomialFeatures(2), LinearRegression())
poly.fit(time_hours.reshape(-1,1), wear)

t_pred = np.linspace(0, 1500, 300)
wear_pred = poly.predict(t_pred.reshape(-1,1))
failure_threshold = 0.8
t_failure_idx = np.searchsorted(wear_pred, failure_threshold)
t_failure = t_pred[min(t_failure_idx, len(t_pred)-1)]

plt.figure(figsize=(9, 5))
plt.scatter(time_hours, wear, alpha=0.7, s=20, label="Measured wear")
plt.plot(t_pred, wear_pred, "r-", lw=2, label="Regression model")
plt.axhline(failure_threshold, color="black", linestyle="--", label=f"Failure threshold={failure_threshold}")
if t_failure < t_pred[-1]:
    plt.axvline(t_failure, color="orange", linestyle="--", label=f"Predicted failure: {t_failure:.0f}h")
plt.xlabel("Operating hours"); plt.ylabel("Wear [mm]")
plt.title("Component Degradation — Polynomial Regression")
plt.legend(); plt.tight_layout(); plt.show()"""),
])
save(ch21, "21_regression_for_engineers.ipynb")


# ── Chapter 22 ────────────────────────────────────────────────────────────────
ch22 = nb([
    md("""# Chapter 22 — Six Sigma & Quality Statistics
*Track 4: Engineers*

## 🎯 Learning Objectives
- Understand the Six Sigma quality standard and DPMO
- Implement measurement system analysis (Gage R&R)
- Apply hypothesis testing in a quality control context"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Six Sigma Quality

**Six Sigma** means the process mean is 6σ away from the nearest spec limit.
With a 1.5σ shift (Motorola convention):

| Sigma level | DPMO | Yield |
|-------------|------|-------|
| 3σ | 66,807 | 93.32% |
| 4σ | 6,210 | 99.38% |
| 5σ | 233 | 99.977% |
| 6σ | 3.4 | 99.9997% |

DPMO = Defects Per Million Opportunities"""),

    code("""# DPMO curve
sigma_levels = np.linspace(1, 6.5, 200)
shift = 1.5  # Motorola long-term shift
dpmo = (stats.norm.sf(sigma_levels - shift) + stats.norm.cdf(-(sigma_levels + shift))) * 1e6

plt.figure(figsize=(9, 5))
plt.semilogy(sigma_levels, dpmo)
for level in [3, 4, 5, 6]:
    d = (stats.norm.sf(level - 1.5) + stats.norm.cdf(-(level + 1.5))) * 1e6
    plt.scatter([level], [d], s=80, zorder=5)
    plt.annotate(f"{level}σ\n{d:.0f} DPMO", (level, d), textcoords="offset points",
                 xytext=(10, 5), fontsize=9)
plt.xlabel("Sigma Level"); plt.ylabel("DPMO (log scale)")
plt.title("Sigma Level vs DPMO (with 1.5σ shift)")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Gage Repeatability & Reproducibility

The total measurement variation is:
$$\\sigma^2_{total} = \\sigma^2_{part} + \\sigma^2_{gage}$$
$$\\sigma^2_{gage} = \\sigma^2_{repeatability} + \\sigma^2_{reproducibility}$$

**%R&R**:
$$\\%R\\&R = \\frac{\\sigma_{gage}}{\\sigma_{total}} \\times 100$$

Rule: %R&R < 10% → acceptable; 10–30% → marginal; >30% → unacceptable."""),

    code("""# Gage R&R study simulation
n_parts = 10
n_operators = 3
n_reps = 2

part_variation = 5.0    # true part-to-part std
repeatability  = 0.8    # within-operator std
reproducibility = 1.2   # between-operator std

part_means = rng.normal(100, part_variation, n_parts)
operator_biases = rng.normal(0, reproducibility, n_operators)

data = []
for p in range(n_parts):
    for o in range(n_operators):
        for r in range(n_reps):
            meas = (part_means[p] + operator_biases[o] +
                    rng.normal(0, repeatability))
            data.append({"part": p+1, "operator": o+1, "rep": r+1, "measurement": meas})
df = pd.DataFrame(data)

# ANOVA-based R&R
grand_mean = df["measurement"].mean()
# Between-part variance
part_means_est = df.groupby("part")["measurement"].mean()
ss_parts = n_operators * n_reps * ((part_means_est - grand_mean)**2).sum()
ms_parts = ss_parts / (n_parts - 1)
# Repeatability
ss_rep = df.groupby(["part","operator"])["measurement"].var(ddof=1).sum() * (n_reps - 1)
ms_rep = ss_rep / (n_parts * n_operators * (n_reps - 1))
sigma_repeat = np.sqrt(ms_rep)
sigma_total  = df["measurement"].std(ddof=1)
sigma_gage   = np.sqrt(max(0, ms_rep + (n_reps * max(0, ms_parts - ms_rep) / n_reps)))

perc_rr = sigma_repeat / sigma_total * 100
print(f"σ_repeatability: {sigma_repeat:.3f}")
print(f"σ_total:         {sigma_total:.3f}")
print(f"%R&R:            {perc_rr:.1f}%")
print("✅ Acceptable" if perc_rr < 10 else "⚠️ Marginal" if perc_rr < 30 else "❌ Unacceptable")"""),

    code("""# Hypothesis tests in quality context
# 1. Are two machine outputs the same mean? (Welch t-test)
machine_A = rng.normal(100.2, 1.5, 50)
machine_B = rng.normal(100.8, 1.7, 50)
t_stat, p_val = stats.ttest_ind(machine_A, machine_B, equal_var=False)
print(f"Machine comparison: t={t_stat:.3f}, p={p_val:.4f}")
print("Different" if p_val < 0.05 else "Same within noise")

# 2. Is variance in spec? F-test
spec_variance = 2.25  # σ = 1.5 → σ² = 2.25
n = len(machine_A)
chi2_stat = (n-1) * machine_A.var(ddof=1) / spec_variance
p_chi2 = 2 * min(stats.chi2.cdf(chi2_stat, n-1), stats.chi2.sf(chi2_stat, n-1))
print(f"\nVariance test: χ²={chi2_stat:.3f}, p={p_chi2:.4f}")
print("Variance OK ✅" if p_chi2 > 0.05 else "Variance out of spec ❌")"""),

    md("""## 🎯 Track 4 Complete! 🏆

**You've mastered:**
- ✅ Reliability & failure probability: Weibull, bathtub curve
- ✅ Poisson processes: inter-arrivals, system applications
- ✅ Queuing theory: M/M/1, Little's Law, capacity planning
- ✅ Statistical Process Control: X̄/R/p charts, Cp/Cpk
- ✅ Signal vs noise: SNR, filtering, Kalman filter
- ✅ Failure mode analysis: FMEA, fault trees, event trees
- ✅ Monte Carlo for engineering: uncertainty propagation, reliability
- ✅ Risk assessment: risk matrices, F-N curves, safety factors
- ✅ Regression: calibration, degradation, residual diagnostics
- ✅ Six Sigma: DPMO, Gage R&R, quality hypothesis tests

**Ready for Tier 3?** → [Chapter 23 — Markov Chains]"""),
])
save(ch22, "22_six_sigma_quality.ipynb")

print("\n🎉 All Track 4 (Engineers) notebooks created successfully!")
