import json
from pathlib import Path

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_url_text_map(raw_dir: Path | str = RAW_DATA_DIR) -> dict[str, str]:
    """Read all JSON files in data/raw and return {url: text}."""
    raw_path = Path(raw_dir)
    url_text_map: dict[str, str] = {}

    for json_file in sorted(raw_path.glob("*.json")):
        if json_file.name == "_index.json":
            continue

        with json_file.open(encoding="utf-8") as f:
            entry = json.load(f)

        url_text_map[entry["url"]] = entry["text"]

    return url_text_map
