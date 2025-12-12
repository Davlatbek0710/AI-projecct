from io import BytesIO
import matplotlib.pyplot as plt

def make_table_png(bins):
    rows = []
    for b in bins:
        items_str = ", ".join(str(x) for x in b["items"])
        rows.append([b["id"], items_str, b["load"]])

    fig, ax = plt.subplots(figsize=(4, 1 + 0.4 * len(rows)))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=["Bin #", "Items (desc.)", "Load"],
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf