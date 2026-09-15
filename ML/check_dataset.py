from pathlib import Path

DATASET = Path(__file__).resolve().parent / "dataset" / "onion" / "onion dataset resized"


print("\nTelegronomy Onion Dataset")
print("=" * 35)


total = 0


for folder in DATASET.iterdir():

    if folder.is_dir():

        images = [
            file for file in folder.iterdir()
            if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
        ]

        count = len(images)

        print(f"{folder.name}: {count} images")

        total += count


print("=" * 35)
print(f"Total images: {total}")