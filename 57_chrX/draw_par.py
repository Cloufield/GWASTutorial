import matplotlib.pyplot as plt
import numpy as np

def plot_xy_with_par(build="hg38", figsize=(12, 4), save_path=None):
    """
    Plot chrX and chrY with PAR regions highlighted.
    
    Parameters
    ----------
    build : str
        Genome build, either 'hg19' or 'hg38'
    figsize : tuple
        Figure size (width, height)
    save_path : str, optional
        Path to save the figure. If None, displays the figure.
    """
    PAR = {
        "hg19": {
            "PAR1": (60001, 2699520),
            "PAR2": (154931044, 155260560),
            "X_LEN": 155270560,
            "Y_LEN": 59373566,
            "X_CEN": 60000000,
            "Y_CEN": 12000000,
        },
        "hg38": {
            "PAR1": (10001, 2781479),
            "PAR2": (155701383, 156030895),
            "X_LEN": 156040895,
            "Y_LEN": 57227415,
            "X_CEN": 61000000,
            "Y_CEN": 12500000,
        },
    }
    if build not in PAR:
        raise ValueError("build must be 'hg19' or 'hg38'")

    par1 = PAR[build]["PAR1"]
    par2 = PAR[build]["PAR2"]
    X_LEN = PAR[build]["X_LEN"]
    Y_LEN = PAR[build]["Y_LEN"]
    X_CEN = PAR[build]["X_CEN"]
    Y_CEN = PAR[build]["Y_CEN"]

    fig, ax = plt.subplots(figsize=figsize)

    y_pos = {"X": 1.0, "Y": 0.0}
    bar_h = 0.35

    # --- chromosome baselines ---
    ax.broken_barh([(0, X_LEN)], (y_pos["X"] - bar_h / 2, bar_h), alpha=0.15)
    ax.broken_barh([(0, Y_LEN)], (y_pos["Y"] - bar_h / 2, bar_h), alpha=0.15)

    # --- PAR on chrX ---
    ax.broken_barh(
        [
            (par1[0], par1[1] - par1[0] + 1),
            (par2[0], par2[1] - par2[0] + 1),
        ],
        (y_pos["X"] - bar_h / 2, bar_h),
        alpha=0.6,
        label=f"PAR ({build})",
    )

    # --- PAR on chrY ---
    par1_len = par1[1] - par1[0] + 1
    par2_len = par2[1] - par2[0] + 1

    ax.broken_barh([(0, par1_len)],
                   (y_pos["Y"] - bar_h / 2, bar_h),
                   alpha=0.6)
    ax.broken_barh([(Y_LEN - par2_len, par2_len)],
                   (y_pos["Y"] - bar_h / 2, bar_h),
                   alpha=0.6)

    # --- centromeres ---
    ax.vlines(X_CEN, y_pos["X"] - bar_h / 2, y_pos["X"] + bar_h / 2,
              color="black", linewidth=2)
    ax.vlines(Y_CEN, y_pos["Y"] - bar_h / 2, y_pos["Y"] + bar_h / 2,
              color="black", linewidth=2)

    # --- annotations (chrX only) ---
    ax.text((par1[0] + par1[1]) / 2, y_pos["X"] + 0.42, "PAR1", ha="center")
    ax.text((par2[0] + par2[1]) / 2, y_pos["X"] + 0.42, "PAR2", ha="center")

    # --- dashed grey linkage lines (start & end of each PAR) ---
    link_kw = dict(color="grey", linestyle="--", linewidth=1)

    # PAR1
    ax.plot([par1[0], 0],
            [y_pos["X"] - bar_h / 2, y_pos["Y"] + bar_h / 2],
            **link_kw)
    ax.plot([par1[1], par1_len],
            [y_pos["X"] - bar_h / 2, y_pos["Y"] + bar_h / 2],
            **link_kw)

    # PAR2
    ax.plot([par2[0], Y_LEN - par2_len],
            [y_pos["X"] - bar_h / 2, y_pos["Y"] + bar_h / 2],
            **link_kw)
    ax.plot([par2[1], Y_LEN],
            [y_pos["X"] - bar_h / 2, y_pos["Y"] + bar_h / 2],
            **link_kw)

    # --- axes & ticks ---
    ax.set_yticks([y_pos["X"], y_pos["Y"]])
    ax.set_yticklabels(["Chr X", "Chr Y"])
    ax.set_xlabel("Position (Mb)")
    ax.set_title("chrX / chrY PAR regions ")

    max_mb = int(np.ceil(X_LEN / 1e6))
    major = np.arange(0, max_mb + 1, 10) * 1e6
    minor = np.arange(0, max_mb + 1, 5) * 1e6

    ax.set_xticks(major)
    ax.set_xticks(minor, minor=True)
    ax.set_xticklabels([f"{int(x/1e6)}" for x in major])

    ax.tick_params(axis="x", which="major", length=6)
    ax.tick_params(axis="x", which="minor", length=3)

    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_ylim(-0.8, 1.8)
    ax.legend(frameon=False)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


if __name__ == "__main__":
    import os
    
    # Get the script directory and construct the output path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "docs", "images", "chrXY_PAR_regions.png")
    output_path = os.path.normpath(output_path)
    
    plot_xy_with_par(build="hg38", save_path=output_path)
