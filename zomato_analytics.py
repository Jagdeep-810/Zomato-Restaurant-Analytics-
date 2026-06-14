"""
============================================================
  Zomato Restaurant Analytics
  Author  : <Your Name>
  Purpose : End-to-end data analysis pipeline — data
            generation → cleaning → insights → visualisation
============================================================
"""

import io
import textwrap

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# ── Visual theme (set once, applies to all charts) ────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "axes.titlesize": 13,
                     "axes.labelsize": 11})


# ═══════════════════════════════════════════════════════════
# SECTION 1 — MOCK DATASET GENERATION
# Why: Eliminates the need to download an external file;
#      the data mirrors the real Zomato Kaggle schema.
# ═══════════════════════════════════════════════════════════

def generate_mock_data() -> pd.DataFrame:
    """Return a 50-row DataFrame that mimics the Zomato dataset."""

    raw_csv = textwrap.dedent("""
    name,location,approx_cost(for_two_people),rate,votes,online_order,cuisines
    Truffles,Koramangala,"800","4.1/5",1000,Yes,"Burgers, American"
    MTR 1924,Lalbagh,"600","4.4/5",3200,No,"South Indian, Breakfast"
    Toit,Indiranagar,"1,500","4.5/5",4800,No,"Beverages, Continental"
    Meghana Foods,Koramangala,"1,000","4.3/5",2100,Yes,"Biryani, Andhra"
    Barbeque Nation,Indiranagar,"1,800","3.9/5",5600,Yes,"BBQ, North Indian"
    The Black Pearl,Whitefield,"2,000","4.2/5",980,No,"Seafood, Continental"
    Pind Balluchi,Koramangala,"1,200","3.8/5",760,Yes,"North Indian, Mughlai"
    Empire Restaurant,Shivajinagar,"700","3.7/5",4100,Yes,"North Indian, Biryani"
    Brahmin's Coffee Bar,Shivajinagar,"200","4.6/5",2900,No,"South Indian, Breakfast"
    Koshy's,Shivajinagar,"800","4.3/5",3400,No,"Continental, Bakery"
    Fatty Bao,Indiranagar,"1,400","4.0/5",1500,Yes,"Asian, Chinese"
    The Permit Room,Indiranagar,"1,200","4.1/5",2200,Yes,"South Indian, Beverages"
    Hammered,Koramangala,"1,600","4.2/5",870,No,"Continental, American"
    Flechazo,Koramangala,"1,800","4.3/5",1100,No,"Mediterranean, Continental"
    Onesta,JP Nagar,"900","4.4/5",3300,Yes,"Italian, Pizza"
    Pizza Hut,JP Nagar,"600","3.5/5",2000,Yes,"Pizza, Italian"
    KFC,Whitefield,"500","3.6/5",3100,Yes,"Fast Food, American"
    Domino's Pizza,Whitefield,"400","3.4/5",5200,Yes,"Pizza, Fast Food"
    Chutney Chang,Koramangala,"600","3.9/5",1400,Yes,"South Indian, Chinese"
    Glen's Bakehouse,Indiranagar,"800","4.5/5",2600,No,"Bakery, Desserts"
    Toast & Tonic,Indiranagar,"2,000","4.4/5",3800,No,"Continental, European"
    Windmills Craftworks,Whitefield,"1,500","4.3/5",1700,No,"Beverages, Continental"
    Social,Koramangala,"1,200","4.0/5",4500,Yes,"Continental, American"
    Smoke House Deli,Indiranagar,"1,600","4.1/5",2300,No,"Continental, European"
    The Humming Tree,Indiranagar,"1,400","4.0/5",900,No,"Beverages, Continental"
    Hole in the Wall Cafe,Koramangala,"1,000","4.2/5",1600,Yes,"Continental, Cafe"
    Sunny's,Indiranagar,"2,200","4.0/5",1200,No,"Italian, Continental"
    Oota,JP Nagar,"1,100","4.5/5",800,No,"Karnataka, South Indian"
    Brahmin's Coffee Bar,Basavanagudi,"200","4.7/5",1800,No,"South Indian, Breakfast"
    Airlines Hotel,Shivajinagar,"400","4.2/5",2700,No,"South Indian, Breakfast"
    Fleury's,Shivajinagar,"600","4.1/5",1300,No,"Bakery, Desserts"
    The Taj West End,Shivajinagar,"4,000","4.6/5",700,No,"Continental, European"
    Casa Del Sol,Koramangala,"1,800","4.0/5",650,No,"Mexican, Continental"
    Punjabi By Nature,Indiranagar,"1,400","3.8/5",1100,Yes,"North Indian, Punjabi"
    Sarvanna Bhavan,Lalbagh,"500","4.2/5",3600,No,"South Indian"
    Subbaiah Hotel,Basavanagudi,"300","4.0/5",900,No,"South Indian, Breakfast"
    Adigas,JP Nagar,"350","3.9/5",1400,Yes,"South Indian"
    Biryani Zone,Whitefield,"700","4.1/5",2100,Yes,"Biryani, Hyderabadi"
    Absolute Barbecue,Whitefield,"1,500","4.3/5",3200,Yes,"BBQ, North Indian"
    Punjabi Tadka,Whitefield,"800","3.8/5",1700,Yes,"North Indian, Punjabi"
    Mainland China,Koramangala,"1,600","3.9/5",2400,Yes,"Chinese, Seafood"
    Shiro,Indiranagar,"2,500","4.1/5",1600,No,"Japanese, Asian"
    Caperberry,Indiranagar,"2,000","4.4/5",1100,No,"European, Continental"
    The Fatty Bao,Koramangala,"1,400","NEW",0,Yes,"Asian, Chinese"
    Mavalli Tiffin Room,Lalbagh,,,"500",No,"South Indian, Breakfast"
    Vidyarthi Bhavan,Basavanagudi,"300","4.4/5",4100,No,"South Indian, Breakfast"
    Taaza Thindi,JP Nagar,"250","4.3/5",2800,No,"South Indian, Breakfast"
    Corner House,Koramangala,"300","4.5/5",5100,Yes,"Desserts, Ice Cream"
    Jamavar,Lalbagh,"3,500","4.6/5",800,No,"North Indian, Mughlai"
    Rim Naam,Whitefield,"2,800","4.2/5",950,No,"Thai, Asian"
    """).strip()

    df = pd.read_csv(io.StringIO(raw_csv))
    return df


# ═══════════════════════════════════════════════════════════
# SECTION 2 — DATA CLEANING & PREPROCESSING
# ═══════════════════════════════════════════════════════════

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all cleaning steps and return a ready-to-analyse DataFrame.
    Each step is documented so intent is clear during a code review.
    """
    df = df.copy()   # avoid mutating the raw frame

    # ── 2a. Standardise text columns ──────────────────────
    # Strip leading/trailing whitespace and normalise to Title Case
    # so "koramangala", "Koramangala " etc. all map to the same key.
    df["location"] = df["location"].str.strip().str.title()
    df["name"]     = df["name"].str.strip()

    # ── 2b. Clean 'approx_cost' ───────────────────────────
    # Raw values look like "1,200" or "" — convert to plain int.
    # errors='coerce' silently turns unparseable strings into NaN.
    df["approx_cost(for_two_people)"] = (
        df["approx_cost(for_two_people)"]
        .astype(str)
        .str.replace(",", "", regex=False)   # remove thousand-separator
        .str.strip()
        .replace("nan", np.nan)              # turn the string "nan" back to NaN
    )
    df["approx_cost(for_two_people)"] = pd.to_numeric(
        df["approx_cost(for_two_people)"], errors="coerce"
    )

    # Impute missing cost with the median (robust to outliers)
    median_cost = df["approx_cost(for_two_people)"].median()
    df["approx_cost(for_two_people)"] = (
        df["approx_cost(for_two_people)"].fillna(median_cost).astype(int)
    )

    # ── 2c. Clean 'rate' ──────────────────────────────────
    # Possible formats: "4.1/5", "NEW", NaN
    # We extract only the numeric part before the slash.
    df["rate"] = (
        df["rate"]
        .astype(str)
        .str.split("/").str[0]   # keep "4.1" from "4.1/5"
        .str.strip()
        .replace({"NEW": np.nan, "nan": np.nan, "-": np.nan})
    )
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

    # Impute missing ratings with the column median
    median_rate = df["rate"].median()
    df["rate"] = df["rate"].fillna(median_rate)

    # ── 2d. Ensure 'votes' is numeric ─────────────────────
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)

    # ── 2e. Normalise 'online_order' ──────────────────────
    df["online_order"] = df["online_order"].str.strip().str.title()  # Yes / No

    print("✔ Cleaning complete — shape:", df.shape)
    print(df.dtypes, "\n")
    return df


# ═══════════════════════════════════════════════════════════
# SECTION 3 — ANALYSIS & INSIGHTS
# ═══════════════════════════════════════════════════════════

def run_analysis(df: pd.DataFrame) -> dict:
    """Compute key business metrics and return them in a dict."""

    # ── 3a. Average cost per location ─────────────────────
    # Useful for understanding which areas are affordable.
    avg_cost_by_location = (
        df.groupby("location")["approx_cost(for_two_people)"]
        .mean()
        .round(0)
        .astype(int)
        .sort_values(ascending=False)
    )

    # ── 3b. Most popular cuisines (by total votes) ────────
    # A restaurant may list multiple cuisines separated by commas,
    # so we explode the list to count each cuisine individually.
    cuisine_votes = (
        df.assign(cuisines=df["cuisines"].str.split(","))
        .explode("cuisines")
        .assign(cuisines=lambda x: x["cuisines"].str.strip())
        .groupby("cuisines")["votes"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    # ── 3c. Online order impact on ratings ────────────────
    # A simple group comparison to test the hypothesis:
    # "Do restaurants with online ordering get rated differently?"
    online_vs_rating = (
        df.groupby("online_order")["rate"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "avg_rating", "count": "num_restaurants"})
        .round(2)
    )

    # ── 3d. Best-rated affordable restaurants ─────────────
    # Define "affordable" as cost ≤ median cost and "well-rated"
    # as rating ≥ 75th percentile — keeps the filter meaningful.
    cost_threshold   = df["approx_cost(for_two_people)"].median()
    rating_threshold = df["rate"].quantile(0.75)

    best_affordable = (
        df[
            (df["approx_cost(for_two_people)"] <= cost_threshold) &
            (df["rate"] >= rating_threshold)
        ]
        [["name", "location", "approx_cost(for_two_people)", "rate", "votes"]]
        .sort_values("rate", ascending=False)
        .drop_duplicates(subset="name")
    )

    # ── Print summary to console ──────────────────────────
    print("=" * 55)
    print("INSIGHT 1 — Average Cost for Two by Location")
    print("=" * 55)
    print(avg_cost_by_location.to_string(), "\n")

    print("=" * 55)
    print("INSIGHT 2 — Top 10 Cuisines by Total Votes")
    print("=" * 55)
    print(cuisine_votes.to_string(), "\n")

    print("=" * 55)
    print("INSIGHT 3 — Online Order vs Avg Rating")
    print("=" * 55)
    print(online_vs_rating.to_string(), "\n")

    print("=" * 55)
    print(f"INSIGHT 4 — Best-Rated Affordable Restaurants")
    print(f"           (cost ≤ ₹{int(cost_threshold)}, "
          f"rating ≥ {rating_threshold:.1f})")
    print("=" * 55)
    print(best_affordable.to_string(index=False), "\n")

    return {
        "avg_cost_by_location": avg_cost_by_location,
        "cuisine_votes":        cuisine_votes,
        "online_vs_rating":     online_vs_rating,
        "best_affordable":      best_affordable,
        "cost_threshold":       cost_threshold,
        "rating_threshold":     rating_threshold,
    }


# ═══════════════════════════════════════════════════════════
# SECTION 4 — VISUALISATION
# ═══════════════════════════════════════════════════════════

def plot_all(df: pd.DataFrame, insights: dict) -> None:
    """Produce and save three charts as a single PNG file."""

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Zomato Restaurant Analytics Dashboard",
                 fontsize=16, fontweight="bold", y=1.02)

    # ── Chart 1: Best-Rated Affordable Food Hubs ──────────
    ax1 = axes[0]
    hub_df = (
        insights["best_affordable"]
        .groupby("location")
        .agg(avg_rating=("rate", "mean"),
             num_restaurants=("name", "count"))
        .reset_index()
        .sort_values("avg_rating", ascending=True)
    )
    bars = ax1.barh(
        hub_df["location"], hub_df["avg_rating"],
        color=sns.color_palette("Greens_d", len(hub_df))
    )
    # Annotate each bar with the restaurant count
    for bar, count in zip(bars, hub_df["num_restaurants"]):
        ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                 f"{count} place{'s' if count > 1 else ''}",
                 va="center", fontsize=8, color="#333")
    ax1.set_title(
        f"Best-Rated Affordable Food Hubs\n"
        f"(Cost ≤ ₹{int(insights['cost_threshold'])}  |  "
        f"Rating ≥ {insights['rating_threshold']:.1f})",
        pad=10
    )
    ax1.set_xlabel("Average Rating")
    ax1.set_xlim(0, 5.5)   # leave room for annotations
    ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))

    # ── Chart 2: Online Ordering Impact on Ratings ────────
    ax2 = axes[1]
    ov = insights["online_vs_rating"].reset_index()
    palette = {"Yes": "#4CAF50", "No": "#F44336"}
    bar_colors = [palette.get(x, "#999") for x in ov["online_order"]]
    bars2 = ax2.bar(ov["online_order"], ov["avg_rating"],
                    color=bar_colors, width=0.45, edgecolor="white")
    # Show the exact rating on top of each bar
    for bar, val in zip(bars2, ov["avg_rating"]):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.03,
                 f"{val:.2f}", ha="center", fontsize=11, fontweight="bold")
    ax2.set_title("Impact of Online Ordering on Avg Rating", pad=10)
    ax2.set_xlabel("Online Order Available")
    ax2.set_ylabel("Average Rating (out of 5)")
    ax2.set_ylim(0, 5.5)
    ax2.tick_params(axis="x", labelsize=11)

    # ── Chart 3: Top 10 Cuisines by Total Votes ───────────
    ax3 = axes[2]
    cv = insights["cuisine_votes"].reset_index()
    cv.columns = ["cuisine", "votes"]
    cv = cv.sort_values("votes", ascending=True)   # ascending for horizontal bar
    colors = sns.color_palette("Blues_d", len(cv))
    ax3.barh(cv["cuisine"], cv["votes"], color=colors)
    ax3.set_title("Top 10 Cuisines by Total Votes", pad=10)
    ax3.set_xlabel("Total Votes")
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{int(x):,}"
    ))

    plt.tight_layout()
    out_path = "/mnt/user-data/outputs/zomato_dashboard.png"
    plt.savefig(out_path, bbox_inches="tight")
    print(f"✔ Dashboard saved → {out_path}")
    plt.close()


# ═══════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════

def main():
    print("\n── Step 1: Generate mock dataset ──")
    raw_df = generate_mock_data()
    print(f"   Rows: {len(raw_df)}  |  Columns: {list(raw_df.columns)}\n")

    print("── Step 2: Clean & preprocess ──")
    clean_df = clean_data(raw_df)

    print("── Step 3: Run analysis ──")
    insights = run_analysis(clean_df)

    print("── Step 4: Visualise ──")
    plot_all(clean_df, insights)

    print("\n✅  All done!")


if __name__ == "__main__":
    main()
