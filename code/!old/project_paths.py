"""Project path scaffolding for the Brookings RSP data task."""

from pathlib import Path

# Project root is the parent of the `code/` directory.
ROOT = Path(__file__).resolve().parents[1]

# Core directories
GIVEN_DIR = ROOT / "_given"
CODE_DIR = ROOT / "code"
NOTEBOOK_BUILD_DIR = CODE_DIR / "build"
DATA_DIR = ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = ROOT / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
WRITEUP_DIR = ROOT / "writeup"
GUIDES_DIR = WRITEUP_DIR / "_guides"

# Key writeup files
C1_WRITEUP_TEX = WRITEUP_DIR / "c1" / "c1_adlt_writeup.tex"
C2_WRITEUP_TEX = WRITEUP_DIR / "c2" / "c2_adlt_summary.tex"
C3_PITCH_TEX = WRITEUP_DIR / "c3" / "c3_adlt_pitch.tex"
BIB_FILE = WRITEUP_DIR / "brookings.bib"


def ensure_project_dirs() -> None:
    """Create processed/output directories if they do not exist."""
    dirs_to_create = [
        PROCESSED_DATA_DIR,
        OUTPUT_DIR,
        FIGURES_DIR,
        TABLES_DIR,
    ]
    for path in dirs_to_create:
        path.mkdir(parents=True, exist_ok=True)


def print_project_paths() -> None:
    """Print all project paths for quick debugging."""
    paths = [
        ("ROOT", ROOT),
        ("GIVEN_DIR", GIVEN_DIR),
        ("CODE_DIR", CODE_DIR),
        ("NOTEBOOK_BUILD_DIR", NOTEBOOK_BUILD_DIR),
        ("DATA_DIR", DATA_DIR),
        ("RAW_DATA_DIR", RAW_DATA_DIR),
        ("PROCESSED_DATA_DIR", PROCESSED_DATA_DIR),
        ("OUTPUT_DIR", OUTPUT_DIR),
        ("FIGURES_DIR", FIGURES_DIR),
        ("TABLES_DIR", TABLES_DIR),
        ("WRITEUP_DIR", WRITEUP_DIR),
        ("GUIDES_DIR", GUIDES_DIR),
        ("C1_WRITEUP_TEX", C1_WRITEUP_TEX),
        ("C2_WRITEUP_TEX", C2_WRITEUP_TEX),
        ("C3_PITCH_TEX", C3_PITCH_TEX),
        ("BIB_FILE", BIB_FILE),
    ]
    print("Project paths:")
    for label, path in paths:
        print(f"- {label}: {path}")
