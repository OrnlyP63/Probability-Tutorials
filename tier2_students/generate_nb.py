"""Generate Track 1 — Students notebooks (Chapters 13-22)."""
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


# ─── Chapter 13: Combinatorics ──────────────────────────────────────────────
ch13 = nb([
    md("""# 🎓 Chapter 13: Combinatorics & Counting
*Track 1 — Students | Tier 2*

> **🎬 Hook:** How many ways can 5 students sit in a row? And does order matter?
> The answer changes completely depending on that one question.

**🎯 Objectives:** Master permutations, combinations, and the multiplication principle."""),

    md("""## 📖 Section 1 — Concept Review

### The Multiplication Principle
If task A can be done in m ways and task B in n ways, together: **m × n ways**.

### Permutations — ORDER MATTERS
Arranging r items from n distinct items:
$$P(n,r) = \\frac{n!}{(n-r)!}$$

### Combinations — ORDER DOESN'T MATTER
Choosing r items from n (groups, not arrangements):
$$C(n,r) = \\binom{n}{r} = \\frac{n!}{r!(n-r)!}$$

### When to use which?
| Question | Type |
|----------|------|
| How many ways to arrange 5 students in a row? | Permutation |
| How many ways to choose 3 students for a committee? | Combination |
| How many 4-digit PINs? | Multiplication principle |
| How many poker hands? | Combination |

### Pascal's Triangle
$$\\binom{n}{r} = \\binom{n-1}{r-1} + \\binom{n-1}{r}$$"""),

    md("""## 🧮 Section 2 — Math Walkthrough

**Example 1:** 5 students, seats in a row. P(5,5) = 5! = 120 ways.

**Example 2:** Choose 3 for a committee from 8 students.
$$C(8,3) = \\frac{8!}{3! \\cdot 5!} = \\frac{8 \\times 7 \\times 6}{3 \\times 2 \\times 1} = 56$$

**Example 3:** PIN lock — 10 digits, 4 spots, repetition allowed.
10 × 10 × 10 × 10 = 10,000 combinations.

**Example 4:** 5-card poker hand from 52 cards.
$$C(52,5) = \\frac{52!}{5! \\cdot 47!} = 2,598,960 \\text{ hands}$$"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import factorial, comb, perm
from itertools import permutations, combinations
import pandas as pd

sns.set_theme(style="whitegrid")

# ── Basic calculations ──
print("📐 Combinatorics Calculations")
print()
print("Permutations P(n,r):")
print(f"  P(5,5) = 5! = {factorial(5)}")
print(f"  P(10,3) = 10!/(10-3)! = {perm(10,3)}")
print()
print("Combinations C(n,r):")
print(f"  C(8,3) = {comb(8,3)}")
print(f"  C(52,5) = {comb(52,5):,}  (poker hands)")
print(f"  C(49,6) = {comb(49,6):,}  (lottery)")
print()

# Show P vs C
print("P vs C comparison:")
for n, r in [(5,2), (10,3), (52,5)]:
    print(f"  n={n}, r={r}: P={perm(n,r):>8,}   C={comb(n,r):>8,}   Ratio={perm(n,r)//comb(n,r)}")"""),

    code("""# ── Pascal's Triangle ──
def pascal_triangle(n):
    triangle = [[1]]
    for i in range(1, n):
        row = [1]
        for j in range(1, i):
            row.append(triangle[i-1][j-1] + triangle[i-1][j])
        row.append(1)
        triangle.append(row)
    return triangle

tri = pascal_triangle(10)
print("Pascal's Triangle (rows 0-9):")
for i, row in enumerate(tri):
    spaces = "  " * (9 - i)
    print(spaces + "  ".join(f"{x:>3}" for x in row))
print()
print(f"Row 6: {tri[6]}")
print(f"Sum of row 6: {sum(tri[6])} = 2^6 = {2**6}")"""),

    code("""# ── Visualize: Birthday problem via counting ──
# P(all different birthdays in group of n) = 365×364×...×(365-n+1) / 365^n
def p_all_diff(n):
    if n > 365: return 0
    p = 1.0
    for i in range(n):
        p *= (365 - i) / 365
    return p

group_sizes = range(1, 70)
p_collision = [1 - p_all_diff(n) for n in group_sizes]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(list(group_sizes), p_collision, color='#e74c3c', lw=3)
ax.axhline(0.5, color='gray', linestyle='--', lw=2, label='50% threshold')
ax.axvline(23, color='#27ae60', linestyle='--', lw=2, label='n=23: P≈0.507')
ax.fill_between(list(group_sizes), p_collision, alpha=0.2, color='#e74c3c')
ax.set_xlabel('Number of people in room')
ax.set_ylabel('P(at least two share a birthday)')
ax.set_title('🎂 Birthday Problem: Counting Leads to a Surprising Result!', fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('ch13_birthday.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"At n=23: P(birthday collision) = {1-p_all_diff(23):.3f}")
print(f"At n=50: P(birthday collision) = {1-p_all_diff(50):.3f}")"""),

    code("""# ── Poker hands: counting exactly ──
total_hands = comb(52, 5)

poker_hands = {
    'Royal Flush':    4,
    'Straight Flush': 36,
    'Four of a Kind': 624,
    'Full House':     3_744,
    'Flush':          5_108,
    'Straight':       10_200,
    'Three of a Kind':54_912,
    'Two Pair':       123_552,
    'One Pair':       1_098_240,
    'High Card':      1_302_540,
}

print(f"🃏 Poker Hand Probabilities (Total hands: {total_hands:,})")
print(f"{'Hand':<20} {'Count':>10} {'Probability':>14} {'1 in ...':>12}")
print("-" * 60)
for hand, count in poker_hands.items():
    prob = count / total_hands
    one_in = int(1/prob)
    print(f"{hand:<20} {count:>10,} {prob:>14.6f} {one_in:>12,}")"""),

    md("""## 📂 Section 5 — Real Exercise: Lottery Analysis"""),

    code("""# Lottery: 6 numbers from 1-49
lottery_combos = comb(49, 6)
print(f"🎰 Lottery: Choose 6 from 49")
print(f"  Total combinations: {lottery_combos:,}")
print(f"  P(jackpot) = 1/{lottery_combos:,} ≈ {1/lottery_combos:.2e}")
print()
print(f"  If you buy 1 ticket/week for 80 years ({80*52:,} tickets):")
print(f"  P(at least one win) ≈ {1-(1-1/lottery_combos)**(80*52):.6f}")
print(f"  (Still basically impossible!)")

# Simulate lottery
np.random.seed(42)
n_sims = 1_000_000
jackpots = sum(
    len(set(np.random.choice(49, 6, replace=False)) & set(np.random.choice(49, 6, replace=False))) == 6
    for _ in range(n_sims)
)
print(f"\n  Simulated: {jackpots} jackpots in {n_sims:,} tickets")
print(f"  Expected:  {n_sims/lottery_combos:.4f}")"""),

    md("""## ✏️ Section 6 — Practice Problems (Exam Style)

**P1:** 8 runners in a race. How many ways can 1st, 2nd, 3rd place be filled?

**P2:** A committee of 4 is chosen from 12 people. How many committees are possible?

**P3:** A password requires 3 uppercase letters followed by 3 digits.
No repetition allowed. How many passwords?

**P4 (Hard):** Prove that C(n,r) = C(n, n-r). What does this mean intuitively?

---
<details><summary>💡 Solutions</summary>

**P1:** P(8,3) = 8×7×6 = **336**

**P2:** C(12,4) = 12!/(4!×8!) = **495**

**P3:** P(26,3) × P(10,3) = 15,600 × 720 = **11,232,000**

**P4:** C(n,r) = n!/[r!(n-r)!]. Swapping r and (n-r): C(n,n-r) = n!/[(n-r)!r!] = same!
Intuitively: choosing 3 from 10 (the included) is the same as choosing 7 (the excluded).
</details>"""),

    code("""from math import perm, comb
print("P1:", perm(8,3))
print("P2:", comb(12,4))
print("P3:", perm(26,3) * perm(10,3))
print("P4 verification: C(10,3)=", comb(10,3), "C(10,7)=", comb(10,7))"""),

    md("## 🎯 Recap\n1. **Multiplication principle**: choices multiply.\n2. **Permutations P(n,r)**: order matters (arrangements).\n3. **Combinations C(n,r)**: order doesn't matter (selections).\n\n**Next:** [Chapter 14 — Probability Trees & Venn Diagrams]"),
])
save(ch13, "13_combinatorics.ipynb")


# ─── Chapter 14: Probability Trees & Venn Diagrams ──────────────────────────
ch14 = nb([
    md("""# 🎓 Chapter 14: Probability Trees & Venn Diagrams
*Track 1 — Students | Tier 2*

> **🎬 Hook:** Some probability problems look impossible — until you draw them.
> Probability trees and Venn diagrams make the invisible visible.

**🎯 Objectives:** Build and read probability trees; use Venn diagrams to find probabilities."""),

    md("""## 📖 Section 1 — Concept Review

### Probability Trees
- Each **branch** represents one possible outcome
- Each branch is labeled with its probability
- **Multiply along branches** (AND rule)
- **Add across branches** for the same outcome (OR rule)
- All leaf probabilities must sum to 1

### Venn Diagrams
- Each circle = one event
- Overlapping area = A AND B (intersection)
- Total circle area = A OR B (union)
- Outside both = neither A nor B

### Reading a 2×2 Table
Often the easiest way to organize joint probabilities:

|         | B    | not B |
|---------|------|-------|
| A       | P(A∩B) | P(A∩B̄) |
| not A   | P(Ā∩B) | P(Ā∩B̄) |"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyArrowPatch
import seaborn as sns
import pandas as pd

sns.set_theme(style="white")
np.random.seed(42)

# ── Draw a Probability Tree ──
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 4.5)
ax.axis('off')
ax.set_title('Probability Tree: Medical Test Example', fontsize=14, fontweight='bold')

# Tree structure: Disease (D/¬D) → Test (+/-)
nodes = {
    'root': (0.5, 2.0),
    'D':    (2.0, 3.2),
    'nD':   (2.0, 0.8),
    'D+':   (3.8, 3.8),
    'D-':   (3.8, 2.6),
    'nD+':  (3.8, 1.4),
    'nD-':  (3.8, 0.2),
}

# Draw edges
edges = [
    ('root','D',  0.01,  'P(D)=0.01',    'top'),
    ('root','nD', 0.99,  'P(¬D)=0.99',   'bottom'),
    ('D',   'D+', 0.99,  'P(+|D)=0.99',  'top'),
    ('D',   'D-', 0.01,  'P(-|D)=0.01',  'bottom'),
    ('nD',  'nD+',0.05,  'P(+|¬D)=0.05', 'top'),
    ('nD',  'nD-',0.95,  'P(-|¬D)=0.95', 'bottom'),
]

for start, end, prob, label, pos in edges:
    x0,y0 = nodes[start]; x1,y1 = nodes[end]
    ax.annotate("", xy=(x1,y1), xytext=(x0,y0),
                arrowprops=dict(arrowstyle='->', lw=1.8, color='#2c3e50'))
    mx,my = (x0+x1)/2, (y0+y1)/2
    offset = 0.15 if pos=='top' else -0.15
    ax.text(mx, my+offset, label, ha='center', fontsize=8.5, color='#2980b9', fontweight='bold')

# Leaf nodes with joint probabilities
leaf_probs = {
    'D+':  0.01*0.99,  'D-':  0.01*0.01,
    'nD+': 0.99*0.05,  'nD-': 0.99*0.95,
}
leaf_labels = {'D+':'D,+\n0.0099','D-':'D,−\n0.0001','nD+':'¬D,+\n0.0495','nD-':'¬D,−\n0.9405'}
colors = {'D+':'#e74c3c','D-':'#e74c3c','nD+':'#3498db','nD-':'#3498db'}

for node, (x,y) in nodes.items():
    if node == 'root':
        ax.scatter([x],[y], s=200, color='#2c3e50', zorder=5)
    elif node in ('D','nD'):
        ax.scatter([x],[y], s=150, color='#8e44ad', zorder=5)
        ax.text(x-0.1, y, node, ha='right', fontsize=10, fontweight='bold', color='#8e44ad')
    else:
        ax.scatter([x],[y], s=120, color=colors[node], zorder=5)
        ax.text(x+0.05, y, leaf_labels[node], ha='left', fontsize=8, fontweight='bold')

ax.text(4.3, 4.0, f'Sum check:\n{sum(leaf_probs.values()):.4f}', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='lightyellow'))
plt.tight_layout()
plt.savefig('ch14_tree.png', dpi=150, bbox_inches='tight')
plt.show()
print("Joint probabilities:")
for k,v in leaf_probs.items(): print(f"  {k}: {v:.4f}")
print(f"Sum: {sum(leaf_probs.values()):.4f}")"""),

    code("""# ── Venn Diagram ──
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.set_style("white")

scenarios = [
    {'A': 0.4, 'B': 0.3, 'AB': 0.15, 'title': 'A∩B (Intersection)\nP(A∩B)=0.15'},
    {'A': 0.4, 'B': 0.3, 'AB': 0.00, 'title': 'Mutually Exclusive\nA∩B = ∅'},
    {'A': 0.6, 'B': 0.4, 'AB': 0.40, 'title': 'B ⊂ A (B inside A)\nP(B)=0.4'},
]

for ax, s in zip(axes, scenarios):
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    ax.set_title(s['title'], fontsize=11, fontweight='bold')

    offset = 0.8 if s['AB'] > 0 else 1.5
    c1 = Circle((4-offset/2, 3.5), 2.0, color='#3498db', alpha=0.35)
    c2 = Circle((6-offset/2, 3.5), 2.0, color='#e74c3c', alpha=0.35)
    ax.add_patch(c1); ax.add_patch(c2)
    ax.text(3-offset/2, 3.5, 'A', ha='center', va='center', fontsize=14, fontweight='bold', color='#2980b9')
    ax.text(7-offset/2, 3.5, 'B', ha='center', va='center', fontsize=14, fontweight='bold', color='#c0392b')
    ax.text(5-offset/2, 3.5, f'P={s["AB"]}', ha='center', va='center', fontsize=9, color='purple')

plt.suptitle("Venn Diagrams: Visualizing Probability Relationships", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch14_venn.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── 2×2 Probability Table ──
# Survey: 500 students — sports and music
data = pd.DataFrame({
    'Sports\\Music': ['Music', 'No Music', 'Total'],
    'Sports':        [75, 125, 200],
    'No Sports':     [100, 200, 300],
    'Total':         [175, 325, 500],
})
data = data.set_index('Sports\\Music')
print("📊 Survey Results: 500 Students")
print(data)
print()

n = 500
print("Probabilities:")
print(f"  P(Sports) = 200/500 = {200/500:.2f}")
print(f"  P(Music) = 175/500 = {175/500:.2f}")
print(f"  P(Sports AND Music) = 75/500 = {75/500:.2f}")
print(f"  P(Sports OR Music) = {(200+175-75)/500:.2f}")
print(f"  P(Sports | Music) = 75/175 = {75/175:.3f}")
print(f"  P(Music | Sports) = 75/200 = {75/200:.3f}")
print()
# Independence check
print(f"Independence check: P(S)×P(M) = {200/500:.2f}×{175/500:.2f} = {(200/500)*(175/500):.3f}")
print(f"  P(S∩M) = {75/500:.3f}")
print(f"  Are they independent? {abs((200/500)*(175/500) - 75/500) < 0.01}")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Draw a probability tree: A bag has 3 red, 2 blue balls. Draw 2 without replacement.
Find P(both red), P(one of each color).

**P2:** In a school: 60% play sports (S), 40% play music (M), 25% do both.
Draw a Venn diagram. Find P(S or M), P(neither), P(S|M).

**P3 (Exam-style):** From a survey:
- P(A) = 0.5, P(B) = 0.3, P(A and B) = 0.1
Find: P(A or B), P(A|B), P(B|A), P(neither).

<details><summary>💡 Solutions</summary>

**P1:** P(both red) = 3/5 × 2/4 = 6/20 = 0.3
P(one each) = (3/5×2/4) + (2/5×3/4) = 0.3 + 0.3 = 0.6

**P2:** P(S or M) = 0.6+0.4-0.25 = 0.75, P(neither) = 0.25, P(S|M) = 0.25/0.40 = 0.625

**P3:** P(A or B) = 0.7, P(A|B) = 0.1/0.3 = 0.333, P(B|A) = 0.1/0.5 = 0.2, P(neither) = 0.3
</details>"""),

    code("""# Simulation: drawing without replacement
np.random.seed(42)
bag = ['R','R','R','B','B']
n_sims = 100_000

both_red = one_each = 0
for _ in range(n_sims):
    draw = np.random.choice(bag, 2, replace=False)
    if list(draw).count('R') == 2: both_red += 1
    elif len(set(draw)) == 2: one_each += 1

print(f"P(both red) = {both_red/n_sims:.4f} (theory: {6/20:.4f})")
print(f"P(one each) = {one_each/n_sims:.4f} (theory: {12/20:.4f})")"""),

    md("## 🎯 Recap\n1. **Trees**: multiply along branches, add across outcomes.\n2. **Venn diagrams**: overlap = intersection, union = everything covered.\n3. **2×2 tables**: organize joint probabilities for easy calculation.\n\n**Next:** [Chapter 15 — Joint, Marginal & Conditional Distributions]"),
])
save(ch14, "14_probability_trees_venn.ipynb")


# ─── Chapter 15: Joint, Marginal & Conditional ──────────────────────────────
ch15 = nb([
    md("""# 🎓 Chapter 15: Joint, Marginal & Conditional Distributions
*Track 1 — Students | Tier 2*

> **🎬 Hook:** What if TWO things are uncertain at once? How do you track probability across two dimensions?

**🎯 Objectives:** Read and compute joint, marginal, and conditional probability distributions."""),

    md("""## 📖 Section 1 — Concept Review

### Joint Probability P(X=x, Y=y)
Probability that BOTH X=x AND Y=y occur simultaneously.

### Marginal Probability
Probability of ONE variable, ignoring the other:
$$P(X=x) = \\sum_y P(X=x, Y=y)$$
(Sum over all possible values of y — "margin" of the table)

### Conditional Distribution P(X=x | Y=y)
Distribution of X given that we KNOW Y=y:
$$P(X=x | Y=y) = \\frac{P(X=x, Y=y)}{P(Y=y)}$$

### Independence
X ⊥ Y if and only if:
$$P(X=x, Y=y) = P(X=x) \\cdot P(Y=y) \\quad \\forall x,y$$"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")
np.random.seed(42)

# Joint distribution table: Hours studied (X) vs Grade (Y)
# X: hours = {1, 2, 3, 4}
# Y: grade = {A, B, C}
joint = pd.DataFrame({
    'A':   [0.02, 0.05, 0.15, 0.18],
    'B':   [0.05, 0.10, 0.12, 0.08],
    'C':   [0.10, 0.08, 0.04, 0.03],
}, index=[1, 2, 3, 4])
joint.index.name = 'Hours Studied'

# Marginal distributions
marginal_X = joint.sum(axis=1)  # sum across grades
marginal_Y = joint.sum(axis=0)  # sum across hours

print("📊 Joint Probability Distribution P(X=hours, Y=grade)")
print(joint.round(3))
print(f"\nMarginal P(X=hours): {dict(marginal_X.round(3))}")
print(f"Marginal P(Y=grade): {dict(marginal_Y.round(3))}")
print(f"\nSum of all joint probs: {joint.values.sum():.3f}")"""),

    code("""# Conditional distributions
print("📊 Conditional P(Grade | Hours Studied)")
cond_grade_given_hours = joint.div(marginal_X, axis=0)
print(cond_grade_given_hours.round(3))
print()

print("📊 Conditional P(Hours | Grade)")
cond_hours_given_grade = joint.div(marginal_Y, axis=1)
print(cond_hours_given_grade.round(3))

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Heat map of joint distribution
sns.heatmap(joint, annot=True, fmt='.3f', cmap='Blues', ax=axes[0],
            cbar_kws={'label': 'P(X,Y)'})
axes[0].set_title('Joint Distribution P(X,Y)', fontweight='bold')
axes[0].set_ylabel('Hours Studied')

# Conditional: grade given hours
sns.heatmap(cond_grade_given_hours, annot=True, fmt='.3f', cmap='Greens', ax=axes[1])
axes[1].set_title('Conditional P(Grade|Hours)', fontweight='bold')

# Marginals
ax = axes[2]
bar_width = 0.35
x = np.arange(4)
ax.bar(x, marginal_X.values, bar_width, label='P(hours)', color='#3498db', alpha=0.8)
ax.set_xticks(x); ax.set_xticklabels(marginal_X.index)
ax.set_title('Marginal: P(Hours Studied)', fontweight='bold')
ax.set_ylabel('Probability'); ax.legend()

plt.suptitle("Joint, Marginal, and Conditional Distributions", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch15_joint.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# Independence check
print("Independence Check: P(X,Y) = P(X)·P(Y)?")
independent = np.outer(marginal_X.values, marginal_Y.values)
independent_df = pd.DataFrame(independent, index=joint.index, columns=joint.columns)
print("\nIf independent, joint would be:")
print(independent_df.round(4))
print("\nActual joint:")
print(joint.round(4))
print(f"\nAre they independent? {np.allclose(joint.values, independent_df.values, atol=0.01)}")
print("No → studying more IS associated with better grades!")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** From the joint table above:
  a) P(studying exactly 3 hours AND getting an A)
  b) P(getting an A | studying 3 hours)
  c) P(studying 3 hours | getting an A)

**P2:** Two fair dice. X=first die, Y=sum.
Find: P(X=3, Y=7), P(Y=7|X=3), P(X=3|Y=7).

<details><summary>💡 Solutions</summary>

**P1:** a) 0.15 (directly from table)
b) P(A|3 hours) = 0.15/0.31 ≈ 0.484
c) P(3 hours|A) = 0.15/0.40 = 0.375

**P2:** P(X=3,Y=7) = P(X=3,second=4) = 1/36
P(Y=7|X=3) = P(X=3,Y=7)/P(X=3) = (1/36)/(1/6) = 1/6
P(X=3|Y=7) = P(X=3,Y=7)/P(Y=7) = (1/36)/(6/36) = 1/6
</details>"""),

    code("""# Problem 2: Two dice
dice_joint = np.zeros((6, 11))  # X: 1-6, Y (sum): 2-12
for d1 in range(1, 7):
    for d2 in range(1, 7):
        dice_joint[d1-1, d1+d2-2] += 1/36

p_x3_y7 = dice_joint[2, 5]  # X=3 (index 2), Y=7 (index 5)
p_y7 = dice_joint[:, 5].sum()
p_x3 = dice_joint[2, :].sum()
print(f"P(X=3, Y=7)   = {p_x3_y7:.4f}  (= 1/36 = {1/36:.4f})")
print(f"P(Y=7|X=3)    = {p_x3_y7/p_x3:.4f}")
print(f"P(X=3|Y=7)    = {p_x3_y7/p_y7:.4f}")"""),

    md("## 🎯 Recap\n1. **Joint**: probability of two events together (the table).\n2. **Marginal**: one variable's probability (sum across the other).\n3. **Conditional**: zoom into a row or column of the table.\n\n**Next:** [Chapter 16 — Law of Total Probability]"),
])
save(ch15, "15_joint_marginal_conditional.ipynb")


# ─── Chapters 16-22: Concise but complete ───────────────────────────────────
def make_student_chapter(num, title, hook, concepts, math_text, code_text1, code_text2, practice_text, solution_code):
    return nb([
        md(f"""# 🎓 Chapter {num}: {title}
*Track 1 — Students | Tier 2*

> **🎬 Hook:** {hook}

**Key Concepts:** {concepts}"""),
        md(f"""## 📖 Section 1 — Concept Review\n\n{math_text}"""),
        code(code_text1),
        code(code_text2),
        md(f"""## ✏️ Section 6 — Practice Problems\n\n{practice_text}"""),
        code(solution_code),
        md(f"## 🎯 Recap\n**Next:** Chapter {num+1}"),
    ])


ch16 = nb([
    md("""# 🎓 Chapter 16: Law of Total Probability
*Track 1 — Students | Tier 2*

> **🎬 Hook:** Sometimes you can't compute P(A) directly — but you can split the world into cases.

**🎯 Objectives:** Apply the Law of Total Probability and understand its connection to Bayes."""),

    md("""## 📖 Section 1 — Concept Review

### The Law of Total Probability
If {B₁, B₂, ..., Bₙ} is a **partition** of Ω (mutually exclusive, exhaustive), then:

$$P(A) = \\sum_{i=1}^n P(A|B_i) \\cdot P(B_i)$$

### When to use it
When you know P(A|something) for several cases, but want P(A) overall.

### Connection to Bayes
The denominator of Bayes' Theorem IS the law of total probability:
$$P(A|B) = \\frac{P(B|A)\\cdot P(A)}{\\sum_i P(B|A_i)\\cdot P(A_i)}$$

### Example: Factory Defects
Factory has 3 machines: M1 (50% of output, 1% defect), M2 (30%, 2%), M3 (20%, 3%).
$$P(\\text{defect}) = 0.01 \\times 0.5 + 0.02 \\times 0.3 + 0.03 \\times 0.2 = 0.005 + 0.006 + 0.006 = 0.017$$"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
np.random.seed(42)

# Factory example
machines = {'M1': {'share': 0.5, 'defect_rate': 0.01},
            'M2': {'share': 0.3, 'defect_rate': 0.02},
            'M3': {'share': 0.2, 'defect_rate': 0.03}}

p_defect = sum(m['share'] * m['defect_rate'] for m in machines.values())
print("🏭 Law of Total Probability: Factory Defects")
for name, m in machines.items():
    contrib = m['share'] * m['defect_rate']
    print(f"  {name}: {m['share']:.0%} × {m['defect_rate']:.0%} = {contrib:.4f}")
print(f"  P(defect) = {p_defect:.4f} = {p_defect*100:.1f}%")

# Now apply Bayes: given defect, which machine?
print("\n🔍 Bayes (which machine caused the defect?):")
for name, m in machines.items():
    p_machine_given_defect = (m['share'] * m['defect_rate']) / p_defect
    print(f"  P({name}|defect) = {p_machine_given_defect:.3f}")"""),

    code("""# Simulation verification
np.random.seed(42)
N = 100_000

# Assign each item to a machine
machine_choice = np.random.choice(['M1','M2','M3'], N, p=[0.5, 0.3, 0.2])
defect_rates = {'M1': 0.01, 'M2': 0.02, 'M3': 0.03}
is_defective = np.array([np.random.random() < defect_rates[m] for m in machine_choice])

print(f"Simulated P(defect) = {is_defective.mean():.4f}")
print(f"Theoretical         = {p_defect:.4f}")

# Visualize the partition
fig, ax = plt.subplots(figsize=(10, 4))
x = np.array([0, 0.5, 0.8, 1.0])
colors = ['#3498db', '#e74c3c', '#27ae60']
labels = ['M1 (50%)', 'M2 (30%)', 'M3 (20%)']
for i, (xi, xj, color, label) in enumerate(zip(x[:-1], x[1:], colors, labels)):
    ax.barh(0, xj-xi, left=xi, color=color, alpha=0.7, label=label)
    defect_r = [0.01, 0.02, 0.03][i]
    ax.text((xi+xj)/2, 0, f'{label}\n{defect_r:.0%} defect', ha='center', va='center',
            fontsize=10, fontweight='bold')
ax.set_xlim(0, 1); ax.set_yticks([])
ax.set_xlabel('Share of Production')
ax.set_title('🏭 Factory Partition: Law of Total Probability', fontweight='bold')
plt.tight_layout()
plt.savefig('ch16_total_prob.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** In a city: 60% use transit (T), 30% drive (D), 10% walk (W).
P(late|T)=0.2, P(late|D)=0.05, P(late|W)=0.01. Find P(late).

**P2:** Using P1, if someone is late, P(they used transit)?

<details><summary>💡 Solutions</summary>

**P1:** P(late) = 0.2×0.6 + 0.05×0.3 + 0.01×0.1 = 0.12+0.015+0.001 = **0.136**

**P2:** P(T|late) = (0.2×0.6)/0.136 = 0.12/0.136 ≈ **0.882**
</details>"""),

    code("""p_late = 0.2*0.6 + 0.05*0.3 + 0.01*0.1
print(f"P(late) = {p_late:.4f}")
print(f"P(T|late) = {0.2*0.6/p_late:.4f}")"""),

    md("## 🎯 Recap\n1. Partition the sample space into exhaustive, mutually exclusive cases.\n2. P(A) = Σ P(A|Bᵢ)P(Bᵢ) — weight each case by its probability.\n3. This IS the denominator of Bayes' Theorem.\n\n**Next:** [Chapter 17 — Hypothesis Testing Intro]"),
])
save(ch16, "16_law_of_total_probability.ipynb")


ch17 = nb([
    md("""# 🎓 Chapter 17: Intro to Hypothesis Testing
*Track 1 — Students | Tier 2*

> **🎬 Hook:** "Our new drug works!" — but how do we know it's not just luck?
> Hypothesis testing is the framework for making decisions from data.

**🎯 Objectives:** Understand H₀ vs H₁, Type I/II errors, and the logic of a hypothesis test."""),

    md("""## 📖 Section 1 — Concept Review

### The Two Hypotheses
- **H₀ (Null Hypothesis):** The boring, default claim. "Nothing is happening."
- **H₁ (Alternative Hypothesis):** What we're trying to show. "Something IS happening."

### The Logic
We assume H₀ is true, then ask: "How surprising is our data IF H₀ were true?"
If sufficiently surprising → reject H₀.

### Two Types of Errors
|              | H₀ True      | H₀ False |
|--------------|-------------|---------|
| **Reject H₀** | ❌ Type I Error (α) | ✅ Correct (Power) |
| **Don't reject** | ✅ Correct | ❌ Type II Error (β) |

- **α** = significance level (typically 0.05) = P(Type I Error)
- **β** = P(Type II Error)
- **Power = 1-β** = P(correctly reject a false H₀)

### The 5-Step Process
1. State H₀ and H₁
2. Choose α (significance level)
3. Calculate the test statistic
4. Find the p-value
5. Make a decision: reject H₀ if p-value < α"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Visualize: null distribution and rejection region ──
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# One-sample z-test visualization
mu0, sigma, n = 100, 15, 30
se = sigma / np.sqrt(n)
alpha = 0.05
z_critical = stats.norm.ppf(1 - alpha)  # one-tailed

x = np.linspace(mu0 - 4*se, mu0 + 4*se, 300)
y = stats.norm.pdf(x, mu0, se)

ax = axes[0]
ax.plot(x, y, lw=3, color='#3498db', label='H₀ distribution')
reject_region = x >= mu0 + z_critical * se
ax.fill_between(x, y, where=reject_region, color='#e74c3c', alpha=0.5, label=f'Rejection region (α={alpha})')
ax.axvline(mu0 + z_critical*se, color='#e74c3c', lw=2, linestyle='--')
ax.axvline(108, color='#27ae60', lw=3, label='Observed x̄=108')
ax.set_title('Hypothesis Test Visualization\nH₀: μ=100, H₁: μ>100', fontweight='bold')
ax.set_xlabel('Sample Mean'); ax.set_ylabel('Density')
ax.legend(fontsize=9)

# Type I and II errors
mu1 = 108  # true mean under H₁
x2 = np.linspace(90, 130, 400)
y0 = stats.norm.pdf(x2, mu0, se)
y1 = stats.norm.pdf(x2, mu1, se)

ax2 = axes[1]
critical_val = mu0 + z_critical * se
ax2.plot(x2, y0, lw=2.5, color='#3498db', label=f'H₀: μ={mu0}')
ax2.plot(x2, y1, lw=2.5, color='#27ae60', label=f'H₁: μ={mu1}')
ax2.fill_between(x2, y0, where=(x2 >= critical_val), color='#e74c3c', alpha=0.4, label='α (Type I)')
ax2.fill_between(x2, y1, where=(x2 < critical_val), color='#9b59b6', alpha=0.4, label='β (Type II)')
ax2.axvline(critical_val, color='black', lw=2, linestyle='--', label=f'Critical={critical_val:.1f}')
ax2.set_title('Type I (α) and Type II (β) Errors', fontweight='bold')
ax2.set_xlabel('Sample Mean'); ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('ch17_hypothesis.png', dpi=150, bbox_inches='tight')
plt.show()

power = 1 - stats.norm.cdf(critical_val, mu1, se)
print(f"Critical value: {critical_val:.2f}")
print(f"α = {alpha:.2f}")
print(f"β = {stats.norm.cdf(critical_val, mu1, se):.3f}")
print(f"Power = {power:.3f}")"""),

    code("""# Worked example: 5-step test
print("📝 5-Step Hypothesis Test")
print("="*50)
print("Claim: Students sleep < 8 hours on average.")
print()
print("Step 1: H₀: μ = 8 hrs  vs  H₁: μ < 8 hrs")
print("Step 2: α = 0.05")
print()

# Sample data
np.random.seed(42)
sample = np.random.normal(7.5, 1.2, 36)
x_bar = sample.mean()
s = sample.std(ddof=1)
n = len(sample)
se = s / np.sqrt(n)
t_stat = (x_bar - 8) / se

print(f"Step 3: x̄={x_bar:.3f}, s={s:.3f}, n={n}, SE={se:.3f}")
print(f"        t = (x̄ - μ₀)/SE = ({x_bar:.3f} - 8)/{se:.3f} = {t_stat:.3f}")
print()

p_value = stats.t.cdf(t_stat, df=n-1)  # one-tailed (left)
print(f"Step 4: p-value = {p_value:.4f}")
print()

alpha = 0.05
if p_value < alpha:
    print(f"Step 5: p={p_value:.4f} < α={alpha} → REJECT H₀")
    print("        Evidence suggests students sleep less than 8 hours!")
else:
    print(f"Step 5: p={p_value:.4f} ≥ α={alpha} → Fail to reject H₀")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Classify each as Type I or Type II error:
  a) Concluding a drug works when it doesn't
  b) Failing to detect a real effect

**P2:** Why do we say "fail to reject H₀" instead of "accept H₀"?

**P3:** If you use α=0.01 instead of α=0.05, what happens to Type I and Type II errors?

<details><summary>💡 Solutions</summary>

**P1:** a) **Type I** (false positive), b) **Type II** (false negative)

**P2:** Failing to reject doesn't prove H₀ is true — we just don't have enough evidence against it. Absence of evidence ≠ evidence of absence.

**P3:** Smaller α → harder to reject → fewer Type I errors, but MORE Type II errors (lower power).
</details>"""),

    code("""# Visualize tradeoff between alpha and power
alphas = np.linspace(0.01, 0.20, 50)
mu0, mu1, sigma, n = 100, 105, 15, 30
se = sigma / np.sqrt(n)
z_crits = stats.norm.ppf(1 - alphas)
critical_vals = mu0 + z_crits * se
powers = 1 - stats.norm.cdf(critical_vals, mu1, se)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(alphas, powers, 'bo-', markersize=4, lw=2)
ax.set_xlabel('α (Significance Level)')
ax.set_ylabel('Power (1-β)')
ax.set_title('Tradeoff: Lower α → Lower Power', fontweight='bold')
ax.axvline(0.05, color='red', linestyle='--', label='α=0.05')
plt.legend(); plt.tight_layout()
plt.savefig('ch17_power_tradeoff.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("## 🎯 Recap\n1. H₀ is assumed true until evidence says otherwise.\n2. Type I = false alarm (p-value threshold = α). Type II = missed detection.\n3. We never 'accept' H₀ — only 'fail to reject'.\n\n**Next:** [Chapter 18 — p-values Explained]"),
])
save(ch17, "17_hypothesis_testing_intro.ipynb")


ch18 = nb([
    md("""# 🎓 Chapter 18: p-values Explained Without Jargon
*Track 1 — Students | Tier 2*

> **🎬 Hook:** "p=0.04, therefore our result is real." That sentence contains at least 2 mistakes.

**🎯 Objectives:** Understand what a p-value actually means, and what it doesn't mean."""),

    md("""## 📖 Section 1 — Concept Review

### What a p-value IS:
> The probability of observing results at least as extreme as ours, **assuming H₀ is true**.

$$p = P(\\text{data this extreme or more} \\mid H_0 \\text{ is true})$$

### What a p-value is NOT:
- ❌ NOT the probability that H₀ is true
- ❌ NOT the probability that your result is due to chance
- ❌ NOT the probability that you're wrong
- ❌ NOT a measure of effect size or importance

### Common Misconceptions

| Wrong | Right |
|-------|-------|
| "p=0.03 means 3% chance H₀ is true" | p-value assumes H₀ is true |
| "p=0.06 means no effect" | Might just need more data |
| "p<0.05 means practically important" | Statistical ≠ practical significance |
| "Small p → big effect" | Small p just means unlikely under H₀ |"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Visualize p-value ──
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

mu0 = 0; sigma = 1
x = np.linspace(-4, 4, 300)
y = stats.norm.pdf(x)

observed_z = 2.1
p_val = 2 * (1 - stats.norm.cdf(abs(observed_z)))  # two-tailed

ax = axes[0]
ax.plot(x, y, lw=3, color='#3498db', label='H₀ distribution N(0,1)')
mask_right = x >= abs(observed_z)
mask_left  = x <= -abs(observed_z)
ax.fill_between(x, y, where=mask_right, color='#e74c3c', alpha=0.6, label=f'p-value = {p_val:.4f}')
ax.fill_between(x, y, where=mask_left,  color='#e74c3c', alpha=0.6)
ax.axvline(observed_z, color='#27ae60', lw=3, linestyle='--', label=f'Observed z={observed_z}')
ax.axvline(-observed_z, color='#27ae60', lw=3, linestyle='--')
ax.set_title('p-value = shaded area (two-tailed)', fontweight='bold')
ax.set_xlabel('Z-score'); ax.set_ylabel('Density')
ax.legend(fontsize=9)

# ── Effect of sample size on p-value ──
true_diff = 2  # true difference in means
sample_sizes = [10, 25, 50, 100, 250, 500, 1000]
p_values = []
for n in sample_sizes:
    samples = np.random.normal(true_diff, 10, n)
    t_stat, p = stats.ttest_1samp(samples, 0)
    p_values.append(p)

ax2 = axes[1]
ax2.plot(sample_sizes, p_values, 'bo-', markersize=8, lw=2)
ax2.axhline(0.05, color='red', linestyle='--', lw=2, label='α=0.05')
ax2.set_xscale('log')
ax2.set_xlabel('Sample Size')
ax2.set_ylabel('p-value')
ax2.set_title('⚠️ Same effect, larger n → smaller p-value\n(Significance ≠ Importance!)', fontweight='bold')
ax2.legend()
plt.tight_layout()
plt.savefig('ch18_pvalue.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# p-hacking demo: run many tests until p<0.05
np.random.seed(123)
n_experiments = 10_000
null_p_values = []

for _ in range(n_experiments):
    # H₀ is TRUE (no effect), but we test anyway
    group_a = np.random.normal(0, 1, 30)
    group_b = np.random.normal(0, 1, 30)
    _, p = stats.ttest_ind(group_a, group_b)
    null_p_values.append(p)

false_positives = sum(1 for p in null_p_values if p < 0.05)
print("⚠️  p-Hacking Demo: What happens when H₀ is TRUE?")
print(f"   Ran {n_experiments:,} tests where H₀ is TRUE")
print(f"   False positives (p<0.05): {false_positives} ({false_positives/n_experiments:.1%})")
print(f"   ≈ α = 5%! p<0.05 is NOT '95% sure it's real'")
print()
print("💡 If you run 100 tests with α=0.05 and H₀ true everywhere:")
print("   You'd expect ~5 'significant' results — pure luck!")

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(null_p_values, bins=50, color='#3498db', edgecolor='white', density=True, alpha=0.8)
ax.axvline(0.05, color='red', lw=2.5, linestyle='--', label='α=0.05 threshold')
ax.fill_between([0, 0.05], [20, 20], alpha=0.3, color='red')
ax.set_xlabel('p-value'); ax.set_ylabel('Density')
ax.set_title('⚠️ Under H₀, p-values are UNIFORM! 5% fall below 0.05.', fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('ch18_phacking.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** A researcher says "p=0.04 means there is a 96% chance our hypothesis is correct."
What are the two things wrong with this statement?

**P2:** Study A: n=10, p=0.04. Study B: n=10,000, p=0.04.
Which has a larger effect size? What can you conclude from each?

**P3:** If you collect data until p<0.05, why is this a problem?

<details><summary>💡 Solutions</summary>

**P1:** (1) p-value is NOT P(H₀ true) — it's P(data | H₀ true). (2) Assumes H₀ is true; doesn't say H₁ is 96% likely.

**P2:** Study A likely has a LARGER effect (small n + small p = big effect). Study B's tiny p might reflect a trivially small effect that's meaningless in practice.

**P3:** This is optional stopping / p-hacking. The Type I error rate inflates far above α=0.05 because you're essentially running many tests and stopping when lucky.
</details>"""),

    code("""# Effect size vs statistical significance
print("Effect Size (Cohen's d) vs p-value")
for n, diff, sigma in [(10, 5, 5), (10000, 0.1, 5), (100, 2, 5)]:
    d = diff / sigma  # Cohen's d
    se = sigma / np.sqrt(n)
    t = diff / se
    p = 2 * stats.t.sf(abs(t), df=n-1)
    print(f"  n={n:>5}, diff={diff}, d={d:.2f}: p={p:.4f}, {'significant' if p<0.05 else 'not significant'}")"""),

    md("## 🎯 Recap\n1. p-value = P(data this extreme | H₀ true). NOT P(H₀ is true).\n2. Small p ≠ big effect. Large n gives small p even for tiny effects.\n3. p-hacking inflates false positives — always plan your analysis before collecting data.\n\n**Next:** [Chapter 19 — Confidence Intervals]"),
])
save(ch18, "18_pvalues_explained.ipynb")


ch19 = nb([
    md("""# 🎓 Chapter 19: Confidence Intervals — What They Actually Mean
*Track 1 — Students | Tier 2*

> **🎬 Hook:** "We are 95% confident the true mean is between 48 and 52."
> Most people get this sentence subtly wrong — and the correct interpretation is more interesting.

**🎯 Objectives:** Construct CIs, state them correctly, understand what 95% really means."""),

    md("""## 📖 Section 1 — Concept Review

### Formula: CI for a Mean
$$\\bar{X} \\pm z_{\\alpha/2} \\cdot \\frac{\\sigma}{\\sqrt{n}}$$

For 95% CI: z* = 1.96. For 99% CI: z* = 2.576.

### What "95% Confidence" REALLY Means
> If we repeated this sampling process many times, 95% of the constructed intervals would contain the true parameter.

### Common Misconceptions
| ❌ Wrong | ✅ Right |
|---------|---------|
| "95% chance μ is in this interval" | The interval either contains μ or doesn't (μ is fixed!) |
| "95% of data is in the interval" | No, this is about the mean, not individual values |
| "Wider CI = less data" | True, but also: wider CI = more confidence level |

### Width of CI
$$\\text{Width} = 2 z^* \\cdot \\frac{\\sigma}{\\sqrt{n}}$$
- Quadruple n to halve the width"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── The KEY insight: 95% of CIs contain the true mean ──
true_mu = 50
sigma = 10
n = 30
z_star = 1.96
n_intervals = 100

fig, ax = plt.subplots(figsize=(10, 12))
contains_mu = 0

for i in range(n_intervals):
    sample = np.random.normal(true_mu, sigma, n)
    x_bar = sample.mean()
    se = sigma / np.sqrt(n)
    lo = x_bar - z_star * se
    hi = x_bar + z_star * se
    contains = lo <= true_mu <= hi
    if contains: contains_mu += 1
    color = '#27ae60' if contains else '#e74c3c'
    ax.plot([lo, hi], [i, i], color=color, lw=1.5, alpha=0.8)
    ax.plot(x_bar, i, 'o', color=color, markersize=3)

ax.axvline(true_mu, color='black', lw=2.5, linestyle='--', label=f'True μ={true_mu}')
ax.set_xlabel('Value')
ax.set_title(f'95% Confidence Intervals: {contains_mu}/{n_intervals} contain μ\\n(green=contains, red=misses)',
             fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('ch19_ci.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Intervals containing μ: {contains_mu}/100 = {contains_mu}%")"""),

    code("""# How width changes with n and confidence level
sigma = 15

print("CI Width for σ=15:")
print(f"{'n':>8} {'90% CI':>12} {'95% CI':>12} {'99% CI':>12}")
print("-" * 48)
for n in [10, 30, 100, 400, 1000]:
    se = sigma / np.sqrt(n)
    for z, label in [(1.645, '90%'), (1.960, '95%'), (2.576, '99%')]:
        if label == '90%':
            row = f"{n:>8}"
        row += f"  ±{z*se:>8.2f}"
    print(row)

# Effect of n on CI width
ns = np.arange(1, 201)
widths_95 = 2 * 1.96 * sigma / np.sqrt(ns)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(ns, widths_95, color='#3498db', lw=3)
ax.axhline(5, color='red', linestyle='--', lw=2, label='Target width = 5')
n_needed = int((2 * 1.96 * sigma / 5) ** 2) + 1
ax.axvline(n_needed, color='red', linestyle=':', lw=2, label=f'Need n≥{n_needed}')
ax.set_xlabel('Sample Size n'); ax.set_ylabel('95% CI Width')
ax.set_title('CI Width Decreases with Sample Size', fontweight='bold')
ax.legend(); plt.tight_layout()
plt.savefig('ch19_ci_width.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Sample: n=64, x̄=120, σ=16. Construct a 95% CI for μ.

**P2:** How large must n be to get a 95% CI with width ≤ 4, if σ=10?

**P3:** True or False: "There is a 95% probability that μ is between 48 and 52."

<details><summary>💡 Solutions</summary>

**P1:** SE = 16/√64 = 2. CI = 120 ± 1.96×2 = (116.08, 123.92)

**P2:** Width = 2×1.96×10/√n ≤ 4 → √n ≥ 9.8 → n ≥ 97

**P3:** **False!** μ is a fixed (unknown) number. The CI is random. 95% refers to the long-run coverage of the procedure.
</details>"""),

    code("""n, xbar, sigma = 64, 120, 16
se = sigma / np.sqrt(n)
z = 1.96
print(f"95% CI: ({xbar - z*se:.2f}, {xbar + z*se:.2f})")
print(f"Required n: {int((2*1.96*10/4)**2)+1}")"""),

    md("## 🎯 Recap\n1. CI = (x̄ ± z*·SE): it's about the procedure, not a probability for fixed μ.\n2. Width ∝ 1/√n — more data → narrower interval.\n3. Higher confidence (99% vs 95%) → wider interval.\n\n**Next:** [Chapter 20 — Chi-Square Test]"),
])
save(ch19, "19_confidence_intervals.ipynb")


ch20 = nb([
    md("""# 🎓 Chapter 20: Chi-Square Test for Beginners
*Track 1 — Students | Tier 2*

> **🎬 Hook:** Is this die fair? Are these two categorical variables related?
> The chi-square test was designed for exactly these questions.

**🎯 Objectives:** Apply chi-square goodness-of-fit and test of independence."""),

    md("""## 📖 Section 1 — Concept Review

### When to use chi-square
- **Goodness-of-fit:** Does observed data match an expected distribution?
- **Test of independence:** Are two categorical variables related?

### The Chi-Square Statistic
$$\\chi^2 = \\sum_i \\frac{(O_i - E_i)^2}{E_i}$$
where O = observed counts, E = expected counts.

### Under H₀:
- χ² ~ chi-square distribution with (categories-1) degrees of freedom
- Large χ² → data doesn't fit expected → reject H₀

### Rule of Thumb
- Expected count ≥ 5 in each cell (otherwise, use Fisher's exact test)"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import pandas as pd
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Goodness of Fit: Is this die fair? ──
observed = np.array([18, 22, 15, 25, 17, 23])  # 120 rolls
expected = np.full(6, 20.0)  # expected if fair: 120/6 = 20

chi2_stat = np.sum((observed - expected)**2 / expected)
df = 5  # 6-1
p_value = 1 - stats.chi2.cdf(chi2_stat, df)

print("🎲 Chi-Square Goodness of Fit: Is the die fair?")
print(f"{'Face':>6} {'Observed':>10} {'Expected':>10} {'(O-E)²/E':>12}")
for i, (o, e) in enumerate(zip(observed, expected)):
    print(f"{i+1:>6} {o:>10} {e:>10.0f} {(o-e)**2/e:>12.2f}")
print(f"\nχ² = {chi2_stat:.4f}, df = {df}, p-value = {p_value:.4f}")
print(f"Conclusion: {'Reject H₀ (die is biased!)' if p_value < 0.05 else 'Fail to reject H₀ (no evidence of bias)'}")

# Visualize chi-square distribution
x = np.linspace(0, 20, 300)
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(x, stats.chi2.pdf(x, df), lw=3, color='#3498db', label=f'χ²(df={df})')
ax.fill_between(x, stats.chi2.pdf(x, df), where=(x >= chi2_stat), color='#e74c3c', alpha=0.5,
                label=f'p-value = {p_value:.3f}')
ax.axvline(chi2_stat, color='#e74c3c', lw=2, linestyle='--', label=f'χ²={chi2_stat:.2f}')
ax.set_xlabel('χ² statistic'); ax.set_ylabel('Density')
ax.set_title('Chi-Square Goodness of Fit: Die Roll Test', fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('ch20_chi2_gof.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── Test of Independence: Gender vs Preference ──
contingency = np.array([[45, 30], [25, 50]])  # [Prefer A, Prefer B] for [Male, Female]
chi2, p, dof, expected = stats.chi2_contingency(contingency)

table = pd.DataFrame(contingency, index=['Male', 'Female'], columns=['Prefer A', 'Prefer B'])
expected_df = pd.DataFrame(expected, index=['Male', 'Female'], columns=['Prefer A', 'Prefer B'])

print("📊 Test of Independence: Gender vs Product Preference")
print("Observed:")
print(table)
print("\nExpected (under H₀: independence):")
print(expected_df.round(2))
print(f"\nχ² = {chi2:.4f}, df = {dof}, p-value = {p:.4f}")
print(f"Conclusion: {'Reject H₀: Gender and preference ARE related' if p < 0.05 else 'Fail to reject H₀'}")"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Roll a die 60 times. Expected: 10 per face. Observed: [12,8,11,9,14,6].
Calculate χ² by hand. Is the die biased (α=0.05)?

**P2:** Survey: 100 students. Smoker vs Exercise (Yes/No).
Observed: [[15,25],[35,25]]. Test independence.

<details><summary>💡 Solutions</summary>

**P1:** χ² = (2²+2²+1²+1²+4²+4²)/10 = (4+4+1+1+16+16)/10 = 42/10 = 4.2. df=5. Critical = 11.07. 4.2 < 11.07 → **Fail to reject H₀**

**P2:** Chi2_contingency gives the answer automatically.
</details>"""),

    code("""# P1
obs_p1 = np.array([12, 8, 11, 9, 14, 6])
exp_p1 = np.full(6, 10.0)
chi2_p1 = np.sum((obs_p1 - exp_p1)**2 / exp_p1)
p_p1 = 1 - stats.chi2.cdf(chi2_p1, df=5)
print(f"P1: χ²={chi2_p1:.2f}, p={p_p1:.4f}, biased? {p_p1<0.05}")

# P2
ct = np.array([[15,25],[35,25]])
chi2_p2, p_p2, _, _ = stats.chi2_contingency(ct)
print(f"P2: χ²={chi2_p2:.4f}, p={p_p2:.4f}, related? {p_p2<0.05}")"""),

    md("## 🎯 Recap\n1. Chi-square tests categorical data: goodness-of-fit or independence.\n2. χ² = Σ(O-E)²/E — bigger = more surprising.\n3. Requires E ≥ 5 per cell.\n\n**Next:** [Chapter 21 — Correlation vs Causation]"),
])
save(ch20, "20_chi_square_test.ipynb")


ch21 = nb([
    md("""# 🎓 Chapter 21: Correlation vs Causation
*Track 1 — Students | Tier 2*

> **🎬 Hook:** Ice cream sales and drowning rates are strongly correlated (r = 0.85).
> Should we ban ice cream to save lives? Understanding why this is absurd is the whole lesson.

**🎯 Objectives:** Compute Pearson r, interpret it correctly, recognize confounders and spurious correlations."""),

    md("""## 📖 Section 1 — Concept Review

### Pearson Correlation Coefficient
$$r = \\frac{\\sum(x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum(x_i-\\bar{x})^2 \\sum(y_i-\\bar{y})^2}}$$

Properties: -1 ≤ r ≤ 1, r=0 (uncorrelated), r=±1 (perfect linear)

### Correlation ≠ Causation
Four reasons for spurious correlation:
1. **Common cause (confounder):** Z causes both X and Y (summer → ice cream AND drowning)
2. **Reverse causation:** Maybe Y causes X, not X causing Y
3. **Coincidence:** Random chance, especially with many comparisons
4. **Selection bias:** The data wasn't collected randomly

### When CAN you infer causation?
- **Randomized Controlled Trial (RCT)**: Gold standard
- **Natural experiment**: Random-ish assignment in the real world
- **Instrumental variables**: More advanced causal methods"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Visualize different correlations ──
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

scenarios = [
    ('Strong positive\nr ≈ 0.95', 0.95),
    ('Moderate positive\nr ≈ 0.5', 0.5),
    ('No correlation\nr ≈ 0', 0.0),
    ('Moderate negative\nr ≈ -0.5', -0.5),
    ('Non-linear\n(r misleads!)', None),
    ('Outlier effect', 0.9),
]

n = 100
for ax, (title, r) in zip(axes.flatten(), scenarios):
    if title == 'Non-linear\n(r misleads!)':
        x = np.linspace(0, 2*np.pi, n)
        y = np.sin(x) + np.random.normal(0, 0.2, n)
        corr = np.corrcoef(x, y)[0,1]
    elif title == 'Outlier effect':
        x = np.random.normal(0, 1, n-5)
        y = x * 0.1 + np.random.normal(0, 1, n-5)
        x = np.append(x, [5, 6, 7, 8, 9])
        y = np.append(y, [5, 6, 7, 8, 9])
        corr = np.corrcoef(x, y)[0,1]
    else:
        cov = [[1, r], [r, 1]]
        data = np.random.multivariate_normal([0,0], cov, n)
        x, y = data[:,0], data[:,1]
        corr = np.corrcoef(x, y)[0,1]

    ax.scatter(x, y, alpha=0.6, s=25, color='#3498db')
    m, b, _, _, _ = stats.linregress(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, m*x_line + b, 'r-', lw=2)
    ax.set_title(f'{title}\nActual r = {corr:.2f}', fontweight='bold', fontsize=9)

plt.suptitle("Correlation Patterns: r can be misleading!", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch21_correlation.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    code("""# ── Spurious Correlation: The Confounder ──
np.random.seed(42)
n = 52  # 52 weeks of data

# Temperature is the hidden confounder (summer heat)
temperature = np.tile(np.sin(np.linspace(0, 2*np.pi, 52)), 1) * 20 + 25
ice_cream_sales = temperature * 50 + np.random.normal(0, 200, n)
drowning_rate   = temperature * 2  + np.random.normal(0, 5, n)

r_spurious = np.corrcoef(ice_cream_sales, drowning_rate)[0,1]
r_partial   = np.corrcoef(ice_cream_sales - 50*temperature,
                           drowning_rate - 2*temperature)[0,1]

print(f"🍦 Spurious Correlation Example")
print(f"r(ice cream, drowning) = {r_spurious:.3f}  ← Strong!")
print(f"r after removing temperature effect = {r_partial:.3f}  ← Near zero!")
print()
print("The confounder (temperature) created the illusion of causation.")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].scatter(ice_cream_sales, drowning_rate, c=temperature, cmap='Reds', alpha=0.8, s=40)
axes[0].set_xlabel('Ice Cream Sales'); axes[0].set_ylabel('Drowning Rate')
axes[0].set_title(f'🍦 Spurious: r={r_spurious:.2f}\n(both caused by temperature!)', fontweight='bold')

weeks = np.arange(52)
ax2 = axes[1]
ax2.plot(weeks, ice_cream_sales/ice_cream_sales.max(), label='Ice Cream (normalized)', color='#e74c3c')
ax2.plot(weeks, drowning_rate/drowning_rate.max(), label='Drowning Rate (normalized)', color='#3498db')
ax2.plot(weeks, temperature/temperature.max(), label='Temperature (the confounder)', color='#f39c12', linestyle='--')
ax2.set_xlabel('Week of Year'); ax2.set_ylabel('Normalized Value')
ax2.set_title('🌡️ Temperature drives both variables', fontweight='bold')
ax2.legend(fontsize=8)
plt.tight_layout()
plt.savefig('ch21_spurious.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Practice Problems

**P1:** Calculate r for: x=[1,2,3,4,5], y=[2,4,5,4,5].

**P2:** Identify the likely confounder: "Cities with more hospitals have higher death rates."

**P3:** Is each causal or merely correlational?
  a) Smoking and lung cancer (RCT would be unethical, but mechanism is known)
  b) Shoe size and reading ability in children
  c) Exercise and lower blood pressure (RCT data available)

<details><summary>💡 Solutions</summary>

**P1:** r ≈ 0.90 (positive, strong)

**P2:** Population size — larger cities have more hospitals AND more deaths.

**P3:** a) Causal (mechanism + natural experiments), b) Confounder: age (older kids = bigger feet + better reading), c) Causal (RCT evidence)
</details>"""),

    code("""x = np.array([1,2,3,4,5]); y = np.array([2,4,5,4,5])
r, p = stats.pearsonr(x, y)
print(f"P1: r = {r:.4f}, p = {p:.4f}")

# Anscombe's Quartet: same r, very different data
print("\nAnscombe's Quartet: all have r ≈ 0.816, but look different!")
anscombe = sns.load_dataset('anscombe')
for dataset in ['I','II','III','IV']:
    d = anscombe[anscombe.dataset==dataset]
    r_val = np.corrcoef(d.x, d.y)[0,1]
    print(f"  Dataset {dataset}: r = {r_val:.3f}")"""),

    md("## 🎯 Recap\n1. Correlation measures LINEAR association (−1 to +1).\n2. r ≠ causation: confounders, reverse causation, and coincidence all create spurious correlations.\n3. Only randomized experiments allow causal claims.\n\n**Next:** [Chapter 22 — Exam Strategy & Common Mistakes]"),
])
save(ch21, "21_correlation_vs_causation.ipynb")


ch22 = nb([
    md("""# 🎓 Chapter 22: Exam Strategy & Common Mistakes
*Track 1 — Students | Tier 2 Finale*

> **🎬 Hook:** You've learned all the material — now let's make sure the exam reflects that.
> This chapter is your probability & statistics survival guide.

**🎯 Objectives:** Review all Track 1 concepts, build a problem-solving checklist, and demolish common mistakes."""),

    md("""## 📖 Section 1 — Exam Problem-Solving Framework

### Step-by-Step Approach
1. **Read carefully** — identify what's given and what's asked
2. **Classify the problem** — which concept applies?
3. **Write out the formula** — don't skip steps
4. **Check the answer** — does it make sense?

### Classification Cheatsheet
| Keywords | Concept |
|----------|---------|
| "at least one", "at least two" | Complement rule |
| "given that", "if we know" | Conditional probability / Bayes |
| "in n trials, how many successes" | Binomial distribution |
| "time until first..." | Geometric or Exponential |
| "average count in fixed interval" | Poisson |
| "test whether..." | Hypothesis testing |
| "estimate range for..." | Confidence interval |
| "how many ways to..." | Combinatorics (P or C) |"""),

    md("""## 🧮 Section 2 — Top 10 Common Mistakes

1. **Adding probabilities that aren't mutually exclusive**
   - Wrong: P(A or B) = P(A) + P(B) always
   - Right: P(A or B) = P(A) + P(B) - P(A and B)

2. **Forgetting the complement rule for "at least one"**
   - Wrong: Add up all cases separately
   - Right: 1 - P(none)

3. **Confusing P(A|B) with P(B|A)**
   - P(positive test | disease) ≠ P(disease | positive test)

4. **Misinterpreting p-values**
   - Wrong: "p=0.03 means 97% chance we're right"
   - Right: P(this data | H₀ is true) = 0.03

5. **Treating dependent events as independent**
   - Drawing without replacement → NOT independent

6. **Wrong degrees of freedom** in t-test (use n-1, not n)

7. **Confusing standard deviation with standard error**
   - SD describes spread in data; SE = SD/√n describes spread in sample means

8. **Base rate neglect** in Bayes (forgetting P(disease) when interpreting test)

9. **Misinterpreting confidence intervals**
   - "95% CI means 95% chance μ is inside" — WRONG

10. **Using wrong distribution** for the problem type"""),

    code("""import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, special
import seaborn as sns
import pandas as pd
sns.set_theme(style="whitegrid")
np.random.seed(42)

# ── Quick Review: All Major Formulas ──
print("📐 FORMULA CHEATSHEET")
print("="*60)
formulas = {
    "P(A or B)":          "P(A) + P(B) - P(A and B)",
    "P(A|B)":             "P(A and B) / P(B)",
    "Bayes":              "P(H|E) = P(E|H)·P(H) / P(E)",
    "Binomial P(X=k)":    "C(n,k)·p^k·(1-p)^(n-k)",
    "E[Binomial]":        "np",
    "Var[Binomial]":      "np(1-p)",
    "Poisson P(X=k)":     "e^(-λ)·λ^k / k!",
    "Normal Z-score":     "(X - μ) / σ",
    "Sample mean SE":     "σ / √n",
    "95% CI":             "x̄ ± 1.96·(σ/√n)",
    "Chi-square stat":    "Σ (O-E)² / E",
    "Pearson r":          "Σ(xi-x̄)(yi-ȳ) / √[Σ(xi-x̄)²·Σ(yi-ȳ)²]",
    "Permutations P(n,r)":"n! / (n-r)!",
    "Combinations C(n,r)":"n! / [r!(n-r)!]",
}
for name, formula in formulas.items():
    print(f"  {name:<22} = {formula}")"""),

    code("""# ── Mixed Practice: Identify the Distribution ──
problems = [
    ("You flip a fair coin 15 times. P(exactly 9 heads)?", "Binomial(15, 0.5)", "binom.pmf(9, 15, 0.5)"),
    ("Bus arrives every 20 min on average. P(wait > 30 min)?", "Exponential(λ=1/20)", "expon.sf(30, scale=20)"),
    ("Call center: avg 3 calls/hour. P(0 calls in an hour)?", "Poisson(λ=3)", "poisson.pmf(0, 3)"),
    ("Height ~ N(170, 10). P(person > 185 cm)?", "Normal(170, 10)", "norm.sf(185, 170, 10)"),
    ("10 items: 2 defective. Pick 3 without replacement. P(exactly 1 defective)?", "Hypergeometric", "hypergeom.pmf(1, 10, 2, 3)"),
]

print("🔍 Distribution Identification Practice")
print("="*70)
for problem, dist, code_str in problems:
    print(f"\nProblem: {problem}")
    print(f"  Distribution: {dist}")
    result = eval(f"stats.{code_str}")
    print(f"  Answer: {result:.4f}")"""),

    code("""# ── Full Exam Problem: End-to-End ──
print("📝 FULL EXAM PROBLEM")
print("="*60)
print(
    "A city has two types of drivers: careful (60%) and aggressive (40%).\\n"
    "Careful drivers have a 5% annual accident rate.\\n"
    "Aggressive drivers have a 25% annual accident rate.\\n\\n"
    "Questions:\\n"
    "1. What is P(accident in a year)?\\n"
    "2. Given an accident, P(the driver is aggressive)?\\n"
    "3. In a sample of n=50 aggressive drivers, what is E[accidents]?\\n"
    "   What is P(at most 10 accidents)?"
)

# Q1: Law of Total Probability
p_careful, p_agg = 0.6, 0.4
p_acc_careful, p_acc_agg = 0.05, 0.25
p_accident = p_careful * p_acc_careful + p_agg * p_acc_agg
print(f"Q1: P(accident) = {p_careful}×{p_acc_careful} + {p_agg}×{p_acc_agg} = {p_accident:.4f}")

# Q2: Bayes
p_agg_given_acc = (p_agg * p_acc_agg) / p_accident
print(f"Q2: P(aggressive|accident) = ({p_agg}×{p_acc_agg})/{p_accident:.3f} = {p_agg_given_acc:.4f}")

# Q3: Binomial
n, p = 50, 0.25
e_x = n * p
p_at_most_10 = stats.binom.cdf(10, n, p)
print(f"Q3: E[accidents] = {n}×{p} = {e_x}")
print(f"    P(≤10 accidents) = {p_at_most_10:.4f}")"""),

    code("""# ── Visual Summary: All Distributions ──
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
k = np.arange(0, 25)
x = np.linspace(0, 20, 300)

# Binomial
pmf = stats.binom.pmf(k[:16], 15, 0.5)
axes[0,0].bar(k[:16], pmf, color='#3498db', edgecolor='white')
axes[0,0].set_title('Binomial(n=15,p=0.5)', fontweight='bold')

# Poisson
axes[0,1].bar(k[:15], stats.poisson.pmf(k[:15], 5), color='#e74c3c', edgecolor='white')
axes[0,1].set_title('Poisson(λ=5)', fontweight='bold')

# Geometric
axes[0,2].bar(k[1:15], stats.geom.pmf(k[1:15], 0.3), color='#27ae60', edgecolor='white')
axes[0,2].set_title('Geometric(p=0.3)', fontweight='bold')

# Normal
x_n = np.linspace(-4, 4, 300)
axes[1,0].plot(x_n, stats.norm.pdf(x_n), color='#9b59b6', lw=3)
axes[1,0].fill_between(x_n, stats.norm.pdf(x_n), alpha=0.3, color='#9b59b6')
axes[1,0].set_title('Normal(0,1)', fontweight='bold')

# Exponential
axes[1,1].plot(x, stats.expon.pdf(x, scale=3), color='#e67e22', lw=3)
axes[1,1].fill_between(x, stats.expon.pdf(x, scale=3), alpha=0.3, color='#e67e22')
axes[1,1].set_title('Exponential(λ=1/3)', fontweight='bold')

# Chi-square
x_chi = np.linspace(0, 20, 300)
for df, color in [(2,'#1abc9c'),(5,'#3498db'),(10,'#e74c3c')]:
    axes[1,2].plot(x_chi, stats.chi2.pdf(x_chi, df), lw=2.5, color=color, label=f'df={df}')
axes[1,2].set_title('Chi-Square Distributions', fontweight='bold')
axes[1,2].legend()

plt.suptitle("🎓 Track 1 Summary: Know Your Distributions!", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch22_distribution_gallery.png', dpi=150, bbox_inches='tight')
plt.show()"""),

    md("""## ✏️ Section 6 — Mixed Practice Exam

**P1:** A biased coin has P(H)=0.6. Flipped 20 times. Find P(exactly 12 heads). E[heads]? P(at least 14)?

**P2:** A test is 90% sensitive, 95% specific. Disease affects 1%.
  a) P(positive test)
  b) P(disease | positive)
  c) P(disease | negative) — why does this matter clinically?

**P3:** 8 people sit in a row.
  a) How many arrangements?
  b) If 3 are friends who must sit together, how many?

**P4:** n=36, x̄=42, s=12. Test H₀:μ=40 (two-tailed, α=0.05). Reject?

---
<details><summary>💡 Full Solutions</summary>

**P1:** Binom(20,0.6): P(12) ≈ 0.1797, E=12, P(≥14) ≈ 0.2500

**P2:** P(+) = 0.9×0.01+0.05×0.99=0.0585. P(D|+)=0.009/0.0585=0.154. P(D|-)=0.001×0.1/0.9415≈0.0001 (very reassuring!)

**P3:** a) 8!=40,320. b) Treat friends as a block: 6!×3!=720×6=4,320

**P4:** t=(42-40)/(12/6)=2/2=1. t₀.₀₂₅(35)=2.030. |t|=1<2.030 → Fail to reject H₀
</details>"""),

    code("""from math import factorial
# Solutions
print("P1:", stats.binom.pmf(12, 20, 0.6), "; E=", 20*0.6, "; P(>=14)=", 1-stats.binom.cdf(13, 20, 0.6))

p_pos = 0.9*0.01 + 0.05*0.99
print("P2a:", p_pos)
print("P2b:", 0.9*0.01/p_pos)

print("P3a:", factorial(8))
print("P3b:", factorial(6)*factorial(3))

t_stat = (42-40)/(12/6); t_crit = stats.t.ppf(0.975, 35)
print(f"P4: t={t_stat:.2f}, critical={t_crit:.3f}, reject={abs(t_stat) > t_crit}")"""),

    md("""## 🎯 Track 1 Complete! 🏆

**You've mastered:**
- ✅ Combinatorics: permutations, combinations, counting
- ✅ Probability trees and Venn diagrams
- ✅ Joint, marginal, and conditional distributions
- ✅ Law of Total Probability
- ✅ Hypothesis testing framework
- ✅ p-values (correctly!)
- ✅ Confidence intervals (correctly!)
- ✅ Chi-square tests
- ✅ Correlation vs. causation

**Ready for Tier 3?** → [Chapter 23 — Markov Chains]"""),
])
save(ch22, "22_exam_strategy.ipynb")

print("\n🎉 All Track 1 (Students) notebooks created successfully!")
