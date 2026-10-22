# Evidence

This directory stores individual MarketPulse checkpoint evidence.

The single source of truth for all evidence requirements is:

```text
docs/04_CHECKPOINTS_AND_EVIDENCE.md
```

That document defines the official filenames, required screenshots, optional evidence, individual README content, live validation principles and security rules.

Do not create a parallel evidence specification in this directory.

## Directory convention

Each student stores evidence under their own GitHub username:

```text
evidence/
├── checkpoint-a/
│   └── <github-username>/
├── checkpoint-b/
│   └── <github-username>/
└── checkpoint-c/
    └── <github-username>/
```

Each checkpoint directory must contain the student's checkpoint `README.md` and the evidence files required by the canonical contract.

## Important

Evidence is collected only for:

- Checkpoint A;
- Checkpoint B;
- Checkpoint C.

Do not add screenshots for every TD.

Screenshots complement:

- Git history;
- Pull Requests;
- reviews;
- execution;
- explanation.

They do not replace those elements.

## Security

Before committing any evidence, inspect it carefully.

Never expose:

- passwords;
- API keys;
- access tokens;
- SSH private keys;
- Bloomberg credentials;
- cloud credentials;
- payment information.

For exact filenames and validation criteria, always return to:

```text
docs/04_CHECKPOINTS_AND_EVIDENCE.md
```

## How to run MarketPulse (current stage)

### Prerequisites

- Python 3 installed (`python --version` or `python3 --version`)
- Git installed
- No external package is needed at this stage: the program only uses the Python standard library (`csv`, `json`, `pathlib`).

### Steps

1. Clone the team repository and move into it:

```bash
git clone https://github.com/hugo-bouchet/esilv-marketpulse-g03-t01.git
cd esilv-marketpulse-g03-t01
```

2. Run the program **from the repository root** (the data path `data/sample` is relative to the current directory):

```bash
python src/main.py
```

On Linux/macOS, use `python3` if `python` is not available.

### Expected output

```text
=== MarketPulse ===

Provider: CSV

Instrument
AAPL - Apple Inc.
Market : NASDAQ
Observations : 21
First date : 2026-09-01
Last date : 2026-09-30
First close : 250.0 USD
Last close : 266.2 USD

Benchmark
SP500 - S&P 500
Market : US
Observations : 21
First date : 2026-09-01
Last date : 2026-09-30
First close : 6600.0
Last close : 6742.0
```

### Common errors

| Error | Cause | Fix |
|---|---|---|
| `FileNotFoundError: data/sample/instruments.json` | The command was run from another folder (e.g. inside `src/`) | Go back to the repository root, then run `python src/main.py` |
| `python: command not found` | Python is not installed or not in the PATH | Install Python 3 or use `python3` |

