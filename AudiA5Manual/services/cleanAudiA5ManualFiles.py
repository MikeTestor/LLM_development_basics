import json
import shutil
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
CLEAN_DIR = Path(__file__).resolve().parent.parent / "data" / "clean"
PURE_TEXT_DIR = Path(__file__).resolve().parent.parent / "data" / "pureText"
TEXT_BY_TYPE_DIR = Path(__file__).resolve().parent.parent / "data" / "textByType"

KEYS_TO_REMOVE = ["headings", "links", "title"]


def clean_file(raw_path: Path, clean_path: Path) -> None:
    with raw_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for key in KEYS_TO_REMOVE:
        data.pop(key, None)

    with clean_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def remove_intro_pages(text_prefix: str = "kort en bondig") -> None:
    for clean_path in CLEAN_DIR.glob("*.json"):
        with clean_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        text = data.get("text", "")
        if text.lower().startswith(text_prefix):
            clean_path.unlink()


def extract_pure_text() -> None:
    for clean_path in CLEAN_DIR.glob("*.json"):
        with clean_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        text = data.get("text", "")
        pure_text_path = PURE_TEXT_DIR / f"{clean_path.stem}.txt"
        with pure_text_path.open("w", encoding="utf-8") as f:
            f.write(text)


def organize_by_type() -> None:
    for pure_text_path in PURE_TEXT_DIR.glob("*.txt"):
        text = pure_text_path.read_text(encoding="utf-8")
        type_label = text.split("\n")[0]

        type_dir = TEXT_BY_TYPE_DIR / type_label
        type_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pure_text_path, type_dir / pure_text_path.name)


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    PURE_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_BY_TYPE_DIR.mkdir(parents=True, exist_ok=True)

    for raw_path in RAW_DIR.glob("*.json"):
        clean_path = CLEAN_DIR / raw_path.name
        clean_file(raw_path, clean_path)

    remove_intro_pages()
    extract_pure_text()
    organize_by_type()


if __name__ == "__main__":
    main()
