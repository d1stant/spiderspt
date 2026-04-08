from pathlib import Path

LICENSE_PATH = Path("./License")
LICENSE_PATH.mkdir(parents=True, exist_ok=True)
LICENSE_FILE: Path = LICENSE_PATH / "license"


def generate_license(machine_code: str, duration: str) -> None:
    pass
