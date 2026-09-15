from pathlib import Path
import random
import shutil


# -----------------------------
# SETTINGS
# -----------------------------

BASE_DIR = (
    Path(__file__).resolve().parent
    / "dataset"
    / "onion"
)

RAW_DIR = BASE_DIR / "raw"
TRAIN_DIR = BASE_DIR / "training"
VALIDATION_DIR = BASE_DIR / "validation"
TEST_DIR = BASE_DIR / "test"


# Make the random split repeatable
random.seed(42)


# -----------------------------
# SPLIT SETTINGS
# -----------------------------

TRAIN_PERCENT = 0.70
VALIDATION_PERCENT = 0.15
TEST_PERCENT = 0.15


# -----------------------------
# START SPLITTING
# -----------------------------

print("\nTelegronomy Dataset Split")
print("=" * 40)


for class_folder in RAW_DIR.iterdir():

    if not class_folder.is_dir():
        continue


    class_name = class_folder.name


    # Get all image files
    images = [
        file
        for file in class_folder.iterdir()
        if file.suffix.lower()
        in [".jpg", ".jpeg", ".png"]
    ]


    # Shuffle images randomly
    random.shuffle(images)


    total_images = len(images)


    # Calculate split points
    train_end = int(total_images * TRAIN_PERCENT)

    validation_end = (
        train_end
        + int(total_images * VALIDATION_PERCENT)
    )


    # Split the list
    training_images = images[:train_end]

    validation_images = images[
        train_end:validation_end
    ]

    test_images = images[
        validation_end:
    ]


    # Create class folders
    train_class = TRAIN_DIR / class_name

    validation_class = (
        VALIDATION_DIR / class_name
    )

    test_class = TEST_DIR / class_name


    train_class.mkdir(
        parents=True,
        exist_ok=True
    )

    validation_class.mkdir(
        parents=True,
        exist_ok=True
    )

    test_class.mkdir(
        parents=True,
        exist_ok=True
    )


    # Copy images
    for image in training_images:

        shutil.copy2(
            image,
            train_class / image.name
        )


    for image in validation_images:

        shutil.copy2(
            image,
            validation_class / image.name
        )


    for image in test_images:

        shutil.copy2(
            image,
            test_class / image.name
        )


    # Print results
    print(f"\n{class_name}")

    print(
        f"Training: {len(training_images)}"
    )

    print(
        f"Validation: {len(validation_images)}"
    )

    print(
        f"Test: {len(test_images)}"
    )


print("\n" + "=" * 40)

print(
    "Dataset split completed successfully!"
)