import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data.csv")

    y = range(len(df))

    values = df["ratio_avg_cites"]
    fields = df["field"]

    plt.figure(figsize=(10, 7))
    plt.scatter(values, y)  # points, not bars
    plt.yticks(y, fields)
    plt.gca().invert_yaxis()  # biggest ratio at the top
    plt.xlabel("OA / non-OA mean-citation ratio")
    plt.title("Citation advantage of OA vs non-OA by field")
    plt.tight_layout()
    plt.savefig("OSvsNOA.pdf")


if __name__ == "__main__":
    main()
