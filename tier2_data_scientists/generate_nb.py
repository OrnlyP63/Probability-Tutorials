"""Generate Tier 2 — Data Scientists track notebooks (chapters 13-22)."""
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
    md("""# Chapter 13 — Probability Distributions in Machine Learning
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Understand which distributions appear naturally in ML models
- Connect log-likelihood to model training
- Visualize how distribution choice affects model behavior"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import expit  # sigmoid
import seaborn as sns

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Distributions in ML

Every ML model is implicitly a **probabilistic model**.  When you choose:
- **MSE loss** → you assume Gaussian noise (linear regression)
- **Cross-entropy loss** → you assume Bernoulli/Categorical output
- **Poisson loss** → you assume count data

The distribution dictates the **likelihood function** the model maximises."""),

    code("""# --- Gaussian assumption behind MSE ---
x = np.linspace(-4, 4, 300)
for sigma in [0.5, 1.0, 2.0]:
    plt.plot(x, stats.norm.pdf(x, 0, sigma), label=f"σ={sigma}")
plt.title("Gaussian Noise Assumptions (MSE regression)")
plt.xlabel("Residual"); plt.ylabel("Density")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Log-Likelihood Derivation

For n i.i.d. observations from $N(\\mu, \\sigma^2)$:

$$\\mathcal{L}(\\mu, \\sigma | x_1,\\ldots,x_n) = \\prod_{i=1}^n \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x_i-\\mu)^2}{2\\sigma^2}}$$

Taking logs (log-likelihood):
$$\\ell = -n\\ln\\sigma - \\frac{n}{2}\\ln(2\\pi) - \\frac{1}{2\\sigma^2}\\sum_{i=1}^n(x_i-\\mu)^2$$

Maximising $\\ell$ w.r.t. $\\mu$ gives $\\hat\\mu = \\bar x$, and minimising
$\\sum(x_i-\\mu)^2$ (MSE) gives the **same answer** — MSE *is* MLE under Gaussian."""),

    code("""# Visualise: negative log-likelihood surface for mu and sigma
x_data = rng.normal(3, 1.5, 50)
mu_grid = np.linspace(1, 5, 60)
sig_grid = np.linspace(0.5, 3.5, 60)
MU, SIG = np.meshgrid(mu_grid, sig_grid)
NLL = np.array([[-stats.norm.logpdf(x_data, m, s).sum()
                  for m in mu_grid] for s in sig_grid])

plt.figure(figsize=(8, 5))
cp = plt.contourf(MU, SIG, NLL, levels=20, cmap="RdYlGn_r")
plt.colorbar(cp, label="Negative Log-Likelihood")
best = np.unravel_index(NLL.argmin(), NLL.shape)
plt.scatter(MU[best], SIG[best], c="red", s=100, zorder=5, label="Minimum NLL")
plt.xlabel("μ"); plt.ylabel("σ"); plt.title("NLL Surface — Gaussian")
plt.legend(); plt.tight_layout(); plt.show()
print(f"MLE μ={MU[best]:.2f} (true 3), MLE σ={SIG[best]:.2f} (true 1.5)")"""),

    md("""## 3. Simulation — Distributions for Classification

For **binary classification**, outputs follow a **Bernoulli** distribution.
The **logistic function** maps any real number to [0,1]:
$$\\sigma(z) = \\frac{1}{1+e^{-z}} = P(y=1|x)$$"""),

    code("""# Logistic regression — decision boundary visualisation
np.random.seed(42)
n = 200
X = rng.normal(0, 1, (n, 2))
true_w = np.array([1.5, -1.0]); true_b = 0.5
z = X @ true_w + true_b
p = expit(z)
y = rng.binomial(1, p)

# Colour by class
plt.figure(figsize=(7, 5))
plt.scatter(X[y==0, 0], X[y==0, 1], alpha=0.5, label="Class 0")
plt.scatter(X[y==1, 0], X[y==1, 1], alpha=0.5, label="Class 1")
# Decision boundary: w.x + b = 0
x1 = np.linspace(-3, 3, 100)
x2 = -(true_w[0]*x1 + true_b) / true_w[1]
plt.plot(x1, x2, "k--", label="Decision boundary")
plt.title("Bernoulli Output — Binary Classification")
plt.legend(); plt.tight_layout(); plt.show()

# Cross-entropy loss
eps = 1e-9
bce = -np.mean(y*np.log(p+eps) + (1-y)*np.log(1-p+eps))
print(f"Cross-entropy loss: {bce:.4f}")"""),

    md("""## 4. Visualisation — Distribution Zoo for ML

| Task | Distribution | Loss function |
|------|-------------|--------------|
| Regression | Gaussian | MSE |
| Binary classification | Bernoulli | Binary cross-entropy |
| Multi-class | Categorical | Categorical cross-entropy |
| Count prediction | Poisson | Poisson NLL |
| Positive continuous | Gamma / Log-Normal | Gamma/Log-Normal NLL |"""),

    code("""fig, axes = plt.subplots(2, 3, figsize=(14, 8))
dists = [
    ("Gaussian (regression)", stats.norm(3, 1), np.linspace(-1, 7, 200), False),
    ("Bernoulli (binary clf)", None, [0, 1], True),
    ("Categorical (multi-class)", None, [0, 1, 2, 3], True),
    ("Poisson (count pred)", stats.poisson(4), range(15), True),
    ("Gamma (positive cont.)", stats.gamma(3, scale=1), np.linspace(0, 12, 200), False),
    ("Log-Normal", stats.lognorm(0.7, scale=np.exp(1)), np.linspace(0, 15, 200), False),
]
for ax, (title, dist, xs, is_discrete) in zip(axes.flat, dists):
    if title.startswith("Bernoulli"):
        ax.bar([0, 1], [0.35, 0.65], color=["steelblue", "salmon"])
    elif title.startswith("Categorical"):
        ax.bar([0,1,2,3], [0.1, 0.5, 0.3, 0.1], color="steelblue")
    elif is_discrete:
        ax.bar(xs, dist.pmf(list(xs)), color="steelblue")
    else:
        ax.plot(xs, dist.pdf(xs), lw=2)
        ax.fill_between(xs, dist.pdf(xs), alpha=0.3)
    ax.set_title(title, fontsize=10)
plt.suptitle("Distributions in Machine Learning", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 5. Real Dataset Exercise — Choosing the Right Distribution

We fit different distributions to the same dataset and compare log-likelihoods."""),

    code("""from scipy.stats import norm, expon, gamma, lognorm

# Generate a right-skewed dataset (like income / latency)
data = rng.gamma(2, scale=3, size=500)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
candidates = [
    ("Normal", norm, norm.fit(data)),
    ("Exponential", expon, expon.fit(data)),
    ("Gamma", gamma, gamma.fit(data)),
    ("Log-Normal", lognorm, lognorm.fit(data)),
]
x_range = np.linspace(data.min(), data.max(), 200)
for ax, (name, dist_cls, params) in zip(axes, candidates):
    ll = dist_cls.logpdf(data, *params).sum()
    ax.hist(data, bins=30, density=True, alpha=0.5, color="steelblue")
    ax.plot(x_range, dist_cls.pdf(x_range, *params), "r-", lw=2)
    ax.set_title(f"{name}\\nLog-L={ll:.0f}")
plt.suptitle("Distribution Fitting Comparison", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 6. Practice Problems

**P1.** A neural network outputs a sigmoid value of 0.82 for a sample whose true label is 1.
Compute the **binary cross-entropy** for this single sample.

**P2.** You observe 8, 3, 5, 12, 2 support tickets per hour.
Fit a Poisson distribution (MLE) and compute the probability of receiving 10+ tickets in one hour.

**P3.** Why does minimising MSE loss and maximising Gaussian log-likelihood give the **same** parameters?
Write a one-paragraph proof."""),

    code("""# P1
p_hat = 0.82; y_true = 1
bce_single = -(y_true * np.log(p_hat) + (1 - y_true) * np.log(1 - p_hat))
print(f"P1 BCE = {bce_single:.4f}")

# P2
tickets = np.array([8, 3, 5, 12, 2])
lam_mle = tickets.mean()
prob_10plus = 1 - stats.poisson.cdf(9, lam_mle)
print(f"P2 λ_MLE={lam_mle:.1f}, P(X>=10)={prob_10plus:.4f}")"""),
])
save(ch13, "13_distributions_in_ml.ipynb")


# ── Chapter 14 ────────────────────────────────────────────────────────────────
ch14 = nb([
    md("""# Chapter 14 — Maximum Likelihood Estimation (MLE)
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Understand MLE as a principled way to fit distributions to data
- Derive MLE analytically for common distributions
- Implement numerical MLE with scipy.optimize"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.optimize as opt

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — What Is MLE?

**Maximum Likelihood Estimation** answers: *which parameter values make the
observed data most probable?*

$$\\hat{\\theta}_{MLE} = \\arg\\max_{\\theta} \\prod_{i=1}^n p(x_i | \\theta)$$

In practice, maximise the **log-likelihood** (same maximum, numerically better):
$$\\hat{\\theta}_{MLE} = \\arg\\max_{\\theta} \\sum_{i=1}^n \\log p(x_i | \\theta)$$"""),

    code("""# Visualise likelihood as function of parameter
data = rng.normal(5, 2, 30)
mu_values = np.linspace(2, 8, 200)
log_likelihoods = [stats.norm.logpdf(data, mu, 2).sum() for mu in mu_values]

plt.plot(mu_values, log_likelihoods)
plt.axvline(data.mean(), color="red", linestyle="--", label=f"MLE μ={data.mean():.2f}")
plt.xlabel("μ"); plt.ylabel("Log-Likelihood")
plt.title("Log-Likelihood as a Function of μ (σ=2 known)")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Deriving MLE for Gaussian

For $X \\sim N(\\mu, \\sigma^2)$:
$$\\ell(\\mu,\\sigma) = -n\\ln\\sigma - \\frac{1}{2\\sigma^2}\\sum(x_i - \\mu)^2 + C$$

Setting $\\frac{\\partial \\ell}{\\partial \\mu} = 0$:
$$\\hat\\mu_{MLE} = \\frac{1}{n}\\sum x_i = \\bar x$$

Setting $\\frac{\\partial \\ell}{\\partial \\sigma} = 0$:
$$\\hat\\sigma^2_{MLE} = \\frac{1}{n}\\sum(x_i - \\bar x)^2$$

⚠️ Note: MLE variance is **biased** (divides by n, not n-1)."""),

    code("""data = rng.normal(5, 2, 1000)
mu_mle = data.mean()
sigma_mle = data.std(ddof=0)   # MLE (biased)
sigma_unb = data.std(ddof=1)   # Unbiased

print(f"True μ=5, σ=2")
print(f"MLE:      μ={mu_mle:.3f}, σ={sigma_mle:.3f}")
print(f"Unbiased: μ={mu_mle:.3f}, σ={sigma_unb:.3f}")
print(f"Bias in σ²: {sigma_unb**2 - sigma_mle**2:.4f}")"""),

    md("""## 3. Simulation — MLE for Exponential Distribution

$X \\sim \\text{Exp}(\\lambda)$:  $f(x) = \\lambda e^{-\\lambda x}$

Log-likelihood: $\\ell(\\lambda) = n\\ln\\lambda - \\lambda \\sum x_i$

MLE: $\\hat\\lambda = \\frac{n}{\\sum x_i} = \\frac{1}{\\bar x}$"""),

    code("""lam_true = 0.5
data_exp = rng.exponential(1/lam_true, 200)

lam_values = np.linspace(0.1, 1.5, 300)
ll_exp = [len(data_exp)*np.log(l) - l*data_exp.sum() for l in lam_values]

lam_mle = 1 / data_exp.mean()
plt.plot(lam_values, ll_exp, label="Log-likelihood")
plt.axvline(lam_mle, color="red", linestyle="--", label=f"MLE λ={lam_mle:.3f}")
plt.axvline(lam_true, color="green", linestyle=":", label=f"True λ={lam_true}")
plt.xlabel("λ"); plt.ylabel("Log-likelihood")
plt.title("MLE for Exponential Distribution")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 4. Visualisation — Numerical MLE with scipy

For distributions where the analytical solution is complex, use `scipy.optimize`."""),

    code("""# Fit a Beta distribution numerically
data_beta = rng.beta(2, 5, 500)

def neg_ll_beta(params):
    a, b = params
    if a <= 0 or b <= 0:
        return np.inf
    return -stats.beta.logpdf(data_beta, a, b).sum()

result = opt.minimize(neg_ll_beta, x0=[1, 1], method="Nelder-Mead")
a_hat, b_hat = result.x

x = np.linspace(0.001, 0.999, 200)
plt.hist(data_beta, bins=30, density=True, alpha=0.5, label="Data")
plt.plot(x, stats.beta.pdf(x, a_hat, b_hat), "r-", lw=2,
         label=f"MLE fit: a={a_hat:.2f}, b={b_hat:.2f}")
plt.plot(x, stats.beta.pdf(x, 2, 5), "g--", lw=2, label="True: a=2, b=5")
plt.title("Numerical MLE — Beta Distribution")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 5. Real Dataset Exercise — Fitting User Session Durations"""),

    code("""# Simulate user session times (right-skewed, like real web analytics)
sessions = rng.lognormal(mean=np.log(120), sigma=0.8, size=1000)

# Fit candidates
dist_candidates = {
    "Exponential": stats.expon,
    "Log-Normal": stats.lognorm,
    "Gamma": stats.gamma,
    "Weibull": stats.weibull_min,
}
print("Distribution Fitting Results:")
print(f"{'Distribution':<15} {'Log-L':>10} {'AIC':>10}")
for name, dist in dist_candidates.items():
    params = dist.fit(sessions)
    ll = dist.logpdf(sessions, *params).sum()
    k = len(params)
    aic = 2*k - 2*ll
    print(f"{name:<15} {ll:>10.1f} {aic:>10.1f}")"""),

    md("""## 6. Practice Problems

**P1.** You observe 7 coin flips: H H T H H T H. Derive the MLE for p (P(Heads)) analytically.

**P2.** A Poisson process produces counts [3, 5, 2, 8, 4]. Write code to find MLE λ both
analytically (formula) and numerically (`scipy.optimize.minimize`). Verify they agree.

**P3.** Why is $\\hat\\sigma^2_{MLE} = \\frac{1}{n}\\sum(x_i - \\bar x)^2$ biased?
Compute $E[\\hat\\sigma^2_{MLE}]$ to show the bias."""),

    code("""# P1
heads, flips = 5, 7
p_mle = heads / flips
print(f"P1: MLE p = {heads}/{flips} = {p_mle:.4f}")

# P2
counts = np.array([3, 5, 2, 8, 4])
lam_analytical = counts.mean()
neg_ll = lambda lam: -stats.poisson.logpmf(counts, lam[0]).sum() if lam[0]>0 else np.inf
res = opt.minimize(neg_ll, [3.0], method="Nelder-Mead")
print(f"P2: Analytical λ={lam_analytical:.2f}, Numerical λ={res.x[0]:.2f}")"""),
])
save(ch14, "14_maximum_likelihood_estimation.ipynb")


# ── Chapter 15 ────────────────────────────────────────────────────────────────
ch15 = nb([
    md("""# Chapter 15 — Bias-Variance Tradeoff
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Decompose prediction error into bias, variance, and irreducible noise
- Visualise underfitting and overfitting
- Use cross-validation to navigate the tradeoff"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — The Bias-Variance Decomposition

Expected MSE for a point $x_0$:
$$E[(y - \\hat f(x_0))^2] = \\text{Bias}^2 + \\text{Variance} + \\sigma^2_{\\varepsilon}$$

- **Bias**: error from wrong assumptions (underfitting)
- **Variance**: sensitivity to training set fluctuations (overfitting)
- **Irreducible noise**: unavoidable noise in the data"""),

    code("""# True function
f_true = lambda x: np.sin(2 * np.pi * x)
sigma_noise = 0.3
x_test = np.linspace(0, 1, 200)

n_train = 30
n_experiments = 200
degrees = [1, 4, 15]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, degree in zip(axes, degrees):
    predictions = []
    for _ in range(n_experiments):
        x_train = rng.uniform(0, 1, n_train)
        y_train = f_true(x_train) + rng.normal(0, sigma_noise, n_train)
        model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-6))
        model.fit(x_train.reshape(-1,1), y_train)
        predictions.append(model.predict(x_test.reshape(-1,1)))
    preds = np.array(predictions)
    bias2 = (preds.mean(axis=0) - f_true(x_test))**2
    variance = preds.var(axis=0)
    for p in preds[:20]:
        ax.plot(x_test, p, alpha=0.1, color="blue")
    ax.plot(x_test, f_true(x_test), "r-", lw=2, label="True")
    ax.plot(x_test, preds.mean(axis=0), "k--", lw=2, label="Mean pred")
    ax.set_title(f"Degree={degree}\nBias²={bias2.mean():.3f}  Var={variance.mean():.3f}")
    ax.legend(fontsize=8)
plt.suptitle("Bias-Variance Tradeoff", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Deriving the Decomposition

Let $y = f(x) + \\varepsilon$ where $E[\\varepsilon]=0$, $\\text{Var}[\\varepsilon]=\\sigma^2$.

$$E[(y - \\hat f)^2] = E[f^2 + \\hat f^2 + \\varepsilon^2 - 2f\\hat f - 2f\\varepsilon + 2\\hat f\\varepsilon]$$

Since $\\varepsilon \\perp \\hat f$, after algebra:
$$= (f - E[\\hat f])^2 + E[(\\hat f - E[\\hat f])^2] + \\sigma^2$$
$$= \\text{Bias}^2[\\hat f] + \\text{Var}[\\hat f] + \\sigma^2$$"""),

    code("""# Quantify bias² and variance for polynomial degrees
results = []
for degree in range(1, 16):
    preds = []
    for _ in range(300):
        x_train = rng.uniform(0, 1, n_train)
        y_train = f_true(x_train) + rng.normal(0, sigma_noise, n_train)
        model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-6))
        model.fit(x_train.reshape(-1,1), y_train)
        preds.append(model.predict(x_test.reshape(-1,1)))
    preds = np.array(preds)
    b2 = ((preds.mean(0) - f_true(x_test))**2).mean()
    v  = preds.var(0).mean()
    results.append((degree, b2, v, b2+v+sigma_noise**2))

degs, b2s, vs, total = zip(*results)
plt.figure(figsize=(9,5))
plt.plot(degs, b2s, "b-o", label="Bias²")
plt.plot(degs, vs,  "r-o", label="Variance")
plt.plot(degs, total, "k-o", label="Total MSE")
plt.axhline(sigma_noise**2, ls="--", color="gray", label=f"Irreducible (σ²={sigma_noise**2:.2f})")
plt.xlabel("Polynomial Degree"); plt.ylabel("Error")
plt.title("Bias-Variance Tradeoff Curve")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 3. Simulation — Regularisation Controls the Tradeoff

**Ridge regression** adds $\\alpha\\|w\\|^2$ to the loss, shrinking weights → increasing bias
but decreasing variance."""),

    code("""alphas = np.logspace(-4, 4, 50)
cv_scores = []
for alpha in alphas:
    model = make_pipeline(PolynomialFeatures(10), Ridge(alpha=alpha))
    x_all = rng.uniform(0, 1, 150)
    y_all = f_true(x_all) + rng.normal(0, sigma_noise, 150)
    scores = cross_val_score(model, x_all.reshape(-1,1), y_all,
                             cv=5, scoring="neg_mean_squared_error")
    cv_scores.append(-scores.mean())

best_alpha = alphas[np.argmin(cv_scores)]
plt.semilogx(alphas, cv_scores)
plt.axvline(best_alpha, color="red", linestyle="--", label=f"Best α={best_alpha:.4f}")
plt.xlabel("Regularisation α"); plt.ylabel("CV MSE")
plt.title("Cross-Validation Chooses Optimal Regularisation")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 4–6. Visualisation, Real Dataset & Practice"""),

    code("""from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

housing = fetch_california_housing()
X, y = housing.data, housing.target
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

alphas_lasso = np.logspace(-3, 1, 30)
train_errs, cv_errs = [], []
for a in alphas_lasso:
    m = Lasso(alpha=a, max_iter=5000)
    train_score = cross_val_score(m, X_scaled, y, cv=5, scoring="neg_mean_squared_error")
    cv_errs.append(-train_score.mean())

plt.semilogx(alphas_lasso, cv_errs, "b-o")
plt.xlabel("Lasso α"); plt.ylabel("CV MSE")
plt.title("California Housing — Lasso Regularisation Path")
plt.tight_layout(); plt.show()"""),

    code("""# Practice P1: compute bias and variance for kNN with k=1,5,20
from sklearn.neighbors import KNeighborsRegressor

x_tr = rng.uniform(0, 1, 50)
y_tr = f_true(x_tr) + rng.normal(0, sigma_noise, 50)

for k in [1, 5, 20]:
    preds_k = []
    for _ in range(200):
        xi = rng.uniform(0, 1, 50)
        yi = f_true(xi) + rng.normal(0, sigma_noise, 50)
        m = KNeighborsRegressor(n_neighbors=k)
        m.fit(xi.reshape(-1,1), yi)
        preds_k.append(m.predict(x_test.reshape(-1,1)))
    preds_k = np.array(preds_k)
    b2 = ((preds_k.mean(0) - f_true(x_test))**2).mean()
    v  = preds_k.var(0).mean()
    print(f"k={k:>2}: Bias²={b2:.4f}, Var={v:.4f}, Total≈{b2+v+sigma_noise**2:.4f}")"""),
])
save(ch15, "15_bias_variance_tradeoff.ipynb")


# ── Chapter 16 ────────────────────────────────────────────────────────────────
ch16 = nb([
    md("""# Chapter 16 — Bayesian vs Frequentist Thinking
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Understand the philosophical divide between Bayesian and Frequentist statistics
- Compute Bayesian credible intervals and frequentist confidence intervals
- See how they diverge and when each is appropriate"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import beta as beta_fn

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review

| | Frequentist | Bayesian |
|--|-------------|---------|
| Parameters | Fixed, unknown constants | Random variables with distributions |
| Data | Random (repeated sampling) | Fixed (observed) |
| Inference | Confidence intervals, p-values | Posterior distribution, credible intervals |
| Prior info | Not used | Explicitly incorporated |
| Statement | "95% of such intervals contain θ" | "P(θ in CI | data) = 0.95" |"""),

    code("""# Frequentist vs Bayesian: coin flip example
n_flips = 20; n_heads = 14

# Frequentist CI (Wilson interval)
p_hat = n_heads / n_flips
z = stats.norm.ppf(0.975)
ci_lo = (p_hat + z**2/(2*n_flips) - z*np.sqrt(p_hat*(1-p_hat)/n_flips + z**2/(4*n_flips**2))) / \
        (1 + z**2/n_flips)
ci_hi = (p_hat + z**2/(2*n_flips) + z*np.sqrt(p_hat*(1-p_hat)/n_flips + z**2/(4*n_flips**2))) / \
        (1 + z**2/n_flips)
print(f"Frequentist 95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")

# Bayesian: Beta(1,1) prior → Beta(1+14, 1+6) posterior
a_prior, b_prior = 1, 1
a_post = a_prior + n_heads
b_post = b_prior + (n_flips - n_heads)
cred_lo, cred_hi = stats.beta.ppf([0.025, 0.975], a_post, b_post)
print(f"Bayesian 95% credible interval: [{cred_lo:.3f}, {cred_hi:.3f}]")

p_range = np.linspace(0, 1, 300)
plt.figure(figsize=(9, 4))
plt.plot(p_range, stats.beta.pdf(p_range, a_post, b_post), "b-", lw=2, label="Posterior")
plt.axvspan(cred_lo, cred_hi, alpha=0.2, color="blue", label="95% Credible Interval")
plt.axvline(p_hat, color="red", linestyle="--", label=f"Freq. MLE p̂={p_hat:.2f}")
plt.xlabel("p"); plt.ylabel("Density"); plt.title("Bayesian vs Frequentist — Coin Flip")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Bayes' Theorem in Practice

$$p(\\theta | \\mathcal D) \\propto p(\\mathcal D | \\theta)\\, p(\\theta)$$

For $n$ Bernoulli trials with $k$ successes and $\\text{Beta}(\\alpha, \\beta)$ prior:
$$p(p | k, n) = \\text{Beta}(\\alpha + k,\\, \\beta + n - k)$$

This is a **conjugate prior** — prior and posterior have the same functional form."""),

    code("""# Show posterior updating step by step
fig, axes = plt.subplots(1, 4, figsize=(15, 4))
observations = [0, 5, 14, 50]
cumulative_heads = [0, 3, 8, 35]
prior_a, prior_b = 1, 1
for ax, (n_obs, k) in zip(axes, zip(observations, cumulative_heads)):
    a_p = prior_a + k
    b_p = prior_b + (n_obs - k)
    p_vals = np.linspace(0, 1, 300)
    ax.plot(p_vals, stats.beta.pdf(p_vals, a_p, b_p), lw=2)
    ax.axvline(a_p/(a_p+b_p), color="red", linestyle="--", label=f"Mean={a_p/(a_p+b_p):.2f}")
    ax.set_title(f"After {n_obs} flips\n({k} heads)")
    ax.legend(fontsize=8)
plt.suptitle("Bayesian Updating — Posterior Evolves with Data", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    md("""## 3-6. Simulation, Visualisation, Real Dataset & Practice"""),

    code("""# Misinterpretation demo: CI doesn't mean what most people think
n_simulations = 1000; n_data = 30; true_mu = 5.0
covered = 0
plt.figure(figsize=(12, 4))
for i in range(100):
    data = rng.normal(true_mu, 1, n_data)
    se = data.std(ddof=1) / np.sqrt(n_data)
    lo, hi = data.mean() - 1.96*se, data.mean() + 1.96*se
    color = "blue" if lo <= true_mu <= hi else "red"
    plt.plot([i, i], [lo, hi], color=color, alpha=0.6, lw=0.8)
for i in range(1000):
    data = rng.normal(true_mu, 1, n_data)
    se = data.std(ddof=1) / np.sqrt(n_data)
    lo, hi = data.mean() - 1.96*se, data.mean() + 1.96*se
    covered += (lo <= true_mu <= hi)
plt.axhline(true_mu, color="black", linewidth=1.5, label=f"True μ={true_mu}")
plt.title(f"95% CI Coverage: {covered/1000:.1%} of 1000 intervals contain μ")
plt.xlabel("Simulation"); plt.ylabel("Interval")
plt.legend(); plt.tight_layout(); plt.show()"""),

    code("""# Practice problems
# P1: Compute posterior mean and MAP for Beta(3,7) prior, 20 flips, 12 heads
a0, b0 = 3, 7; k, n = 12, 20
a1, b1 = a0+k, b0+(n-k)
post_mean = a1 / (a1+b1)
post_map  = (a1-1)/(a1+b1-2) if a1+b1>2 else 0.5
print(f"P1 posterior: Beta({a1},{b1})")
print(f"   Mean={post_mean:.4f}, MAP={post_map:.4f}")

# P2: Compare credible vs confidence interval width as n grows
for n_obs in [10, 50, 200, 1000]:
    k_obs = int(n_obs * 0.6)
    # Bayesian (uniform prior)
    a_p, b_p = 1+k_obs, 1+(n_obs-k_obs)
    cred = stats.beta.ppf(0.975, a_p, b_p) - stats.beta.ppf(0.025, a_p, b_p)
    # Frequentist
    ph = k_obs/n_obs
    conf = 2 * 1.96 * np.sqrt(ph*(1-ph)/n_obs)
    print(f"n={n_obs:>5}: Credible width={cred:.4f}, CI width={conf:.4f}")"""),
])
save(ch16, "16_bayesian_vs_frequentist.ipynb")


# ── Chapter 17 ────────────────────────────────────────────────────────────────
ch17 = nb([
    md("""# Chapter 17 — Hypothesis Testing for Model Evaluation
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Apply statistical tests to compare ML model performance
- Understand paired tests vs. independent tests
- Avoid common pitfalls: multiple comparisons, data leakage in testing"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Testing Models, Not Just Parameters

When comparing two models, we ask:
*Is Model A's performance **significantly better** than Model B, or is the
difference just random fluctuation from the train/test split?*

Key tests:
- **Paired t-test** (same CV folds): corrected for fold correlation
- **McNemar's test**: for binary classifiers on same test set
- **Wilcoxon signed-rank**: non-parametric alternative"""),

    code("""# Load real dataset
data = load_breast_cancer()
X, y = data.data, data.target
scaler = StandardScaler()
X_sc = scaler.fit_transform(X)

kf = KFold(n_splits=10, shuffle=True, random_state=42)
lr_scores  = cross_val_score(LogisticRegression(max_iter=1000), X_sc, y, cv=kf, scoring="accuracy")
rf_scores  = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=42), X_sc, y, cv=kf)

print(f"Logistic Regression: mean={lr_scores.mean():.4f}, std={lr_scores.std():.4f}")
print(f"Random Forest:       mean={rf_scores.mean():.4f}, std={rf_scores.std():.4f}")

# Paired t-test
t_stat, p_val = stats.ttest_rel(rf_scores, lr_scores)
print(f"\nPaired t-test: t={t_stat:.3f}, p={p_val:.4f}")
print("RF is significantly better" if p_val < 0.05 else "No significant difference")"""),

    md("""## 2. Math Walkthrough — Corrected Resampled t-Test

The standard paired t-test overestimates significance because CV folds
share training data. Nadeau & Bengio correction:

$$t = \\frac{\\bar d}{\\sqrt{(\\frac{1}{k} + \\frac{n_{test}}{n_{train}}) \\cdot \\hat\\sigma^2_d}}$$

where $d_i$ = performance difference on fold $i$."""),

    code("""def corrected_ttest(scores_a, scores_b, n_train_ratio=0.9):
    diffs = scores_a - scores_b
    n = len(diffs)
    mean_diff = diffs.mean()
    var_diff = diffs.var(ddof=1)
    correction = 1/n + (1-n_train_ratio)/n_train_ratio
    t_stat = mean_diff / np.sqrt(correction * var_diff)
    p_val = 2 * stats.t.sf(abs(t_stat), df=n-1)
    return t_stat, p_val

t_corr, p_corr = corrected_ttest(rf_scores, lr_scores)
t_std, p_std = stats.ttest_rel(rf_scores, lr_scores)
print(f"Standard paired t:  t={t_std:.3f},  p={p_std:.4f}")
print(f"Corrected t-test:   t={t_corr:.3f}, p={p_corr:.4f}")"""),

    md("""## 3–6. Multiple Comparisons, McNemar's, and Practice"""),

    code("""# Multiple comparisons — Bonferroni correction
models = {
    "LR": LogisticRegression(max_iter=1000),
    "RF": RandomForestClassifier(n_estimators=50, random_state=42),
    "GB": GradientBoostingClassifier(n_estimators=50, random_state=42),
}
all_scores = {name: cross_val_score(m, X_sc, y, cv=kf) for name, m in models.items()}

comparisons = [("RF", "LR"), ("GB", "LR"), ("RF", "GB")]
print("Model Comparison Results (α=0.05):")
for a, b in comparisons:
    t, p = stats.ttest_rel(all_scores[a], all_scores[b])
    p_bonf = min(p * len(comparisons), 1.0)
    sig = "✅ Significant" if p_bonf < 0.05 else "❌ Not significant"
    print(f"  {a} vs {b}: p={p:.4f}, p_bonf={p_bonf:.4f} — {sig}")"""),

    code("""# Practice: McNemar's test on binary predictions
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_sc, y, test_size=0.3, random_state=42)
lr = LogisticRegression(max_iter=1000).fit(X_train, y_train)
rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)

pred_lr = lr.predict(X_test)
pred_rf = rf.predict(X_test)

# Build 2x2 contingency table
b = ((pred_lr == y_test) & (pred_rf != y_test)).sum()  # LR right, RF wrong
c = ((pred_lr != y_test) & (pred_rf == y_test)).sum()  # LR wrong, RF right
print(f"McNemar: b={b}, c={c}")
chi2_mn = (abs(b-c)-1)**2 / (b+c)
p_mcnemar = 1 - stats.chi2.cdf(chi2_mn, df=1)
print(f"χ²={chi2_mn:.3f}, p={p_mcnemar:.4f}")
print("Significant difference" if p_mcnemar < 0.05 else "No significant difference")"""),
])
save(ch17, "17_hypothesis_testing_model_evaluation.ipynb")


# ── Chapter 18 ────────────────────────────────────────────────────────────────
ch18 = nb([
    md("""# Chapter 18 — Resampling: Bootstrap & Jackknife
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Understand bootstrapping for confidence intervals
- Implement the jackknife for bias estimation
- Apply resampling to ML model uncertainty"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Resampling Without Assumptions

The **bootstrap** simulates the sampling distribution by resampling with
replacement from the observed data:

1. Draw $B$ bootstrap samples of size $n$ (with replacement)
2. Compute the statistic $\\hat\\theta^*_b$ for each
3. The distribution of $\\hat\\theta^*_b$ estimates the sampling distribution

No Gaussian assumptions required — works for **any** statistic."""),

    code("""# Bootstrap CI for median — no closed-form formula exists
data = rng.exponential(scale=3, size=50)
B = 2000
boot_medians = [rng.choice(data, size=len(data), replace=True).mean() for _ in range(B)]

ci_lo, ci_hi = np.percentile(boot_medians, [2.5, 97.5])
print(f"Sample mean: {data.mean():.3f}")
print(f"Bootstrap 95% CI for mean: [{ci_lo:.3f}, {ci_hi:.3f}]")
print(f"Analytic CI (t-dist): [{data.mean()-1.96*data.std()/np.sqrt(len(data)):.3f}, {data.mean()+1.96*data.std()/np.sqrt(len(data)):.3f}]")

plt.hist(boot_medians, bins=50, density=True, alpha=0.7)
plt.axvspan(ci_lo, ci_hi, alpha=0.3, color="red", label="95% CI")
plt.axvline(data.mean(), color="black", linestyle="--", label="Sample mean")
plt.title("Bootstrap Distribution of Sample Mean")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — Jackknife Bias Estimation

The **jackknife** removes one observation at a time:
$$\\hat\\theta_{(-i)} = \\hat\\theta \\text{ computed without } x_i$$

Jackknife bias estimate:
$$\\widehat{\\text{bias}} = (n-1)(\\bar{\\hat\\theta}_{(-\\cdot)} - \\hat\\theta)$$

Jackknife variance estimate:
$$\\widehat{\\text{Var}}(\\hat\\theta) = \\frac{n-1}{n}\\sum_{i=1}^n (\\hat\\theta_{(-i)} - \\bar{\\hat\\theta}_{(-\\cdot)})^2$$"""),

    code("""# Jackknife for variance of correlation coefficient
np.random.seed(0)
n = 40
x = rng.normal(0, 1, n)
y = 0.7*x + rng.normal(0, 0.7, n)
r_hat = np.corrcoef(x, y)[0, 1]

jack_rs = [np.corrcoef(np.delete(x, i), np.delete(y, i))[0,1] for i in range(n)]
jack_mean = np.mean(jack_rs)
jack_bias = (n-1) * (jack_mean - r_hat)
jack_var  = (n-1)/n * sum((r - jack_mean)**2 for r in jack_rs)

print(f"r_hat = {r_hat:.4f}")
print(f"Jackknife bias = {jack_bias:.4f}")
print(f"Jackknife SE   = {np.sqrt(jack_var):.4f}")

# Bootstrap for comparison
boot_rs = [np.corrcoef(*rng.choice(np.c_[x,y], n, replace=True).T)[0,1] for _ in range(2000)]
print(f"Bootstrap SE   = {np.std(boot_rs):.4f}")"""),

    md("""## 3–6. Bootstrap for ML, Real Dataset, Practice"""),

    code("""from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_diabetes

diabetes = load_diabetes()
X_d, y_d = diabetes.data, diabetes.target

# Bootstrap coefficients
lr = LinearRegression()
coef_boots = []
for _ in range(1000):
    idx = rng.choice(len(X_d), len(X_d), replace=True)
    lr.fit(X_d[idx], y_d[idx])
    coef_boots.append(lr.coef_.copy())
coef_boots = np.array(coef_boots)

fig, axes = plt.subplots(2, 5, figsize=(15, 6))
feature_names = diabetes.feature_names
for i, ax in enumerate(axes.flat):
    if i < X_d.shape[1]:
        ax.hist(coef_boots[:, i], bins=30, alpha=0.7)
        ci = np.percentile(coef_boots[:, i], [2.5, 97.5])
        ax.axvline(ci[0], color="red", linestyle="--", lw=1)
        ax.axvline(ci[1], color="red", linestyle="--", lw=1)
        ax.axvline(0, color="black", lw=0.8)
        ax.set_title(feature_names[i], fontsize=9)
plt.suptitle("Bootstrap Distribution of Linear Regression Coefficients", fontweight="bold")
plt.tight_layout(); plt.show()"""),

    code("""# Practice: bootstrap CI for Sharpe ratio
returns = rng.normal(0.001, 0.02, 252)  # daily returns for 1 year
sharpe = returns.mean() / returns.std() * np.sqrt(252)
boot_sharpes = [(rng.choice(returns, len(returns), replace=True).mean() /
                 rng.choice(returns, len(returns), replace=True).std() * np.sqrt(252))
                for _ in range(2000)]
lo, hi = np.percentile(boot_sharpes, [2.5, 97.5])
print(f"Sharpe ratio: {sharpe:.3f}")
print(f"Bootstrap 95% CI: [{lo:.3f}, {hi:.3f}]")
print(f"Significantly > 0: {lo > 0}")"""),
])
save(ch18, "18_bootstrap_jackknife.ipynb")


# ── Chapter 19 ────────────────────────────────────────────────────────────────
ch19 = nb([
    md("""# Chapter 19 — Correlation, Covariance & Feature Selection
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Distinguish correlation from covariance
- Identify multicollinearity and its effects on models
- Apply correlation-based feature selection"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Covariance and Correlation

$$\\text{Cov}(X,Y) = E[(X-\\mu_X)(Y-\\mu_Y)]$$

$$r = \\text{Cor}(X,Y) = \\frac{\\text{Cov}(X,Y)}{\\sigma_X \\sigma_Y} \\in [-1, 1]$$

- Covariance: scale-dependent; hard to interpret
- Pearson r: scale-free; measures **linear** relationship
- Spearman ρ: rank-based; measures **monotonic** relationship
- Kendall τ: concordance pairs; robust to outliers"""),

    code("""# Visualise different correlation patterns
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
scenarios = [
    ("Strong positive", 0.95, "linear"),
    ("Moderate positive", 0.6, "linear"),
    ("No correlation", 0.0, "linear"),
    ("Strong negative", -0.9, "linear"),
    ("Non-linear", 0.0, "quadratic"),
    ("Outlier effect", 0.3, "outlier"),
    ("Anscombe Quartet", 0, "anscombe"),
    ("Spearman vs Pearson", 0, "monotone"),
]
n = 100
for ax, (label, r, stype) in zip(axes.flat, scenarios):
    if stype == "linear":
        x = rng.normal(0, 1, n)
        y = r*x + np.sqrt(1-r**2)*rng.normal(0, 1, n)
        pearson = np.corrcoef(x, y)[0,1]
        ax.scatter(x, y, alpha=0.5, s=20)
        ax.set_title(f"{label}\nr={pearson:.2f}", fontsize=9)
    elif stype == "quadratic":
        x = rng.uniform(-2, 2, n)
        y = x**2 + rng.normal(0, 0.5, n)
        pearson = np.corrcoef(x, y)[0,1]
        spearman = stats.spearmanr(x, y).statistic
        ax.scatter(x, y, alpha=0.5, s=20)
        ax.set_title(f"Quadratic\nPearson={pearson:.2f}, Spearman={spearman:.2f}", fontsize=9)
    elif stype == "outlier":
        x = rng.normal(0, 1, n)
        y = 0.1*x + rng.normal(0, 1, n)
        x = np.append(x, [10]); y = np.append(y, [10])
        pearson = np.corrcoef(x, y)[0,1]
        ax.scatter(x, y, alpha=0.5, s=20)
        ax.set_title(f"Outlier distortion\nr={pearson:.2f}", fontsize=9)
    elif stype == "anscombe":
        xA = np.array([10,8,13,9,11,14,6,4,12,7,5])
        yA = np.array([8.04,6.95,7.58,8.81,8.33,9.96,7.24,4.26,10.84,4.82,5.68])
        pearson = np.corrcoef(xA, yA)[0,1]
        ax.scatter(xA, yA, s=30)
        ax.set_title(f"Anscombe's Quartet\nr={pearson:.2f}", fontsize=9)
    else:
        x = rng.uniform(0, 5, n)
        y = np.exp(x/2) + rng.normal(0, 0.5, n)
        pearson = np.corrcoef(x, y)[0,1]
        spearman = stats.spearmanr(x, y).statistic
        ax.scatter(x, y, alpha=0.5, s=20)
        ax.set_title(f"Monotone nonlinear\nPearson={pearson:.2f}, Spearman={spearman:.2f}", fontsize=9)
plt.suptitle("Correlation Patterns", fontweight="bold", fontsize=13)
plt.tight_layout(); plt.show()"""),

    md("""## 2–6. Multicollinearity, VIF, Feature Selection, Practice"""),

    code("""# Variance Inflation Factor (VIF) for multicollinearity
from sklearn.preprocessing import StandardScaler

diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)

def compute_vif(X_df):
    vif = {}
    for col in X_df.columns:
        other_cols = [c for c in X_df.columns if c != col]
        r2 = LinearRegression().fit(X_df[other_cols], X_df[col])
        r2_val = r2.score(X_df[other_cols], X_df[col])
        vif[col] = 1 / (1 - r2_val) if r2_val < 1 else np.inf
    return pd.Series(vif).sort_values(ascending=False)

vif_scores = compute_vif(X)
print("VIF Scores (>5 suggests multicollinearity):")
print(vif_scores.round(2))

vif_scores.plot(kind="barh")
plt.axvline(5, color="red", linestyle="--", label="VIF=5 threshold")
plt.xlabel("VIF"); plt.title("Variance Inflation Factors — Diabetes Dataset")
plt.legend(); plt.tight_layout(); plt.show()"""),

    code("""# Correlation heatmap and feature selection
corr_matrix = X.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True)
plt.title("Feature Correlation Matrix — Diabetes Dataset")
plt.tight_layout(); plt.show()

# Select features with |r| > 0.5 with target
y_d = diabetes.target
target_corr = pd.Series({col: abs(np.corrcoef(X[col], y_d)[0,1]) for col in X.columns})
selected = target_corr[target_corr > 0.2].index.tolist()
print(f"\nFeatures with |r|>0.2 with target: {selected}")"""),

    code("""# Practice: Pearson vs Spearman on income data
income = rng.lognormal(10, 1, 200)
age = rng.uniform(22, 65, 200)
income += 500 * (age - 22)  # monotone but nonlinear relationship

pearson_r, p_pearson = stats.pearsonr(age, income)
spearman_r, p_spearman = stats.spearmanr(age, income)
print(f"Pearson r={pearson_r:.4f}, p={p_pearson:.4f}")
print(f"Spearman ρ={spearman_r:.4f}, p={p_spearman:.4f}")
print("Spearman catches the monotone relationship better for skewed data.")"""),
])
save(ch19, "19_correlation_covariance_feature_selection.ipynb")


# ── Chapter 20 ────────────────────────────────────────────────────────────────
ch20 = nb([
    md("""# Chapter 20 — Information Theory Basics
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Understand entropy, cross-entropy, and KL divergence
- Connect information theory to ML training objectives
- Apply mutual information for feature selection"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.datasets import load_iris
from sklearn.feature_selection import mutual_info_classif

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — Entropy and Information

**Shannon Entropy** measures the expected surprise (uncertainty):
$$H(X) = -\\sum_{x} p(x)\\log_2 p(x) \\quad \\text{(bits)}$$

Intuition:
- Fair coin: $H = -2 \\times 0.5\\log_2(0.5) = 1$ bit
- Biased coin p=0.9: $H ≈ 0.47$ bits (less surprising)
- Deterministic: $H = 0$ bits

**Cross-entropy** between true $p$ and model $q$:
$$H(p, q) = -\\sum_x p(x)\\log q(x) = H(p) + D_{KL}(p \\| q)$$

**KL Divergence** (not symmetric!):
$$D_{KL}(p \\| q) = \\sum_x p(x)\\log\\frac{p(x)}{q(x)} \\geq 0$$"""),

    code("""# Entropy as function of bias
p_values = np.linspace(0.001, 0.999, 300)
entropy = -p_values*np.log2(p_values) - (1-p_values)*np.log2(1-p_values)

plt.figure(figsize=(8, 4))
plt.plot(p_values, entropy, lw=2)
plt.scatter([0.5], [1.0], color="red", zorder=5, label="Max entropy at p=0.5 (1 bit)")
plt.xlabel("p (bias of coin)"); plt.ylabel("Entropy H(p) [bits]")
plt.title("Binary Entropy Function")
plt.legend(); plt.tight_layout(); plt.show()"""),

    md("""## 2. Math Walkthrough — KL Divergence"""),

    code("""def kl_divergence(p, q, eps=1e-10):
    p = np.array(p) + eps; q = np.array(q) + eps
    p, q = p/p.sum(), q/q.sum()
    return (p * np.log(p/q)).sum()

# Compare Gaussian distributions
mu_true, sig_true = 0, 1
for mu_q, sig_q in [(0, 1), (1, 1), (0, 2), (2, 2)]:
    p = stats.norm(mu_true, sig_true)
    q = stats.norm(mu_q, sig_q)
    x = np.linspace(-5, 7, 1000)
    dx = x[1]-x[0]
    kl = (p.pdf(x) * np.log((p.pdf(x)+1e-10)/(q.pdf(x)+1e-10)) * dx).sum()
    print(f"KL(N(0,1) || N({mu_q},{sig_q})) = {kl:.4f}")"""),

    code("""# Mutual Information for feature selection
iris = load_iris()
X_iris, y_iris = iris.data, iris.target
mi_scores = mutual_info_classif(X_iris, y_iris, random_state=42)

plt.bar(iris.feature_names, mi_scores, color="steelblue")
plt.ylabel("Mutual Information (bits)")
plt.title("Mutual Information — Iris Feature Selection")
plt.tight_layout(); plt.show()
for name, score in zip(iris.feature_names, mi_scores):
    print(f"  {name}: {score:.4f} bits")"""),

    code("""# Cross-entropy loss in practice
def cross_entropy(y_true, y_pred, eps=1e-9):
    return -np.mean(y_true*np.log(y_pred+eps) + (1-y_true)*np.log(1-y_pred+eps))

probs = np.array([0.9, 0.8, 0.1, 0.3, 0.7])
labels = np.array([1,   1,   0,   0,   1])
ce = cross_entropy(labels, probs)
print(f"Cross-entropy loss: {ce:.4f}")

# Show how CE decreases as model improves
noise_levels = np.linspace(0, 0.45, 100)
ces = [cross_entropy(labels, np.clip(labels + rng.uniform(-n, n, len(labels)), 0.01, 0.99))
       for n in noise_levels]
plt.plot(noise_levels, ces)
plt.xlabel("Prediction noise"); plt.ylabel("Cross-entropy")
plt.title("Cross-Entropy vs. Prediction Quality")
plt.tight_layout(); plt.show()"""),

    code("""# Practice: entropy of uniform vs peaked distributions
distributions = [
    ("Uniform over 4", [0.25]*4),
    ("Peaked at 1", [0.7, 0.1, 0.1, 0.1]),
    ("Deterministic", [1.0, 0, 0, 0]),
    ("Two-peaked", [0.45, 0.45, 0.05, 0.05]),
]
for name, p in distributions:
    p_arr = np.array(p, dtype=float)
    h = -np.sum(p_arr[p_arr>0] * np.log2(p_arr[p_arr>0]))
    print(f"{name:<25} H={h:.4f} bits")"""),
])
save(ch20, "20_information_theory.ipynb")


# ── Chapter 21 ────────────────────────────────────────────────────────────────
ch21 = nb([
    md("""# Chapter 21 — Experiment Design & Power Analysis
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Design experiments with sufficient statistical power
- Compute required sample sizes for A/B tests and ML comparisons
- Understand Type I and Type II errors in practice"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — The Four Quantities

Experiment design involves balancing four linked quantities:

| Symbol | Meaning | Typical value |
|--------|---------|---------------|
| α | Significance level (Type I error) | 0.05 |
| β | Type II error rate | 0.20 |
| 1-β | **Power** (probability of detecting true effect) | 0.80 |
| δ | Minimum Detectable Effect (MDE) | depends on domain |

Given any three, the fourth is determined. Usually we fix α, β, δ and solve for **n**."""),

    code("""# Visualise Type I and Type II errors
delta = 0.3  # effect size
se = 1.0     # standard error
z_alpha = stats.norm.ppf(0.975)  # two-tailed α=0.05

x = np.linspace(-4, 5, 400)
null = stats.norm(0, se)
alt  = stats.norm(delta, se)

plt.figure(figsize=(10, 5))
plt.plot(x, null.pdf(x), "b-", lw=2, label="H₀: δ=0")
plt.plot(x, alt.pdf(x),  "r-", lw=2, label=f"H₁: δ={delta}")
crit_hi = z_alpha * se
plt.axvline(crit_hi, color="black", linestyle="--", label=f"Critical value={crit_hi:.2f}")
plt.fill_between(x[x >= crit_hi], null.pdf(x[x >= crit_hi]), alpha=0.4, color="blue", label="Type I (α)")
plt.fill_between(x[x < crit_hi], alt.pdf(x[x < crit_hi]), alpha=0.4, color="red", label="Type II (β)")
plt.title("Type I and Type II Errors")
plt.legend(); plt.tight_layout(); plt.show()

power = 1 - alt.cdf(crit_hi)
print(f"Power = {power:.3f}")"""),

    md("""## 2. Math Walkthrough — Sample Size Formula

For a two-sample z-test (large n), assuming equal group sizes:
$$n = \\frac{(z_{\\alpha/2} + z_\\beta)^2 (\\sigma_1^2 + \\sigma_2^2)}{\\delta^2}$$

For a two-proportion test (A/B testing):
$$n = \\frac{(z_{\\alpha/2} + z_\\beta)^2 (p_1(1-p_1) + p_2(1-p_2))}{(p_1 - p_2)^2}$$"""),

    code("""def sample_size_proportions(p1, p2, alpha=0.05, power=0.80):
    z_a = stats.norm.ppf(1 - alpha/2)
    z_b = stats.norm.ppf(power)
    numerator = (z_a + z_b)**2 * (p1*(1-p1) + p2*(1-p2))
    denominator = (p1 - p2)**2
    return int(np.ceil(numerator / denominator))

# Example: conversion rate from 5% to 7%
n = sample_size_proportions(0.05, 0.07)
print(f"Sample size (5% → 7%): {n} per group")

# Power curve: effect size vs sample size
effects = np.linspace(0.01, 0.05, 50)
ns = [sample_size_proportions(0.10, 0.10+e) for e in effects]
plt.plot(effects*100, ns)
plt.xlabel("Absolute Effect Size (%)"); plt.ylabel("Required n per group")
plt.title("Sample Size vs Effect Size (baseline p=10%, α=0.05, power=80%)")
plt.tight_layout(); plt.show()"""),

    code("""# Power curve: n vs power for fixed effect
n_values = np.arange(50, 2000, 25)
p1, p2 = 0.10, 0.12
z_alpha = stats.norm.ppf(0.975)

powers = []
for n in n_values:
    se_pool = np.sqrt(p1*(1-p1)/n + p2*(1-p2)/n)
    z_beta = (abs(p2-p1) / se_pool) - z_alpha
    powers.append(stats.norm.cdf(z_beta))

plt.plot(n_values, powers)
plt.axhline(0.80, color="red", linestyle="--", label="Power=0.80")
plt.axhline(0.90, color="orange", linestyle="--", label="Power=0.90")
req_n = n_values[np.searchsorted(powers, 0.80)]
plt.axvline(req_n, color="gray", linestyle=":", label=f"n={req_n}")
plt.xlabel("Sample size per group"); plt.ylabel("Power")
plt.title("Power Curve — Detect 2pp lift from 10% baseline")
plt.legend(); plt.tight_layout(); plt.show()"""),

    code("""# Practice: full experiment design for an ML evaluation
# Suppose we want to detect 1% accuracy improvement from 85% to 86%
n_model = sample_size_proportions(0.85, 0.86)
print(f"To detect 85%→86% accuracy: {n_model} test samples per model")

# Monte Carlo power simulation
actual_power = 0
n_sim = 5000
for _ in range(n_sim):
    preds_a = rng.binomial(n_model, 0.85) / n_model
    preds_b = rng.binomial(n_model, 0.86) / n_model
    diff = preds_b - preds_a
    se = np.sqrt(preds_a*(1-preds_a)/n_model + preds_b*(1-preds_b)/n_model)
    z = diff / se if se > 0 else 0
    actual_power += (z > stats.norm.ppf(0.95))
print(f"Monte Carlo power (one-sided): {actual_power/n_sim:.3f}")"""),
])
save(ch21, "21_experiment_design_power_analysis.ipynb")


# ── Chapter 22 ────────────────────────────────────────────────────────────────
ch22 = nb([
    md("""# Chapter 22 — Causal Inference Introduction
*Track 3: Data Scientists*

## 🎯 Learning Objectives
- Distinguish correlation from causation rigorously
- Understand confounding, selection bias, and collider bias
- Apply difference-in-differences and propensity score matching"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
print("Libraries loaded ✅")"""),

    md("""## 1. Concept Review — The Fundamental Problem of Causal Inference

The **Potential Outcomes Framework** (Rubin):

For unit $i$:
- $Y_i(1)$ = outcome if treated
- $Y_i(0)$ = outcome if not treated
- **Individual Treatment Effect (ITE):** $\\tau_i = Y_i(1) - Y_i(0)$
- **Average Treatment Effect (ATE):** $\\tau = E[Y(1) - Y(0)]$

**The fundamental problem:** We can only observe one potential outcome —
the **counterfactual** is never seen.

Random assignment ensures:
$$E[Y(1)|T=1] = E[Y(1)|T=0] \\implies \\hat\\tau = \\bar Y_{treated} - \\bar Y_{control}$$"""),

    code("""# Simulate: confounding bias without randomisation
n = 1000
# True treatment effect = 2.0
# Confounder: age affects both treatment assignment and outcome
age = rng.normal(40, 10, n)
# Treatment: older people more likely to get treatment
prob_treated = 1 / (1 + np.exp(-(age - 40) / 5))
treated = rng.binomial(1, prob_treated)
# Outcome: treatment adds 2, but age also increases outcome
outcome = 2*treated + 0.3*age + rng.normal(0, 1, n)

# Naive estimate (biased)
ate_naive = outcome[treated==1].mean() - outcome[treated==0].mean()
print(f"True ATE: 2.0")
print(f"Naive ATE (ignoring confounding): {ate_naive:.3f}")

# Correct: control for age with regression
import statsmodels.api as sm
X_reg = sm.add_constant(np.c_[treated, age])
model = sm.OLS(outcome, X_reg).fit()
ate_adjusted = model.params[1]
print(f"Regression-adjusted ATE: {ate_adjusted:.3f}")"""),

    md("""## 2. Math Walkthrough — Difference-in-Differences

DiD identifies causal effect from panel data under **parallel trends**:
$$\\hat\\tau_{DiD} = (\\bar Y^{post}_{treat} - \\bar Y^{pre}_{treat}) - (\\bar Y^{post}_{control} - \\bar Y^{pre}_{control})$$"""),

    code("""# Simulate DiD: new checkout feature rolled out to Group B
n_users = 500
# Pre-period
revenue_pre_A = rng.normal(100, 20, n_users)  # Control
revenue_pre_B = rng.normal(95, 20, n_users)   # Treatment (slightly lower pre)

# Post-period: treatment effect = +10
revenue_post_A = rng.normal(103, 20, n_users)  # Control: small time trend
revenue_post_B = rng.normal(108, 20, n_users)  # Treatment: time trend + effect

did = ((revenue_post_B.mean() - revenue_pre_B.mean()) -
       (revenue_post_A.mean() - revenue_pre_A.mean()))
print(f"True treatment effect: +10")
print(f"DiD estimate: {did:.2f}")

fig, ax = plt.subplots(figsize=(8, 5))
periods = ["Pre", "Post"]
ax.plot(periods, [revenue_pre_A.mean(), revenue_post_A.mean()], "b-o", label="Control", lw=2)
ax.plot(periods, [revenue_pre_B.mean(), revenue_post_B.mean()], "r-o", label="Treatment", lw=2)
cf_B = revenue_pre_B.mean() + (revenue_post_A.mean() - revenue_pre_A.mean())
ax.plot(periods, [revenue_pre_B.mean(), cf_B], "r--", label="Counterfactual (no treatment)", lw=2)
ax.annotate(f"DiD={did:.1f}", xy=("Post", (revenue_post_B.mean()+cf_B)/2),
            fontsize=11, color="darkred")
ax.set_ylabel("Revenue"); ax.legend(); ax.set_title("Difference-in-Differences")
plt.tight_layout(); plt.show()"""),

    md("""## 3–6. Propensity Score Matching, Colliders, and Practice"""),

    code("""# Propensity Score Matching (PSM)
df = pd.DataFrame({"age": age, "treated": treated, "outcome": outcome})

# Fit propensity score model
lr = LogisticRegression()
lr.fit(df[["age"]], df["treated"])
df["pscore"] = lr.predict_proba(df[["age"]])[:, 1]

# Greedy 1:1 nearest-neighbor matching
treated_df  = df[df.treated == 1].copy()
control_df  = df[df.treated == 0].copy()
matched_pairs = []
used_controls = set()
for _, t_row in treated_df.iterrows():
    diffs = abs(control_df[~control_df.index.isin(used_controls)]["pscore"] - t_row["pscore"])
    best  = diffs.idxmin()
    used_controls.add(best)
    matched_pairs.append((t_row["outcome"], control_df.loc[best, "outcome"]))

matched = np.array(matched_pairs)
ate_psm = (matched[:, 0] - matched[:, 1]).mean()
print(f"PSM ATE: {ate_psm:.3f} (true=2.0)")"""),

    code("""# Practice: confounders in model evaluation
# Students who take an ML course (treated) tend to have higher GPA already
n = 300
gpa_prior = rng.normal(3.2, 0.5, n)
prob_takes_course = 1/(1+np.exp(-(gpa_prior - 3.2)/0.3))
takes_course = rng.binomial(1, prob_takes_course)
# Course adds 0.1 to GPA
gpa_post = gpa_prior + 0.1*takes_course + rng.normal(0, 0.2, n)

naive_effect = gpa_post[takes_course==1].mean() - gpa_post[takes_course==0].mean()

import statsmodels.api as sm
X_c = sm.add_constant(np.c_[takes_course, gpa_prior])
m = sm.OLS(gpa_post, X_c).fit()
adjusted_effect = m.params[1]

print(f"True course effect: 0.1")
print(f"Naive estimate: {naive_effect:.3f}  ← inflated by confounding")
print(f"Regression-adjusted: {adjusted_effect:.3f}  ← closer to truth")"""),

    md("""## 🎯 Track 3 Complete! 🏆

**You've mastered:**
- ✅ Distributions in ML and log-likelihood
- ✅ MLE: analytical and numerical estimation
- ✅ Bias-variance tradeoff and regularisation
- ✅ Bayesian vs Frequentist perspectives
- ✅ Hypothesis testing for model evaluation
- ✅ Bootstrap and Jackknife resampling
- ✅ Correlation, covariance, and feature selection
- ✅ Information theory: entropy, KL divergence, cross-entropy
- ✅ Power analysis and experiment design
- ✅ Causal inference: DiD, PSM, confounders

**Ready for Tier 3?** → [Chapter 23 — Markov Chains]"""),
])
save(ch22, "22_causal_inference.ipynb")

print("\n🎉 All Track 3 (Data Scientists) notebooks created successfully!")
