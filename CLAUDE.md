# CLAUDE.md — Project Log

## Project
**Probability & Statistics Tutorial** — YouTube series by Phiphat Chomchit (วิศวกรสอน AI).
60 Jupyter notebooks across 4 audience tracks and 3 tiers.

---

## What We Built Together

### 1. Notebook Generation Scripts (`generate_nb.py` × 6)
Programmatically generated all 60 `.ipynb` notebooks via `json.dump()`.

| Script | Notebooks | Status |
|--------|-----------|--------|
| `tier1_foundations/generate_nb.py` | Ch 1–12 (shared foundations) | ✅ written & executed |
| `tier2_students/generate_nb.py` | Ch 13–22 (exam prep) | ✅ fixed & executed |
| `tier2_developers/generate_nb.py` | Ch 13–22 (software engineering) | ✅ fixed & executed |
| `tier2_data_scientists/generate_nb.py` | Ch 13–22 (ML/DS) | ✅ written & executed |
| `tier2_engineers/generate_nb.py` | Ch 13–22 (systems/reliability) | ✅ written & executed |
| `tier3_advanced/generate_nb.py` | Ch 23–30 (all tracks) | ✅ written & executed |

**Critical bug fixed across all scripts:** Python `"""docstrings"""` inside `code("""...""")` cells terminate the outer triple-quoted string and crash the parser. All fixed to `# comments`.

### 2. README.md
Full project summary: learning path diagram, 60-chapter table, notebook structure, setup instructions, stats.

### 3. YouTube Covers (`generate_covers.py`)
Generates 60 YouTube thumbnails (1280×720 PNG) via Pillow.

**Design:**
- Dark navy `#0D1117` background, dot grid
- Red→yellow gradient left bar (matches logo)
- Diagonal accent stripes (track color)
- `logo.png` badge top-left (rounded, 110px)
- Track/tier badge pill top-right (color-coded per track)
- Faint watermark chapter number
- Thai hook text (68pt Ayuthaya, auto-scales if line overflows)
- English topic subtitle
- Bottom bar: "วิศวกรสอน AI" in amber

**Track accent colors:**
| Track | Color |
|-------|-------|
| Tier 1 Foundations | `#4361EE` blue |
| Students | `#06D6A0` green |
| Developers | `#FF6B35` orange |
| Data Scientists | `#7B2FBE` purple |
| Engineers | `#00B4D8` cyan |
| Tier 3 Advanced | `#F4A100` gold |

**Output:** `covers/{tier}/{filename}.png` — 60 files total.

---

## How to Regenerate Everything

```bash
# Install deps
uv sync

# Regenerate notebooks
python tier1_foundations/generate_nb.py
python tier2_students/generate_nb.py
python tier2_developers/generate_nb.py
python tier2_data_scientists/generate_nb.py
python tier2_engineers/generate_nb.py
python tier3_advanced/generate_nb.py

# Regenerate YouTube covers
python generate_covers.py

# Launch Jupyter
jupyter lab
```

---

## Project Structure

```
probability/
├── tier1_foundations/       # 12 notebooks + generate_nb.py
├── tier2_students/          # 10 notebooks + generate_nb.py
├── tier2_developers/        # 10 notebooks + generate_nb.py
├── tier2_data_scientists/   # 10 notebooks + generate_nb.py
├── tier2_engineers/         # 10 notebooks + generate_nb.py
├── tier3_advanced/          # 8 notebooks + generate_nb.py
├── covers/                  # 60 YouTube thumbnails (1280×720 PNG)
│   ├── tier1_foundations/
│   ├── tier2_students/
│   ├── tier2_developers/
│   ├── tier2_data_scientists/
│   ├── tier2_engineers/
│   └── tier3_advanced/
├── generate_covers.py       # YouTube thumbnail generator
├── logo.png                 # Channel logo (500×500)
├── pyproject.toml
└── README.md
```
