from __future__ import annotations

import logging
import subprocess
from datetime import datetime, timedelta, UTC
from pathlib import Path

from PIL import Image

GITHUB_NAME: str = "Your Name"
GITHUB_MAIL: str = "your@mail.com"
TARGET_YEAR: int = 2020

IMAGE_PATH: Path = Path("art.png")
REPO_DIR: Path = Path("github_art")

WEEKS_COUNT: int = 51

first_date: datetime = datetime(TARGET_YEAR, 1, 1, tzinfo=UTC)
start_date: datetime = first_date + timedelta(days=(6 - first_date.weekday()) % 7)


def create_repo() -> None:
    REPO_DIR.mkdir(parents=True, exist_ok=True)
    git_dir: Path = REPO_DIR / ".git"

    if not git_dir.exists():
        subprocess.run(["git", "init"], cwd=REPO_DIR, check=True)

        readme_path: Path = REPO_DIR / "README.md"
        readme_path.write_text(f"# GitHub Art {TARGET_YEAR}\n", encoding="utf-8")

        subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=REPO_DIR, check=True)


def make_commit(date: datetime, data_file: Path) -> None:
    date_str: str = date.strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(
        ["git", "commit", "--allow-empty", f"--date={date_str}", f"--author={GITHUB_NAME} <{GITHUB_MAIL}>", "-m",
            f"{date_str} commit", ], cwd=REPO_DIR, check=True, )

    subprocess.run(["git", "add", str(data_file)], cwd=REPO_DIR, check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], cwd=REPO_DIR, check=True)


def is_dark_pixel(pixel: tuple[int, ...]) -> bool:
    if len(pixel) == 4:
        r, g, b, a = pixel
    elif len(pixel) == 3:
        r, g, b = pixel
        a = 255
    else:
        r = g = b = pixel[0]
        a = 255

    if a <= 128:
        return False

    brightness: int = (r + g + b) // 3
    return brightness < 50


def main() -> None:
    create_repo()

    img: Image.Image = Image.open(IMAGE_PATH)
    if img.size != (WEEKS_COUNT, 7):
        raise ValueError(f"The image should be {WEEKS_COUNT}x{7} pixels, but now {img.size}")

    pixels = img.load()
    data_file: Path = REPO_DIR / "data.txt"
    data_file.write_text("", encoding="utf-8")

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info("Start")

    commits_made: int = 0

    for week in range(WEEKS_COUNT):
        for day_in_week in range(7):
            pixel = pixels[week, day_in_week]

            if not is_dark_pixel(pixel):
                continue

            target_date: datetime = start_date + timedelta(days=week * 7 + day_in_week)

            with data_file.open("a", encoding="utf-8") as f:
                f.write(f"Commit on {target_date.isoformat()}\n")

            make_commit(target_date, data_file)
            commits_made += 1

            logging.info(f"Commit {target_date.date()} created")

    logging.info(f"Success! Commits count: {commits_made}")


if __name__ == "__main__":
    main()
