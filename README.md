# Probability & Statistics Tutorial

A complete, multi-track Probability & Statistics tutorial series by **Phiphat Chomchit** — companion notebooks for the YouTube channel.

60 Jupyter notebooks across 4 audience tracks and 3 tiers of depth, from first principles to advanced inference.

---

## Learning Paths

All tracks share **Tier 1**. After Chapter 12, learners branch into the track that matches their goals.

```
Tier 1 (Ch 1-12)  →  Tier 2, choose one:
                       ├── Students       (Ch 13-22)
                       ├── Developers     (Ch 13-22)
                       ├── Data Scientists (Ch 13-22)
                       └── Engineers      (Ch 13-22)
                  →  Tier 3 Advanced (Ch 23-30)  [all tracks reconverge]
```

---

## Tier 1 — Foundations `tier1_foundations/`

> **Who:** Everyone. Start here regardless of your track.

| # | Notebook | Topic |
|---|----------|-------|
| 1 | `01_what_is_probability` | Sample space, events, outcomes, randomness vs uncertainty |
| 2 | `02_types_of_probability` | Classical, empirical, and subjective probability |
| 3 | `03_rules_of_probability` | Addition rule, multiplication rule, complement |
| 4 | `04_conditional_probability` | P(A\|B), independence, common intuition traps |
| 5 | `05_bayes_theorem` | Prior, likelihood, posterior — visual proof |
| 6 | `06_random_variables` | Discrete vs continuous, PMF, PDF, CDF |
| 7 | `07_expected_value_and_variance` | Mean, spread, and the intuition behind the formulas |
| 8 | `08_distributions_part1` | Bernoulli, Binomial, Geometric |
| 9 | `09_distributions_part2` | Poisson, Uniform, Exponential |
| 10 | `10_normal_distribution` | Bell curve, Z-scores, empirical rule |
| 11 | `11_sampling_and_clt` | Central Limit Theorem — the most important theorem |
| 12 | `12_descriptive_statistics` | Mean, median, mode, IQR, skewness, kurtosis |

---

## Tier 2 — Intermediate (Track-Specific)

### Track 1 — Students `tier2_students/`

> **Who:** High school / undergraduate students preparing for exams. Focus on intuition, visual learning, and worked examples.

| # | Notebook | Topic |
|---|----------|-------|
| 13 | `13_combinatorics` | Permutations, combinations, counting principles |
| 14 | `14_probability_trees_venn` | Probability trees and Venn diagrams |
| 15 | `15_joint_marginal_conditional` | Joint, marginal, and conditional distributions |
| 16 | `16_law_of_total_probability` | Law of Total Probability — the bridge formula |
| 17 | `17_hypothesis_testing_intro` | Hypothesis testing framework (conceptual) |
| 18 | `18_pvalues_explained` | p-values explained without jargon |
| 19 | `19_confidence_intervals` | Confidence intervals — what they actually mean |
| 20 | `20_chi_square_test` | Chi-square test for beginners |
| 21 | `21_correlation_vs_causation` | Correlation vs causation |
| 22 | `22_exam_strategy` | Exam strategy and common mistakes |

---

### Track 2 — Developers `tier2_developers/`

> **Who:** Software engineers and developers. Bridge probability theory to code — randomness, testing, and probabilistic systems.

| # | Notebook | Topic |
|---|----------|-------|
| 13 | `13_probability_in_code` | PRNGs, seeds, reproducibility, entropy |
| 14 | `14_monte_carlo_methods` | Monte Carlo integration, convergence, variance reduction |
| 15 | `15_ab_testing` | A/B test design, analysis, and the peeking problem |
| 16 | `16_bayesian_updating` | Conjugate priors, Thompson Sampling |
| 17 | `17_log_probabilities` | Numerical stability, log-sum-exp, softmax |
| 18 | `18_probability_in_apis` | Poisson traffic, token bucket, queuing theory |
| 19 | `19_randomized_algorithms` | Quicksort, reservoir sampling, hashing |
| 20 | `20_probabilistic_data_structures` | Bloom filters, HyperLogLog, Count-Min Sketch |
| 21 | `21_statistical_testing_feature_flags` | Sequential testing (SPRT), multi-armed bandits |
| 22 | `22_debugging_probabilistic_systems` | KS test, chi-square, property-based testing |

---

### Track 3 — Data Scientists `tier2_data_scientists/`

> **Who:** ML practitioners. Connect probability theory to model training, evaluation, and experiment design.

| # | Notebook | Topic |
|---|----------|-------|
| 13 | `13_distributions_in_ml` | Distributions behind MSE, cross-entropy, Poisson loss |
| 14 | `14_maximum_likelihood_estimation` | MLE: analytical derivation and numerical optimisation |
| 15 | `15_bias_variance_tradeoff` | Bias-variance decomposition, regularisation |
| 16 | `16_bayesian_vs_frequentist` | Credible intervals vs confidence intervals |
| 17 | `17_hypothesis_testing_model_evaluation` | Paired t-test, McNemar's test, multiple comparisons |
| 18 | `18_bootstrap_jackknife` | Bootstrap CIs, jackknife bias estimation |
| 19 | `19_correlation_covariance_feature_selection` | VIF, multicollinearity, mutual information |
| 20 | `20_information_theory` | Entropy, KL divergence, cross-entropy loss |
| 21 | `21_experiment_design_power_analysis` | Sample size, power curves, MDE |
| 22 | `22_causal_inference` | DiD, propensity score matching, confounders |

---

### Track 4 — Engineers `tier2_engineers/`

> **Who:** Systems, reliability, and quality engineers. Apply probability to hardware, signals, processes, and safety.

| # | Notebook | Topic |
|---|----------|-------|
| 13 | `13_reliability_failure_probability` | Weibull, bathtub curve, MTTF, series vs parallel |
| 14 | `14_poisson_processes` | Inter-arrivals, non-homogeneous processes, network packets |
| 15 | `15_queuing_theory` | M/M/1, Little's Law, capacity planning |
| 16 | `16_statistical_process_control` | X-bar/R/p charts, Cp, Cpk, process capability |
| 17 | `17_signal_noise_snr_filtering` | SNR, moving average, exponential smoothing, Kalman filter |
| 18 | `18_failure_mode_analysis` | FMEA/RPN, fault trees, event trees |
| 19 | `19_monte_carlo_engineering` | Uncertainty propagation, tolerance stackup, reliability index |
| 20 | `20_risk_assessment_safety_factors` | Risk matrix, F-N curves, probabilistic safety factor |
| 21 | `21_regression_for_engineers` | Calibration, degradation modelling, residual diagnostics |
| 22 | `22_six_sigma_quality` | DPMO, Gage R&R, quality hypothesis tests |

---

## Tier 3 — Advanced `tier3_advanced/`

> **Who:** All tracks reconverge. Topics apply across students, developers, data scientists, and engineers.

| # | Notebook | Topic |
|---|----------|-------|
| 23 | `23_markov_chains` | Transition matrices, stationary distributions, PageRank |
| 24 | `24_stochastic_processes` | Brownian motion, GBM, Ornstein-Uhlenbeck, option pricing |
| 25 | `25_bayesian_networks` | DAGs, variable elimination, naive Bayes |
| 26 | `26_regression_deep_dive` | OLS inference, heteroscedasticity, GLMs |
| 27 | `27_time_series_autocorrelation` | Stationarity, ACF/PACF, ARIMA, seasonal decomposition |
| 28 | `28_mcmc` | Metropolis-Hastings, Gibbs sampling, convergence diagnostics |
| 29 | `29_multivariate_statistics` | Multivariate normal, PCA, Mahalanobis distance |
| 30 | `30_capstone_probabilistic_pipeline` | End-to-end Bayesian A/B test with business impact analysis |

---

## Notebook Structure

Every notebook follows the same six-section format:

1. **Concept Review** — plain-English explanation with intuition first
2. **Math Walkthrough** — LaTeX derivations, step by step
3. **Simulation** — build the concept from scratch in code
4. **Visualisation** — plots of distributions, convergence, and results
5. **Real Dataset Exercise** — apply to actual data
6. **Practice Problems** — with worked solutions in hidden code cells

---

## Project Structure

```
probability/
├── tier1_foundations/       # 12 notebooks — shared foundations
│   └── generate_nb.py
├── tier2_students/          # 10 notebooks — exam prep track
│   └── generate_nb.py
├── tier2_developers/        # 10 notebooks — software engineering track
│   └── generate_nb.py
├── tier2_data_scientists/   # 10 notebooks — ML/DS track
│   └── generate_nb.py
├── tier2_engineers/         # 10 notebooks — systems/reliability track
│   └── generate_nb.py
├── tier3_advanced/          # 8 notebooks — advanced topics, all tracks
│   └── generate_nb.py
├── pyproject.toml
└── README.md
```

Each `generate_nb.py` programmatically builds all notebooks in its directory and can be re-run to regenerate them.

---

## Setup

```bash
# Install dependencies (requires uv)
uv sync

# Regenerate all notebooks
python tier1_foundations/generate_nb.py
python tier2_students/generate_nb.py
python tier2_developers/generate_nb.py
python tier2_data_scientists/generate_nb.py
python tier2_engineers/generate_nb.py
python tier3_advanced/generate_nb.py

# Launch Jupyter
jupyter lab
```

**Requirements:** Python 3.12+, numpy, scipy, matplotlib, seaborn, pandas, statsmodels, scikit-learn, networkx, plotly, ipywidgets.

---

## Stats

| | Count |
|--|-------|
| Total notebooks | 60 |
| Tier 1 (shared) | 12 |
| Tier 2 per track | 10 x 4 tracks |
| Tier 3 (advanced) | 8 |
| Estimated video content | ~1,700 minutes |

---

*Probability & Statistics Tutorial — YouTube Channel by Phiphat Chomchit*
