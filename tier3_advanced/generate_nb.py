"""Generate Tier 3 — Advanced notebooks (chapters 23-30, all tracks)."""
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


# ── Chapter 23 ────────────────────────────────────────────────────────────────
ch23 = nb([
    md("""# Chapter 23 — Markov Chains
*Tier 3: All Tracks*

## 🎯 Learning Objectives
- Define Markov chains and transition matrices
- Compute stationary distributions
- Apply to web ranking, weather, and recommendation systems"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import networkx as nx

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — The Markov Property

A sequence $X_0, X_1, X_2, \\ldots$ is a **Markov chain** if:

$$P(X_{n+1} = j \\mid X_n = i, X_{n-1}, \\ldots) = P(X_{n+1} = j \\mid X_n = i) = P_{ij}$$

The **transition matrix** $P$ is a stochastic matrix:
$$P_{ij} \\geq 0, \\quad \\sum_j P_{ij} = 1 \\text{ for all } i$$

The **n-step distribution**: $\\pi^{(n)} = \\pi^{(0)} P^n$"""),

    code("""# Weather Markov chain: Sunny, Cloudy, Rainy
states = ["Sunny", "Cloudy", "Rainy"]
P = np.array([
    [0.70, 0.20, 0.10],   # from Sunny
    [0.30, 0.40, 0.30],   # from Cloudy
    [0.20, 0.35, 0.45],   # from Rainy
])

# Verify stochastic
assert np.allclose(P.sum(axis=1), 1), "Not a valid stochastic matrix"

# Visualise transition graph
G = nx.DiGraph()
G.add_nodes_from(states)
for i, s1 in enumerate(states):
    for j, s2 in enumerate(states):
        if P[i, j] > 0.05:
            G.add_edge(s1, s2, weight=P[i, j])

plt.figure(figsize=(7, 5))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="steelblue", alpha=0.8)
nx.draw_networkx_labels(G, pos, font_color="white", font_size=11)
edge_labels = {(u,v): f"{d['weight']:.2f}" for u,v,d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, connectionstyle="arc3,rad=0.1")
plt.title("Weather Markov Chain")
plt.axis("off"); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Stationary Distribution

The **stationary distribution** $\\pi$ satisfies:
$$\\pi P = \\pi, \\quad \\sum_i \\pi_i = 1$$

For ergodic chains: regardless of initial state, $\\pi^{(n)} \\to \\pi$ as $n \\to \\infty$."""),

    code("""# Find stationary distribution by eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(P.T)
idx = np.argmin(np.abs(eigenvalues - 1))
pi = np.real(eigenvectors[:, idx])
pi /= pi.sum()
print("Stationary distribution (eigenvector):")
for s, p in zip(states, pi):
    print(f"  P({s}) = {p:.4f}")

# Verify by power iteration
pi_current = np.array([1.0, 0.0, 0.0])  # start sunny
for n in range(100):
    pi_current = pi_current @ P
print("\nStationary distribution (power iteration after 100 steps):")
for s, p in zip(states, pi_current):
    print(f"  P({s}) = {p:.4f}")"""),

    md("""## 3. Simulation — Convergence to Stationary Distribution"""),

    code("""n_steps = 200
n_chains = 5
initial_states = [0, 0, 1, 2, 2]
colors = ["blue", "red", "green", "purple", "orange"]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, state_idx, sname in zip(axes, range(3), states):
    ax.axhline(pi[state_idx], color="black", lw=2, linestyle="--",
               label=f"Stationary π={pi[state_idx]:.3f}")
    for init, color in zip(initial_states, colors):
        dist = np.zeros((n_steps+1, 3))
        dist[0, init] = 1.0
        for n in range(1, n_steps+1):
            dist[n] = dist[n-1] @ P
        ax.plot(dist[:, state_idx], alpha=0.6, color=color, lw=1)
    ax.set_title(f"P({sname} at step n)"); ax.set_xlabel("Step")
    ax.legend(fontsize=9)
plt.suptitle("Convergence to Stationary Distribution", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 4. Application — PageRank Algorithm"""),

    code("""# PageRank as Markov chain
# 5-page website
pages = ["Home", "About", "Blog", "Shop", "Contact"]
links = np.array([
    [0, 1, 1, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0],
])

# Row-normalise to make transition matrix
row_sums = links.sum(axis=1, keepdims=True)
P_pages = links / row_sums

# PageRank with damping factor d=0.85
d = 0.85
n_pages = len(pages)
P_pagerank = d * P_pages + (1-d) * np.ones((n_pages, n_pages)) / n_pages

# Power iteration
rank = np.ones(n_pages) / n_pages
for _ in range(100):
    rank = rank @ P_pagerank
rank_sorted = sorted(zip(pages, rank), key=lambda x: -x[1])
print("PageRank scores:")
for page, r in rank_sorted:
    print(f"  {page:<10} {r:.4f}")

plt.barh([p for p, _ in rank_sorted], [r for _, r in rank_sorted], color="steelblue")
plt.xlabel("PageRank"); plt.title("PageRank Scores")
plt.tight_layout(); plt.show()"""),

    code("""# Practice: Absorbing Markov chain — Gambler's ruin
# States: 0 (broke), 1, 2, 3, 4, 5 (goal), with 0 and 5 absorbing
p_win = 0.45  # probability of winning each bet
states_gambler = list(range(6))
P_gambler = np.zeros((6, 6))
P_gambler[0, 0] = 1.0   # absorbing
P_gambler[5, 5] = 1.0   # absorbing
for i in range(1, 5):
    P_gambler[i, i+1] = p_win
    P_gambler[i, i-1] = 1 - p_win

# Simulate from starting position 2
n_sim = 10_000
wins = 0
for _ in range(n_sim):
    state = 2
    for _ in range(1000):
        state = rng.choice(6, p=P_gambler[state])
        if state == 0 or state == 5:
            break
    wins += (state == 5)
print(f"P(reach 5 | start at 2) ≈ {wins/n_sim:.4f}")
# Analytic: (1-(q/p)^i) / (1-(q/p)^N)
q = 1 - p_win
analytic = (1-(q/p_win)**2) / (1-(q/p_win)**5)
print(f"Analytic:                 {analytic:.4f}")"""),
])
save(ch23, "23_markov_chains.ipynb")


# ── Chapter 24 ────────────────────────────────────────────────────────────────
ch24 = nb([
    md("""# Chapter 24 — Stochastic Processes
*Tier 3: All Tracks*

## 🎯 Learning Objectives
- Understand key stochastic processes: Brownian motion, random walks, Poisson processes
- Simulate and analyse paths of continuous-time processes
- Apply to finance, engineering, and diffusion problems"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Key Stochastic Processes

| Process | Definition | Key property |
|---------|-----------|-------------|
| Random Walk | $S_n = \\sum_{i=1}^n X_i$, $X_i \\in \\{\\pm 1\\}$ | Discrete, integer-valued |
| Brownian Motion | $W(t) = \\lim$ of scaled random walk | Continuous paths, $W(t) \\sim N(0,t)$ |
| Geometric BM | $S(t) = S_0 e^{(\\mu-\\sigma^2/2)t + \\sigma W(t)}$ | Always positive, used in finance |
| Ornstein-Uhlenbeck | $dX = \\theta(\\mu - X)dt + \\sigma dW$ | Mean-reverting |"""),

    code("""# Standard Brownian motion via random walk limit
dt = 0.01
T  = 10
t  = np.arange(0, T+dt, dt)
n_paths = 5

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for _ in range(n_paths):
    increments = rng.normal(0, np.sqrt(dt), len(t)-1)
    W = np.concatenate([[0], np.cumsum(increments)])
    axes[0].plot(t, W, alpha=0.7, lw=0.8)
axes[0].set_title("Standard Brownian Motion")
axes[0].set_xlabel("t"); axes[0].set_ylabel("W(t)")

# Distribution at various times
for time_pt in [1, 4, 9]:
    samples = rng.normal(0, np.sqrt(time_pt), 5000)
    axes[1].hist(samples, bins=50, density=True, alpha=0.5, label=f"t={time_pt}")
    x_r = np.linspace(-10, 10, 300)
    axes[1].plot(x_r, stats.norm.pdf(x_r, 0, np.sqrt(time_pt)), lw=2)
axes[1].set_title("W(t) ~ N(0,t) at Different Times"); axes[1].legend()
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Geometric Brownian Motion (GBM)

$$dS = \\mu S\\, dt + \\sigma S\\, dW$$

Solution (Itô's lemma):
$$S(t) = S_0 \\exp\\left(\\left(\\mu - \\frac{\\sigma^2}{2}\\right)t + \\sigma W(t)\\right)$$

Properties:
- $E[S(t)] = S_0 e^{\\mu t}$
- $\\text{Var}[S(t)] = S_0^2 e^{2\\mu t}(e^{\\sigma^2 t} - 1)$"""),

    code("""# GBM simulation (stock price)
S0 = 100; mu = 0.08; sigma = 0.20
T_years = 2; n_steps = 504  # ~252 trading days per year
dt = T_years / n_steps
t_yr = np.linspace(0, T_years, n_steps+1)
n_paths = 500

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
final_prices = []
for _ in range(n_paths):
    Z = rng.normal(0, 1, n_steps)
    increments = (mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z
    log_S = np.log(S0) + np.concatenate([[0], np.cumsum(increments)])
    S = np.exp(log_S)
    final_prices.append(S[-1])
    if _ < 50:
        axes[0].plot(t_yr, S, alpha=0.15, lw=0.6, color="steelblue")
E_S = S0 * np.exp(mu * T_years)
axes[0].plot(t_yr, S0*np.exp(mu*t_yr), "r-", lw=2, label=f"E[S]={E_S:.0f}")
axes[0].set_title(f"GBM — {n_paths} paths, μ={mu}, σ={sigma}")
axes[0].set_xlabel("Years"); axes[0].set_ylabel("Price")
axes[0].legend()

axes[1].hist(final_prices, bins=60, density=True, alpha=0.7, edgecolor="none")
axes[1].axvline(np.mean(final_prices), color="red", lw=2, label=f"Mean={np.mean(final_prices):.0f}")
axes[1].set_title(f"Distribution of S(T={T_years})")
axes[1].legend()
plt.tight_layout(); plt.show()

# Option pricing (European call)
K = 100  # strike
call_payoffs = np.maximum(np.array(final_prices) - K, 0)
call_price = np.exp(-0.04 * T_years) * np.mean(call_payoffs)
print(f"Monte Carlo call price (K=100, r=4%): ${call_price:.2f}")"""),

    md("""## 3. Ornstein-Uhlenbeck (Mean-Reverting) Process"""),

    code("""# Ornstein-Uhlenbeck: interest rate model
theta = 2.0   # mean reversion speed
mu_ou = 0.05  # long-run mean
sigma_ou = 0.02
X0 = 0.10
dt = 1/252; T_ou = 5; n_ou = int(T_ou/dt)
t_ou = np.linspace(0, T_ou, n_ou+1)

n_paths_ou = 5
plt.figure(figsize=(10, 5))
for _ in range(n_paths_ou):
    X = np.zeros(n_ou+1); X[0] = X0
    for k in range(n_ou):
        X[k+1] = (X[k] + theta*(mu_ou - X[k])*dt +
                  sigma_ou*np.sqrt(dt)*rng.standard_normal())
    plt.plot(t_ou, X*100, alpha=0.8, lw=1)
plt.axhline(mu_ou*100, color="red", lw=2, linestyle="--", label=f"Long-run mean={mu_ou*100:.1f}%")
plt.xlabel("Years"); plt.ylabel("Interest rate (%)")
plt.title("Ornstein-Uhlenbeck Process (Vasicek Rate Model)")
plt.legend(); plt.tight_layout(); plt.show()"""),

    code("""# Practice: First passage time
# How long until BM first hits level a?
a = 2.0
n_trials = 10_000
dt_fine = 0.001
first_passage = []
for _ in range(n_trials):
    W = 0
    t = 0
    for _ in range(100_000):
        W += rng.normal(0, np.sqrt(dt_fine))
        t += dt_fine
        if W >= a:
            first_passage.append(t)
            break

print(f"Simulated E[T_a={a}] = {np.mean(first_passage):.4f}")
print(f"Analytic: the first passage time has an inverse Gaussian distribution")
print(f"  (The distribution is heavy-tailed — mean may not converge for large a)")"""),
])
save(ch24, "24_stochastic_processes.ipynb")


# ── Chapter 25 ────────────────────────────────────────────────────────────────
ch25 = nb([
    md("""# Chapter 25 — Bayesian Networks
*Tier 3: Data Scientists & Developers*

## 🎯 Learning Objectives
- Represent conditional independence structures with DAGs
- Perform exact inference (variable elimination)
- Build and query a real Bayesian network with pgmpy/numpy"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import networkx as nx

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Bayesian Networks

A Bayesian network is a **DAG** where nodes are random variables
and edges encode direct conditional dependencies.

**Factorisation theorem:**
$$P(X_1, \\ldots, X_n) = \\prod_{i=1}^n P(X_i \\mid \\text{parents}(X_i))$$

This is the key computational advantage — we only need to store CPDs
(Conditional Probability Distributions), not the full joint table."""),

    code("""# Visualise the Asia BN (classic benchmark)
G = nx.DiGraph()
edges = [
    ("Smoking", "LungCancer"),
    ("Smoking", "Bronchitis"),
    ("LungCancer", "Dyspnoea"),
    ("LungCancer", "XRay"),
    ("Bronchitis", "Dyspnoea"),
    ("VisitToAsia", "Tuberculosis"),
    ("Tuberculosis", "XRay"),
    ("Tuberculosis", "Dyspnoea"),
]
G.add_edges_from(edges)

pos = {
    "Smoking": (2, 3), "VisitToAsia": (0, 3),
    "LungCancer": (1, 2), "Bronchitis": (3, 2), "Tuberculosis": (0, 2),
    "XRay": (0.5, 1), "Dyspnoea": (2, 1),
}
plt.figure(figsize=(9, 6))
nx.draw_networkx(G, pos, node_size=2500, node_color="steelblue",
                 font_color="white", font_size=9, arrows=True, arrowsize=20,
                 connectionstyle="arc3,rad=0.05")
plt.title("Asia Bayesian Network (Classic Benchmark)")
plt.axis("off"); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Variable Elimination

To compute $P(A)$ from a joint distribution, sum out (marginalise) other variables:
$$P(A) = \\sum_{B,C,\\ldots} P(A, B, C, \\ldots)$$

Variable elimination exploits the factorisation to do this efficiently,
multiplying and marginalising factor by factor."""),

    code("""# Manual Bayesian network inference: Burglar Alarm example
# P(B), P(E), P(A|B,E), P(J|A), P(M|A)

p_B = 0.001  # prior burglary
p_E = 0.002  # prior earthquake

# P(A | B, E)
p_A_given = {
    (True,  True):  0.95,
    (True,  False): 0.94,
    (False, True):  0.29,
    (False, False): 0.001,
}
p_J_given = {True: 0.90, False: 0.05}  # P(J=1 | A)
p_M_given = {True: 0.70, False: 0.01}  # P(M=1 | A)

def compute_joint(b, e, a, j, m):
    p_b = p_B if b else 1-p_B
    p_e = p_E if e else 1-p_E
    p_a = p_A_given[(b,e)] if a else 1-p_A_given[(b,e)]
    p_j = p_J_given[a] if j else 1-p_J_given[a]
    p_m = p_M_given[a] if m else 1-p_M_given[a]
    return p_b * p_e * p_a * p_j * p_m

# Query: P(B=1 | J=1, M=1)
numerator   = sum(compute_joint(True,  e, a, True, True)
                  for e in [True,False] for a in [True,False])
denominator = sum(compute_joint(b, e, a, True, True)
                  for b in [True,False] for e in [True,False] for a in [True,False])
print(f"P(Burglary | JohnCalls=1, MaryCalls=1) = {numerator/denominator:.6f}")"""),

    code("""# Naive Bayes classifier (a simple BN)
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X, y = iris.data, iris.target
nb_model = GaussianNB()
scores = cross_val_score(nb_model, X, y, cv=10)
print(f"Naive Bayes on Iris — CV accuracy: {scores.mean():.4f} ± {scores.std():.4f}")

nb_model.fit(X, y)
print("\nClass priors:", nb_model.class_prior_.round(3))
print("Learned feature means per class:")
print(nb_model.theta_.round(2))"""),

    code("""# Practice: build a simple spam filter BN
# P(spam), P(word | spam), P(word | not spam)
p_spam = 0.30
# Feature: contains word "free"
p_free_given_spam = 0.70
p_free_given_ham  = 0.05

# Query: P(spam | "free" present)
p_free = p_free_given_spam * p_spam + p_free_given_ham * (1 - p_spam)
p_spam_given_free = (p_free_given_spam * p_spam) / p_free
print(f"P(spam | 'free') = {p_spam_given_free:.4f}")

# Multiple evidence: "free" AND "win"
p_win_given_spam = 0.65; p_win_given_ham = 0.02
# Naive Bayes (conditional independence assumed)
p_spam_given_both = (p_free_given_spam * p_win_given_spam * p_spam)
p_ham_given_both  = (p_free_given_ham  * p_win_given_ham  * (1-p_spam))
p_spam_posterior  = p_spam_given_both / (p_spam_given_both + p_ham_given_both)
print(f"P(spam | 'free', 'win') = {p_spam_posterior:.4f}")"""),
])
save(ch25, "25_bayesian_networks.ipynb")


# ── Chapter 26 ────────────────────────────────────────────────────────────────
ch26 = nb([
    md("""# Chapter 26 — Regression Deep Dive: OLS, Assumptions, Diagnostics
*Tier 3: All Tracks*

## 🎯 Learning Objectives
- Master OLS inference: t-tests, F-test, R², adjusted R²
- Detect and fix violations: heteroscedasticity, multicollinearity, non-linearity
- Extend to logistic and Poisson regression"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
import pandas as pd
import seaborn as sns

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. OLS — The Full Inference Framework

$$y = X\\beta + \\varepsilon, \\quad \\varepsilon \\sim N(0, \\sigma^2 I)$$

Key statistics:
- $\\hat\\beta = (X^TX)^{-1}X^Ty$
- $\\hat\\sigma^2 = \\text{RSS}/(n-p-1)$
- $\\text{Var}(\\hat\\beta) = \\hat\\sigma^2 (X^TX)^{-1}$
- **t-test** for each $\\hat\\beta_j$: $t = \\hat\\beta_j / \\text{SE}(\\hat\\beta_j)$
- **F-test** for overall significance: $F = \\frac{\\text{RSS}_{\\text{null}} - \\text{RSS}}{p} / \\frac{\\text{RSS}}{n-p-1}$"""),

    code("""# Boston housing-like data simulation
n = 500
rooms = rng.normal(6, 1.5, n)
crime = rng.exponential(5, n)
dist  = rng.uniform(1, 10, n)
price = 30 + 5*rooms - 0.3*crime - 1.2*dist + rng.normal(0, 5, n)

df = pd.DataFrame({"price": price, "rooms": rooms, "crime": crime, "dist": dist})
X = sm.add_constant(df[["rooms", "crime", "dist"]])
model = sm.OLS(df["price"], X).fit()
print(model.summary())"""),

    md("""## 2. Detecting and Fixing Heteroscedasticity"""),

    code("""# Generate heteroscedastic data
x_hetero = rng.uniform(1, 10, 200)
y_hetero = 2*x_hetero + rng.normal(0, x_hetero*0.4, 200)  # variance grows with x

model_ols = sm.OLS(y_hetero, sm.add_constant(x_hetero)).fit()
residuals = model_ols.resid

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].scatter(model_ols.fittedvalues, residuals, alpha=0.5, s=20)
axes[0].axhline(0, color="red"); axes[0].set_title("Residuals vs Fitted (Heteroscedastic)")
axes[0].set_xlabel("Fitted"); axes[0].set_ylabel("Residuals")

# Fix: WLS or log-transform
model_log = sm.OLS(np.log(y_hetero), sm.add_constant(np.log(x_hetero))).fit()
res_log = model_log.resid
axes[1].scatter(model_log.fittedvalues, res_log, alpha=0.5, s=20)
axes[1].axhline(0, color="red"); axes[1].set_title("After Log Transform (Fixed)")
axes[1].set_xlabel("Fitted log(y)"); axes[1].set_ylabel("Residuals")
plt.tight_layout(); plt.show()

# Breusch-Pagan test
from statsmodels.stats.diagnostic import het_breuschpagan
bp_stat, bp_p, _, _ = het_breuschpagan(residuals, model_ols.model.exog)
print(f"Breusch-Pagan test: LM={bp_stat:.3f}, p={bp_p:.4f}")
print("Heteroscedasticity detected ✅" if bp_p < 0.05 else "Homoscedastic ✅")"""),

    md("""## 3. Logistic and Poisson Regression (GLMs)"""),

    code("""# Logistic regression: probability of default
income = rng.normal(50, 15, 400)
age    = rng.normal(35, 10, 400)
logit  = -2 + 0.03*income - 0.05*age
p_default = 1 / (1 + np.exp(-logit))
default = rng.binomial(1, p_default)

glm_data = pd.DataFrame({"default": default, "income": income, "age": age})
X_glm = sm.add_constant(glm_data[["income", "age"]])
logit_model = sm.Logit(glm_data["default"], X_glm).fit(disp=False)
print(logit_model.summary().tables[1])

# Marginal effects
print("\nAverage Marginal Effects:")
print(logit_model.get_margeff().summary())"""),

    code("""# Poisson regression: accident counts
exposure = rng.uniform(1, 10, 200)
safety_score = rng.uniform(0, 10, 200)
mu_count = np.exp(0.5 + 0.1*exposure - 0.2*safety_score)
counts = rng.poisson(mu_count)

poisson_data = pd.DataFrame({"count": counts, "exposure": exposure, "safety": safety_score})
X_pois = sm.add_constant(poisson_data[["exposure", "safety"]])
pois_model = sm.GLM(poisson_data["count"], X_pois,
                    family=sm.families.Poisson()).fit()
print(pois_model.summary().tables[1])"""),
])
save(ch26, "26_regression_deep_dive.ipynb")


# ── Chapter 27 ────────────────────────────────────────────────────────────────
ch27 = nb([
    md("""# Chapter 27 — Time Series & Autocorrelation
*Tier 3: Engineers & Data Scientists*

## 🎯 Learning Objectives
- Identify stationarity, trend, and seasonality
- Compute ACF and PACF for model identification
- Fit ARIMA and decompose time series"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Time Series Components

Any time series can be decomposed:
$$Y_t = T_t + S_t + R_t \\quad \\text{(additive)}$$
$$Y_t = T_t \\times S_t \\times R_t \\quad \\text{(multiplicative)}$$

- $T_t$: **Trend** — long-run direction
- $S_t$: **Seasonality** — periodic patterns
- $R_t$: **Residual** — irregular random fluctuations

A series is **stationary** if mean, variance, and autocovariance don't change with time."""),

    code("""# Generate a time series with trend + seasonality + noise
n = 240  # 20 years of monthly data
t = np.arange(n)
trend     = 0.05 * t
seasonal  = 10 * np.sin(2*np.pi*t/12)
noise_ts  = rng.normal(0, 2, n)
y_ts = 50 + trend + seasonal + noise_ts

dates = pd.date_range("2000-01-01", periods=n, freq="ME")
ts = pd.Series(y_ts, index=dates)

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
axes[0,0].plot(ts); axes[0,0].set_title("Original Series")
axes[0,1].plot(trend); axes[0,1].set_title("Trend Component")
axes[1,0].plot(seasonal[:48]); axes[1,0].set_title("Seasonal Component (4 cycles)")
axes[1,1].plot(noise_ts[:60]); axes[1,1].set_title("Residuals (first 60)")
plt.suptitle("Time Series Decomposition Components", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — ACF and PACF

**Autocorrelation at lag $k$:**
$$\\rho_k = \\frac{\\text{Cov}(Y_t, Y_{t-k})}{\\text{Var}(Y_t)}$$

**ARIMA(p, d, q):**
- **p**: AR order (PACF cuts off after lag p)
- **d**: differencing order (to achieve stationarity)
- **q**: MA order (ACF cuts off after lag q)"""),

    code("""# Stationarity test and differencing
result = adfuller(y_ts, autolag="AIC")
print(f"ADF test on original series: stat={result[0]:.3f}, p={result[1]:.4f}")
print("Stationary ✅" if result[1] < 0.05 else "Non-stationary — need differencing")

y_diff = np.diff(y_ts)
result_d = adfuller(y_diff, autolag="AIC")
print(f"\nADF test after 1st differencing: stat={result_d[0]:.3f}, p={result_d[1]:.4f}")
print("Stationary ✅" if result_d[1] < 0.05 else "Still non-stationary")"""),

    code("""# Decomposition and ARIMA modelling
decomp = seasonal_decompose(ts, model="additive", period=12)
fig = decomp.plot()
fig.set_size_inches(12, 8)
plt.suptitle("STL Decomposition", fontweight="bold")
plt.tight_layout(); plt.show()

# Fit ARIMA(1,1,1) with seasonal component
model_arima = ARIMA(ts, order=(1,1,1), seasonal_order=(1,1,1,12)).fit()
forecast = model_arima.forecast(steps=24)
plt.figure(figsize=(12, 5))
ts[-48:].plot(label="Observed")
forecast.plot(label="Forecast (24 months)", style="r--")
plt.title("SARIMA(1,1,1)(1,1,1)[12] Forecast")
plt.legend(); plt.tight_layout(); plt.show()
print(f"\nAIC: {model_arima.aic:.1f}")"""),
])
save(ch27, "27_time_series_autocorrelation.ipynb")


# ── Chapter 28 ────────────────────────────────────────────────────────────────
ch28 = nb([
    md("""# Chapter 28 — MCMC: Markov Chain Monte Carlo
*Tier 3: Data Scientists & Students*

## 🎯 Learning Objectives
- Understand why direct sampling from complex posteriors is hard
- Implement Metropolis-Hastings and Gibbs sampling
- Apply MCMC to Bayesian parameter estimation"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Why MCMC?

For Bayesian inference, we want samples from:
$$p(\\theta | \\mathcal D) \\propto p(\\mathcal D | \\theta) \\cdot p(\\theta)$$

When this has no closed form (most real problems), we use **MCMC**:
construct a Markov chain whose **stationary distribution = target posterior**.

Key algorithms:
- **Metropolis-Hastings** (MH): general purpose, requires proposal distribution
- **Gibbs sampling**: samples each parameter conditional on others
- **HMC / NUTS**: gradient-based (used by Stan, PyMC)"""),

    code("""# Metropolis-Hastings for a bimodal distribution
def log_target(x):
    # Log density of bimodal: 0.3*N(-3,1) + 0.7*N(2,0.8)
    return np.log(0.3*stats.norm.pdf(x, -3, 1) + 0.7*stats.norm.pdf(x, 2, 0.8) + 1e-300)

def metropolis_hastings(n_samples, proposal_std=1.0, x0=0.0):
    samples = np.zeros(n_samples)
    x = x0
    n_accept = 0
    for i in range(n_samples):
        x_prop = x + rng.normal(0, proposal_std)
        log_ratio = log_target(x_prop) - log_target(x)
        if np.log(rng.random()) < log_ratio:
            x = x_prop
            n_accept += 1
        samples[i] = x
    return samples, n_accept/n_samples

samples, accept_rate = metropolis_hastings(50_000, proposal_std=1.5)
burn_in = 1000
samples_post = samples[burn_in:]
print(f"Acceptance rate: {accept_rate:.3f}")

x_range = np.linspace(-7, 6, 400)
target_pdf = 0.3*stats.norm.pdf(x_range,-3,1) + 0.7*stats.norm.pdf(x_range,2,0.8)

fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].plot(samples[:500], alpha=0.7, lw=0.8)
axes[0].axvline(burn_in, color="red", lw=1, label="Burn-in end")
axes[0].set_title("MH Trace (first 500 steps)"); axes[0].legend()

axes[1].hist(samples_post, bins=100, density=True, alpha=0.6, label="MH samples")
axes[1].plot(x_range, target_pdf, "r-", lw=2, label="True target")
axes[1].set_title("MH Posterior vs True Target"); axes[1].legend()
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Detailed Balance

MH satisfies **detailed balance** (→ stationary distribution = target):
$$\\pi(x)q(x'|x)\\alpha(x,x') = \\pi(x')q(x|x')\\alpha(x',x)$$

where the acceptance ratio:
$$\\alpha(x,x') = \\min\\left(1,\\; \\frac{\\pi(x')q(x|x')}{\\pi(x)q(x'|x)}\\right)$$"""),

    code("""# Gibbs sampling for Bayesian linear regression
# y = beta0 + beta1*x + eps, eps~N(0, sigma^2)
# Priors: beta~N(0,100), sigma^2~InvGamma(1,1)

n_data = 50
x_data = rng.uniform(-3, 3, n_data)
y_data = 2 + 1.5*x_data + rng.normal(0, 1, n_data)

X_mat = np.column_stack([np.ones(n_data), x_data])

# Gibbs sampler (conjugate Normal-InvGamma)
n_mcmc = 10_000; burnin = 2000
beta_samples = np.zeros((n_mcmc, 2))
sig2_samples = np.zeros(n_mcmc)

beta = np.array([0.0, 0.0]); sig2 = 1.0
prior_var = 100.0

for i in range(n_mcmc):
    # Sample beta | sigma^2, data
    V_post = np.linalg.inv(X_mat.T @ X_mat / sig2 + np.eye(2) / prior_var)
    m_post = V_post @ (X_mat.T @ y_data / sig2)
    beta = rng.multivariate_normal(m_post, V_post)
    # Sample sigma^2 | beta, data
    resid = y_data - X_mat @ beta
    a_post = 1 + n_data/2
    b_post = 1 + resid @ resid / 2
    sig2 = 1/rng.gamma(a_post, 1/b_post)
    beta_samples[i] = beta
    sig2_samples[i] = sig2

b0_post = beta_samples[burnin:, 0]
b1_post = beta_samples[burnin:, 1]
s2_post = sig2_samples[burnin:]
print(f"β₀: mean={b0_post.mean():.3f}, 95% CI=[{np.percentile(b0_post,2.5):.3f}, {np.percentile(b0_post,97.5):.3f}] (true=2)")
print(f"β₁: mean={b1_post.mean():.3f}, 95% CI=[{np.percentile(b1_post,2.5):.3f}, {np.percentile(b1_post,97.5):.3f}] (true=1.5)")
print(f"σ²: mean={s2_post.mean():.3f}, 95% CI=[{np.percentile(s2_post,2.5):.3f}, {np.percentile(s2_post,97.5):.3f}] (true=1)")"""),

    code("""# Convergence diagnostics
fig, axes = plt.subplots(2, 2, figsize=(13, 7))
# Trace plots
axes[0,0].plot(b0_post[:2000], lw=0.5); axes[0,0].set_title("β₀ Trace")
axes[0,1].plot(b1_post[:2000], lw=0.5); axes[0,1].set_title("β₁ Trace")
# Posteriors
axes[1,0].hist(b0_post, bins=60, density=True, alpha=0.7)
axes[1,0].axvline(2, color="red", lw=2, label="True β₀=2"); axes[1,0].legend()
axes[1,0].set_title("β₀ Posterior")
axes[1,1].hist(b1_post, bins=60, density=True, alpha=0.7)
axes[1,1].axvline(1.5, color="red", lw=2, label="True β₁=1.5"); axes[1,1].legend()
axes[1,1].set_title("β₁ Posterior")
plt.tight_layout(); plt.show()"""),
])
save(ch28, "28_mcmc.ipynb")


# ── Chapter 29 ────────────────────────────────────────────────────────────────
ch29 = nb([
    md("""# Chapter 29 — Multivariate Statistics
*Tier 3: Students & Data Scientists*

## 🎯 Learning Objectives
- Work with multivariate normal distributions
- Apply PCA for dimensionality reduction
- Understand MANOVA, discriminant analysis"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris, load_digits
from sklearn.preprocessing import StandardScaler
import seaborn as sns

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Multivariate Normal Distribution

$$\\mathbf X \\sim N_p(\\boldsymbol\\mu, \\boldsymbol\\Sigma)$$

$$f(\\mathbf x) = \\frac{1}{(2\\pi)^{p/2}|\\boldsymbol\\Sigma|^{1/2}}
\\exp\\left(-\\frac{1}{2}(\\mathbf x - \\boldsymbol\\mu)^T \\boldsymbol\\Sigma^{-1} (\\mathbf x - \\boldsymbol\\mu)\\right)$$

Key properties:
- Marginals are univariate normals
- Conditional distributions are also normal
- $\\mathbf{X}^T \\boldsymbol\\Sigma^{-1}\\mathbf X \\sim \\chi^2_p$ (Mahalanobis distance)"""),

    code("""# Bivariate normal: effect of correlation
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, rho in zip(axes, [-0.8, 0.0, 0.8]):
    Sigma = np.array([[1, rho], [rho, 1]])
    mu_bv = np.array([0, 0])
    data_bv = rng.multivariate_normal(mu_bv, Sigma, 500)
    ax.scatter(data_bv[:,0], data_bv[:,1], alpha=0.3, s=15)
    # Plot contour of PDF
    x_g = np.linspace(-3.5, 3.5, 80)
    X1, X2 = np.meshgrid(x_g, x_g)
    pos = np.dstack((X1, X2))
    rv = stats.multivariate_normal(mu_bv, Sigma)
    ax.contour(X1, X2, rv.pdf(pos), levels=6, colors="red", linewidths=1)
    ax.set_title(f"ρ={rho}")
    ax.set_xlabel("X₁"); ax.set_ylabel("X₂")
plt.suptitle("Bivariate Normal — Effect of Correlation", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Principal Component Analysis

PCA finds orthogonal directions of maximum variance.

1. Compute covariance matrix $\\mathbf S$
2. Eigen-decompose: $\\mathbf S = \\mathbf V \\mathbf\\Lambda \\mathbf V^T$
3. Project: $\\mathbf Z = \\mathbf X \\mathbf V_k$ (first $k$ eigenvectors)

Proportion of variance explained by PC $j$:
$$\\frac{\\lambda_j}{\\sum_i \\lambda_i}$$"""),

    code("""# PCA on Iris dataset
iris = load_iris()
X_iris, y_iris = iris.data, iris.target
X_scaled = StandardScaler().fit_transform(X_iris)

pca = PCA()
pca.fit(X_scaled)
explained = pca.explained_variance_ratio_

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].bar(range(1, 5), explained*100, color="steelblue")
axes[0].plot(range(1, 5), np.cumsum(explained)*100, "ro-")
axes[0].set_xlabel("Principal Component"); axes[0].set_ylabel("Variance Explained (%)")
axes[0].set_title("Scree Plot — Iris PCA")

X_pca = pca.transform(X_scaled)
colors = ["red", "blue", "green"]
for cls in range(3):
    mask = y_iris == cls
    axes[1].scatter(X_pca[mask,0], X_pca[mask,1], alpha=0.7, s=30,
                    label=iris.target_names[cls], color=colors[cls])
axes[1].set_xlabel(f"PC1 ({explained[0]*100:.1f}%)"); axes[1].set_ylabel(f"PC2 ({explained[1]*100:.1f}%)")
axes[1].set_title("PCA — Iris (2 Components)"); axes[1].legend()
plt.tight_layout(); plt.show()
print(f"PC1+PC2 explain {(explained[0]+explained[1])*100:.1f}% of variance")"""),

    code("""# Mahalanobis distance for outlier detection
Sigma_est = np.cov(X_iris.T)
mu_est = X_iris.mean(axis=0)
Sigma_inv = np.linalg.inv(Sigma_est)
mahal_dist = np.array([
    np.sqrt((x - mu_est) @ Sigma_inv @ (x - mu_est))
    for x in X_iris
])
threshold = np.sqrt(stats.chi2.ppf(0.975, df=4))
outliers = np.where(mahal_dist > threshold)[0]
print(f"Outliers (Mahalanobis > {threshold:.2f}): {len(outliers)} samples")
print(f"Indices: {outliers}")

plt.figure(figsize=(10, 4))
plt.plot(mahal_dist, "b.", markersize=4)
plt.axhline(threshold, color="red", linestyle="--", label=f"χ² threshold (97.5%)")
plt.scatter(outliers, mahal_dist[outliers], color="red", s=60, zorder=5, label="Outliers")
plt.xlabel("Sample index"); plt.ylabel("Mahalanobis distance")
plt.title("Outlier Detection via Mahalanobis Distance")
plt.legend(); plt.tight_layout(); plt.show()"""),
])
save(ch29, "29_multivariate_statistics.ipynb")


# ── Chapter 30 ────────────────────────────────────────────────────────────────
ch30 = nb([
    md("""# Chapter 30 — Capstone: End-to-End Probabilistic Problem
*Tier 3: All Tracks*

## 🎯 Capstone Challenge

Build a complete probabilistic pipeline from raw data to actionable decision.

**Scenario:** You are a data scientist at an e-commerce company.
You need to:
1. Analyse conversion rate data and understand its distribution
2. Run a Bayesian A/B test for a new checkout flow
3. Quantify uncertainty with bootstrap confidence intervals
4. Make a business decision with expected value calculations
5. Communicate the result with visualisations"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("="*55)
print("CAPSTONE: End-to-End Probabilistic A/B Test Analysis")
print("="*55)"""),

    md("""## Step 1 — Data Generation & Exploration"""),

    code("""# Simulate experiment data
n_control   = 2000  # control group size
n_treatment = 2000  # treatment group size

p_control   = 0.050   # baseline conversion rate
p_treatment = 0.063   # true treatment effect (+1.3pp)

conversions_control   = rng.binomial(1, p_control,   n_control)
conversions_treatment = rng.binomial(1, p_treatment, n_treatment)

cr_control   = conversions_control.mean()
cr_treatment = conversions_treatment.mean()
lift = (cr_treatment - cr_control) / cr_control * 100

print(f"Control:   n={n_control:,}, conversions={conversions_control.sum():,}, CR={cr_control:.4f} ({cr_control*100:.2f}%)")
print(f"Treatment: n={n_treatment:,}, conversions={conversions_treatment.sum():,}, CR={cr_treatment:.4f} ({cr_treatment*100:.2f}%)")
print(f"Observed lift: {lift:.1f}%")"""),

    md("""## Step 2 — Frequentist Inference"""),

    code("""# Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

counts  = np.array([conversions_treatment.sum(), conversions_control.sum()])
nobs    = np.array([n_treatment, n_control])
z_stat, p_val = proportions_ztest(counts, nobs)

ci_control   = proportion_confint(conversions_control.sum(),   n_control,   method="wilson")
ci_treatment = proportion_confint(conversions_treatment.sum(), n_treatment, method="wilson")

print(f"Z-statistic: {z_stat:.3f}")
print(f"p-value:     {p_val:.4f}")
print(f"Control CI (95%):   [{ci_control[0]:.4f}, {ci_control[1]:.4f}]")
print(f"Treatment CI (95%): [{ci_treatment[0]:.4f}, {ci_treatment[1]:.4f}]")
print("✅ Statistically significant" if p_val < 0.05 else "❌ Not significant")"""),

    md("""## Step 3 — Bayesian Analysis"""),

    code("""# Bayesian A/B test: Beta-Binomial model
# Prior: Beta(1, 1) — uninformative
a0, b0 = 1, 1

# Posterior parameters
a_ctrl  = a0 + conversions_control.sum()
b_ctrl  = b0 + n_control - conversions_control.sum()
a_treat = a0 + conversions_treatment.sum()
b_treat = b0 + n_treatment - conversions_treatment.sum()

# Sample from posteriors
n_post = 200_000
samples_ctrl  = rng.beta(a_ctrl, b_ctrl, n_post)
samples_treat = rng.beta(a_treat, b_treat, n_post)

p_treatment_wins = (samples_treat > samples_ctrl).mean()
lift_samples = (samples_treat - samples_ctrl) / samples_ctrl * 100

print(f"P(treatment > control): {p_treatment_wins:.4f}")
print(f"Expected lift (mean):   {lift_samples.mean():.2f}%")
print(f"95% Credible interval for lift: [{np.percentile(lift_samples, 2.5):.2f}%, {np.percentile(lift_samples, 97.5):.2f}%]")

p_range = np.linspace(0.02, 0.10, 500)
plt.figure(figsize=(10, 5))
plt.plot(p_range, stats.beta.pdf(p_range, a_ctrl, b_ctrl), lw=2, label="Control posterior")
plt.plot(p_range, stats.beta.pdf(p_range, a_treat, b_treat), lw=2, label="Treatment posterior")
plt.axvline(p_control, color="blue", lw=1, linestyle=":", label="True p_control")
plt.axvline(p_treatment, color="orange", lw=1, linestyle=":", label="True p_treatment")
plt.xlabel("Conversion rate p"); plt.ylabel("Density")
plt.title(f"Bayesian Posteriors — P(treatment wins)={p_treatment_wins:.1%}")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## Step 4 — Bootstrap & Business Impact"""),

    code("""# Bootstrap CI for the lift
n_boot = 10_000
boot_lifts = []
for _ in range(n_boot):
    ctrl_b  = rng.choice(conversions_control,  n_control,  replace=True).mean()
    treat_b = rng.choice(conversions_treatment, n_treatment, replace=True).mean()
    boot_lifts.append((treat_b - ctrl_b) / ctrl_b * 100 if ctrl_b > 0 else 0)

boot_lo, boot_hi = np.percentile(boot_lifts, [2.5, 97.5])
print(f"Bootstrap 95% CI for lift: [{boot_lo:.2f}%, {boot_hi:.2f}%]")

# Expected value calculation
daily_visitors = 10_000
avg_order_value = 85  # dollars
current_revenue = daily_visitors * p_control * avg_order_value
expected_lift_frac = np.array(boot_lifts).mean() / 100
new_revenue = daily_visitors * cr_treatment * avg_order_value
uplift_daily = new_revenue - current_revenue
uplift_annual = uplift_daily * 365

print(f"\nBusiness Impact:")
print(f"  Current daily revenue:  ${current_revenue:,.0f}")
print(f"  Projected daily revenue: ${new_revenue:,.0f}")
print(f"  Daily uplift:            ${uplift_daily:,.0f}")
print(f"  Annual uplift (95% CI):  ${uplift_annual:,.0f}")"""),

    md("""## Step 5 — Final Dashboard & Decision"""),

    code("""fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.35)

# 1. Conversion rates with CI
ax1 = fig.add_subplot(gs[0, 0])
groups = ["Control", "Treatment"]
crs  = [cr_control, cr_treatment]
cis  = [ci_control, ci_treatment]
errs_lo = [cr - ci[0] for cr, ci in zip(crs, cis)]
errs_hi = [ci[1] - cr for cr, ci in zip(crs, cis)]
bars = ax1.bar(groups, [r*100 for r in crs], color=["steelblue","tomato"], width=0.5)
ax1.errorbar(groups, [r*100 for r in crs],
             yerr=[[e*100 for e in errs_lo], [e*100 for e in errs_hi]],
             fmt="none", color="black", capsize=8, lw=2)
ax1.set_ylabel("Conversion Rate (%)"); ax1.set_title("A/B Test Results")

# 2. Posterior distributions
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(p_range, stats.beta.pdf(p_range, a_ctrl, b_ctrl), lw=2, label="Control")
ax2.plot(p_range, stats.beta.pdf(p_range, a_treat, b_treat), lw=2, label="Treatment")
ax2.set_title(f"Bayesian Posteriors\nP(treatment wins)={p_treatment_wins:.1%}")
ax2.legend(fontsize=9); ax2.set_xlabel("p")

# 3. Bootstrap lift distribution
ax3 = fig.add_subplot(gs[0, 2])
ax3.hist(boot_lifts, bins=60, density=True, alpha=0.7, color="steelblue")
ax3.axvline(0, color="red", lw=2, linestyle="--", label="No effect")
ax3.axvspan(boot_lo, boot_hi, alpha=0.2, color="green", label="95% CI")
ax3.set_xlabel("Lift (%)"); ax3.set_title(f"Bootstrap Lift Distribution\nCI=[{boot_lo:.1f}%, {boot_hi:.1f}%]")
ax3.legend(fontsize=9)

# 4. Lift posterior from Bayesian
ax4 = fig.add_subplot(gs[1, 0:2])
ax4.hist(lift_samples, bins=100, density=True, alpha=0.7, color="tomato")
ax4.axvline(0, color="black", lw=2, linestyle="--", label="No effect")
lo_b, hi_b = np.percentile(lift_samples, [2.5, 97.5])
ax4.axvspan(lo_b, hi_b, alpha=0.2, color="blue", label=f"95% Credible: [{lo_b:.1f}%, {hi_b:.1f}%]")
ax4.set_xlabel("Lift (%)"); ax4.set_title("Bayesian Posterior of Lift")
ax4.legend(fontsize=9)

# 5. Decision summary
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis("off")
summary_text = (
    "DECISION SUMMARY\n"
    "─────────────────────\n"
    f"p-value: {p_val:.4f} {'✅' if p_val<0.05 else '❌'}\n"
    f"P(treatment wins): {p_treatment_wins:.1%}\n"
    f"Expected lift: {lift_samples.mean():.1f}%\n"
    f"Annual uplift: ${uplift_annual:,.0f}\n\n"
    "RECOMMENDATION:\n"
    "SHIP THE TREATMENT\n"
    "(strong evidence,\n"
    " profitable uplift)"
)
ax5.text(0.05, 0.95, summary_text, transform=ax5.transAxes, fontsize=11,
         verticalalignment="top", fontfamily="monospace",
         bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.3))

plt.suptitle("Capstone: End-to-End A/B Test Probabilistic Analysis",
             fontsize=14, fontweight="bold")
plt.savefig("capstone_dashboard.png", dpi=100, bbox_inches="tight")
plt.show()
print("\n✅ Dashboard saved as capstone_dashboard.png")"""),

    md("""## 🏆 Congratulations — You've Completed the Full Curriculum!

### What you've mastered:

**Tier 1 — Foundations (Chapters 1–12)**
- Probability rules, conditional probability, Bayes' Theorem
- Random variables, distributions, CLT, descriptive statistics

**Tier 2 — Track-Specific (Chapters 13–22)**
- 🎓 Students: combinatorics, hypothesis testing, exam strategy
- 💻 Developers: Monte Carlo, A/B testing, probabilistic data structures
- 📈 Data Scientists: MLE, bias-variance, causal inference
- ⚙️ Engineers: reliability, queuing, SPC, Six Sigma

**Tier 3 — Advanced (Chapters 23–30)**
- Markov chains, stochastic processes, Bayesian networks
- Regression, time series, MCMC, multivariate statistics
- ✅ This capstone: end-to-end probabilistic reasoning

**Total: 30 chapters | 4 tracks | ~1,700 minutes of content**

Keep exploring, keep building, and trust the math! 🎲"""),
])
save(ch30, "30_capstone_probabilistic_pipeline.ipynb")

print("\n🎉 All Tier 3 (Advanced) notebooks created successfully!")
