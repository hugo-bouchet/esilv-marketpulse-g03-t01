# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (instructor reference, not present in the team repository)
- Live connectivity: **not demonstrated**

The fixture declares `"is_live_bloomberg_output": false`.
Its values are illustrative teaching values reused from `data/sample/prices.csv`.
They are not certified Bloomberg historical observations.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier | Yahoo identifier |
|---|---|---|---|
| Instrument | AAPL | AAPL US Equity | AAPL |
| Benchmark | SP500 | SPX Index | ^GSPC |

The canonical tickers `AAPL` and `SP500` are preserved.
Bloomberg identifiers must disappear at the provider boundary, before rows reach `analytics.py`.

## Inspected inputs

### Instrument: AAPL US Equity

- `role`: instrument
- `provider_identifier`: AAPL US Equity
- `canonical_ticker`: AAPL
- Observations: 21 (2026-09-01 -> 2026-09-30)
- Date representation: string `YYYY-MM-DD`
- Missing values: none

### Benchmark: SPX Index

- `role`: benchmark
- `provider_identifier`: SPX Index
- `canonical_ticker`: SP500
- Observations: 21 (2026-09-01 -> 2026-09-30)
- Date representation: string `YYYY-MM-DD`
- Missing values: none (`volume_value` is always `0` for the index)

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | teaching wrapper key, `YYYY-MM-DD` string |
| ticker | application mapping (series `canonical_ticker`) | AAPL or SP500, never the Bloomberg identifier |
| open | `open_value` | teaching wrapper key, convert to float |
| high | `high_value` | teaching wrapper key, convert to float |
| low | `low_value` | teaching wrapper key, convert to float |
| close | `close_value` | teaching wrapper key, convert to float |
| volume | `volume_value` | teaching wrapper key, convert to int; 0 for SPX Index |

**Important:** teaching wrapper key != Bloomberg LIVE field mnemonic.
The keys `observation_date`, `open_value`, `high_value`, `low_value`, `close_value` and `volume_value` exist only in the approved fallback fixture.
They must not be presented or reused as Bloomberg field names.
No LIVE Bloomberg field name was observed, so none is documented here.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity -> canonical AAPL
- Benchmark identifier: SPX Index -> canonical SP500
- Date representation: `YYYY-MM-DD` string in `observation_date`
- Input structure: JSON object -> `series` list -> each series has `role`, `canonical_ticker`, `provider_identifier`, `observations` (list of dicts)
- Missing fields: none in the fixture
- Special normalization notes:
  - select the series by `provider_identifier`;
  - assign `ticker` from the canonical ticker, not from the Bloomberg identifier;
  - prices -> float, volume -> int;
  - SPX Index volume is 0 (index, no traded volume): keep it as 0;
  - the output must match `data/sample/bloomberg_reference_expected.json`;
  - terminal output must display `APPROVED_SAMPLE`, never `LIVE`.
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`