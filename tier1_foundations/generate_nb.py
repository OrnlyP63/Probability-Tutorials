"""Generate Tier 1 Foundation notebooks (Chapters 1-12, shared by all tracks)."""
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


# ─── Chapter 1: What is Probability? ────────────────────────────────────────
ch01 = nb([
    md("""# 📊 Chapter 1: What is Probability?
*Tier 1 — Foundations | All Tracks*

---
> **🎬 Hook:** You just got a weather forecast saying *"70% chance of rain"* — but what does that actually **mean**?
> Does it mean it rains 70% of the day? That 70% of cities get rain? That the meteorologist is 70% confident?
> By the end of this notebook, you'll know exactly what that number means — and why it matters.

**🎯 Learning Objectives**
- Define probability precisely using sample spaces and events
- Distinguish between outcomes, events, and experiments
- Understand what a probability number actually represents
- Simulate randomness with Python to build intuition"""),

    md("""## 📖 Section 1 — Concept Review

### The Language of Probability

Before we can *calculate* probability, we need to speak the language.

| Term | Meaning | Example |
|------|---------|---------|
| **Experiment** | Any process with an uncertain outcome | Rolling a die |
| **Sample Space (Ω)** | ALL possible outcomes | {1, 2, 3, 4, 5, 6} |
| **Event** | A subset of the sample space | Getting an even number: {2, 4, 6} |
| **Outcome** | A single result | Rolling a 4 |
| **Probability P(E)** | A number between 0 and 1 | P(even) = 3/6 = 0.5 |

### The Probability Scale
```
0 ────────────────────────────────── 1
│           │           │           │
Impossible  Unlikely   Likely    Certain
  (0%)      (25%)      (75%)     (100%)
```

### The Three Axioms (Kolmogorov)
All of probability theory rests on just 3 rules:
1. **P(E) ≥ 0** — Probability is never negative
2. **P(Ω) = 1** — Something always happens
3. **P(A ∪ B) = P(A) + P(B)** if A and B are mutually exclusive"""),

    md("""## 🧮 Section 2 — Math Walkthrough

### Formal Definition

For a **finite, equally likely** sample space:

$$P(E) = \\frac{|E|}{|\\Omega|} = \\frac{\\text{number of favorable outcomes}}{\\text{total number of outcomes}}$$

### Example: Rolling a fair 6-sided die

- Sample space: $\\Omega = \\{1, 2, 3, 4, 5, 6\\}$, so $|\\Omega| = 6$
- Event A = "roll greater than 4" = $\\{5, 6\\}$, so $|A| = 2$

$$P(A) = \\frac{2}{6} = \\frac{1}{3} \\approx 0.333$$

### What does "70% rain" actually mean?
It means: if we ran today's atmospheric conditions **100 times**, it would rain in approximately **70 of those runs**.
This is called the **frequentist interpretation** — probability as long-run frequency."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid", palette="muted")
np.random.seed(42)

# --- Visualize a sample space ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Die sample space
die_faces = [1, 2, 3, 4, 5, 6]
colors = ['#e74c3c' if x > 4 else '#3498db' for x in die_faces]
axes[0].bar(die_faces, [1/6]*6, color=colors, edgecolor='white', linewidth=2)
axes[0].set_title("🎲 Rolling a Fair Die\\nRed = Event A: {roll > 4}", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Outcome")
axes[0].set_ylabel("Probability")
axes[0].set_ylim(0, 0.3)
axes[0].text(5, 0.18, f'P(A) = 2/6 = {2/6:.3f}', ha='center', fontsize=11,
             bbox=dict(boxstyle='round', facecolor='#e74c3c', alpha=0.3))

# Coin flip sample space
outcomes = ['Heads', 'Tails']
axes[1].bar(outcomes, [0.5, 0.5], color=['#f39c12', '#9b59b6'], edgecolor='white', linewidth=2)
axes[1].set_title("🪙 Fair Coin Flip\\nSample Space = {H, T}", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Outcome")
axes[1].set_ylabel("Probability")
axes[1].set_ylim(0, 0.8)

plt.tight_layout()
plt.savefig('ch01_sample_space.png', dpi=150, bbox_inches='tight')
plt.show()
print("Sample space visualization complete!")"""),

    md("""## 🔬 Section 3 — Simulation

The best way to build intuition for probability is to **simulate** it.
Let's verify that the law of large numbers works: as we flip more coins, the observed frequency approaches 0.5."""),

    code("""# Simulate coin flips and watch probability converge
n_flips_list = [10, 50, 100, 500, 1000, 5000, 10000]
results = []

for n in n_flips_list:
    flips = np.random.randint(0, 2, size=n)  # 0=Tails, 1=Heads
    p_heads = flips.mean()
    results.append(p_heads)
    print(f"n={n:>6} flips → P(Heads) = {p_heads:.4f}  (error: {abs(p_heads - 0.5):.4f})")

# Plot convergence
n_range = np.arange(1, 10001)
cumulative_heads = np.cumsum(np.random.randint(0, 2, size=10000)) / n_range

plt.figure(figsize=(10, 5))
plt.plot(n_range, cumulative_heads, color='#3498db', lw=1.5, label='Observed P(Heads)')
plt.axhline(0.5, color='#e74c3c', linestyle='--', lw=2, label='True P(Heads) = 0.5')
plt.fill_between(n_range, 0.45, 0.55, alpha=0.1, color='#e74c3c')
plt.xlabel("Number of Coin Flips", fontsize=12)
plt.ylabel("Observed Probability", fontsize=12)
plt.title("🪙 Law of Large Numbers: Coin Flips Converge to 0.5", fontsize=13, fontweight='bold')
plt.legend(fontsize=11)
plt.xscale('log')
plt.ylim(0.3, 0.7)
plt.savefig('ch01_convergence.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📊 Section 4 — Visualization

Let's explore what different probability values *look* like using a dart board analogy."""),

    code("""# Probability as frequency: simulate 1000 experiments
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

events = [
    {"label": "P = 0.1 (Rare)", "p": 0.1, "color": "#e74c3c"},
    {"label": "P = 0.5 (50/50)", "p": 0.5, "color": "#f39c12"},
    {"label": "P = 0.9 (Likely)", "p": 0.9, "color": "#27ae60"},
]

n = 200
for ax, event in zip(axes, events):
    outcomes = np.random.random(n) < event["p"]
    x = np.random.uniform(0, 10, n)
    y = np.random.uniform(0, 10, n)
    colors_scatter = [event["color"] if o else '#ecf0f1' for o in outcomes]
    ax.scatter(x, y, c=colors_scatter, s=30, edgecolors='gray', linewidths=0.3)
    observed = outcomes.mean()
    ax.set_title(f"{event['label']}\\nObserved: {observed:.2f}", fontsize=11, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(5, -0.8, f"● = Event occurred ({outcomes.sum()}/{n})", ha='center', fontsize=9)

plt.suptitle("Visualizing Probability: Each dot is one experiment", fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('ch01_probability_visual.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📂 Section 5 — Real Dataset Exercise

Let's use real sports data to calculate empirical probabilities.
We'll analyze free throw shooting percentages from the NBA."""),

    code("""import pandas as pd

# Simulate realistic NBA free throw data
np.random.seed(42)
players = ['LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis A.', 'Nikola Jokic']
true_pcts = [0.734, 0.921, 0.885, 0.685, 0.818]

data = []
for player, pct in zip(players, true_pcts):
    attempts = np.random.randint(200, 500)
    makes = np.random.binomial(attempts, pct)
    data.append({'Player': player, 'Attempts': attempts, 'Makes': makes,
                 'P(Make)': makes/attempts, 'True %': pct})

df = pd.DataFrame(data)
df['Error'] = abs(df['P(Make)'] - df['True %'])

print("📊 NBA Free Throw Probability Analysis")
print("=" * 65)
print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
print(f"\n💡 Average estimation error: {df['Error'].mean():.3f}")
print(f"💡 The empirical probability gets CLOSER to true probability with more attempts!")

# Visualization
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(players))
bars = ax.bar(x - 0.2, df['P(Make)'], 0.4, label='Observed %', color='#3498db', alpha=0.8)
bars2 = ax.bar(x + 0.2, df['True %'], 0.4, label='True %', color='#e74c3c', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(players, rotation=15, ha='right')
ax.set_ylabel("Free Throw Probability")
ax.set_title("🏀 NBA Free Throw: Observed vs True Probability", fontsize=13, fontweight='bold')
ax.legend()
ax.set_ylim(0.5, 1.0)
plt.tight_layout()
plt.savefig('ch01_nba_data.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

Work through these before checking the solutions!

---

**Problem 1 — Warm Up:**
A standard deck has 52 cards (4 suits × 13 ranks).
What is the probability of drawing:
a) A King?
b) A Heart?
c) The King of Hearts?

**Problem 2 — Die Roll:**
Roll two fair 6-sided dice. What is P(sum = 7)?
*Hint: List all pairs that sum to 7.*

**Problem 3 — Think Critically:**
A sportscaster says "Team A wins 60% of their home games."
Is this classical, empirical, or subjective probability? Why?

**Problem 4 — Simulation:**
Write code to estimate P(sum = 7) when rolling two dice, using 100,000 simulations.
How close is it to the true value?

---
<details>
<summary>💡 Click to reveal solutions</summary>

**Solution 1:**
a) P(King) = 4/52 = 1/13 ≈ 0.077
b) P(Heart) = 13/52 = 1/4 = 0.25
c) P(King of Hearts) = 1/52 ≈ 0.019

**Solution 2:**
Pairs summing to 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) → 6 pairs
Total pairs: 36
P(sum=7) = 6/36 = 1/6 ≈ 0.167

**Solution 3:**
Empirical probability — it's based on historical frequency of past games.

**Solution 4:** See code below.
</details>"""),

    code("""# Solution to Problem 4: Simulate P(sum = 7) with two dice
n_simulations = 100_000
die1 = np.random.randint(1, 7, n_simulations)
die2 = np.random.randint(1, 7, n_simulations)
sums = die1 + die2

p_sum_7 = (sums == 7).mean()
true_p = 6 / 36

print(f"🎲 Simulating {n_simulations:,} rolls of two dice...")
print(f"   Estimated P(sum=7) = {p_sum_7:.5f}")
print(f"   True P(sum=7)      = {true_p:.5f} (= 6/36)")
print(f"   Error              = {abs(p_sum_7 - true_p):.5f}")
print()

# Bonus: show the full distribution of sums
from collections import Counter
sum_counts = Counter(sums)
possible_sums = range(2, 13)

fig, ax = plt.subplots(figsize=(10, 5))
observed_probs = [sum_counts[s]/n_simulations for s in possible_sums]
true_probs = [(6 - abs(s - 7)) / 36 for s in possible_sums]
x = list(possible_sums)
ax.bar(x, observed_probs, width=0.4, align='center', label='Simulated', color='#3498db', alpha=0.7)
ax.bar([xi + 0.4 for xi in x], true_probs, width=0.4, align='center', label='True', color='#e74c3c', alpha=0.7)
ax.set_xticks(x)
ax.set_xlabel("Sum of Two Dice")
ax.set_ylabel("Probability")
ax.set_title("🎲 Distribution of Two-Dice Sums: Simulated vs Theoretical", fontsize=12, fontweight='bold')
ax.legend()
plt.savefig('ch01_dice_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print("\\n🎯 Key insight: The distribution is triangular (not uniform) because there are more ways to get a middle sum!")"""),

    md("""## 🎯 Episode Recap

**3 Key Takeaways:**
1. **Probability is a number between 0 and 1** — it measures how likely an event is relative to all possibilities.
2. **The Law of Large Numbers** — as we repeat an experiment more, the observed frequency converges to the true probability.
3. **Sample space matters** — always define Ω first before calculating any probabilities.

**🔗 Next Episode:** [Chapter 2 — Types of Probability: Classical, Empirical, and Subjective]

**💬 Challenge for viewers:**
Roll a real die 20 times and record your results. Is your frequency for each face close to 1/6?
Share your results in the comments! 🎲"""),
])

save(ch01, "01_what_is_probability.ipynb")


# ─── Chapter 2: Types of Probability ────────────────────────────────────────
ch02 = nb([
    md("""# 📊 Chapter 2: Types of Probability
*Tier 1 — Foundations | All Tracks*

---
> **🎬 Hook:** Three people are each asked "What's the probability it rains tomorrow?"
> A **mathematician** says 1/2 (either it rains or it doesn't).
> A **meteorologist** says 0.72 (based on 50 years of data).
> A **farmer** says 0.9 (she can feel it in her bones).
> They're all using the word *probability* — but they mean completely different things.

**🎯 Learning Objectives**
- Identify the three types of probability: classical, empirical, subjective
- Understand when to use each type
- Know the strengths and weaknesses of each approach"""),

    md("""## 📖 Section 1 — Concept Review

### The Three Types at a Glance

| Type | Definition | Requires | Best For |
|------|-----------|----------|---------|
| **Classical** | Count equally likely outcomes | Symmetry / known structure | Dice, cards, lotteries |
| **Empirical** | Long-run relative frequency | Historical data | Weather, sports, actuarial |
| **Subjective** | Personal degree of belief | Expert judgment | Unique events, diagnosis |

### 1. Classical Probability
Based on **symmetry** — all outcomes are equally likely.

$$P(E) = \\frac{\\text{favorable outcomes}}{\\text{total outcomes}}$$

Works perfectly when: coin flips, fair dice, shuffled cards.
Breaks when: outcomes are NOT equally likely.

### 2. Empirical Probability
Based on **observation** — what actually happened.

$$P(E) = \\frac{\\text{times E occurred}}{\\text{total trials}}$$

Gets better with more data. The backbone of statistics and ML.

### 3. Subjective Probability
Based on **belief** — your personal assessment.
Used in: medical diagnosis, intelligence estimates, business decisions.
Formalized in Bayesian statistics (coming in Chapter 5!)"""),

    md("""## 🧮 Section 2 — Math Walkthrough

### Classical: Card Drawing
A standard deck: 52 cards, 4 suits, 13 ranks.
P(drawing an Ace) = ?

$$P(\\text{Ace}) = \\frac{4 \\text{ Aces}}{52 \\text{ cards}} = \\frac{1}{13} \\approx 0.077$$

This is **classical** — we know the structure of the deck.

### Empirical: Free Throw Shooting
Stephen Curry made 337 out of 366 free throws in the 2015-16 season.

$$P(\\text{make}) = \\frac{337}{366} \\approx 0.921$$

This is **empirical** — based on observed data.

### Calibration: Are Subjective Probabilities Accurate?
Good forecasters have *calibrated* beliefs:
Events they say have P=0.7 should happen ~70% of the time.
This is measurable — and it's how forecasters like Superforecasters are evaluated."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid", palette="muted")
np.random.seed(42)

# ── Classical Probability: Card Deck ──
suits = ['♠ Spades', '♥ Hearts', '♦ Diamonds', '♣ Clubs']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
deck = [(r, s) for s in suits for r in ranks]

print(f"Total cards in deck: {len(deck)}")
print(f"P(Ace)   = 4/{len(deck)} = {4/len(deck):.4f}")
print(f"P(Heart) = 13/{len(deck)} = {13/len(deck):.4f}")
print(f"P(Face)  = 12/{len(deck)} = {12/len(deck):.4f}")"""),

    code("""# ── Empirical Probability: Simulating Weather Data ──
# Simulate 10 years of daily weather
n_days = 3650
rain_prob_true = 0.35  # true underlying probability
actual_rain = np.random.random(n_days) < rain_prob_true

# Calculate empirical probability over growing windows
window_sizes = [10, 30, 100, 365, 1000, 3650]
empirical_probs = []

for w in window_sizes:
    emp = actual_rain[:w].mean()
    empirical_probs.append(emp)
    print(f"After {w:>5} days: P(rain) = {emp:.3f}  (true = {rain_prob_true})")

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))

ax1.plot(window_sizes, empirical_probs, 'bo-', markersize=8, label='Empirical P(rain)')
ax1.axhline(rain_prob_true, color='red', linestyle='--', label=f'True P = {rain_prob_true}')
ax1.set_xscale('log')
ax1.set_xlabel('Days of Data')
ax1.set_ylabel('Estimated P(rain)')
ax1.set_title('🌧️ Empirical Probability Converges with Data', fontweight='bold')
ax1.legend()
ax1.set_ylim(0, 0.7)

# Show 3 types comparison
types = ['Classical\\n(Coin Flip)', 'Empirical\\n(Historical data)', 'Subjective\\n(Expert guess)']
certainty = [1.0, 0.7, 0.4]  # how much we "trust" each
colors = ['#27ae60', '#3498db', '#e74c3c']
ax2.barh(types, certainty, color=colors, alpha=0.8)
ax2.set_xlabel('Objectivity / Replicability')
ax2.set_title('Comparing the 3 Types of Probability', fontweight='bold')
ax2.set_xlim(0, 1.2)
for i, v in enumerate(certainty):
    ax2.text(v + 0.02, i, f"{v:.0%}", va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('ch02_types_comparison.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 🔬 Section 3 — Simulation

**Experiment:** Compare classical vs empirical probability with dice.
If classical theory is right, empirical probability should converge to it."""),

    code("""# Compare classical vs empirical for a biased die
# A "biased" die: P(6) = 0.25 instead of 1/6
true_p6_biased = 0.25

n_rolls = 10000
rolls = np.random.choice([1, 2, 3, 4, 5, 6],
                          size=n_rolls,
                          p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.25])

# Running empirical probability
running_p6 = np.cumsum(rolls == 6) / np.arange(1, n_rolls + 1)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(running_p6, color='#3498db', lw=1.5, label='Empirical P(roll=6)', alpha=0.8)
ax.axhline(true_p6_biased, color='#e74c3c', linestyle='--', lw=2, label=f'True P = {true_p6_biased}')
ax.axhline(1/6, color='#27ae60', linestyle=':', lw=2, label=f'Classical P = 1/6 ≈ {1/6:.3f}')
ax.set_xlabel('Number of Rolls')
ax.set_ylabel('P(roll = 6)')
ax.set_title('🎲 Biased Die: Empirical converges to TRUE probability, not classical!', fontweight='bold')
ax.legend(fontsize=11)
ax.set_ylim(0.05, 0.4)
plt.tight_layout()
plt.savefig('ch02_biased_die.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Final empirical estimate: {running_p6[-1]:.4f}")
print(f"True probability:         {true_p6_biased:.4f}")
print(f"Classical probability:    {1/6:.4f}")
print("\\n💡 Key insight: Empirical beats classical when the system isn't perfectly symmetric!")"""),

    md("""## 📊 Section 4 — Visualization: Calibration Curve

A subjective probability is "good" if it's **calibrated**.
Let's visualize what a well-calibrated vs poorly-calibrated forecaster looks like."""),

    code("""# Calibration curves for forecasters
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

stated_probs = np.linspace(0.05, 0.95, 10)

# Well-calibrated forecaster
actual_good = stated_probs + np.random.normal(0, 0.03, 10)
actual_good = np.clip(actual_good, 0, 1)

# Overconfident forecaster (thinks P is higher than it is)
actual_overconf = stated_probs * 0.6 + 0.1

for ax, actual, title in zip(axes,
                               [actual_good, actual_overconf],
                               ['✅ Well-Calibrated Forecaster', '⚠️ Overconfident Forecaster']):
    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Perfect calibration')
    ax.plot(stated_probs, actual, 'o-', markersize=8, lw=2, color='#3498db', label='Actual outcomes')
    ax.fill_between([0, 1], [0, 1], alpha=0.05, color='green')
    ax.set_xlabel('Stated Probability', fontsize=11)
    ax.set_ylabel('Observed Frequency', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

plt.suptitle("Calibration: Do Your Stated Probabilities Match Reality?", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch02_calibration.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📂 Section 5 — Real Dataset Exercise

Let's classify real-world probability statements and verify them empirically."""),

    code("""# Real-world probability exercise: classify and verify
import pandas as pd

statements = [
    {"Statement": "P(coin = Heads) = 0.5", "Type": "Classical",
     "Basis": "Symmetry of coin", "Verify": "Yes, by flipping"},
    {"Statement": "P(rain in Seattle in Nov) = 0.78", "Type": "Empirical",
     "Basis": "NOAA historical data", "Verify": "Yes, with weather records"},
    {"Statement": "P(this startup succeeds) = 0.4", "Type": "Subjective",
     "Basis": "VC's expert judgment", "Verify": "Only if we can repeat history"},
    {"Statement": "P(die shows 6) = 1/6", "Type": "Classical",
     "Basis": "6 equally likely faces", "Verify": "Yes, by rolling many times"},
    {"Statement": "P(patient has cancer | positive test) = 0.15", "Type": "Empirical",
     "Basis": "Clinical trial data", "Verify": "Yes, with patient records"},
]

df = pd.DataFrame(statements)
print("📋 Classifying Real-World Probability Statements")
print("=" * 75)
print(df.to_string(index=False))

# Count by type
print("\\n📊 Distribution of types in practice:")
print(df['Type'].value_counts().to_string())"""),

    md("""## ✏️ Section 6 — Practice Problems

**Problem 1:** Classify each as Classical, Empirical, or Subjective:
- a) P(drawing a red card from a shuffled deck) = 0.5
- b) P(your flight is delayed) based on airline's historical data
- c) A doctor estimates 30% chance a patient has appendicitis
- d) P(exactly 3 heads in 5 coin flips)

**Problem 2:** You flip a coin 20 times and get 14 heads.
- a) What is the empirical probability of heads?
- b) Does this mean the coin is biased?
- c) How many flips would you need to be 95% confident about the true bias?

**Problem 3:** A weather model says P(rain) = 0.6. Over 100 days with this forecast, it rained 45 times.
Is the model well-calibrated? What would perfect calibration look like?

---
<details>
<summary>💡 Solutions</summary>

**P1:** a) Classical, b) Empirical, c) Subjective, d) Classical

**P2:** a) 14/20 = 0.7, b) Not necessarily — this can happen by chance with a fair coin (P ≈ 0.058), c) ~1000+ flips for tight confidence

**P3:** Perfect calibration = 60 rainy days. Model said 0.6, got 0.45 — slightly overconfident.
</details>"""),

    code("""# Problem 2: Simulating the "biased coin?" question
np.random.seed(42)

# How often do we get 14+ heads in 20 flips of a FAIR coin?
n_experiments = 100_000
results = np.random.binomial(n=20, p=0.5, size=n_experiments)
p_14_or_more = (results >= 14).mean()

print(f"P(14 or more heads in 20 flips | fair coin) = {p_14_or_more:.4f}")
print(f"So getting 14 heads happens about {p_14_or_more*100:.1f}% of the time with a FAIR coin.")
print("This is unusual but not impossible — we'd need more data to conclude bias.\\n")

# Show the distribution
from scipy import stats
k = np.arange(0, 21)
probs = stats.binom.pmf(k, 20, 0.5)
colors = ['#e74c3c' if ki >= 14 else '#3498db' for ki in k]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(k, probs, color=colors, edgecolor='white', linewidth=1.5)
ax.axvline(14, color='#e74c3c', linestyle='--', lw=2, label='Our result: 14 heads')
ax.set_xlabel('Number of Heads in 20 Flips')
ax.set_ylabel('Probability')
ax.set_title(f'🪙 Distribution of Heads (Fair Coin) | P(≥14) = {p_14_or_more:.3f}', fontweight='bold')
ax.legend()
plt.savefig('ch02_binom_test.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 🎯 Episode Recap

**3 Key Takeaways:**
1. **Classical probability** uses equally-likely symmetry — perfect for idealized scenarios.
2. **Empirical probability** is the gold standard in practice — it gets better with more data.
3. **Subjective probability** is unavoidable for unique or novel events — formalized by Bayesian statistics.

**🔗 Next Episode:** [Chapter 3 — Rules of Probability: Addition, Multiplication, Complement]

**💬 Viewer Challenge:** Find one example of each type of probability in a news article this week!"""),
])

save(ch02, "02_types_of_probability.ipynb")


# ─── Chapter 3: Rules of Probability ───────────────────────────────────────
ch03 = nb([
    md("""# 📊 Chapter 3: Rules of Probability
*Tier 1 — Foundations | All Tracks*

---
> **🎬 Hook:** What are the odds that at least ONE thing goes wrong today?
> Your alarm might not go off (P = 0.05), your train might be late (P = 0.2), or your laptop might crash (P = 0.1).
> Combining these probabilities is NOT as simple as adding them up...

**🎯 Learning Objectives**
- Apply the Addition Rule (including for non-mutually-exclusive events)
- Apply the Multiplication Rule (independent and dependent events)
- Use the Complement Rule to simplify "at least one" problems
- Avoid the most common mistakes when combining probabilities"""),

    md("""## 📖 Section 1 — Concept Review

### Three Fundamental Rules

**Rule 1: The Complement Rule**
$$P(A^c) = 1 - P(A)$$
*"The probability A does NOT happen = 1 minus P(A does happen)"*

**Rule 2: The Addition Rule**
- If A and B are **mutually exclusive** (can't both happen):
$$P(A \\cup B) = P(A) + P(B)$$
- If A and B **can both happen** (general case):
$$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$$

*Why subtract P(A∩B)? Because if we just add P(A) + P(B), we count the overlap twice!*

**Rule 3: The Multiplication Rule**
- If A and B are **independent** (one doesn't affect the other):
$$P(A \\cap B) = P(A) \\times P(B)$$
- If A and B are **dependent** (one affects the other):
$$P(A \\cap B) = P(A) \\times P(B|A)$$

### ⚠️ Common Mistake
**WRONG:** P(alarm fails OR train late) = 0.05 + 0.20 = 0.25
**RIGHT:** P(alarm fails OR train late) = 0.05 + 0.20 - (0.05 × 0.20) = 0.24"""),

    md("""## 🧮 Section 2 — Math Walkthrough

### Example: Drawing Cards

From a standard 52-card deck:
- P(King) = 4/52
- P(Heart) = 13/52
- P(King AND Heart) = 1/52 (only the King of Hearts)

**Addition rule (not mutually exclusive):**
$$P(\\text{King OR Heart}) = \\frac{4}{52} + \\frac{13}{52} - \\frac{1}{52} = \\frac{16}{52} \\approx 0.308$$

### Example: "At Least One" Problem (Complement Rule)

What's P(at least one head in 3 coin flips)?

*Direct method is painful:* P(1H) + P(2H) + P(3H)
*Complement is elegant:*
$$P(\\text{at least one H}) = 1 - P(\\text{no heads}) = 1 - \\left(\\frac{1}{2}\\right)^3 = 1 - \\frac{1}{8} = \\frac{7}{8} = 0.875$$

### Example: Murphy's Law
What's P(at least ONE thing goes wrong) if:
- P(alarm fails) = 0.05, P(train late) = 0.20, P(laptop crashes) = 0.10

$$P(\\text{all OK}) = (1-0.05)(1-0.20)(1-0.10) = 0.95 \\times 0.80 \\times 0.90 = 0.684$$
$$P(\\text{something goes wrong}) = 1 - 0.684 = 0.316$$"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import seaborn as sns

sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Visualize the Addition Rule with Venn Diagrams ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, (title, overlap) in zip(axes, [
    ("Mutually Exclusive\\nP(A∪B) = P(A) + P(B)", False),
    ("Non-Mutually Exclusive\\nP(A∪B) = P(A) + P(B) - P(A∩B)", True)
]):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')

    if overlap:
        c1 = Circle((3.5, 3.5), 2, color='#3498db', alpha=0.4, label='A')
        c2 = Circle((5.5, 3.5), 2, color='#e74c3c', alpha=0.4, label='B')
        ax.text(2.5, 3.5, 'A only', ha='center', fontsize=10, fontweight='bold')
        ax.text(6.5, 3.5, 'B only', ha='center', fontsize=10, fontweight='bold')
        ax.text(4.5, 3.5, 'A∩B', ha='center', fontsize=9, fontweight='bold', color='purple')
    else:
        c1 = Circle((2.5, 3.5), 2, color='#3498db', alpha=0.4, label='A')
        c2 = Circle((6.5, 3.5), 2, color='#e74c3c', alpha=0.4, label='B')
        ax.text(2.5, 3.5, 'A', ha='center', fontsize=12, fontweight='bold')
        ax.text(6.5, 3.5, 'B', ha='center', fontsize=12, fontweight='bold')

    ax.add_patch(c1)
    ax.add_patch(c2)
    ax.set_title(title, fontsize=11, fontweight='bold')

plt.suptitle("Addition Rule: Mutually Exclusive vs Overlapping Events", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch03_venn.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 🔬 Section 3 — Simulation"""),

    code("""# Verify the rules through simulation
np.random.seed(42)
N = 100_000

# Simulate drawing a card (King OR Heart)
deck = list(range(52))  # 0-51
ranks = [i % 13 for i in deck]   # 0=Ace, 12=King
suits = [i // 13 for i in deck]  # 0=Spades, 1=Hearts, 2=Diamonds, 3=Clubs

draws = np.random.randint(0, 52, N)
is_king  = ranks[draws[0]:N+draws[0]] if False else np.array([ranks[d] == 12 for d in draws])
is_heart = np.array([suits[d] == 1 for d in draws])
is_king_of_hearts = is_king & is_heart

p_king        = is_king.mean()
p_heart       = is_heart.mean()
p_king_heart  = is_king_of_hearts.mean()
p_king_or_heart = (is_king | is_heart).mean()

print("🃏 Card Drawing Verification")
print(f"  P(King)          = {p_king:.4f}  (theoretical: {4/52:.4f})")
print(f"  P(Heart)         = {p_heart:.4f}  (theoretical: {13/52:.4f})")
print(f"  P(King∩Heart)    = {p_king_heart:.4f}  (theoretical: {1/52:.4f})")
print(f"  P(King∪Heart)    = {p_king_or_heart:.4f}  (theoretical: {16/52:.4f})")
print(f"  P(K)+P(H)-P(K∩H) = {p_king + p_heart - p_king_heart:.4f}  ← Addition rule verified!")"""),

    code("""# Simulate Murphy's Law: at least one thing goes wrong
N = 100_000
p_alarm_fail = 0.05
p_train_late = 0.20
p_laptop_crash = 0.10

alarm_fails = np.random.random(N) < p_alarm_fail
train_late  = np.random.random(N) < p_train_late
laptop_crash = np.random.random(N) < p_laptop_crash

something_wrong = alarm_fails | train_late | laptop_crash
p_something_wrong = something_wrong.mean()

# Theoretical
p_all_ok = (1 - p_alarm_fail) * (1 - p_train_late) * (1 - p_laptop_crash)
p_theory = 1 - p_all_ok

print("😤 Murphy's Law Simulation")
print(f"  P(alarm fails)    = {p_alarm_fail}")
print(f"  P(train late)     = {p_train_late}")
print(f"  P(laptop crashes) = {p_laptop_crash}")
print()
print(f"  Theoretical P(something wrong) = {p_theory:.4f}")
print(f"  Simulated   P(something wrong) = {p_something_wrong:.4f}")
print()
print(f"  Common mistake (just adding): {p_alarm_fail + p_train_late + p_laptop_crash:.4f} ← WRONG!")

# Visualize breakdown
fig, ax = plt.subplots(figsize=(9, 4))
labels = ['Alarm Only', 'Train Only', 'Laptop Only', 'Multiple Problems', 'All Fine']
only_alarm   = (alarm_fails & ~train_late & ~laptop_crash).mean()
only_train   = (~alarm_fails & train_late & ~laptop_crash).mean()
only_laptop  = (~alarm_fails & ~train_late & laptop_crash).mean()
multiple     = (alarm_fails.astype(int) + train_late.astype(int) + laptop_crash.astype(int) > 1).mean()
all_fine     = (~alarm_fails & ~train_late & ~laptop_crash).mean()

sizes = [only_alarm, only_train, only_laptop, multiple, all_fine]
colors = ['#e74c3c', '#e67e22', '#9b59b6', '#c0392b', '#27ae60']
ax.pie(sizes, labels=[f"{l}\\n({s:.1%})" for l, s in zip(labels, sizes)],
       colors=colors, autopct='', startangle=90)
ax.set_title("😤 Murphy's Law: How Your Morning Goes Wrong", fontsize=12, fontweight='bold')
plt.savefig('ch03_murphys_law.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📊 Section 4 — Visualization"""),

    code("""# Visualize all three rules side by side
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Complement Rule
p_A = 0.3
outcomes = np.random.random(1000)
colors_comp = ['#e74c3c' if x < p_A else '#3498db' for x in outcomes]
ax = axes[0]
ax.scatter(np.random.uniform(0, 10, 1000), np.random.uniform(0, 10, 1000),
           c=colors_comp, s=20, alpha=0.6)
ax.set_title(f"Complement Rule\\nP(A) = {p_A}, P(Aᶜ) = {1-p_A}", fontweight='bold')
ax.set_xticks([]); ax.set_yticks([])
red_patch = mpatches.Patch(color='#e74c3c', label=f'A: {p_A:.0%}')
blue_patch = mpatches.Patch(color='#3498db', label=f'Aᶜ: {1-p_A:.0%}')
ax.legend(handles=[red_patch, blue_patch])

# Addition Rule
p_A, p_B = 0.4, 0.3
p_both = p_A * p_B  # independent
outcomes_A = np.random.random(1000) < p_A
outcomes_B = np.random.random(1000) < p_B
colors_add = ['#9b59b6' if (a and b) else '#e74c3c' if a else '#3498db' if b else '#ecf0f1'
              for a, b in zip(outcomes_A, outcomes_B)]
axes[1].scatter(np.random.uniform(0, 10, 1000), np.random.uniform(0, 10, 1000),
                c=colors_add, s=20, alpha=0.6)
axes[1].set_title(f"Addition Rule\\nP(A∪B) = {p_A+p_B-p_both:.2f}", fontweight='bold')
axes[1].set_xticks([]); axes[1].set_yticks([])

# Multiplication Rule (independent)
n = [10, 100, 1000, 10000]
p_product = [np.mean((np.random.random(ni) < 0.5) & (np.random.random(ni) < 0.5)) for ni in n]
axes[2].semilogx(n, p_product, 'bo-', markersize=8)
axes[2].axhline(0.25, color='red', linestyle='--', label='True: 0.5×0.5=0.25')
axes[2].set_xlabel('Sample Size')
axes[2].set_ylabel('Estimated P(A∩B)')
axes[2].set_title("Multiplication Rule\\nP(A∩B) = P(A)×P(B) if independent", fontweight='bold')
axes[2].legend()

plt.suptitle("The Three Rules of Probability", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('ch03_three_rules.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📂 Section 5 — Real Dataset Exercise: Quality Control

A factory produces components. Each component passes through 3 quality checks.
Let's use probability rules to analyze the production line."""),

    code("""import pandas as pd

# Quality control scenario
np.random.seed(42)

p_fail_check1 = 0.05   # 5% fail check 1
p_fail_check2 = 0.03   # 3% fail check 2 (given they passed check 1)
p_fail_check3 = 0.02   # 2% fail check 3 (given they passed checks 1 and 2)

N = 10_000
# Simulate production line
pass1 = np.random.random(N) > p_fail_check1
pass2 = np.where(pass1, np.random.random(N) > p_fail_check2, False)
pass3 = np.where(pass2, np.random.random(N) > p_fail_check3, False)

p_pass_all_sim = pass3.mean()
p_pass_all_theory = (1 - p_fail_check1) * (1 - p_fail_check2) * (1 - p_fail_check3)

print("🏭 Quality Control Analysis")
print(f"  P(pass check 1)   = {pass1.mean():.4f}  (theory: {1-p_fail_check1:.4f})")
print(f"  P(pass checks 1&2) = {pass2.mean():.4f}  (theory: {(1-p_fail_check1)*(1-p_fail_check2):.4f})")
print(f"  P(pass all 3)      = {pass3.mean():.4f}  (theory: {p_pass_all_theory:.4f})")
print(f"  P(defective product) = {1-pass3.mean():.4f}  (theory: {1-p_pass_all_theory:.4f})")
print()

# How many defects in a day if 10,000 units produced?
n_defective_sim = (~pass3).sum()
n_defective_theory = int(N * (1 - p_pass_all_theory))
print(f"  Defective units (simulated): {n_defective_sim}")
print(f"  Defective units (theory):    {n_defective_theory}")
print()

stages = ['After Check 1', 'After Check 2', 'After Check 3']
defect_rates = [1 - pass1.mean(), 1 - pass2.mean(), 1 - pass3.mean()]

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(stages, [r*100 for r in defect_rates], color=['#e74c3c', '#e67e22', '#27ae60'])
ax.set_ylabel('Cumulative Defect Rate (%)')
ax.set_title('🏭 Quality Control: Defect Rate Through Production Line', fontweight='bold')
for bar, rate in zip(bars, defect_rates):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{rate:.2%}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('ch03_quality_control.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**Problem 1 — Complement:**
A fair die is rolled 3 times. What is P(at least one 6)?

**Problem 2 — Addition Rule:**
In a class, 40% of students play sports, 30% play music, and 15% do both.
What is P(a random student plays sports OR music)?

**Problem 3 — Multiplication Rule:**
A password requires 2 characters. Each is randomly chosen from {A, B, C, D, E}.
a) P(both are vowels)?
b) P(at least one vowel)?

**Problem 4 — Quality Control:**
A system has 3 components in series. Each fails independently with P = 0.01.
What is P(system failure)?

---
<details>
<summary>💡 Solutions</summary>

**P1:** P(at least one 6) = 1 - P(no 6)³ = 1 - (5/6)³ = 1 - 0.579 = **0.421**

**P2:** P(sports OR music) = 0.40 + 0.30 - 0.15 = **0.55**

**P3:** Vowels = {A, E}, P(vowel) = 2/5
a) P(both vowels) = (2/5)² = 4/25 = **0.16**
b) P(at least one vowel) = 1 - (3/5)² = 1 - 9/25 = **0.64**

**P4:** P(system OK) = (0.99)³ ≈ 0.9703
P(failure) = 1 - 0.9703 ≈ **0.0297**
</details>"""),

    code("""# Verify all solutions
print("✅ Solution Verification")
print()
print("Problem 1: P(at least one 6 in 3 rolls)")
print(f"  = 1 - (5/6)^3 = {1 - (5/6)**3:.4f}")
sim_p1 = np.mean([np.any(np.random.randint(1, 7, 3) == 6) for _ in range(100_000)])
print(f"  Simulated: {sim_p1:.4f}")

print()
print("Problem 2: P(sports OR music)")
print(f"  = 0.40 + 0.30 - 0.15 = {0.40 + 0.30 - 0.15:.2f}")

print()
print("Problem 3:")
print(f"  a) P(both vowels) = (2/5)^2 = {(2/5)**2:.4f}")
print(f"  b) P(at least one vowel) = 1 - (3/5)^2 = {1 - (3/5)**2:.4f}")

print()
print("Problem 4: P(system failure)")
print(f"  = 1 - (0.99)^3 = {1 - 0.99**3:.6f}")"""),

    md("""## 🎯 Episode Recap

**3 Key Takeaways:**
1. **Complement rule** is your best friend for "at least one" problems.
2. **Addition rule** requires subtracting the intersection if events can overlap.
3. **Multiplication rule** requires independence — always check this assumption!

**🔗 Next Episode:** [Chapter 4 — Conditional Probability: P(A|B) and Why It Breaks Your Intuition]

**💬 Viewer Challenge:** If each person in a room of 23 has an independent birthday, what's P(at least 2 share a birthday)? Use the complement rule! (Spoiler: it's > 50%)"""),
])

save(ch03, "03_rules_of_probability.ipynb")


# ─── Chapter 4: Conditional Probability ────────────────────────────────────
ch04 = nb([
    md("""# 📊 Chapter 4: Conditional Probability
*Tier 1 — Foundations | All Tracks*

---
> **🎬 Hook:** A medical test for a rare disease is 99% accurate.
> You test positive. Are you 99% likely to have the disease?
> The answer is **NO** — and it might be less than 10%.
> This is the most important (and most misunderstood) concept in probability.

**🎯 Learning Objectives**
- Calculate conditional probability P(A|B) correctly
- Understand what "given that" means mathematically
- Spot independence vs dependence
- Avoid the Prosecutor's Fallacy and Base Rate Neglect"""),

    md("""## 📖 Section 1 — Concept Review

### What is Conditional Probability?

P(A|B) = "Probability of A, **given that** B has already happened"

When we learn that B occurred, it **shrinks our sample space** from Ω to just B.
Then we ask: within B, what fraction of outcomes are also in A?

$$P(A|B) = \\frac{P(A \\cap B)}{P(B)} \\quad \\text{(assuming P(B) > 0)}$$

### Visual Intuition: Restricting the Sample Space

Before knowing B: We look at ALL of Ω
After knowing B: We zoom in — B is now our entire world

```
     Ω                    B (our new world)
  ┌──────────┐         ┌────────┐
  │    A  ╔══╪══╗      │   A∩B  │
  │   ╔══╪═╪══╗│      │        │
  │   ║  │ ║  ║│  →   └────────┘
  │   ╚══╪═╪══╝│      P(A|B) =
  │      ╚══╪══╝      |A∩B| / |B|
  └──────────┘
```

### Independence
A and B are **independent** if knowing B tells you NOTHING about A:
$$P(A|B) = P(A) \quad \\Leftrightarrow \\quad P(A \\cap B) = P(A) \\cdot P(B)$$

### ⚠️ Common Traps
1. **Base Rate Neglect:** Ignoring how rare the disease is before the test
2. **Prosecutor's Fallacy:** Confusing P(evidence|innocent) with P(innocent|evidence)
3. **Confusion of the inverse:** P(A|B) ≠ P(B|A)"""),

    md("""## 🧮 Section 2 — Math Walkthrough

### The Medical Test Problem

- Disease prevalence (base rate): P(Disease) = 0.001 (1 in 1,000)
- Test sensitivity: P(Positive | Disease) = 0.99
- Test specificity: P(Negative | No Disease) = 0.99 → P(Positive | No Disease) = 0.01

**What we want:** P(Disease | Positive test) = ?

Using the definition:
$$P(D|+) = \\frac{P(+ \\cap D)}{P(+)}$$

**Step 1:** P(+ and Disease) = P(+|D) × P(D) = 0.99 × 0.001 = **0.00099**

**Step 2:** P(+) = P(+|D)×P(D) + P(+|¬D)×P(¬D)
= 0.99×0.001 + 0.01×0.999 = 0.00099 + 0.00999 = **0.01098**

**Step 3:**
$$P(D|+) = \\frac{0.00099}{0.01098} \\approx \\mathbf{0.090 = 9\\%}$$

**Despite a 99% accurate test, a positive result means only a 9% chance of disease!**
This is called the **False Positive Paradox** — and it's caused by base rate neglect."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")
np.random.seed(42)

# The Medical Test Problem — visualized
def medical_test_analysis(prevalence, sensitivity, specificity):
    fp_rate = 1 - specificity

    # Bayes' theorem
    p_pos_and_disease   = sensitivity * prevalence
    p_pos_and_no_disease = fp_rate * (1 - prevalence)
    p_positive           = p_pos_and_disease + p_pos_and_no_disease
    p_disease_given_pos  = p_pos_and_disease / p_positive

    return {
        'P(D)': prevalence,
        'P(+|D)': sensitivity,
        'P(+|¬D)': fp_rate,
        'P(+)': p_positive,
        'P(D|+)': p_disease_given_pos
    }

# Scenario: common vs rare disease
scenarios = [
    {"name": "Rare disease (1 in 1000)", "prev": 0.001, "sens": 0.99, "spec": 0.99},
    {"name": "Common disease (1 in 10)", "prev": 0.10,  "sens": 0.99, "spec": 0.99},
    {"name": "Very common (1 in 3)",     "prev": 0.33,  "sens": 0.99, "spec": 0.99},
]

print("🏥 Medical Test Analysis: P(Disease | Positive Test)")
print("=" * 65)
for s in scenarios:
    result = medical_test_analysis(s['prev'], s['sens'], s['spec'])
    print(f"\\n{s['name']}")
    print(f"  Base rate:          {s['prev']:.3f}")
    print(f"  P(Disease | +test): {result['P(D|+)']:.3f} ({result['P(D|+)']:.1%})")

print("\\n💡 KEY INSIGHT: Same 99% accurate test — but VERY different results based on base rate!")"""),

    code("""# Visualize how base rate affects P(Disease | Positive)
prevalences = np.linspace(0.001, 0.5, 200)
p_d_given_pos = []
for prev in prevalences:
    r = medical_test_analysis(prev, 0.99, 0.99)
    p_d_given_pos.append(r['P(D|+)'])

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(prevalences, p_d_given_pos, lw=3, color='#e74c3c', label='P(Disease | Positive test)')
ax.axhline(0.5, color='gray', linestyle=':', lw=1.5, label='50% threshold')
ax.fill_between(prevalences, p_d_given_pos, alpha=0.2, color='#e74c3c')

# Mark our key scenarios
for prev, label in [(0.001, 'Rare: 0.1%'), (0.10, 'Common: 10%'), (0.33, 'Very common: 33%')]:
    r = medical_test_analysis(prev, 0.99, 0.99)
    ax.scatter([prev], [r['P(D|+)']], s=100, zorder=5, color='black')
    ax.annotate(f"{label}\\n→ P(D|+)={r['P(D|+)']:.1%}",
                xy=(prev, r['P(D|+)']), xytext=(prev+0.03, r['P(D|+)']-0.08),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))

ax.set_xlabel('Disease Prevalence (Base Rate)', fontsize=12)
ax.set_ylabel('P(Disease | Positive Test)', fontsize=12)
ax.set_title('🏥 The Base Rate Effect: How Rare the Disease is Changes Everything', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('ch04_base_rate.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 🔬 Section 3 — Simulation: The Monty Hall Problem

The most famous conditional probability puzzle:
You're on a game show. 3 doors: one has a car, two have goats.
You pick door 1. The host (who knows where the car is) opens door 3 showing a goat.
Should you switch to door 2?

**Most people say: doesn't matter, 50/50.**
**Math says: SWITCH — P(win|switch) = 2/3!**"""),

    code("""def monty_hall_simulation(n=100_000, switch=True):
    wins = 0
    for _ in range(n):
        car_door = np.random.randint(0, 3)
        chosen   = np.random.randint(0, 3)

        # Host opens a door that has a goat and isn't chosen
        remaining = [d for d in range(3) if d != chosen and d != car_door]
        host_opens = np.random.choice(remaining)

        if switch:
            # Switch to the remaining door
            chosen = [d for d in range(3) if d != chosen and d != host_opens][0]

        wins += (chosen == car_door)
    return wins / n

p_win_stay   = monty_hall_simulation(100_000, switch=False)
p_win_switch = monty_hall_simulation(100_000, switch=True)

print("🚗 Monty Hall Problem Simulation (100,000 games)")
print(f"  P(win | STAY)   = {p_win_stay:.4f}  (theory: 1/3 = {1/3:.4f})")
print(f"  P(win | SWITCH) = {p_win_switch:.4f}  (theory: 2/3 = {2/3:.4f})")
print()
print("💡 ALWAYS SWITCH! Your initial guess is wrong 2/3 of the time.")
print("   The host's action gives you NEW INFORMATION — use it!")

# Visualize
fig, ax = plt.subplots(figsize=(7, 4))
strategies = ['Stay', 'Switch']
probs = [p_win_stay, p_win_switch]
colors = ['#e74c3c', '#27ae60']
bars = ax.bar(strategies, probs, color=colors, width=0.4, edgecolor='white', linewidth=2)
ax.axhline(1/3, color='gray', linestyle='--', alpha=0.5, label='1/3')
ax.axhline(2/3, color='gray', linestyle=':', alpha=0.5, label='2/3')
for bar, p in zip(bars, probs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{p:.1%}', ha='center', fontsize=14, fontweight='bold')
ax.set_ylim(0, 0.8)
ax.set_ylabel('P(Win)')
ax.set_title('🚗 Monty Hall: Always Switch!', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch04_monty_hall.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📊 Section 4 — Visualization: Conditional Probability Table"""),

    code("""# Contingency table visualization
np.random.seed(42)
n = 10_000

# Gender and sport preference (hypothetical data)
is_female = np.random.random(n) < 0.5
likes_soccer = np.where(is_female,
                        np.random.random(n) < 0.45,   # P(soccer|female) = 0.45
                        np.random.random(n) < 0.65)   # P(soccer|male) = 0.65

# Build contingency table
df = pd.DataFrame({'Gender': np.where(is_female, 'Female', 'Male'),
                   'Sport': np.where(likes_soccer, 'Soccer', 'Other')})
ct = pd.crosstab(df['Gender'], df['Sport'], margins=True, normalize=False)
ct_pct = pd.crosstab(df['Gender'], df['Sport'], normalize='index')

print("📊 Contingency Table (Counts)")
print(ct)
print()
print("📊 Conditional Probabilities P(Sport | Gender)")
print(ct_pct.round(3))
print()
print(f"P(Soccer | Female) = {ct_pct.loc['Female', 'Soccer']:.3f}")
print(f"P(Soccer | Male)   = {ct_pct.loc['Male', 'Soccer']:.3f}")
print(f"P(Soccer)          = {likes_soccer.mean():.3f}  ← marginal probability")
print()
print("Since P(Soccer|Female) ≠ P(Soccer|Male), Gender and Sport preference are NOT independent!")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
ct_pct.plot(kind='bar', ax=axes[0], color=['#3498db', '#e74c3c'], rot=0)
axes[0].set_title('Conditional: P(Sport | Gender)', fontweight='bold')
axes[0].set_ylabel('Probability')
axes[0].legend(title='Sport')

# Joint probabilities
ct_joint = pd.crosstab(df['Gender'], df['Sport'], normalize=True)
ct_joint.plot(kind='bar', ax=axes[1], color=['#3498db', '#e74c3c'], rot=0)
axes[1].set_title('Joint: P(Gender, Sport)', fontweight='bold')
axes[1].set_ylabel('Probability')

plt.tight_layout()
plt.savefig('ch04_contingency.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📂 Section 5 — Real Dataset Exercise: Spam Filter

Email spam filters use conditional probability.
P(spam | contains "FREE") vs P(spam | contains "meeting")"""),

    code("""# Simulate spam filter scenario
np.random.seed(42)
n_emails = 5000
p_spam = 0.3

is_spam = np.random.random(n_emails) < p_spam

# Word "FREE": appears in 60% of spam, 5% of legitimate emails
has_free = np.where(is_spam, np.random.random(n_emails) < 0.60,
                    np.random.random(n_emails) < 0.05)

# Word "meeting": appears in 5% of spam, 40% of legitimate emails
has_meeting = np.where(is_spam, np.random.random(n_emails) < 0.05,
                        np.random.random(n_emails) < 0.40)

# Calculate conditional probabilities
p_spam_given_free    = (is_spam & has_free).sum() / has_free.sum()
p_spam_given_meeting = (is_spam & has_meeting).sum() / has_meeting.sum()
p_spam_given_neither = (is_spam & ~has_free & ~has_meeting).sum() / (~has_free & ~has_meeting).sum()

print("📧 Email Spam Filter: Conditional Probabilities")
print(f"  Prior: P(spam) = {is_spam.mean():.3f}")
print()
print(f"  P(spam | contains 'FREE')    = {p_spam_given_free:.3f}  ← very suspicious!")
print(f"  P(spam | contains 'meeting') = {p_spam_given_meeting:.3f}  ← likely legitimate")
print(f"  P(spam | neither word)       = {p_spam_given_neither:.3f}")
print()
print("💡 This is Naive Bayes classification — used in every spam filter!")

words = ["Contains 'FREE'", "Contains 'meeting'", "Neither word"]
spam_probs = [p_spam_given_free, p_spam_given_meeting, p_spam_given_neither]
colors = ['#e74c3c' if p > 0.5 else '#27ae60' for p in spam_probs]

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(words, spam_probs, color=colors, alpha=0.8)
ax.axvline(0.5, color='black', linestyle='--', lw=2, label='Decision threshold (0.5)')
ax.axvline(p_spam, color='gray', linestyle=':', lw=2, label=f'Prior P(spam) = {p_spam}')
ax.set_xlabel('P(Spam | Word)')
ax.set_title('📧 Spam Filter: Conditional Probability Updates Belief', fontweight='bold')
ax.legend()
for bar, p in zip(bars, spam_probs):
    ax.text(p + 0.01, bar.get_y() + bar.get_height()/2, f'{p:.3f}', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('ch04_spam_filter.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**Problem 1 — Basic:**
P(A) = 0.4, P(B) = 0.3, P(A∩B) = 0.12.
Find P(A|B) and P(B|A). Are A and B independent?

**Problem 2 — Medical:**
A disease affects 2% of a population. A test has 95% sensitivity and 90% specificity.
What is P(disease | positive test)?

**Problem 3 — Challenge (Prosecutor's Fallacy):**
A crime was committed. DNA evidence matches the suspect with P = 1/1,000,000.
Prosecutor argues: "P(innocent | match) = 0.000001"
Why is this WRONG? What do we actually need to know?

---
<details>
<summary>💡 Solutions</summary>

**P1:** P(A|B) = P(A∩B)/P(B) = 0.12/0.30 = **0.40**
P(B|A) = P(A∩B)/P(A) = 0.12/0.40 = **0.30**
Since P(A|B) = P(A) = 0.40, they ARE independent.

**P2:** P(D|+) = (0.95×0.02) / (0.95×0.02 + 0.10×0.98) = 0.019/(0.019+0.098) = **16.2%**

**P3:** The prosecutor confused P(match|innocent) with P(innocent|match).
We need P(innocent) = 1 - P(guilty before DNA evidence). If only 1 person in a city of 1M could have done it, P(match|innocent) = 1/1M seems damning. But it needs prior probability applied correctly.
</details>"""),

    code("""# Verify Problem 2
prevalence = 0.02
sensitivity = 0.95
specificity = 0.90
fp_rate = 1 - specificity

p_pos_given_disease    = sensitivity
p_pos_given_no_disease = fp_rate

p_pos = p_pos_given_disease * prevalence + p_pos_given_no_disease * (1 - prevalence)
p_disease_given_pos = (p_pos_given_disease * prevalence) / p_pos

print(f"Problem 2 Solution:")
print(f"  P(D)       = {prevalence}")
print(f"  P(+|D)     = {sensitivity}")
print(f"  P(+|¬D)    = {fp_rate}")
print(f"  P(+)       = {p_pos:.4f}")
print(f"  P(D|+)     = {p_disease_given_pos:.4f} = {p_disease_given_pos:.1%}")
print()
print(f"Even with a 95% sensitive test, only {p_disease_given_pos:.1%} of positives actually have the disease!")
print("This is because the disease is RARE — base rate matters enormously.")"""),

    md("""## 🎯 Episode Recap

**3 Key Takeaways:**
1. **P(A|B) means we restrict our sample space to B** — we're no longer considering all outcomes.
2. **Base Rate Neglect is everywhere** — always consider how rare/common an event is before interpreting a test.
3. **P(A|B) ≠ P(B|A)** — the direction of conditioning completely changes the answer.

**🔗 Next Episode:** [Chapter 5 — Bayes' Theorem: Prior, Likelihood, and Posterior]

**💬 Viewer Challenge:** Solve the Birthday Problem: What's the minimum number of people in a room for P(at least two share a birthday) > 50%? (Hint: use the complement rule!)"""),
])

save(ch04, "04_conditional_probability.ipynb")

save(ch04, "04_conditional_probability.ipynb")  # already called above, skip duplicate

# ─── Chapter 5: Bayes' Theorem ───────────────────────────────────────────────
ch05 = nb([
    md("""# 📊 Chapter 5: Bayes' Theorem
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** A test for a rare disease is 99% accurate. You test positive. Are you doomed?
> Bayes' Theorem says: probably not — and gives us the exact number.

**🎯 Objectives:** Understand prior, likelihood, posterior. Apply Bayes to real problems."""),

    md("""## 📖 Section 1 — Concept Review

Bayes' Theorem is the engine of rational belief updating:

$$P(H|E) = \\frac{P(E|H) \\cdot P(H)}{P(E)}$$

| Term | Name | Meaning |
|------|------|---------|
| P(H) | **Prior** | Your belief BEFORE seeing evidence |
| P(E\\|H) | **Likelihood** | How probable is the evidence IF H is true? |
| P(H\\|E) | **Posterior** | Your updated belief AFTER seeing evidence |
| P(E) | **Normalizing constant** | Total probability of seeing this evidence |

The denominator expands as:
$$P(E) = P(E|H)P(H) + P(E|\\neg H)P(\\neg H)$$

### Intuition: Bayes as Belief Updating
```
PRIOR → [Evidence arrives] → POSTERIOR
  ↑                               ↑
What we believed              What we should believe now
before seeing data             given the data
```"""),

    md("""## 🧮 Section 2 — Math Walkthrough

### Cookie Jar Example
Two jars: Jar 1 has 30 chocolate + 10 vanilla. Jar 2 has 20 of each.
You pick a jar at random and draw a chocolate cookie. Which jar is it probably from?

- P(Jar 1) = P(Jar 2) = 0.5 (equal prior)
- P(Choc | Jar 1) = 30/40 = 0.75
- P(Choc | Jar 2) = 20/40 = 0.50

$$P(\\text{Jar 1} | \\text{Choc}) = \\frac{0.75 \\times 0.5}{0.75 \\times 0.5 + 0.50 \\times 0.5} = \\frac{0.375}{0.625} = 0.6$$

After drawing a chocolate cookie, P(Jar 1) goes from 50% to **60%**."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
np.random.seed(42)

# Bayes' Theorem calculator
def bayes(prior, likelihood_h, likelihood_not_h):
    numerator = likelihood_h * prior
    denominator = likelihood_h * prior + likelihood_not_h * (1 - prior)
    return numerator / denominator

# Medical test: vary prevalence
prevalences = np.linspace(0.001, 0.5, 300)
posterior = [bayes(p, 0.99, 0.01) for p in prevalences]

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

axes[0].plot(prevalences, posterior, lw=3, color='#e74c3c')
axes[0].axhline(0.5, color='gray', linestyle='--', lw=1.5)
axes[0].set_xlabel('Prior P(Disease)')
axes[0].set_ylabel('Posterior P(Disease | Positive)')
axes[0].set_title('🏥 Bayes: How Base Rate Shapes Posterior', fontweight='bold')
axes[0].fill_between(prevalences, posterior, alpha=0.2, color='#e74c3c')

# Sequential Bayesian updating
prior = 0.5
evidence_seq = [0.75, 0.75, 0.50, 0.75, 0.75]  # likelihood each time chocolate drawn
posteriors = [prior]
for lik in evidence_seq:
    prior = bayes(prior, lik, 0.50)
    posteriors.append(prior)

axes[1].plot(posteriors, 'bo-', markersize=10, lw=2.5)
axes[1].axhline(0.5, color='gray', linestyle='--', lw=1.5, label='50/50 prior')
axes[1].set_xlabel('Number of Cookie Draws')
axes[1].set_ylabel('P(Jar 1 | Observations)')
axes[1].set_title('🍪 Sequential Bayesian Updating', fontweight='bold')
axes[1].set_ylim(0.4, 1.0)
axes[1].legend()

plt.tight_layout()
plt.savefig('ch05_bayes.png', dpi=150, bbox_inches='tight')
plt.show()

print("Medical test (99% accurate, disease prevalence 0.1%):")
print(f"  P(Disease | Positive) = {bayes(0.001, 0.99, 0.01):.3f}")
print()
print("Cookie jar after 5 chocolate draws:")
print(f"  P(Jar 1) = {posteriors[-1]:.3f}")"""),

    md("""## 🔬 Section 3 — Simulation"""),

    code("""# Simulate Bayesian spam filter updating
np.random.seed(42)
n = 10000
is_spam = np.random.random(n) < 0.3

# 5 features: each has different P(feature|spam) and P(feature|legit)
features = {
    'FREE':    {'p_spam': 0.7, 'p_legit': 0.05},
    'WINNER':  {'p_spam': 0.6, 'p_legit': 0.02},
    'Meeting': {'p_spam': 0.05,'p_legit': 0.5},
    'Invoice': {'p_spam': 0.1, 'p_legit': 0.3},
    'Urgent':  {'p_spam': 0.4, 'p_legit': 0.1},
}

# Sequential update for one email with features: FREE=yes, WINNER=yes, Meeting=no
prior = 0.3
updates = [('Prior', prior)]

for fname, vals in list(features.items())[:3]:
    present = True if fname in ['FREE', 'WINNER'] else False
    if present:
        prior = bayes(prior, vals['p_spam'], vals['p_legit'])
    updates.append((f"After '{fname}'", prior))

print("📧 Bayesian Spam Filter - Sequential Updates")
for name, p in updates:
    bar = '█' * int(p * 40)
    print(f"  {name:<20} P(spam) = {p:.3f}  {bar}")"""),

    md("""## 📊 Section 4 — Visualization: Prior → Posterior"""),

    code("""# Visualize prior vs posterior distributions
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

scenarios = [
    {'prior': 0.01, 'lik_h': 0.95, 'lik_nh': 0.05, 'title': 'Rare disease\n(Prior=1%)'},
    {'prior': 0.20, 'lik_h': 0.95, 'lik_nh': 0.05, 'title': 'Moderate prevalence\n(Prior=20%)'},
    {'prior': 0.50, 'lik_h': 0.95, 'lik_nh': 0.05, 'title': 'Common condition\n(Prior=50%)'},
]

for ax, s in zip(axes, scenarios):
    posterior_val = bayes(s['prior'], s['lik_h'], s['lik_nh'])
    categories = ['No Disease', 'Disease']
    prior_vals = [1 - s['prior'], s['prior']]
    post_vals  = [1 - posterior_val, posterior_val]
    x = np.arange(2)
    ax.bar(x - 0.2, prior_vals,  0.35, label='Prior', color='#3498db', alpha=0.7)
    ax.bar(x + 0.2, post_vals,   0.35, label='Posterior', color='#e74c3c', alpha=0.7)
    ax.set_xticks(x); ax.set_xticklabels(categories)
    ax.set_title(s['title'] + f'\n→ P(D|+) = {posterior_val:.2f}', fontweight='bold', fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=8)

plt.suptitle("Bayes' Theorem: Prior vs Posterior (given positive test)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch05_prior_posterior.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 📂 Section 5 — Real Exercise: A/B Testing with Bayes

You're testing a new website button. Your prior belief: P(new is better) = 0.5.
After 100 visits: new gets 65 clicks, old gets 50 clicks. Update your belief."""),

    code("""from scipy import stats

np.random.seed(42)
# Beta-Binomial Bayesian A/B test
# Prior: Beta(1,1) = uniform (no preference)
# Observed: new=65 clicks out of 100, old=50 out of 100

alpha_prior, beta_prior = 1, 1  # uniform prior

# Posterior for each variant
new_clicks, new_visits = 65, 100
old_clicks, old_visits = 50, 100

new_posterior = stats.beta(alpha_prior + new_clicks, beta_prior + new_visits - new_clicks)
old_posterior = stats.beta(alpha_prior + old_clicks, beta_prior + old_visits - old_clicks)

x = np.linspace(0.3, 0.9, 300)
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(x, new_posterior.pdf(x), lw=3, color='#27ae60', label=f'New button (65/100)')
ax.plot(x, old_posterior.pdf(x), lw=3, color='#e74c3c', label=f'Old button (50/100)')
ax.fill_between(x, new_posterior.pdf(x), alpha=0.2, color='#27ae60')
ax.fill_between(x, old_posterior.pdf(x), alpha=0.2, color='#e74c3c')
ax.axvline(0.65, color='#27ae60', linestyle='--', alpha=0.5)
ax.axvline(0.50, color='#e74c3c', linestyle='--', alpha=0.5)
ax.set_xlabel('Click-Through Rate')
ax.set_ylabel('Posterior Density')
ax.set_title('🖱️ Bayesian A/B Test: Posterior Distributions', fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('ch05_ab_test.png', dpi=150, bbox_inches='tight')
plt.show()

# P(new > old) via Monte Carlo
samples_new = new_posterior.rvs(100_000)
samples_old = old_posterior.rvs(100_000)
p_new_better = (samples_new > samples_old).mean()
print(f"P(new button is better) = {p_new_better:.3f}")
print(f"Expected CTR (new): {new_posterior.mean():.3f}")
print(f"Expected CTR (old): {old_posterior.mean():.3f}")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** A factory has 2 machines. Machine A produces 60% of output with 2% defect rate.
Machine B produces 40% with 5% defect rate. You pick a random defective item.
P(from Machine A)?

**P2:** You take a COVID test with sensitivity=85%, specificity=95%.
Population prevalence=3%. You test positive. What is P(you have COVID)?

---
<details><summary>💡 Solutions</summary>

**P1:** P(A) = 0.6, P(defect|A) = 0.02, P(defect|B) = 0.05
P(defect) = 0.6×0.02 + 0.4×0.05 = 0.012 + 0.020 = 0.032
P(A|defect) = (0.02×0.6)/0.032 = **0.375**

**P2:** P(D|+) = (0.85×0.03)/(0.85×0.03 + 0.05×0.97) = 0.0255/0.0740 = **34.5%**
</details>"""),

    code("""# Solutions
print("P1:", bayes(0.6, 0.02, 0.05))
print("P2:", bayes(0.03, 0.85, 0.05))"""),

    md("""## 🎯 Recap
1. **Prior × Likelihood → Posterior** — the core of Bayesian reasoning.
2. Base rate (prior) is crucial — ignoring it causes the False Positive Paradox.
3. Bayesian updating is sequential — each new piece of evidence refines your belief.

**Next:** [Chapter 6 — Random Variables: PMF, PDF, and CDF]"""),
])
save(ch05, "05_bayes_theorem.ipynb")


# ─── Chapter 6: Random Variables ────────────────────────────────────────────
ch06 = nb([
    md("""# 📊 Chapter 6: Random Variables
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** A "random variable" isn't really random at all — it's the most precise tool in probability.
> It's a function that maps every outcome to a number.

**🎯 Objectives:** Understand discrete vs continuous RVs, PMF, PDF, and CDF."""),

    md("""## 📖 Section 1 — Concept Review

A **Random Variable X** is a function: X : Ω → ℝ (maps outcomes to numbers).

### Discrete vs Continuous
| | **Discrete** | **Continuous** |
|--|--|--|
| Values | Countable (0,1,2,3,...) | Uncountable interval |
| Description | **PMF** P(X=x) | **PDF** f(x) |
| Cumulative | CDF F(x) = P(X ≤ x) | CDF F(x) = ∫f(t)dt |
| Example | Number of goals | Height, weight, time |

### PMF (Probability Mass Function)
$$P(X = x) \\geq 0 \\quad \\text{and} \\quad \\sum_x P(X=x) = 1$$

### PDF (Probability Density Function)
$$f(x) \\geq 0 \\quad \\text{and} \\quad \\int_{-\\infty}^{\\infty} f(x)dx = 1$$

⚠️ For continuous RVs, P(X = exact value) = 0. We always compute P(a ≤ X ≤ b)."""),

    md("""## 🧮 Section 2 — Math Walkthrough

### Discrete Example: Die Roll
X = face value of a fair die. PMF: P(X=k) = 1/6 for k ∈ {1,2,3,4,5,6}

### CDF of die roll:
$$F(x) = P(X \\leq x) = \\frac{\\lfloor x \\rfloor}{6} \\quad \\text{for } 1 \\leq x \\leq 6$$

### Continuous Example: Uniform on [0,1]
$$f(x) = 1 \\quad \\text{for } 0 \\leq x \\leq 1$$
$$P(0.3 \\leq X \\leq 0.7) = \\int_{0.3}^{0.7} 1 \\, dx = 0.4$$"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid")
np.random.seed(42)

fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(2, 3, figure=fig)

# ── Discrete: Die Roll PMF and CDF ──
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
die_vals = np.arange(1, 7)
pmf = np.ones(6) / 6
ax1.bar(die_vals, pmf, color='#3498db', edgecolor='white', lw=2)
ax1.set_title('🎲 Die Roll — PMF', fontweight='bold')
ax1.set_xlabel('X'); ax1.set_ylabel('P(X=x)')
ax1.set_ylim(0, 0.25)

cdf = np.cumsum(pmf)
ax2.step(die_vals, cdf, where='post', color='#3498db', lw=2.5)
ax2.scatter(die_vals, cdf, color='#3498db', s=80, zorder=5)
ax2.set_title('Die Roll — CDF', fontweight='bold')
ax2.set_xlabel('X'); ax2.set_ylabel('F(x) = P(X≤x)')

# ── Continuous: Normal PDF and CDF ──
ax3 = fig.add_subplot(gs[0, 1])
ax4 = fig.add_subplot(gs[1, 1])
x = np.linspace(-4, 4, 300)
pdf = stats.norm.pdf(x)
cdf_norm = stats.norm.cdf(x)

ax3.plot(x, pdf, color='#e74c3c', lw=3)
ax3.fill_between(x, pdf, where=(x >= -1) & (x <= 1), alpha=0.3, color='#e74c3c',
                 label='P(-1 ≤ X ≤ 1) = 68.3%')
ax3.set_title('📊 Normal — PDF', fontweight='bold')
ax3.set_xlabel('X'); ax3.set_ylabel('f(x)')
ax3.legend(fontsize=8)

ax4.plot(x, cdf_norm, color='#e74c3c', lw=3)
ax4.axhline(0.5, color='gray', linestyle='--', lw=1)
ax4.set_title('Normal — CDF', fontweight='bold')
ax4.set_xlabel('X'); ax4.set_ylabel('F(x) = P(X≤x)')

# ── Poisson: discrete, for counts ──
ax5 = fig.add_subplot(gs[0, 2])
ax6 = fig.add_subplot(gs[1, 2])
poisson = stats.poisson(mu=3)
k = np.arange(0, 13)
ax5.bar(k, poisson.pmf(k), color='#27ae60', edgecolor='white', lw=1.5)
ax5.set_title('🔢 Poisson(λ=3) — PMF', fontweight='bold')
ax5.set_xlabel('k'); ax5.set_ylabel('P(X=k)')

ax6.step(k, poisson.cdf(k), where='post', color='#27ae60', lw=2.5)
ax6.set_title('Poisson — CDF', fontweight='bold')
ax6.set_xlabel('k'); ax6.set_ylabel('F(k)')

plt.suptitle("PMF vs PDF vs CDF: Discrete and Continuous Random Variables", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch06_rv_overview.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## 🔬 Section 3 — Simulation: Build PMF and PDF from data"""),

    code("""# Simulate and recover the distribution
np.random.seed(42)

# Discrete: count of emails per hour (Poisson)
lambda_true = 5
email_counts = np.random.poisson(lambda_true, size=1000)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Empirical PMF vs Theoretical
k = np.arange(0, 16)
empirical_pmf = [(email_counts == ki).mean() for ki in k]
theoretical_pmf = stats.poisson.pmf(k, lambda_true)

axes[0].bar(k - 0.2, empirical_pmf, 0.4, label='Empirical', color='#3498db', alpha=0.7)
axes[0].bar(k + 0.2, theoretical_pmf, 0.4, label='Theoretical', color='#e74c3c', alpha=0.7)
axes[0].set_title(f'📧 Emails/Hour: Empirical vs Poisson(λ={lambda_true})', fontweight='bold')
axes[0].set_xlabel('Count'); axes[0].set_ylabel('Probability')
axes[0].legend()

# Continuous: height data (Normal)
heights = np.random.normal(170, 10, 500)
axes[1].hist(heights, bins=30, density=True, alpha=0.6, color='#3498db', label='Data (n=500)')
x = np.linspace(135, 205, 200)
axes[1].plot(x, stats.norm.pdf(x, 170, 10), color='#e74c3c', lw=3, label='Normal(170,10)')
axes[1].set_title('📏 Heights: Histogram vs PDF', fontweight='bold')
axes[1].set_xlabel('Height (cm)'); axes[1].set_ylabel('Density')
axes[1].legend()

plt.tight_layout()
plt.savefig('ch06_simulation.png', dpi=150, bbox_inches='tight')
plt.show()

print("Key observations:")
print(f"  Max empirical PMF at k={np.argmax(empirical_pmf)}, theoretical at k={np.argmax(theoretical_pmf)}")
print(f"  Heights: mean={heights.mean():.1f}, std={heights.std():.1f} (true: 170, 10)")"""),

    md("""## 📂 Section 5 — Real Exercise: CDF for Decision Making

Use the CDF to answer: "What fraction of students score below 75?"
"""),

    code("""# Exam scores: use CDF to answer probability questions
np.random.seed(42)
exam_scores = np.random.normal(68, 12, 500)
exam_scores = np.clip(exam_scores, 0, 100)

# Fit a normal distribution
mu, sigma = exam_scores.mean(), exam_scores.std()
dist = stats.norm(mu, sigma)

questions = [
    ("P(score < 75)",   dist.cdf(75)),
    ("P(score > 80)",   1 - dist.cdf(80)),
    ("P(60 < score < 80)", dist.cdf(80) - dist.cdf(60)),
    ("Score at 90th percentile", dist.ppf(0.90)),
]

print("📝 Exam Score Analysis (Normal distribution fit)")
print(f"  Mean = {mu:.1f}, Std = {sigma:.1f}")
print()
for q, ans in questions:
    print(f"  {q} = {ans:.3f}")

x = np.linspace(30, 105, 300)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.hist(exam_scores, bins=30, density=True, alpha=0.5, color='#3498db', label='Scores')
ax1.plot(x, dist.pdf(x), 'r-', lw=3, label=f'N({mu:.0f},{sigma:.0f})')
ax1.axvline(75, color='green', linestyle='--', lw=2, label='Score=75')
ax1.fill_between(x, dist.pdf(x), where=(x < 75), alpha=0.2, color='green')
ax1.set_title('PDF: Shaded area = P(score < 75)', fontweight='bold')
ax1.legend(fontsize=8)

ax2.plot(x, dist.cdf(x), 'r-', lw=3)
ax2.axvline(75, color='green', linestyle='--', lw=2)
ax2.axhline(dist.cdf(75), color='green', linestyle=':', lw=2)
ax2.scatter([75], [dist.cdf(75)], s=100, color='green', zorder=5)
ax2.set_title('CDF: F(75) = P(score ≤ 75)', fontweight='bold')
ax2.set_xlabel('Score'); ax2.set_ylabel('F(x)')
plt.tight_layout()
plt.savefig('ch06_exam_scores.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** X ~ Poisson(λ=4). Find P(X=2), P(X≤3), P(X>5).
**P2:** X ~ N(100, 15). Find P(X > 130), P(85 < X < 115), the 95th percentile.
**P3:** Why is P(X = 1.5) = 0 for a continuous random variable?

<details><summary>💡 Solutions</summary>

**P1:** P(X=2) = e⁻⁴·4²/2! ≈ 0.147, P(X≤3) ≈ 0.433, P(X>5) ≈ 0.215

**P2:** P(X>130) = P(Z>2) ≈ 0.023, P(85<X<115) ≈ 0.683, 95th pct = 100+1.645×15 ≈ 124.7

**P3:** Continuous distributions have infinitely many possible values — any single point has zero "width" and thus zero probability. Only intervals have positive probability.
</details>"""),

    code("""# Solutions
print("P1: Poisson(λ=4)")
print(f"  P(X=2)  = {stats.poisson.pmf(2, 4):.4f}")
print(f"  P(X≤3)  = {stats.poisson.cdf(3, 4):.4f}")
print(f"  P(X>5)  = {1 - stats.poisson.cdf(5, 4):.4f}")
print()
print("P2: Normal(100, 15)")
print(f"  P(X>130)       = {1 - stats.norm.cdf(130, 100, 15):.4f}")
print(f"  P(85<X<115)    = {stats.norm.cdf(115,100,15) - stats.norm.cdf(85,100,15):.4f}")
print(f"  95th percentile = {stats.norm.ppf(0.95, 100, 15):.2f}")"""),

    md("## 🎯 Recap\n1. RVs map outcomes to numbers — discrete (PMF) or continuous (PDF).\n2. CDF tells you P(X ≤ x) — use it to answer real questions.\n3. For continuous RVs, P(X = exact value) = 0; only intervals have probability.\n\n**Next:** [Chapter 7 — Expected Value & Variance]"),
])
save(ch06, "06_random_variables.ipynb")


# ─── Chapter 7: Expected Value & Variance ───────────────────────────────────
ch07 = nb([
    md("""# 📊 Chapter 7: Expected Value & Variance
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** A casino game: roll a die, win $10 on 6, lose $2 otherwise. Should you play?
> Expected value says: play 1000 times and you'll lose money, guaranteed (in the long run).

**🎯 Objectives:** Compute E[X] and Var(X), understand what they represent, apply to decisions."""),

    md("""## 📖 Section 1 — Concept Review

### Expected Value E[X]
The **long-run average** value of a random variable over many trials.

$$E[X] = \\sum_x x \\cdot P(X=x) \\quad \\text{(discrete)}$$
$$E[X] = \\int_{-\\infty}^{\\infty} x \\cdot f(x) \\, dx \\quad \\text{(continuous)}$$

### Variance Var(X)
How **spread out** the values are around the mean.
$$\\text{Var}(X) = E[(X - \\mu)^2] = E[X^2] - (E[X])^2$$

### Standard Deviation σ
$$\\sigma = \\sqrt{\\text{Var}(X)}$$
Same units as X — much more interpretable than variance.

### Key Properties
- $E[aX + b] = aE[X] + b$ (linearity)
- $\\text{Var}(aX + b) = a^2 \\text{Var}(X)$
- $E[X + Y] = E[X] + E[Y]$ (always!)
- $\\text{Var}(X + Y) = \\text{Var}(X) + \\text{Var}(Y)$ only if independent"""),

    md("""## 🧮 Section 2 — Math Walkthrough

### Casino Die Game
- Roll a fair die: win $10 on 6, lose $2 otherwise.

$$E[\\text{profit}] = 10 \\cdot P(6) + (-2) \\cdot P(\\text{not 6})$$
$$= 10 \\cdot \\frac{1}{6} + (-2) \\cdot \\frac{5}{6} = \\frac{10 - 10}{6} = 0$$

This is a **fair game** — neither player has an advantage!

### Insurance Example
You pay $100/year for car insurance.
Without insurance: 1% chance of $8000 loss. Is insurance worth it?

- E[loss without insurance] = 0.01 × 8000 = **$80**
- Cost of insurance = **$100**
- E[loss with insurance] = $100 (certain)

Insurance costs more than expected loss — but reduces **variance** (uncertainty).
This is why risk-averse people buy insurance: they pay to reduce variance."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Casino Game Simulation ──
n_games = 50_000
rolls = np.random.randint(1, 7, n_games)
payoffs = np.where(rolls == 6, 10, -2)

running_avg = np.cumsum(payoffs) / np.arange(1, n_games + 1)
theoretical_ev = 10 * (1/6) + (-2) * (5/6)

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

axes[0].plot(running_avg, color='#3498db', lw=1.5, alpha=0.9, label='Running average profit')
axes[0].axhline(theoretical_ev, color='#e74c3c', lw=2, linestyle='--',
                label=f'E[profit] = {theoretical_ev:.2f}')
axes[0].set_xlabel('Number of Games Played')
axes[0].set_ylabel('Average Profit per Game ($)')
axes[0].set_title(f'🎰 Casino Die Game: Convergence to E[X] = {theoretical_ev:.2f}', fontweight='bold')
axes[0].legend()
axes[0].set_ylim(-5, 5)

# Compare high vs low variance investments
low_var  = np.random.normal(0.05, 0.05, 1000)   # bonds
high_var = np.random.normal(0.08, 0.25, 1000)   # stocks

axes[1].hist(low_var * 100, bins=40, alpha=0.6, color='#27ae60', density=True, label=f'Bonds: E={5:.0f}%, σ={5:.0f}%')
axes[1].hist(high_var * 100, bins=40, alpha=0.5, color='#e74c3c', density=True, label=f'Stocks: E={8:.0f}%, σ={25:.0f}%')
axes[1].axvline(5, color='#27ae60', lw=2, linestyle='--')
axes[1].axvline(8, color='#e74c3c', lw=2, linestyle='--')
axes[1].set_xlabel('Annual Return (%)')
axes[1].set_ylabel('Density')
axes[1].set_title('📈 Same(ish) E[X], Very Different Variance', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.savefig('ch07_ev_variance.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"🎰 Casino game: E[profit] = {theoretical_ev:.2f} (simulated: {payoffs.mean():.3f})")
print(f"🎰 Casino game: Var[profit] = {payoffs.var():.2f}, Std = {payoffs.std():.2f}")"""),

    code("""# E[X] and Var(X) for common distributions
distributions = {
    'Bernoulli(p=0.3)':  {'dist': stats.bernoulli(0.3),  'theoretical': ('p=0.3', 'p(1-p)=0.21')},
    'Binomial(10,0.3)':  {'dist': stats.binom(10, 0.3),  'theoretical': ('np=3',  'np(1-p)=2.1')},
    'Poisson(λ=4)':      {'dist': stats.poisson(4),       'theoretical': ('λ=4',   'λ=4')},
    'Normal(5,2)':       {'dist': stats.norm(5, 2),       'theoretical': ('μ=5',   'σ²=4')},
    'Exponential(λ=1)':  {'dist': stats.expon(scale=1),   'theoretical': ('1/λ=1', '1/λ²=1')},
}

print(f"{'Distribution':<20} {'E[X] sim':>10} {'E[X] theory':>15} {'Var(X) sim':>12}")
print("-" * 60)
for name, info in distributions.items():
    samples = info['dist'].rvs(10_000)
    ev_sim = samples.mean()
    var_sim = samples.var()
    ev_th, var_th = info['theoretical']
    print(f"{name:<20} {ev_sim:>10.3f} {ev_th:>15} {var_sim:>12.3f}")"""),

    md("""## 🔬 Section 3 — Simulation: Linearity of Expectation"""),

    code("""# Verify E[aX+b] = aE[X]+b and Var(aX+b) = a²Var(X)
np.random.seed(42)
X = np.random.normal(5, 2, 100_000)
a, b = 3, 10
Y = a * X + b

print("Linearity of Expectation & Variance:")
print(f"  E[X]     = {X.mean():.4f}  (theory: 5)")
print(f"  E[Y=3X+10] = {Y.mean():.4f}  (theory: {a*5+b})")
print()
print(f"  Var[X]   = {X.var():.4f}  (theory: 4)")
print(f"  Var[Y]   = {Y.var():.4f}  (theory: {a**2 * 4} = 3²×4)")
print()

# Sum of RVs
X1 = np.random.normal(3, 1, 100_000)
X2 = np.random.normal(7, 2, 100_000)
S  = X1 + X2
print(f"  E[X1+X2] = {S.mean():.4f}  (theory: {3+7}  = E[X1]+E[X2])")
print(f"  Var[X1+X2] = {S.var():.4f}  (theory: {1**2 + 2**2} = Var[X1]+Var[X2] since independent)")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** You play a lottery: pay $2, win $100 with P=0.01, $0 otherwise. What is E[profit]? Should you play?
**P2:** X ~ Binomial(n=20, p=0.4). Find E[X] and Var(X).
**P3:** You have 2 investments: A has E=$1000, σ=$200; B has E=$1000, σ=$500. Which do you prefer and why?

<details><summary>💡 Solutions</summary>

**P1:** E[profit] = 100×0.01 + 0×0.99 − 2 = 1 − 2 = **−$1**. No, expected to lose $1 per play.

**P2:** E[X] = np = 20×0.4 = **8**, Var(X) = np(1-p) = 20×0.4×0.6 = **4.8**

**P3:** Same expected return → prefer A (lower variance = lower risk). Unless you need a big payoff, lower variance is better.
</details>"""),

    code("""# P1 solution
ev_lottery = 100 * 0.01 + 0 * 0.99 - 2
print(f"Lottery E[profit] = {ev_lottery}")
# P2 solution
print(f"Binomial(20,0.4): E={20*0.4}, Var={20*0.4*0.6}")"""),

    md("## 🎯 Recap\n1. **E[X]** is the long-run average — it's where the distribution 'balances'.\n2. **Var(X)** measures spread — high variance = more uncertainty.\n3. **Linearity of expectation** always holds, even for dependent variables.\n\n**Next:** [Chapter 8 — Common Distributions Part 1: Bernoulli, Binomial, Geometric]"),
])
save(ch07, "07_expected_value_and_variance.ipynb")


# ─── Chapter 8: Distributions Part 1 ───────────────────────────────────────
ch08 = nb([
    md("""# 📊 Chapter 8: Common Distributions Part 1
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** 70% free throw shooter, 10 attempts — what's the probability of exactly 7 makes?
> There's a distribution *designed* for this exact question.

**🎯 Objectives:** Understand and apply Bernoulli, Binomial, and Geometric distributions."""),

    md("""## 📖 Section 1 — Concept Review

### When to use which distribution?
```
Is it a single yes/no trial? → Bernoulli
How many successes in n trials? → Binomial
How many trials until first success? → Geometric
```

### Bernoulli(p)
Single binary trial. X = 1 (success) or 0 (failure).
- PMF: P(X=1) = p, P(X=0) = 1-p
- E[X] = p, Var(X) = p(1-p)

### Binomial(n, p)
Count of successes in **n independent** Bernoulli(p) trials.
$$P(X=k) = \\binom{n}{k} p^k (1-p)^{n-k}$$
- E[X] = np, Var(X) = np(1-p)

### Geometric(p)
Number of trials until the **first success**.
$$P(X=k) = (1-p)^{k-1} p \\quad k = 1, 2, 3, \\ldots$$
- E[X] = 1/p, Var(X) = (1-p)/p²
- **Memoryless property:** P(X > m+n | X > m) = P(X > n)"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set_theme(style="whitegrid")
np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# ── Bernoulli ──
p = 0.7
b_vals = [0, 1]
b_pmf  = [1-p, p]
axes[0,0].bar(b_vals, b_pmf, color=['#e74c3c','#27ae60'], width=0.4, edgecolor='white', lw=2)
axes[0,0].set_title(f'Bernoulli(p={p})', fontweight='bold')
axes[0,0].set_xticks([0,1]); axes[0,0].set_xticklabels(['Fail','Success'])
axes[0,0].set_ylabel('P(X=x)')
axes[0,0].text(0, 0.35, f'{1-p}', ha='center', fontsize=12, fontweight='bold')
axes[0,0].text(1, 0.75, f'{p}', ha='center', fontsize=12, fontweight='bold')

# ── Binomial: different n ──
k = np.arange(0, 21)
for ax, (n, p, color) in zip([axes[0,1], axes[0,2]],
    [(10, 0.7, '#3498db'), (20, 0.4, '#9b59b6')]):
    pmf = stats.binom.pmf(k[:n+1], n, p)
    ax.bar(k[:n+1], pmf, color=color, edgecolor='white', lw=1.5)
    ax.axvline(n*p, color='red', linestyle='--', lw=2, label=f'E[X]={n*p}')
    ax.set_title(f'Binomial(n={n}, p={p})', fontweight='bold')
    ax.set_xlabel('k (number of successes)'); ax.set_ylabel('P(X=k)')
    ax.legend()

# ── Geometric ──
k_geom = np.arange(1, 20)
for ax, (p, color) in zip([axes[1,0], axes[1,1]],
    [(0.3, '#e74c3c'), (0.7, '#27ae60')]):
    pmf = stats.geom.pmf(k_geom, p)
    ax.bar(k_geom, pmf, color=color, edgecolor='white', lw=1.5)
    ax.axvline(1/p, color='black', linestyle='--', lw=2, label=f'E[X]=1/p={1/p:.1f}')
    ax.set_title(f'Geometric(p={p})', fontweight='bold')
    ax.set_xlabel('Trial of first success'); ax.set_ylabel('P(X=k)')
    ax.legend()

# ── Comparison: different p for Binomial(10, p) ──
for p, color in [(0.2,'#3498db'), (0.5,'#e74c3c'), (0.8,'#27ae60')]:
    axes[1,2].plot(range(11), stats.binom.pmf(range(11), 10, p), 'o-',
                   color=color, lw=2, markersize=6, label=f'p={p}')
axes[1,2].set_title('Binomial(10,p): Effect of p', fontweight='bold')
axes[1,2].set_xlabel('k'); axes[1,2].set_ylabel('P(X=k)')
axes[1,2].legend()

plt.suptitle("Bernoulli, Binomial, Geometric Distributions", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('ch08_distributions_p1.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Real application: Free throw shooting
np.random.seed(42)
n_shots = 10
p_make  = 0.70

# Simulate 10,000 game nights (10 free throws each)
simulated = np.random.binomial(n_shots, p_make, 10_000)
k = np.arange(0, 11)
theoretical = stats.binom.pmf(k, n_shots, p_make)

print("🏀 Free Throw Analysis: 70% shooter, 10 attempts")
print(f"{'k':>4} {'Simulated':>12} {'Theoretical':>14}")
print("-" * 32)
for ki in k:
    sim_p = (simulated == ki).mean()
    th_p  = theoretical[ki]
    print(f"{ki:>4} {sim_p:>12.4f} {th_p:>14.4f}")

print(f"\nE[makes] = {simulated.mean():.2f} (theory: {n_shots*p_make})")
print(f"Std[makes] = {simulated.std():.2f} (theory: {(n_shots*p_make*(1-p_make))**0.5:.2f})")
print(f"\nP(exactly 7 makes) = {stats.binom.pmf(7, 10, 0.7):.4f}")
print(f"P(7 or more makes) = {1 - stats.binom.cdf(6, 10, 0.7):.4f}")"""),

    md("""## 🔬 Section 3 — Geometric: The Memoryless Property

The Geometric distribution has a unique property: the past doesn't matter."""),

    code("""# Geometric: Memoryless property
np.random.seed(42)
p = 0.2  # 20% chance of success per trial (e.g., getting a job offer)

# Simulate "number of interviews until first offer"
interviews = np.random.geometric(p, 100_000)

print(f"🎯 Job Interview Simulation (P(offer/interview) = {p})")
print(f"  Expected interviews until offer: {1/p:.1f}")
print(f"  Simulated average: {interviews.mean():.2f}")
print()

# Memoryless property: P(X > 10 | X > 5) should = P(X > 5)
p_x_gt_10_given_gt_5 = (interviews > 10)[interviews > 5].mean()
p_x_gt_5 = (interviews > 5).mean()

print("Memoryless Property Verification:")
print(f"  P(X > 10 | X > 5) = {p_x_gt_10_given_gt_5:.4f}")
print(f"  P(X > 5)           = {p_x_gt_5:.4f}")
print(f"  Equal? {abs(p_x_gt_10_given_gt_5 - p_x_gt_5) < 0.01}")
print()
print("💡 Even if you've had 5 failed interviews, you're no 'closer' to success!")
print("   Each interview is a fresh 20% chance. Past failures don't help.")

fig, ax = plt.subplots(figsize=(9, 4))
k = np.arange(1, 30)
ax.bar(k, stats.geom.pmf(k, p), color='#3498db', edgecolor='white', lw=1.5, label='Theoretical PMF')
ax.hist(interviews[interviews <= 30], bins=range(1, 31), density=True,
        alpha=0.4, color='#e74c3c', label='Simulated')
ax.axvline(1/p, color='black', linestyle='--', lw=2, label=f'E[X] = {1/p:.0f}')
ax.set_title(f'🎯 Geometric(p={p}): Interviews Until First Offer', fontweight='bold')
ax.set_xlabel('Number of Interviews'); ax.set_ylabel('Probability')
ax.legend()
plt.tight_layout()
plt.savefig('ch08_geometric.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** A fair coin is flipped 8 times. P(exactly 5 heads)?
**P2:** You roll a die until you get a 6. What is E[rolls]? P(need more than 10 rolls)?
**P3:** Manufacturing: each item has 3% defect rate. A batch of 50 is inspected.
  a) P(no defects), b) P(2 or fewer defects), c) E[defects]

<details><summary>💡 Solutions</summary>

**P1:** Binomial(8, 0.5): C(8,5)×0.5⁸ = 56/256 ≈ **0.219**

**P2:** Geometric(1/6): E = 6. P(X>10) = (5/6)^10 ≈ **0.162**

**P3:** Binomial(50, 0.03): a) 0.97^50 ≈ **0.218**, b) CDF(2) ≈ **0.812**, c) np = **1.5**
</details>"""),

    code("""from scipy.special import comb
# Solutions
print("P1:", stats.binom.pmf(5, 8, 0.5))
print("P2 E[X]:", 6, "  P(X>10):", stats.geom.sf(10, 1/6))
print("P3a:", stats.binom.pmf(0, 50, 0.03))
print("P3b:", stats.binom.cdf(2, 50, 0.03))
print("P3c:", 50*0.03)"""),

    md("## 🎯 Recap\n1. **Bernoulli** = one coin flip (yes/no).\n2. **Binomial** = count successes in n independent flips.\n3. **Geometric** = wait time until first success; memoryless.\n\n**Next:** [Chapter 9 — Distributions Part 2: Poisson, Uniform, Exponential]"),
])
save(ch08, "08_distributions_part1.ipynb")


# ─── Chapter 9: Distributions Part 2 ───────────────────────────────────────
ch09 = nb([
    md("""# 📊 Chapter 9: Common Distributions Part 2
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** How many customers walk into a store in an hour? How long until the next bus arrives?
> There are distributions *designed* for these exact questions.

**🎯 Objectives:** Understand and apply Poisson, Uniform, and Exponential distributions."""),

    md("""## 📖 Section 1 — Concept Review

### Poisson(λ) — For COUNTS of rare events in a fixed interval
$$P(X=k) = \\frac{e^{-\\lambda} \\lambda^k}{k!} \\quad k = 0,1,2,\\ldots$$
- E[X] = λ, Var(X) = λ (mean = variance!)
- Use when: counting arrivals, defects, events per time unit

### Uniform(a,b) — All values equally likely in [a,b]
$$f(x) = \\frac{1}{b-a} \\quad a \\leq x \\leq b$$
- E[X] = (a+b)/2, Var(X) = (b-a)²/12

### Exponential(λ) — Waiting TIME between Poisson events
$$f(x) = \\lambda e^{-\\lambda x} \\quad x \\geq 0$$
- E[X] = 1/λ, Var(X) = 1/λ²
- **Memoryless:** P(X > s+t | X > s) = P(X > t)
- If events arrive at rate λ, waiting time ~ Exp(λ)

### The Poisson-Exponential Connection
If customers arrive at rate λ per hour (Poisson), then the time BETWEEN arrivals ~ Exponential(λ)."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set_theme(style="whitegrid")
np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# ── Poisson: different λ ──
k = np.arange(0, 25)
for ax, (lam, color) in zip([axes[0,0], axes[0,1]],
    [(2, '#3498db'), (8, '#e74c3c')]):
    ax.bar(k, stats.poisson.pmf(k, lam), color=color, edgecolor='white', lw=1.5)
    ax.axvline(lam, color='black', linestyle='--', lw=2, label=f'E[X]=λ={lam}')
    ax.set_title(f'Poisson(λ={lam})', fontweight='bold')
    ax.set_xlabel('k'); ax.set_ylabel('P(X=k)')
    ax.legend()

# ── Uniform ──
x = np.linspace(-0.5, 5.5, 300)
for ax, (a, b, color) in zip([axes[0,2]],
    [(0, 5, '#27ae60')]):
    ax.plot(x, stats.uniform.pdf(x, a, b-a), color=color, lw=3)
    ax.fill_between(x, stats.uniform.pdf(x, a, b-a), alpha=0.3, color=color)
    ax.axvline((a+b)/2, color='red', linestyle='--', lw=2, label=f'E[X]={(a+b)/2}')
    ax.set_title(f'Uniform({a},{b})', fontweight='bold')
    ax.set_xlabel('x'); ax.set_ylabel('f(x)')
    ax.legend()
    ax.set_ylim(0, 0.5)

# ── Exponential ──
x_exp = np.linspace(0, 10, 300)
for ax, (lam, color) in zip([axes[1,0], axes[1,1]],
    [(0.5, '#9b59b6'), (2, '#e67e22')]):
    ax.plot(x_exp, stats.expon.pdf(x_exp, scale=1/lam), color=color, lw=3)
    ax.fill_between(x_exp, stats.expon.pdf(x_exp, scale=1/lam), alpha=0.3, color=color)
    ax.axvline(1/lam, color='black', linestyle='--', lw=2, label=f'E[X]=1/λ={1/lam:.1f}')
    ax.set_title(f'Exponential(λ={lam})', fontweight='bold')
    ax.set_xlabel('x (time)'); ax.set_ylabel('f(x)')
    ax.legend()

# ── All three together: comparison ──
x_all = np.linspace(0, 15, 300)
axes[1,2].plot(x_all, stats.norm.pdf(x_all, 7, 2),    label='Normal(7,2)', lw=2.5)
axes[1,2].plot(x_all, stats.expon.pdf(x_all, scale=3), label='Exponential(λ=1/3)', lw=2.5)
axes[1,2].plot(x_all, stats.uniform.pdf(x_all, 0, 14), label='Uniform(0,14)', lw=2.5)
axes[1,2].set_title('Shape Comparison: All with E[X]≈7', fontweight='bold')
axes[1,2].set_xlabel('x'); axes[1,2].set_ylabel('f(x)')
axes[1,2].legend(fontsize=8)

plt.suptitle("Poisson, Uniform, Exponential Distributions", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('ch09_distributions_p2.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Poisson-Exponential connection: bus arrivals
np.random.seed(42)
lambda_rate = 3  # buses per hour

# Simulate 1 hour: count arrivals (Poisson)
# Then simulate inter-arrival times (Exponential)
n_hours = 10_000

# Count method (Poisson)
counts = np.random.poisson(lambda_rate, n_hours)

# Time method (Exponential inter-arrivals)
inter_arrival_times = np.random.exponential(scale=1/lambda_rate, size=100_000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

k = np.arange(0, 12)
ax1.bar(k, [(counts == ki).mean() for ki in k], color='#3498db', edgecolor='white', label='Simulated')
ax1.plot(k, stats.poisson.pmf(k, lambda_rate), 'ro-', markersize=6, lw=2, label=f'Poisson(λ={lambda_rate})')
ax1.set_title('🚌 Buses per Hour: Poisson', fontweight='bold')
ax1.set_xlabel('Buses per hour'); ax1.set_ylabel('Probability')
ax1.legend()

x = np.linspace(0, 3, 200)
ax2.hist(inter_arrival_times, bins=50, density=True, alpha=0.5, color='#e74c3c', label='Simulated')
ax2.plot(x, stats.expon.pdf(x, scale=1/lambda_rate), 'b-', lw=3,
         label=f'Exponential(λ={lambda_rate})')
ax2.axvline(1/lambda_rate, color='black', linestyle='--', lw=2,
            label=f'E[wait] = {1/lambda_rate:.2f} hr = 20 min')
ax2.set_title('🚌 Time Between Buses: Exponential', fontweight='bold')
ax2.set_xlabel('Hours between buses'); ax2.set_ylabel('Density')
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('ch09_poisson_exp_connection.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Avg buses/hour: {counts.mean():.2f} (theory: {lambda_rate})")
print(f"Avg inter-arrival: {inter_arrival_times.mean():.3f} hr (theory: {1/lambda_rate:.3f} hr)")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Calls arrive at a call center at 10/hour. P(exactly 8 calls in an hour)?
**P2:** A server processes requests in U(0.5, 2.5) seconds. E[time]? P(time < 1 sec)?
**P3:** A machine fails on average every 200 hours (Exponential). P(survives 100 hours)?

<details><summary>💡 Solutions</summary>

**P1:** Poisson(10): P(X=8) = e⁻¹⁰·10⁸/8! ≈ **0.113**

**P2:** E = (0.5+2.5)/2 = **1.5 sec**, P(X<1) = (1-0.5)/(2.5-0.5) = **0.25**

**P3:** Exponential(λ=1/200): P(X>100) = e^(-100/200) = e^(-0.5) ≈ **0.607**
</details>"""),

    code("""# Solutions
print("P1:", stats.poisson.pmf(8, 10))
print("P2 E[X]:", (0.5+2.5)/2, "  P(X<1):", stats.uniform.cdf(1, 0.5, 2.0))
print("P3:", stats.expon.sf(100, scale=200))"""),

    md("## 🎯 Recap\n1. **Poisson**: counts of events in fixed interval; mean = variance = λ.\n2. **Uniform**: all values equally likely; maximum entropy for a bounded range.\n3. **Exponential**: waiting times; memoryless; connected to Poisson arrivals.\n\n**Next:** [Chapter 10 — The Normal Distribution]"),
])
save(ch09, "09_distributions_part2.ipynb")


# ─── Chapter 10: Normal Distribution ────────────────────────────────────────
ch10 = nb([
    md("""# 📊 Chapter 10: The Normal Distribution
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** Heights, exam scores, measurement errors, blood pressure — they all follow a bell curve.
> But WHY? The answer connects to the Central Limit Theorem (next chapter).

**🎯 Objectives:** Understand the Normal distribution, Z-scores, the empirical rule, and standardization."""),

    md("""## 📖 Section 1 — Concept Review

### The Normal Distribution N(μ, σ²)
$$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$

- **μ** = mean (where it's centered)
- **σ** = standard deviation (how spread out)
- Symmetric, bell-shaped, extends to ±∞

### The Empirical Rule (68-95-99.7)
```
μ ± 1σ   → 68.3% of data
μ ± 2σ   → 95.4% of data
μ ± 3σ   → 99.7% of data
```

### Z-Score: Standardization
$$Z = \\frac{X - \\mu}{\\sigma} \\quad \\Rightarrow \\quad Z \\sim N(0,1)$$

Z-scores let you compare values from **different** normal distributions.
"How many standard deviations from the mean?"

### Standard Normal N(0,1)
Once standardized, use Z-tables or `scipy.stats.norm.cdf()` to find probabilities."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Empirical Rule ──
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

mu, sigma = 0, 1
x = np.linspace(-4, 4, 1000)
y = stats.norm.pdf(x, mu, sigma)

ax = axes[0]
ax.plot(x, y, 'k-', lw=3)
regions = [
    ((-1, 1),   0.683, '#3498db', '±1σ: 68.3%'),
    ((-2, -1),  None,  '#e74c3c', '±2σ: 95.4%'),
    ((1,  2),   None,  '#e74c3c', None),
    ((-3, -2),  None,  '#27ae60', '±3σ: 99.7%'),
    ((2,  3),   None,  '#27ae60', None),
]
for (lo, hi), pct, color, label in regions:
    mask = (x >= lo) & (x <= hi)
    ax.fill_between(x, y, where=mask, alpha=0.5, color=color, label=label)
ax.set_title('The Empirical Rule: 68-95-99.7', fontweight='bold')
ax.set_xlabel('Z-score (standard deviations from mean)')
ax.set_ylabel('Density')
handles, labels = ax.get_legend_handles_labels()
ax.legend([h for h, l in zip(handles, labels) if l], [l for l in labels if l], fontsize=9)

# ── Effect of μ and σ ──
ax2 = axes[1]
for mu_v, sigma_v, color, label in [
    (0,  1,   '#3498db', 'N(0,1)'),
    (2,  1,   '#e74c3c', 'N(2,1)'),
    (0,  2,   '#27ae60', 'N(0,2)'),
    (-1, 0.5, '#9b59b6', 'N(-1,0.5)'),
]:
    x_v = np.linspace(-6, 6, 300)
    ax2.plot(x_v, stats.norm.pdf(x_v, mu_v, sigma_v), lw=2.5, color=color, label=label)
ax2.set_title('Effect of μ and σ on Normal Shape', fontweight='bold')
ax2.set_xlabel('x'); ax2.set_ylabel('f(x)')
ax2.legend()

plt.tight_layout()
plt.savefig('ch10_normal.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Z-scores in practice: SAT scores
mu_sat, sigma_sat = 1050, 210

scores_of_interest = [900, 1050, 1260, 1470]
print("📝 SAT Score Analysis: N(1050, 210)")
print(f"{'Score':>8} {'Z-score':>9} {'Percentile':>12} {'Better than...':>16}")
print("-" * 48)
for score in scores_of_interest:
    z = (score - mu_sat) / sigma_sat
    pct = stats.norm.cdf(z) * 100
    print(f"{score:>8} {z:>9.2f} {pct:>11.1f}% {pct:>14.1f}%")

print()
print("Questions:")
print(f"  P(score > 1260) = {1 - stats.norm.cdf(1260, mu_sat, sigma_sat):.4f}")
print(f"  P(900 < score < 1200) = {stats.norm.cdf(1200, mu_sat, sigma_sat) - stats.norm.cdf(900, mu_sat, sigma_sat):.4f}")
print(f"  Top 10% score ≥ {stats.norm.ppf(0.90, mu_sat, sigma_sat):.0f}")

# ── Visualize SAT distribution ──
x = np.linspace(400, 1600, 400)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, stats.norm.pdf(x, mu_sat, sigma_sat), 'b-', lw=3)
ax.fill_between(x, stats.norm.pdf(x, mu_sat, sigma_sat),
                where=(x > 1260), alpha=0.4, color='#e74c3c', label='P(score>1260)')
ax.axvline(mu_sat, color='black', linestyle='--', lw=2, label=f'Mean={mu_sat}')
ax.set_xlabel('SAT Score'); ax.set_ylabel('Density')
ax.set_title('📝 SAT Score Distribution: N(1050, 210)', fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('ch10_sat.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** X ~ N(70, 10). Find P(X < 85), P(60 < X < 80), the 25th percentile.
**P2:** Blood pressure ~ N(120, 15). P(hypertension if threshold is 140)?
**P3:** Standardize: X=95, μ=80, σ=12. What is Z? What percentile?

<details><summary>💡 Solutions</summary>

**P1:** P(X<85) = Φ(1.5) ≈ **0.933**, P(60<X<80) = Φ(1)-Φ(-1) ≈ **0.683**, 25th pct = 70-0.674×10 ≈ **63.3**

**P2:** P(X>140) = 1-Φ(1.33) ≈ **0.092**

**P3:** Z = (95-80)/12 = **1.25**, percentile = Φ(1.25) ≈ **89.4%**
</details>"""),

    code("""print("P1:", stats.norm.cdf(85, 70, 10), stats.norm.cdf(80,70,10)-stats.norm.cdf(60,70,10), stats.norm.ppf(0.25,70,10))
print("P2:", 1-stats.norm.cdf(140, 120, 15))
print("P3:", (95-80)/12, stats.norm.cdf((95-80)/12))"""),

    md("## 🎯 Recap\n1. **Normal distribution** is symmetric, bell-shaped, defined by μ and σ.\n2. **Empirical rule**: 68/95/99.7% of data within 1/2/3 standard deviations.\n3. **Z-scores** standardize to N(0,1) for probability calculations.\n\n**Next:** [Chapter 11 — Sampling & The Central Limit Theorem]"),
])
save(ch10, "10_normal_distribution.ipynb")


# ─── Chapter 11: Sampling & CLT ─────────────────────────────────────────────
ch11 = nb([
    md("""# 📊 Chapter 11: Sampling & The Central Limit Theorem
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** You can't survey all 330 million Americans. But 1,000 people is usually enough.
> The Central Limit Theorem is why — and it's perhaps the most powerful theorem in all of statistics.

**🎯 Objectives:** Understand sampling distributions, standard error, and why the CLT is so important."""),

    md("""## 📖 Section 1 — Concept Review

### The Problem
We want to know a population parameter (e.g., mean income of all Americans).
We can only observe a **sample** (e.g., 1,000 people).

### Sampling Distribution
The distribution of a **statistic** (like sample mean X̄) over many repeated samples.

### The Central Limit Theorem (CLT)
> **If X₁, X₂, ..., Xₙ are i.i.d. with mean μ and variance σ², then:**
>
> $$\\bar{X}_n = \\frac{1}{n}\\sum_{i=1}^n X_i \\xrightarrow{d} N\\left(\\mu, \\frac{\\sigma^2}{n}\\right) \\text{ as } n \\to \\infty$$

### What this means:
1. The sample mean is **approximately normally distributed** (regardless of the original distribution!)
2. Mean of sample mean = μ (unbiased estimator)
3. Std of sample mean = σ/√n (**Standard Error**)

### Standard Error
$$SE = \\frac{\\sigma}{\\sqrt{n}}$$
Doubling sample size cuts standard error by √2 ≈ 1.41."""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── CLT Demo: Sample from ANY distribution ──
fig, axes = plt.subplots(3, 4, figsize=(16, 10))

distributions = [
    ('Uniform(0,1)',    lambda n: np.random.uniform(0,1,n)),
    ('Exponential(1)', lambda n: np.random.exponential(1,n)),
    ('Bimodal',        lambda n: np.where(np.random.random(n)<0.5,
                                          np.random.normal(-2,0.5,n),
                                          np.random.normal(2,0.5,n))),
]

n_samples = [1, 5, 30, 100]

for row, (dist_name, sampler) in enumerate(distributions):
    for col, n in enumerate(n_samples):
        ax = axes[row, col]
        sample_means = [sampler(n).mean() for _ in range(3000)]
        ax.hist(sample_means, bins=40, density=True, color='#3498db', alpha=0.7, edgecolor='white')

        if n >= 5:
            mu_sm = np.mean(sample_means)
            se = np.std(sample_means)
            x = np.linspace(min(sample_means), max(sample_means), 200)
            ax.plot(x, stats.norm.pdf(x, mu_sm, se), 'r-', lw=2.5, label='Normal fit')

        if row == 0:
            ax.set_title(f'n = {n}', fontweight='bold', fontsize=11)
        if col == 0:
            ax.set_ylabel(dist_name, fontsize=9, rotation=90)
        ax.set_xlabel('')
        ax.tick_params(labelsize=7)

plt.suptitle("Central Limit Theorem: Sample Means Become Normal\\n(regardless of original distribution!)",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch11_clt.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Standard Error and Sample Size
np.random.seed(42)
true_mean = 50_000
true_std  = 15_000  # annual income distribution

sample_sizes = [10, 50, 100, 500, 1000, 5000]
n_repeats = 10_000

print("📊 Sampling Distribution of Sample Mean (Income)")
print(f"{'Sample Size n':>14} {'SE=σ/√n':>12} {'Observed SE':>12} {'95% CI Width':>14}")
print("-" * 55)

ses = []
for n in sample_sizes:
    means = [np.random.normal(true_mean, true_std, n).mean() for _ in range(n_repeats)]
    obs_se = np.std(means)
    theory_se = true_std / np.sqrt(n)
    ci_width = 2 * 1.96 * theory_se
    ses.append(theory_se)
    print(f"{n:>14} {theory_se:>12,.0f} {obs_se:>12,.0f} {ci_width:>14,.0f}")

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(sample_sizes, ses, 'bo-', markersize=8, lw=2.5, label='SE = σ/√n')
ax.plot(sample_sizes, [true_std/np.sqrt(n) for n in sample_sizes],
        'r--', lw=2, label='Theoretical SE')
ax.set_xlabel('Sample Size (n)')
ax.set_ylabel('Standard Error ($)')
ax.set_title('📏 Standard Error Decreases with Sample Size', fontweight='bold')
ax.legend()
ax.set_xscale('log')
plt.tight_layout()
plt.savefig('ch11_se.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Population: μ=100, σ=20. Sample of n=25.
What is the distribution of X̄? Find P(X̄ > 104).

**P2:** A fair die: E[X]=3.5, Var(X)=35/12. Roll n=60 dice. P(sum > 220)?

**P3:** Why can't you apply CLT to find P(a SINGLE observation X > 104)?

<details><summary>💡 Solutions</summary>

**P1:** X̄ ~ N(100, 20²/25) = N(100, 4²). P(X̄>104) = P(Z>(104-100)/4) = P(Z>1) ≈ **0.159**

**P2:** Sum = 60·X̄ ~ N(60·3.5, 60·35/12) = N(210, 175). P(Sum>220) = P(Z>(220-210)/√175) = P(Z>0.756) ≈ **0.225**

**P3:** CLT applies to AVERAGES of many observations, not individual observations. One die roll has a discrete uniform distribution, not Normal.
</details>"""),

    code("""# Solutions
se = 20 / np.sqrt(25)
print("P1:", 1 - stats.norm.cdf(104, 100, se))

mu_sum = 60 * 3.5
var_sum = 60 * 35/12
print("P2:", 1 - stats.norm.cdf(220, mu_sum, var_sum**0.5))"""),

    md("## 🎯 Recap\n1. The **CLT** says sample means approach Normal, regardless of the original distribution.\n2. **Standard Error = σ/√n** — more data → less uncertainty.\n3. CLT is the foundation of confidence intervals, hypothesis tests, and much of statistics.\n\n**Next:** [Chapter 12 — Descriptive Statistics: Summarizing Data]"),
])
save(ch11, "11_sampling_and_clt.ipynb")


# ─── Chapter 12: Descriptive Statistics ─────────────────────────────────────
ch12 = nb([
    md("""# 📊 Chapter 12: Descriptive Statistics
*Tier 1 — Foundations | All Tracks*

> **🎬 Hook:** A company reports "average salary of $85,000." Half the employees make less than $60,000.
> Both statements are technically true. Descriptive statistics tells you which story to trust.

**🎯 Objectives:** Compute and interpret measures of center, spread, shape, and outlier detection."""),

    md("""## 📖 Section 1 — Concept Review

### Measures of Center
| Measure | Formula | Best When |
|---------|---------|-----------|
| **Mean** | Σxᵢ/n | Symmetric, no outliers |
| **Median** | Middle value | Skewed data, outliers present |
| **Mode** | Most frequent | Categorical, multimodal |

### Measures of Spread
| Measure | Formula | Best When |
|---------|---------|-----------|
| **Range** | max-min | Quick overview |
| **IQR** | Q3-Q1 | Robust, outliers present |
| **Variance** | Σ(xᵢ-μ)²/n | Mathematical analysis |
| **Std Dev** | √Variance | Same units as data |

### Shape: Skewness & Kurtosis
- **Skewness > 0**: Right tail (mean > median) — income, housing prices
- **Skewness < 0**: Left tail (mean < median) — exam scores
- **Kurtosis**: How heavy the tails are (normal = 3)

### Outlier Detection: IQR Method
Outlier if: x < Q1 - 1.5×IQR  OR  x > Q3 + 1.5×IQR"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
sns.set_theme(style="whitegrid")
np.random.seed(42)

# Realistic income data (right-skewed)
incomes = np.concatenate([
    np.random.lognormal(10.8, 0.4, 950),   # typical workers
    np.random.lognormal(13, 0.5, 50),       # executives
])
incomes = np.clip(incomes, 20_000, 2_000_000)

mean_inc   = incomes.mean()
median_inc = np.median(incomes)
mode_approx = stats.mode(incomes.astype(int)//5000*5000, keepdims=True).mode[0]

print("💰 Income Distribution Analysis")
print(f"  Mean:    ${mean_inc:>10,.0f}")
print(f"  Median:  ${median_inc:>10,.0f}")
print(f"  Std Dev: ${incomes.std():>10,.0f}")
print(f"  IQR:     ${np.percentile(incomes,75) - np.percentile(incomes,25):>10,.0f}")
print(f"  Skewness:{stats.skew(incomes):>10.3f}")
print()
print(f"  👆 Mean is {mean_inc/median_inc:.1f}x the median — classic right-skew signal!")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(incomes/1000, bins=60, color='#3498db', edgecolor='white', lw=0.5)
axes[0].axvline(mean_inc/1000, color='red', lw=2.5, linestyle='--', label=f'Mean ${mean_inc/1000:.0f}k')
axes[0].axvline(median_inc/1000, color='green', lw=2.5, linestyle='-', label=f'Median ${median_inc/1000:.0f}k')
axes[0].set_title('💰 Income Distribution', fontweight='bold')
axes[0].set_xlabel('Income ($thousands)'); axes[0].set_ylabel('Count')
axes[0].legend(); axes[0].set_xlim(0, 500)

axes[1].boxplot(incomes/1000, vert=True, patch_artist=True,
                boxprops=dict(facecolor='#3498db', alpha=0.6))
axes[1].set_title('Box Plot (IQR View)', fontweight='bold')
axes[1].set_ylabel('Income ($thousands)'); axes[1].set_ylim(0, 500)

# Compare: symmetric vs skewed
sym = np.random.normal(50000, 15000, 1000)
skew_data = np.random.lognormal(10.8, 0.5, 1000)
for data, color, label in [(sym, '#3498db', 'Symmetric'), (skew_data/1000, '#e74c3c', 'Right-Skewed')]:
    axes[2].hist(data/1000 if label == 'Symmetric' else data,
                 bins=40, alpha=0.5, density=True, color=color, label=label)
axes[2].set_title('Symmetric vs Skewed: Mean≠Median', fontweight='bold')
axes[2].set_xlabel('Value (thousands)')
axes[2].legend()

plt.tight_layout()
plt.savefig('ch12_descriptive.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Five-Number Summary and Outlier Detection
np.random.seed(42)
data = pd.Series(np.concatenate([np.random.normal(100, 15, 200), [200, 220, -10]]))

Q1  = data.quantile(0.25)
Q3  = data.quantile(0.75)
IQR = Q3 - Q1
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR
outliers = data[(data < lower_fence) | (data > upper_fence)]

print("📊 Five-Number Summary")
print(f"  Min:    {data.min():.1f}")
print(f"  Q1:     {Q1:.1f}")
print(f"  Median: {data.median():.1f}")
print(f"  Q3:     {Q3:.1f}")
print(f"  Max:    {data.max():.1f}")
print(f"  IQR:    {IQR:.1f}")
print(f"  Fences: [{lower_fence:.1f}, {upper_fence:.1f}]")
print(f"  Outliers: {sorted(outliers.values)}")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
data.hist(bins=30, ax=axes[0], color='#3498db', edgecolor='white')
for o in outliers:
    axes[0].axvline(o, color='red', lw=2, linestyle='--')
axes[0].set_title('Histogram with Outliers', fontweight='bold')

axes[1].boxplot(data, vert=True, patch_artist=True,
                boxprops=dict(facecolor='#3498db', alpha=0.6),
                flierprops=dict(marker='o', color='red', markersize=8))
axes[1].set_title('Box Plot: Outliers as Red Dots', fontweight='bold')
plt.tight_layout()
plt.savefig('ch12_outliers.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Comprehensive summary statistics: pandas describe() + extras
np.random.seed(42)
datasets = {
    'Normal(50,10)':     np.random.normal(50, 10, 500),
    'Right-Skewed':      np.random.lognormal(3.8, 0.5, 500),
    'Left-Skewed':       100 - np.random.lognormal(3.5, 0.4, 500),
    'Bimodal':           np.concatenate([np.random.normal(30, 5, 250), np.random.normal(70, 5, 250)]),
}

print(f"{'Metric':<20} {'Normal':>14} {'Right-Skew':>14} {'Left-Skew':>14} {'Bimodal':>12}")
print("-" * 76)
metrics = {
    'Mean':     lambda d: d.mean(),
    'Median':   lambda d: np.median(d),
    'Std Dev':  lambda d: d.std(),
    'IQR':      lambda d: np.percentile(d,75)-np.percentile(d,25),
    'Skewness': lambda d: stats.skew(d),
    'Kurtosis': lambda d: stats.kurtosis(d),
}
names = list(datasets.keys())
for metric_name, func in metrics.items():
    vals = [func(d) for d in datasets.values()]
    row = " ".join(f"{v:>14.2f}" for v in vals)
    print(f"{metric_name:<20} {row}")

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, (name, data) in zip(axes, datasets.items()):
    ax.hist(data, bins=30, color='#3498db', edgecolor='white', density=True)
    ax.axvline(data.mean(), color='red', lw=2, linestyle='--', label='Mean')
    ax.axvline(np.median(data), color='green', lw=2, linestyle='-', label='Median')
    ax.set_title(name, fontweight='bold', fontsize=9)
    ax.legend(fontsize=7)
plt.suptitle("Descriptive Statistics Across Different Distributions", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('ch12_summary.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Data: [12, 15, 14, 10, 98, 13, 16, 11]. Find mean, median, IQR. Is 98 an outlier?
**P2:** A distribution has mean=70, median=60. What does this tell you about its shape?
**P3:** Which is more informative about "typical salary" — mean or median? Why?

<details><summary>💡 Solutions</summary>

**P1:** Mean=(189/8)=23.6, Median=(13+14)/2=13.5, IQR=15-11=4.
Outlier check: Q3+1.5×IQR=15+6=21. Since 98>21, **yes, 98 is an outlier**.

**P2:** Mean>Median → **right-skewed** (long right tail pulling mean up).

**P3:** **Median** — it's not affected by extreme values (like a CEO's $10M salary).
</details>"""),

    code("""data_p1 = np.array([12, 15, 14, 10, 98, 13, 16, 11])
Q1, Q3 = np.percentile(data_p1, [25, 75])
IQR = Q3 - Q1
print(f"Mean={data_p1.mean():.1f}, Median={np.median(data_p1)}, IQR={IQR}")
print(f"Upper fence = {Q3 + 1.5*IQR:.1f}")
print(f"Is 98 an outlier? {98 > Q3 + 1.5*IQR}")"""),

    md("""## 🎯 Episode Recap & Tier 1 Summary

**This episode's takeaways:**
1. Use **median** for skewed data or when outliers are present.
2. **IQR** is a robust measure of spread; use it to detect outliers.
3. Skewness and kurtosis describe the **shape** beyond mean and variance.

## 🏆 Tier 1 Complete!

You've covered the foundations of probability and statistics:
- ✅ What probability means and its three types
- ✅ Rules: complement, addition, multiplication
- ✅ Conditional probability and Bayes' Theorem
- ✅ Random variables: PMF, PDF, CDF
- ✅ Expected value and variance
- ✅ Five key distributions: Bernoulli, Binomial, Geometric, Poisson, Normal, Exponential
- ✅ Central Limit Theorem — the keystone of statistical inference
- ✅ Descriptive statistics: summarizing data meaningfully

**Choose your path:**
- 🎓 [Track 1 — Students: Combinatorics, Hypothesis Testing, Exam Prep]
- 💻 [Track 2 — Developers: Monte Carlo, A/B Testing, Probabilistic Systems]
- 📈 [Track 3 — Data Scientists: MLE, Bias-Variance, Causal Inference]
- ⚙️ [Track 4 — Engineers: Reliability, Queuing Theory, Six Sigma]"""),
])
save(ch12, "12_descriptive_statistics.ipynb")

print("\n🎉 All Tier 1 notebooks (Chapters 1-12) created successfully!")
