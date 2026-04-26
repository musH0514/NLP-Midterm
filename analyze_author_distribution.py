from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


TARGET_YEARS = [1991, 2000, 2010, 2020, 2024]

US_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC",
}

COUNTRY_ALIASES = {
    "USA": "United States",
    "U S A": "United States",
    "UNITED STATES": "United States",
    "UNITED STATES OF AMERICA": "United States",
    "US": "United States",
    "PR USA": "United States",
    "ENGLAND": "United Kingdom",
    "SCOTLAND": "United Kingdom",
    "WALES": "United Kingdom",
    "NORTHERN IRELAND": "United Kingdom",
    "NORTH IRELAND": "United Kingdom",
    "UK": "United Kingdom",
    "U K": "United Kingdom",
    "UNITED KINGDOM": "United Kingdom",
    "GREAT BRITAIN": "United Kingdom",
    "HONG KONG": "China",
    "HONG KONG SAR": "China",
    "TAIWAN": "China",
    "MACAO": "China",
    "MACAU": "China",
    "PEOPLE S REPUBLIC OF CHINA": "China",
    "PEOPLES REPUBLIC OF CHINA": "China",
    "PEOPLES R CHINA": "China",
    "PEOPLE S R CHINA": "China",
    "P R CHINA": "China",
    "P R C": "China",
    "PRC": "China",
    "MAINLAND CHINA": "China",
    "U ARAB EMIRATES": "United Arab Emirates",
    "TURKIYE": "Turkey",
}


def normalize_text(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", " ", value.upper()).strip()


def extract_country(address: str) -> str | None:
    if not isinstance(address, str) or not address.strip():
        return None

    parts = [part.strip() for part in address.split(",") if part.strip()]
    if not parts:
        return None

    last_normalized = normalize_text(parts[-1])
    if not last_normalized:
        return None

    if last_normalized in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[last_normalized]

    if last_normalized.startswith("SINGAPORE"):
        return "Singapore"

    first_token = last_normalized.split(" ", 1)[0]
    if first_token in US_STATE_CODES:
        return "United States"

    if last_normalized in {"UK", "UNITED KINGDOM", "GREAT BRITAIN"}:
        return "United Kingdom"

    if last_normalized in {"CHINA", "PEOPLES REPUBLIC OF CHINA", "PEOPLES R CHINA", "P R CHINA"}:
        return "China"

    return last_normalized.title()


def load_data(input_file: Path) -> pd.DataFrame:
    df = pd.read_csv(input_file, encoding="utf-8-sig")
    required_columns = {"name", "address", "year"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in input file: {sorted(missing)}")

    df = df.copy()
    df["name"] = df["name"].astype(str).str.strip()
    df["address"] = df["address"].astype(str).str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["name", "address", "year"])
    return df


def print_name_address_summary(df: pd.DataFrame) -> None:
    address_counts = df.groupby("name")["address"].nunique().sort_values(ascending=False)
    multi_address_people = address_counts[address_counts > 1]

    print(f"Total valid rows: {len(df)}")
    print(f"People with more than one address: {len(multi_address_people)}")
    if not multi_address_people.empty:
        print("Top multi-address people:")
        for name, count in multi_address_people.head(10).items():
            print(f"  {name}: {count} addresses")


def build_yearly_country_counts(df: pd.DataFrame, years: list[int]) -> dict[int, pd.DataFrame]:
    results: dict[int, pd.DataFrame] = {}

    for year in years:
        year_frame = df[df["year"] == year].copy()
        if year_frame.empty:
            results[year] = pd.DataFrame(columns=["country", "people_count"])
            continue

        year_frame["country"] = year_frame["address"].map(extract_country)
        year_frame = year_frame.dropna(subset=["country"])
        year_frame = year_frame.drop_duplicates(subset=["name", "country"])

        counts = (
            year_frame.groupby("country")["name"]
            .nunique()
            .reset_index(name="people_count")
            .sort_values(["people_count", "country"], ascending=[False, True])
        )
        results[year] = counts

    return results


def build_migration_records(df: pd.DataFrame) -> pd.DataFrame:
    work_frame = df.copy()
    work_frame["country"] = work_frame["address"].map(extract_country)
    work_frame = work_frame.dropna(subset=["country"])

    author_country_counts = work_frame.groupby("name")["country"].nunique()
    migrating_authors = author_country_counts[author_country_counts > 1].index

    migration_frame = work_frame[work_frame["name"].isin(migrating_authors)].copy()
    migration_frame = migration_frame.drop_duplicates(subset=["name", "country", "year"])
    migration_frame = migration_frame.sort_values(["name", "year", "country"], ascending=[True, True, True])
    return migration_frame[["name", "country", "year"]]


def build_discrete_color_bins(counts: pd.DataFrame) -> pd.DataFrame:
    if counts.empty:
        return counts.assign(color_bin=pd.Series(dtype="object"))

    binned = counts.copy()
    positive = binned[binned["people_count"] > 0].copy()
    if positive.empty:
        binned["color_bin"] = pd.NA
        return binned

    bin_count = min(5, positive["people_count"].nunique())
    if bin_count <= 1:
        binned["color_bin"] = f"{int(positive['people_count'].iloc[0])}"
        return binned

    categories = pd.qcut(positive["people_count"], q=bin_count, duplicates="drop")
    binned["color_bin"] = pd.NA
    binned.loc[positive.index, "color_bin"] = categories.astype(str)
    return binned


def make_blue_palette(bin_count: int) -> list[str]:
    return px.colors.sample_colorscale("Blues", [0.35 + 0.6 * i / max(bin_count - 1, 1) for i in range(bin_count)])


def save_year_map(counts: pd.DataFrame, year: int, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"author_distribution_{year}.html"
    label_font_size = 9 if year == 2024 else 11

    binned = build_discrete_color_bins(counts)
    positive = binned[binned["people_count"] > 0].copy()

    figure = go.Figure()

    if not positive.empty:
        ordered_positive = positive.sort_values(["people_count", "country"], ascending=[True, True])
        bin_labels = list(dict.fromkeys(ordered_positive["color_bin"].tolist()))
        palette = make_blue_palette(len(bin_labels))

        for label, color in zip(bin_labels, palette, strict=False):
            bin_rows = positive[positive["color_bin"] == label]
            figure.add_trace(
                go.Choropleth(
                    locations=bin_rows["country"],
                    locationmode="country names",
                    z=bin_rows["people_count"],
                    text=bin_rows["country"],
                    name=label,
                    colorscale=[[0, color], [1, color]],
                    showscale=False,
                    marker_line_color="white",
                    marker_line_width=0.4,
                    hovertemplate="Country/region: %{location}<br>People: %{z}<extra></extra>",
                )
            )

        figure.add_trace(
            go.Scattergeo(
                locations=positive["country"],
                locationmode="country names",
                text=positive["people_count"].astype(str),
                mode="markers+text",
                marker=dict(size=6, color="#163f7a", opacity=0.9),
                textposition="top center",
                textfont=dict(size=label_font_size, color="#1f1f1f"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    figure.update_layout(
        title=f"Author distribution in {year}",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showcountries=True,
            showland=True,
            landcolor="#e6e6e6",
            countrycolor="white",
            projection_type="natural earth",
        ),
        legend_title_text="People count range",
        margin=dict(l=0, r=0, t=60, b=0),
    )
    figure.write_html(str(html_path), include_plotlyjs="cdn", full_html=True)
    return html_path


def save_summary_csv(yearly_counts: dict[int, pd.DataFrame], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "yearly_country_counts.csv"
    records = []

    for year, counts in yearly_counts.items():
        for row in counts.itertuples(index=False):
            records.append({"year": year, "country": row.country, "people_count": int(row.people_count)})

    pd.DataFrame(records).to_csv(summary_path, index=False, encoding="utf-8-sig")
    return summary_path


def save_migration_csv(df: pd.DataFrame, output_root: Path) -> tuple[Path, int]:
    migration_path = output_root / "multi_address_author_migrations.csv"
    migration_frame = build_migration_records(df)
    migration_frame.to_csv(migration_path, index=False, encoding="utf-8-sig")
    distinct_authors = migration_frame["name"].nunique()
    return migration_path, distinct_authors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze author locations by year and draw world maps for each target year."
    )
    parser.add_argument("--input", default="chinesename_address_year.csv", help="Input CSV path.")
    parser.add_argument("--output-dir", default="author_maps", help="Output directory for HTML maps.")
    parser.add_argument(
        "--years",
        nargs="*",
        type=int,
        default=TARGET_YEARS,
        help="Years to analyze. Default: 1991 2000 2010 2020 2024.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    df = load_data(input_path)
    print_name_address_summary(df)

    yearly_counts = build_yearly_country_counts(df, args.years)
    summary_path = save_summary_csv(yearly_counts, output_dir)
    migration_path, distinct_authors = save_migration_csv(df, input_path.parent)

    for year in args.years:
        map_path = save_year_map(yearly_counts[year], year, output_dir)
        print(f"Year {year}: {len(yearly_counts[year])} countries/regions -> {map_path}")

    print(f"Summary CSV written to {summary_path}")
    print(f"Migration CSV written to {migration_path}")
    print(f"Migration distinct authors: {distinct_authors}")


if __name__ == "__main__":
    main()