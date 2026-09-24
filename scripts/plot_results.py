"""Regenerate figures/00_deformation_vs_mass.png from data/results.csv."""
import pandas as pd, matplotlib.pyplot as plt
df = pd.read_csv("data/results.csv"); fr = df[df.impact == "front"]
base = fr[fr.case == "Baseline"].iloc[0]; att = fr[fr.case != "Baseline"]
colors = {"Kevlar-29/Epoxy": "#2a78d6", "P707AG-15/2510": "#eb6834", "T650/Epoxy (est.)": "#1baf7a"}
ink, muted, grid = "#1f1f1e", "#6b6a64", "#e6e5df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, ax = plt.subplots(figsize=(8, 4.6), dpi=160)
ax.axhline(base.max_enclosure_deformation_mm, color=muted, lw=1.2, ls="--")
ax.text(1, base.max_enclosure_deformation_mm + 0.2, f"Baseline, no attenuator: {base.max_enclosure_deformation_mm} mm", color=muted, fontsize=9)
ax.axhline(5, color=muted, lw=1.2, ls=":")
ax.text(1, 5.2, "Design target: 5 mm", color=muted, fontsize=9)
for mat, g in att.groupby("material_system", sort=False):
    ax.scatter(g.added_mass_kg, g.max_enclosure_deformation_mm, s=70, color=colors[mat], edgecolor="white", linewidth=2, zorder=3, label=mat)
    for _, r in g.iterrows():
        dy = 0.35 if "0,45" in r.layup else -0.55
        tag = "quasi" if "0,0,45" in r.layup else "0° core"
        ax.text(r.added_mass_kg + 1.5, r.max_enclosure_deformation_mm + dy, f"{r.case} ({tag}) {r.max_enclosure_deformation_mm} mm", fontsize=8, color=ink, va="center")
ax.set_xlim(0, 95); ax.set_ylim(0, 14)
ax.set_xlabel("Attenuator added mass (kg)", color=ink); ax.set_ylabel("Peak enclosure deformation (mm)", color=ink)
ax.set_title("Front impact at 13.86 m/s: deformation vs. mass penalty", loc="left", color=ink, fontsize=12)
ax.grid(axis="y", color=grid, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(muted)
ax.tick_params(colors=muted)
ax.legend(frameon=False, loc="lower right", fontsize=9)
fig.tight_layout(); fig.savefig("figures/00_deformation_vs_mass.png", facecolor="white")
