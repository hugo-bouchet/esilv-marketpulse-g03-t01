"""MarketPulse Bloomberg-stage provider (TD10).

Access mode: APPROVED_SAMPLE.
Raw input comes from the instructor-approved fallback fixture.
This module does NOT prove live Bloomberg connectivity.

Mapping source: docs/BLOOMBERG_FIELD_MAPPING.md
"""

import json
from pathlib import Path

ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample"
    / "bloomberg_reference_sample.json"
)

# Provider identifiers stay inside the provider boundary.
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

# Teaching wrapper keys (NOT Bloomberg field mnemonics) -> canonical fields.
SAMPLE_FIELD_MAPPING = {
    "observation_date": "date",
    "open_value": "open",
    "high_value": "high",
    "low_value": "low",
    "close_value": "close",
    "volume_value": "volume",
}


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    """Raw input boundary.

    APPROVED_SAMPLE: read the series from the approved fixture.
    A LIVE implementation would only replace the body of this function
    with the instructor-approved classroom mechanism.
    """
    with open(SAMPLE_FILE, encoding="utf-8") as file:
        fixture = json.load(file)

    for series in fixture["series"]:
        if series["provider_identifier"] == identifier:
            observations = [
                observation
                for observation in series["observations"]
                if (start_date is None or observation["observation_date"] >= start_date)
                and (end_date is None or observation["observation_date"] <= end_date)
            ]
            return {
                "provider_identifier": series["provider_identifier"],
                "canonical_ticker": series["canonical_ticker"],
                "observations": observations,
            }

    raise ValueError(f"Identifier not found in approved sample: {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Normalization boundary: approved input -> canonical rows."""
    if raw_data["canonical_ticker"] != canonical_ticker:
        raise ValueError(
            f"Canonical ticker mismatch: expected {canonical_ticker}, "
            f"got {raw_data['canonical_ticker']}"
        )

    rows = []
    for observation in raw_data["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    rows.sort(key=lambda row: row["date"])
    return rows


def fetch_bloomberg_prices(canonical_ticker, start_date=None, end_date=None):
    """Public entry point: canonical ticker in, canonical rows out."""
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Unsupported canonical ticker: {canonical_ticker}")

    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier, start_date, end_date)
    rows = normalize_bloomberg_history(raw_data, canonical_ticker)

    if not rows:
        raise ValueError(f"No Bloomberg-stage rows for {canonical_ticker}")

    return rows