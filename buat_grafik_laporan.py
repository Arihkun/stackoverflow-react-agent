from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, FancyBboxPatch


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 180})

# Grafik 1: sepuluh tag terpopuler.
top_tags = pd.read_csv(BASE_DIR / "hasil_get_top_tags.csv")
fig, ax = plt.subplots(figsize=(10, 5.8))
sns.barplot(
    data=top_tags,
    x="question_count",
    y="tag",
    color="#4f86d9",
    ax=ax,
)
ax.set_title("10 Tag Stack Overflow Terpopuler", weight="bold")
ax.set_xlabel("Jumlah pertanyaan")
ax.set_ylabel("Tag")
ax.ticklabel_format(style="plain", axis="x")
for container in ax.containers:
    ax.bar_label(container, fmt="{:,.0f}", padding=4, fontsize=8)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "01_top_tags.png", bbox_inches="tight")
plt.close(fig)

# Grafik 2: tren tahunan lima tag utama.
trend = pd.read_csv(BASE_DIR / "hasil_compare_tags.csv")
trend["year"] = trend["year"].astype(int)
trend["question_count"] = pd.to_numeric(trend["question_count"])
fig, ax = plt.subplots(figsize=(10, 5.8))
sns.lineplot(
    data=trend,
    x="year",
    y="question_count",
    hue="tag",
    marker="o",
    linewidth=2.2,
    ax=ax,
)
ax.set_title("Tren Tahunan Lima Tag Terpopuler (Data Aktual 2020–2022)", weight="bold")
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah pertanyaan")
ax.set_xticks(sorted(trend["year"].unique()))
ax.ticklabel_format(style="plain", axis="y")
ax.legend(title="Tag", frameon=True)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "02_tren_tahunan.png", bbox_inches="tight")
plt.close(fig)

# Grafik 3: pertumbuhan tahunan.
trend_matrix = (
    trend.pivot(index="tag", columns="year", values="question_count")
    .fillna(0)
    .astype(float)
)
growth = (
    trend_matrix.pct_change(axis=1, fill_method=None)
    .replace([float("inf"), -float("inf")], float("nan"))
    * 100
)
growth = growth.dropna(axis=1, how="all")
fig, ax = plt.subplots(figsize=(8.5, 4.5))
sns.heatmap(
    growth,
    annot=True,
    fmt=".1f",
    cmap="RdYlGn",
    center=0,
    linewidths=0.5,
    cbar_kws={"label": "Pertumbuhan (%)"},
    ax=ax,
)
ax.set_title("Pertumbuhan Jumlah Pertanyaan dari Tahun Sebelumnya (%)", weight="bold")
ax.set_xlabel("Tahun")
ax.set_ylabel("Tag")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "03_pertumbuhan_tahunan.png", bbox_inches="tight")
plt.close(fig)

# Grafik 4: kualitas respons dari CSV ekspor interaktif terakhir (tiga tag).
quality = pd.read_csv(BASE_DIR / "hasil_get_answer_rate.csv")
quality_long = quality.melt(
    id_vars="tag",
    value_vars=["answered_rate_pct", "accepted_answer_rate_pct"],
    var_name="metric",
    value_name="percent",
)
quality_long["metric"] = quality_long["metric"].map(
    {
        "answered_rate_pct": "Answered rate",
        "accepted_answer_rate_pct": "Accepted-answer rate",
    }
)
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.barplot(
    data=quality_long,
    x="tag",
    y="percent",
    hue="metric",
    palette=["#4f6fa3", "#d08a60"],
    ax=ax,
)
ax.set_title("Kualitas Respons Python, JavaScript, dan Java", weight="bold")
ax.set_xlabel("Tag")
ax.set_ylabel("Persentase (%)")
ax.set_ylim(0, 85)
ax.legend(title="Metrik", loc="upper left", bbox_to_anchor=(1.01, 1))
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f%%", padding=3, fontsize=8)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "04_kualitas_respons.png", bbox_inches="tight")
plt.close(fig)

print(f"Empat grafik laporan tersimpan di: {OUTPUT_DIR}")

# Infografik editorial berukuran tepat 1080 x 1350 px untuk unggahan LinkedIn.
top_five = top_tags.head(5).copy()
quality_five = pd.DataFrame(
    {
        "tag": ["python", "javascript", "reactjs", "c#", "java"],
        "answered_rate_pct": [77.14, 76.42, 74.51, 73.86, 72.65],
        "accepted_answer_rate_pct": [43.11, 42.35, 38.71, 40.83, 36.35],
    }
)

BG = "#F3F6FB"
NAVY = "#0B1F3A"
BLUE = "#3978F6"
SKY = "#66C7FF"
CORAL = "#FF7A66"
INK = "#14243A"
MUTED = "#66758A"
WHITE = "#FFFFFF"
BORDER = "#E3E9F2"

fig = plt.figure(figsize=(10.8, 13.5), dpi=100, facecolor=BG)
canvas = fig.add_axes([0, 0, 1, 1])
canvas.set_xlim(0, 1)
canvas.set_ylim(0, 1)
canvas.axis("off")


def rounded_card(x, y, width, height, color=WHITE, radius=0.022, edgecolor="none"):
    card = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        linewidth=1,
        facecolor=color,
        edgecolor=edgecolor,
        transform=canvas.transAxes,
    )
    canvas.add_patch(card)
    return card


# Header dengan aksen abstrak agar terasa seperti infografik, bukan screenshot dashboard.
canvas.add_patch(
    FancyBboxPatch(
        (0, 0.765),
        1,
        0.255,
        boxstyle="square,pad=0",
        facecolor=NAVY,
        edgecolor="none",
        transform=canvas.transAxes,
    )
)
canvas.add_patch(Circle((0.93, 0.98), 0.17, color=BLUE, alpha=0.24, transform=canvas.transAxes))
canvas.add_patch(Circle((0.86, 0.77), 0.10, color=SKY, alpha=0.16, transform=canvas.transAxes))
canvas.text(
    0.065,
    0.958,
    "DATA ANALYTICS  •  REACT AGENT",
    color=SKY,
    fontsize=11,
    fontweight="bold",
    va="top",
    transform=canvas.transAxes,
)
canvas.text(
    0.065,
    0.920,
    "Banyak ditanyakan\n≠ respons terbaik",
    color=WHITE,
    fontsize=31,
    fontweight="bold",
    linespacing=1.05,
    va="top",
    transform=canvas.transAxes,
)
canvas.text(
    0.065,
    0.805,
    "Membaca aktivitas Stack Overflow melalui data, bukan asumsi.",
    color="#D5E2F3",
    fontsize=12.5,
    va="top",
    transform=canvas.transAxes,
)
rounded_card(0.745, 0.855, 0.19, 0.078, color="#15345E", radius=0.018)
canvas.text(0.77, 0.910, "STACK OVERFLOW", color=SKY, fontsize=9, fontweight="bold", transform=canvas.transAxes)
canvas.text(0.77, 0.875, "2020–2025", color=WHITE, fontsize=16, fontweight="bold", transform=canvas.transAxes)

# Tiga temuan utama.
cards = [
    (0.065, "750.502", "PYTHON", "pertanyaan terbanyak", BLUE),
    (0.375, "−45,9%", "JAVA", "penurunan 2020–2022", CORAL),
    (0.685, "735,49", "REACTJS", "rata-rata view tertinggi", "#22A98A"),
]
for x, value, label, note, accent in cards:
    rounded_card(x, 0.650, 0.25, 0.088, edgecolor=BORDER)
    canvas.add_patch(
        FancyBboxPatch(
            (x, 0.650),
            0.012,
            0.088,
            boxstyle="round,pad=0,rounding_size=0.006",
            facecolor=accent,
            edgecolor="none",
            transform=canvas.transAxes,
        )
    )
    canvas.text(x + 0.028, 0.713, label, color=accent, fontsize=9.5, fontweight="bold", transform=canvas.transAxes)
    canvas.text(x + 0.028, 0.677, value, color=INK, fontsize=21, fontweight="bold", transform=canvas.transAxes)
    canvas.text(x + 0.028, 0.658, note, color=MUTED, fontsize=8.5, transform=canvas.transAxes)

# Ranking volume, ditampilkan sebagai satu cerita visual utama.
rounded_card(0.065, 0.373, 0.87, 0.238, edgecolor=BORDER)
canvas.text(0.095, 0.578, "TOPIK PALING AKTIF", color=BLUE, fontsize=9.5, fontweight="bold", transform=canvas.transAxes)
canvas.text(0.095, 0.550, "Lima tag dengan volume pertanyaan terbesar", color=INK, fontsize=16, fontweight="bold", transform=canvas.transAxes)
canvas.text(0.095, 0.526, "Akumulasi hasil query periode 2020–2025", color=MUTED, fontsize=9.5, transform=canvas.transAxes)

rank_ax = fig.add_axes([0.115, 0.405, 0.76, 0.105])
rank_ax.set_facecolor(WHITE)
rank_colors = [BLUE, "#6C9AF8", "#8BB0F9", "#AAC7FB", "#CADDFD"]
rank_ax.barh(top_five["tag"], top_five["question_count"], color=rank_colors, height=0.58)
rank_ax.invert_yaxis()
rank_ax.set_xlim(0, 820000)
rank_ax.axis("off")
for index, (tag, value) in enumerate(zip(top_five["tag"], top_five["question_count"])):
    rank_ax.text(-17000, index, tag.upper(), ha="right", va="center", color=INK, fontsize=10, fontweight="bold")
    rank_ax.text(value + 11000, index, f"{value:,.0f}".replace(",", "."), va="center", color=INK, fontsize=9.5, fontweight="bold")

# Perbandingan kualitas respons.
rounded_card(0.065, 0.140, 0.87, 0.198, edgecolor=BORDER)
canvas.text(0.095, 0.306, "KUALITAS RESPONS", color=BLUE, fontsize=9.5, fontweight="bold", transform=canvas.transAxes)
canvas.text(0.095, 0.280, "Dijawab vs jawaban diterima", color=INK, fontsize=14.5, fontweight="bold", transform=canvas.transAxes)
canvas.text(0.095, 0.258, "Persentase seluruh pertanyaan", color=MUTED, fontsize=9, transform=canvas.transAxes)

quality_ax = fig.add_axes([0.105, 0.167, 0.79, 0.077])
quality_ax.set_facecolor(WHITE)
x_positions = list(range(len(quality_five)))
width = 0.32
quality_ax.bar(
    [value - width / 2 for value in x_positions],
    quality_five["answered_rate_pct"],
    width,
    label="Dijawab",
    color=BLUE,
)
quality_ax.bar(
    [value + width / 2 for value in x_positions],
    quality_five["accepted_answer_rate_pct"],
    width,
    label="Diterima",
    color=CORAL,
)
quality_ax.set_ylim(0, 88)
quality_ax.set_xticks(x_positions, ["Python", "JS", "React", "C#", "Java"], fontsize=8.5)
quality_ax.set_yticks([])
quality_ax.grid(False)
quality_ax.spines[:].set_visible(False)
quality_ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=2, frameon=False, fontsize=8)
for container in quality_ax.containers:
    quality_ax.bar_label(container, fmt="%.1f", padding=2, fontsize=6.8, color=MUTED)

# Footer metodologi dan batasan cakupan.
canvas.plot([0.065, 0.935], [0.105, 0.105], color="#D9E1EC", linewidth=1, transform=canvas.transAxes)
canvas.text(0.065, 0.079, "REACT AGENT  +  BIGQUERY  +  GEMINI", color=INK, fontsize=9.5, fontweight="bold", transform=canvas.transAxes)
canvas.text(
    0.065,
    0.050,
    "Query: 2020–2025  •  Data tren aktual: 2020–2022  •  Aktivitas Stack Overflow ≠ adopsi industri",
    color=MUTED,
    fontsize=8.8,
    transform=canvas.transAxes,
)
fig.savefig(
    OUTPUT_DIR / "05_linkedin_summary.png",
    dpi=100,
    facecolor=fig.get_facecolor(),
)
plt.close(fig)

print(f"Visual LinkedIn tersimpan di: {OUTPUT_DIR / '05_linkedin_summary.png'}")
