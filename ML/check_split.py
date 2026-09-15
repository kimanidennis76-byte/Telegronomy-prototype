from pathlib import Path


BASE_DIR = (
    Path(__file__).resolve().parent
    / "dataset"
    / "onion"
)


DATASETS = [
    "training",
    "validation",
    "test"
]


print("\nTelegronomy Dataset Verification")
print("=" * 45)


for dataset_name in DATASETS:

    dataset_path = BASE_DIR / dataset_name

    print(f"\n{dataset_name.upper()}")

    total = 0

    for class_folder in dataset_path.iterdir():

        if class_folder.is_dir():

            images = [
                file
                for file in class_folder.iterdir()
                if file.suffix.lower()
                in [".jpg", ".jpeg", ".png"]
            ]

            count = len(images)

            print(
                f"{class_folder.name}: {count}"
            )

            total += count

    print(f"Total: {total}")


print("\n" + "=" * 45)
print("Verification completed.")