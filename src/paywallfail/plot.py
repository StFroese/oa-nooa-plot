import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data.csv")

    y = range(len(df))

    values = df["ratio_avg_cites"]
    fields = df["field"]
    domains = df["domain"]

    plt.figure(figsize=(10, 7))
    for domain in sorted(set(domains)):
        mask = domains == domain
        plt.scatter(
            values[mask],
            [i for i, m in enumerate(mask) if m],
            label=domain,
        )
    plt.vlines(1, -1, y[-1] + 1, color="gray", ls="--")
    plt.yticks(y, fields)
    plt.ylim(-1, y[-1] + 0.5)
    plt.gca().invert_yaxis()  # biggest ratio at the top
    plt.legend(loc="lower right", frameon=False)
    plt.xlabel("OA / non-OA mean-citation ratio")
    plt.tight_layout()
    plt.savefig("OSvsNOA.pdf")


if __name__ == "__main__":
    main()
