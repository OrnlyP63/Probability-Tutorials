"""Generate 60 YouTube thumbnail covers (1280x720) for the Probability & Statistics series."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1280, 720
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")
OUT_ROOT = os.path.join(os.path.dirname(__file__), "covers")

FONT_THAI     = "/System/Library/Fonts/Supplemental/Ayuthaya.ttf"
FONT_EN_BOLD  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_EN       = "/System/Library/Fonts/Supplemental/Arial.ttf"

RED    = (255, 58,  58)
YELLOW = (255, 214, 10)

# ---------------------------------------------------------------------------
# Chapter data: (ch_num, filename, badge_label, accent_hex, thai_hook, en_topic)
# ---------------------------------------------------------------------------

TIER1 = [
    ("01", "01_what_is_probability",       "TIER 1 · FOUNDATIONS", "#4361EE",
     "ความน่าจะเป็นคืออะไร?\nทำไมมันถึงสำคัญมาก?",            "What is Probability?"),
    ("02", "02_types_of_probability",      "TIER 1 · FOUNDATIONS", "#4361EE",
     "ความน่าจะเป็น 3 แบบ\nต่างกันยังไง?",                   "Types of Probability"),
    ("03", "03_rules_of_probability",      "TIER 1 · FOUNDATIONS", "#4361EE",
     "กฎที่ต้องรู้ก่อน\nเรียน Statistics!",                   "Rules of Probability"),
    ("04", "04_conditional_probability",   "TIER 1 · FOUNDATIONS", "#4361EE",
     "P(A|B) คืออะไร?\nทำไมสับสนกันมาก?",                    "Conditional Probability"),
    ("05", "05_bayes_theorem",             "TIER 1 · FOUNDATIONS", "#4361EE",
     "ทฤษฎีเบย์ส\nเปลี่ยนวิธีคิดทุกอย่าง!",                  "Bayes' Theorem"),
    ("06", "06_random_variables",          "TIER 1 · FOUNDATIONS", "#4361EE",
     "PMF, PDF, CDF\nอธิบายง่ายๆ ครั้งเดียวจบ",               "Random Variables"),
    ("07", "07_expected_value_and_variance","TIER 1 · FOUNDATIONS","#4361EE",
     "ค่าเฉลี่ยและความแปรปรวน\nสอนแบบเข้าใจจริงๆ",            "Expected Value & Variance"),
    ("08", "08_distributions_part1",       "TIER 1 · FOUNDATIONS", "#4361EE",
     "Binomial, Geometric\nเลือกใช้เมื่อไหร่?",               "Distributions Part 1"),
    ("09", "09_distributions_part2",       "TIER 1 · FOUNDATIONS", "#4361EE",
     "Poisson, Exponential\nในชีวิตจริงใช้ยังไง?",            "Distributions Part 2"),
    ("10", "10_normal_distribution",       "TIER 1 · FOUNDATIONS", "#4361EE",
     "โค้งปกติ\nทำไมมันอยู่ทุกที่?",                          "Normal Distribution"),
    ("11", "11_sampling_and_clt",          "TIER 1 · FOUNDATIONS", "#4361EE",
     "CLT ทฤษฎีที่\nเปลี่ยนโลก Statistics",                   "Sampling & Central Limit Theorem"),
    ("12", "12_descriptive_statistics",    "TIER 1 · FOUNDATIONS", "#4361EE",
     "อ่านข้อมูลให้ออก\nใน 5 นาที!",                          "Descriptive Statistics"),
]

TIER2_STUDENTS = [
    ("13", "13_combinatorics",                  "TRACK · STUDENTS", "#06D6A0",
     "จัดเรียง-เลือก กี่แบบ?\nคอมบินาทอริกส์ทำง่าย",          "Combinatorics"),
    ("14", "14_probability_trees_venn",         "TRACK · STUDENTS", "#06D6A0",
     "ต้นไม้ความน่าจะเป็น\nวาดแล้วไม่งง!",                    "Probability Trees & Venn"),
    ("15", "15_joint_marginal_conditional",     "TRACK · STUDENTS", "#06D6A0",
     "Joint, Marginal, Conditional\nเข้าใจครั้งเดียวจบ",      "Joint · Marginal · Conditional"),
    ("16", "16_law_of_total_probability",       "TRACK · STUDENTS", "#06D6A0",
     "กฎความน่าจะเป็นรวม\nสูตรเชื่อมทุกอย่าง",                "Law of Total Probability"),
    ("17", "17_hypothesis_testing_intro",       "TRACK · STUDENTS", "#06D6A0",
     "ทดสอบสมมติฐาน\nอย่างถูกต้องตั้งแต่ต้น",                 "Hypothesis Testing — Intro"),
    ("18", "18_pvalues_explained",              "TRACK · STUDENTS", "#06D6A0",
     "p-value คืออะไร?\nเข้าใจจริงๆ ไม่ใช่แค่จำ",             "p-values Explained"),
    ("19", "19_confidence_intervals",           "TRACK · STUDENTS", "#06D6A0",
     "Confidence Interval\nหมายความว่าอะไรกันแน่?",            "Confidence Intervals"),
    ("20", "20_chi_square_test",                "TRACK · STUDENTS", "#06D6A0",
     "Chi-Square Test\nทดสอบข้อมูลแบบนี้",                    "Chi-Square Test"),
    ("21", "21_correlation_vs_causation",       "TRACK · STUDENTS", "#06D6A0",
     "สหสัมพันธ์ ≠ เหตุและผล\nอย่าสับสน!",                    "Correlation vs Causation"),
    ("22", "22_exam_strategy",                  "TRACK · STUDENTS", "#06D6A0",
     "เทคนิคทำข้อสอบ\nProbability ไม่พลาด!",                  "Exam Strategy"),
]

TIER2_DEVELOPERS = [
    ("13", "13_probability_in_code",                  "TRACK · DEVELOPERS", "#FF6B35",
     "Random ใน Code\nทำงานยังไง?",                           "Probability in Code"),
    ("14", "14_monte_carlo_methods",                  "TRACK · DEVELOPERS", "#FF6B35",
     "Monte Carlo\nแก้ปัญหาซับซ้อนด้วยการสุ่ม",               "Monte Carlo Methods"),
    ("15", "15_ab_testing",                           "TRACK · DEVELOPERS", "#FF6B35",
     "A/B Testing\nทดสอบ Feature อย่างถูกวิธี",               "A/B Testing"),
    ("16", "16_bayesian_updating",                    "TRACK · DEVELOPERS", "#FF6B35",
     "Bayesian Updating\nอัปเดตความเชื่อด้วยข้อมูลใหม่",      "Bayesian Updating"),
    ("17", "17_log_probabilities",                    "TRACK · DEVELOPERS", "#FF6B35",
     "Log Probability\nทำไม ML ต้องใช้?",                     "Log Probabilities"),
    ("18", "18_probability_in_apis",                  "TRACK · DEVELOPERS", "#FF6B35",
     "API Traffic แบบ Poisson\nวางแผน Scale ได้แม่น",          "Probability in APIs"),
    ("19", "19_randomized_algorithms",                "TRACK · DEVELOPERS", "#FF6B35",
     "Randomized Algorithms\nเร็วกว่าที่คิด!",                "Randomized Algorithms"),
    ("20", "20_probabilistic_data_structures",        "TRACK · DEVELOPERS", "#FF6B35",
     "Bloom Filter ทำงานยังไง?\nประหยัด RAM แบบนี้",           "Probabilistic Data Structures"),
    ("21", "21_statistical_testing_feature_flags",    "TRACK · DEVELOPERS", "#FF6B35",
     "Sequential Testing\nสำหรับ Feature Flags",              "Statistical Testing & Feature Flags"),
    ("22", "22_debugging_probabilistic_systems",      "TRACK · DEVELOPERS", "#FF6B35",
     "Debug ระบบสุ่ม\nทำอย่างไรให้ถูกต้อง?",                  "Debugging Probabilistic Systems"),
]

TIER2_DS = [
    ("13", "13_distributions_in_ml",                       "TRACK · DATA SCIENCE", "#7B2FBE",
     "MSE, Cross-Entropy\nมาจาก Distribution ไหน?",          "Distributions in ML"),
    ("14", "14_maximum_likelihood_estimation",              "TRACK · DATA SCIENCE", "#7B2FBE",
     "MLE\nหาพารามิเตอร์ที่ดีที่สุดอย่างไร?",                "Maximum Likelihood Estimation"),
    ("15", "15_bias_variance_tradeoff",                     "TRACK · DATA SCIENCE", "#7B2FBE",
     "Bias-Variance\nทำไม Model ถึง Overfit?",                "Bias-Variance Tradeoff"),
    ("16", "16_bayesian_vs_frequentist",                    "TRACK · DATA SCIENCE", "#7B2FBE",
     "Bayesian vs Frequentist\nต่างกันอย่างไรจริงๆ?",         "Bayesian vs Frequentist"),
    ("17", "17_hypothesis_testing_model_evaluation",        "TRACK · DATA SCIENCE", "#7B2FBE",
     "ทดสอบ Model ด้วยสถิติ\nMcNemar's & t-test",              "Hypothesis Testing for Models"),
    ("18", "18_bootstrap_jackknife",                        "TRACK · DATA SCIENCE", "#7B2FBE",
     "Bootstrap CI\nสร้างได้แม้ข้อมูลน้อย",                   "Bootstrap & Jackknife"),
    ("19", "19_correlation_covariance_feature_selection",   "TRACK · DATA SCIENCE", "#7B2FBE",
     "เลือก Feature อย่างไร?\nVIF, Mutual Information",        "Correlation & Feature Selection"),
    ("20", "20_information_theory",                         "TRACK · DATA SCIENCE", "#7B2FBE",
     "Entropy, KL Divergence\nทฤษฎีสารสนเทศใน ML",            "Information Theory"),
    ("21", "21_experiment_design_power_analysis",           "TRACK · DATA SCIENCE", "#7B2FBE",
     "ต้องใช้ข้อมูลกี่ตัว?\nPower Analysis ตอบได้",            "Experiment Design & Power"),
    ("22", "22_causal_inference",                           "TRACK · DATA SCIENCE", "#7B2FBE",
     "Causal Inference\nพิสูจน์เหตุและผลด้วยข้อมูล",          "Causal Inference"),
]

TIER2_ENG = [
    ("13", "13_reliability_failure_probability",   "TRACK · ENGINEERS", "#00B4D8",
     "Weibull & MTTF\nวิเคราะห์ความน่าเชื่อถือระบบ",          "Reliability & Failure Probability"),
    ("14", "14_poisson_processes",                 "TRACK · ENGINEERS", "#00B4D8",
     "Poisson Process\nโมเดลเวลาระหว่าง Event",               "Poisson Processes"),
    ("15", "15_queuing_theory",                    "TRACK · ENGINEERS", "#00B4D8",
     "M/M/1 Queue\nคำนวณ Capacity อย่างถูกต้อง",              "Queuing Theory"),
    ("16", "16_statistical_process_control",       "TRACK · ENGINEERS", "#00B4D8",
     "SPC\nควบคุมกระบวนการด้วยสถิติ",                         "Statistical Process Control"),
    ("17", "17_signal_noise_snr_filtering",        "TRACK · ENGINEERS", "#00B4D8",
     "SNR & Kalman Filter\nกรองสัญญาณรบกวน",                  "Signal, Noise & Filtering"),
    ("18", "18_failure_mode_analysis",             "TRACK · ENGINEERS", "#00B4D8",
     "FMEA & Fault Tree\nวิเคราะห์ความล้มเหลวก่อนเกิด",       "Failure Mode Analysis"),
    ("19", "19_monte_carlo_engineering",           "TRACK · ENGINEERS", "#00B4D8",
     "Monte Carlo Engineering\nคำนวณความไม่แน่นอน",            "Monte Carlo for Engineers"),
    ("20", "20_risk_assessment_safety_factors",    "TRACK · ENGINEERS", "#00B4D8",
     "Risk Matrix & F-N Curve\nประเมินความเสี่ยง",             "Risk Assessment"),
    ("21", "21_regression_for_engineers",          "TRACK · ENGINEERS", "#00B4D8",
     "Regression ในงานวิศวกร\nCalibration & Degradation",      "Regression for Engineers"),
    ("22", "22_six_sigma_quality",                 "TRACK · ENGINEERS", "#00B4D8",
     "Six Sigma: DPMO, Gage R&R\nวัดคุณภาพแบบมือโปร",         "Six Sigma & Quality"),
]

TIER3 = [
    ("23", "23_markov_chains",                  "TIER 3 · ADVANCED", "#F4A100",
     "Markov Chain & PageRank\nอัลกอริทึมที่เปลี่ยนอินเทอร์เน็ต", "Markov Chains"),
    ("24", "24_stochastic_processes",           "TIER 3 · ADVANCED", "#F4A100",
     "Brownian Motion & GBM\nโมเดลราคาหุ้นด้วย Math",          "Stochastic Processes"),
    ("25", "25_bayesian_networks",              "TIER 3 · ADVANCED", "#F4A100",
     "Bayesian Network\nAI ตัดสินใจด้วยความน่าจะเป็น",          "Bayesian Networks"),
    ("26", "26_regression_deep_dive",           "TIER 3 · ADVANCED", "#F4A100",
     "OLS Deep Dive\nสถิติเบื้องหลัง Regression",               "Regression Deep Dive"),
    ("27", "27_time_series_autocorrelation",    "TIER 3 · ADVANCED", "#F4A100",
     "ARIMA & Seasonality\nพยากรณ์ Time Series",                "Time Series & Autocorrelation"),
    ("28", "28_mcmc",                           "TIER 3 · ADVANCED", "#F4A100",
     "MCMC\nสุ่มตัวอย่างจาก Distribution ที่ซับซ้อน",           "MCMC"),
    ("29", "29_multivariate_statistics",        "TIER 3 · ADVANCED", "#F4A100",
     "PCA & Mahalanobis\nสถิติหลายตัวแปร",                     "Multivariate Statistics"),
    ("30", "30_capstone_probabilistic_pipeline","TIER 3 · ADVANCED", "#F4A100",
     "Capstone\nBayesian A/B Test แบบครบวงจร",                  "Capstone: Probabilistic Pipeline"),
]

TRACKS = [
    (TIER1,           "tier1_foundations"),
    (TIER2_STUDENTS,  "tier2_students"),
    (TIER2_DEVELOPERS,"tier2_developers"),
    (TIER2_DS,        "tier2_data_scientists"),
    (TIER2_ENG,       "tier2_engineers"),
    (TIER3,           "tier3_advanced"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Cover renderer
# ---------------------------------------------------------------------------

def make_cover(ch_num, filename, badge_label, accent_hex, thai_hook, en_topic, out_dir):
    accent = _hex(accent_hex)

    # --- base layer (RGBA) ---
    img = Image.new("RGBA", (W, H), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)

    # dot grid
    for gx in range(0, W, 40):
        for gy in range(0, H, 40):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(28, 35, 51, 255))

    # left gradient bar (red → yellow, vertical)
    for y in range(H):
        t = y / (H - 1)
        r = int(RED[0] * (1 - t) + YELLOW[0] * t)
        g = int(RED[1] * (1 - t) + YELLOW[1] * t)
        b = int(RED[2] * (1 - t) + YELLOW[2] * t)
        draw.line([(0, y), (7, y)], fill=(r, g, b, 255))

    # faint chapter-number watermark (composited on separate layer)
    fnt_wm = _load_font(FONT_EN_BOLD, 360)
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(wm).text((760, -30), ch_num, font=fnt_wm, fill=(255, 255, 255, 22))
    img = Image.alpha_composite(img, wm)
    draw = ImageDraw.Draw(img)

    # accent diagonal stripe (decorative, top-right corner)
    stripe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripe)
    for off in range(0, 220, 22):
        sd.line([(W - 300 + off, 0), (W + off, 300)], fill=accent + (18,), width=12)
    img = Image.alpha_composite(img, stripe)
    draw = ImageDraw.Draw(img)

    # --- logo (rounded badge, top-left) ---
    logo_raw = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = 110
    logo_img = logo_raw.resize((logo_size, logo_size), Image.LANCZOS)
    lmask = Image.new("L", (logo_size, logo_size), 0)
    ImageDraw.Draw(lmask).rounded_rectangle(
        [0, 0, logo_size - 1, logo_size - 1], radius=14, fill=255
    )
    logo_img.putalpha(lmask)
    img.paste(logo_img, (28, 20), logo_img)
    draw = ImageDraw.Draw(img)

    # --- track badge pill (top-right) ---
    fnt_badge = _load_font(FONT_EN_BOLD, 21)
    badge_tw = int(draw.textlength(badge_label, font=fnt_badge))
    badge_w  = badge_tw + 36
    badge_h  = 34
    bx = W - badge_w - 36
    by = 32
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h],
                           radius=17, fill=accent + (255,))
    draw.text((bx + 18, by + 7), badge_label, font=fnt_badge, fill=(255, 255, 255, 255))

    # --- Thai hook text (auto-scale per line to fit width) ---
    MAX_TEXT_W = W - 120  # leave room for watermark
    lines = thai_hook.split("\n")
    y_cursor = 195
    rendered_fonts = []
    for line in lines:
        size = 68
        fnt_thai = _load_font(FONT_THAI, size)
        while int(draw.textlength(line, font=fnt_thai)) > MAX_TEXT_W and size > 30:
            size -= 3
            fnt_thai = _load_font(FONT_THAI, size)
        rendered_fonts.append((line, fnt_thai, size))

    for line, fnt_thai, size in rendered_fonts:
        draw.text((60, y_cursor), line, font=fnt_thai, fill=(255, 255, 255, 255))
        y_cursor += max(size + 22, 90)

    # accent underline
    first_line, first_fnt, _ = rendered_fonts[0]
    underline_w = max(int(draw.textlength(first_line, font=first_fnt)), 180)
    draw.rectangle([60, y_cursor + 4, 60 + underline_w, y_cursor + 8],
                   fill=accent + (255,))

    # --- English topic ---
    fnt_en = _load_font(FONT_EN, 30)
    draw.text((62, y_cursor + 22), en_topic, font=fnt_en, fill=(156, 163, 175, 255))

    # --- bottom bar ---
    bar_y = 658
    draw.rectangle([0, bar_y, W, H], fill=(18, 22, 30, 255))
    draw.line([(0, bar_y), (W, bar_y)], fill=accent + (160,), width=2)

    # channel name (warm amber)
    fnt_bottom = _load_font(FONT_THAI, 32)
    channel = "วิศวกรสอน AI"
    cw = int(draw.textlength(channel, font=fnt_bottom))
    draw.text(((W - cw) // 2, 669), channel, font=fnt_bottom, fill=(255, 195, 50, 255))

    # chapter label bottom-left
    fnt_ch = _load_font(FONT_EN_BOLD, 26)
    draw.text((24, 672), f"Ch.{ch_num}", font=fnt_ch, fill=(100, 110, 130, 255))

    # --- save ---
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename + ".png")
    img.convert("RGB").save(out_path, "PNG")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    total = 0
    for chapters, subdir in TRACKS:
        out_dir = os.path.join(OUT_ROOT, subdir)
        for entry in chapters:
            ch_num, filename, badge, accent, thai, en = entry
            path = make_cover(ch_num, filename, badge, accent, thai, en, out_dir)
            print(f"  {path}")
            total += 1
    print(f"\n{total} covers generated → {OUT_ROOT}/")


if __name__ == "__main__":
    main()
