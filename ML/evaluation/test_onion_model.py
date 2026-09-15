from pathlib import Path

import torch
import torch.nn as nn

import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)

from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# --------------------------------------
# PROJECT PATHS
# --------------------------------------

ML_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = ML_DIR / "dataset" / "onion"

TEST_DIR = DATASET_DIR / "test"

MODELS_DIR = ML_DIR / "models"

MODEL_PATH = (
    MODELS_DIR
    / "telegronomy_onion_model.pth"
)

# --------------------------------------
# IMAGE TRANSFORMATION
# --------------------------------------

IMAGE_SIZE = 224


test_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# --------------------------------------
# LOAD TEST DATASET
# --------------------------------------

test_dataset = datasets.ImageFolder(
    TEST_DIR,
    transform=test_transform
)


BATCH_SIZE = 16


test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


print("\nFarmer AI Test Dataset")

print("=" * 40)

print(
    f"Test images: {len(test_dataset)}"
)

print("\nDisease Classes:")

for index, class_name in enumerate(
    test_dataset.classes
):

    print(
        f"{index}: {class_name}"
    )

# --------------------------------------
# DEVICE CONFIGURATION
# --------------------------------------

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print(f"\nUsing device: {device}")


# --------------------------------------
# LOAD SAVED MODEL
# --------------------------------------

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device
)


class_names = checkpoint[
    "class_names"
]


model = models.mobilenet_v3_small(
    weights=None
)


model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_names)
)


model.load_state_dict(
    checkpoint["model_state_dict"]
)


model = model.to(device)

model.eval()


print("\nModel Loaded Successfully!")

print(
    f"Saved validation accuracy: "
    f"{checkpoint['validation_accuracy']:.2f}%"
)


# --------------------------------------
# TEST MODEL
# --------------------------------------

correct_predictions = 0

total_predictions = 0


# Store all actual labels
all_labels = []

# Store all model predictions
all_predictions = []


# Track performance for each class
class_correct = [
    0
    for _ in class_names
]

class_total = [
    0
    for _ in class_names
]


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)

        labels = labels.to(device)


        # Make predictions
        outputs = model(images)


        # Get predicted classes
        _, predicted = torch.max(
            outputs,
            1
        )


        # Save actual labels
        all_labels.extend(
            labels.cpu().tolist()
        )


        # Save model predictions
        all_predictions.extend(
            predicted.cpu().tolist()
        )


        # Overall accuracy
        total_predictions += labels.size(0)

        correct_predictions += (
            predicted == labels
        ).sum().item()


        # Accuracy for each disease class
        for label, prediction in zip(
            labels,
            predicted
        ):

            label_index = label.item()

            class_total[label_index] += 1


            if prediction == label:

                class_correct[
                    label_index
                ] += 1


# --------------------------------------
# OVERALL TEST RESULTS
# --------------------------------------

test_accuracy = (
    100
    * correct_predictions
    / total_predictions
)


print("\n" + "=" * 40)

print(
    "TELEGRONOMY FINAL TEST RESULTS"
)

print("=" * 40)

print(
    f"\nCorrect Predictions: "
    f"{correct_predictions}"
)

print(
    f"Total Test Images: "
    f"{total_predictions}"
)

print(
    f"\nOverall Test Accuracy: "
    f"{test_accuracy:.2f}%"
)


# --------------------------------------
# RESULTS FOR EACH CLASS
# --------------------------------------

print("\n" + "=" * 40)

print(
    "DISEASE CLASS PERFORMANCE"
)

print("=" * 40)


for index, class_name in enumerate(
    class_names
):

    if class_total[index] > 0:

        accuracy = (
            100
            * class_correct[index]
            / class_total[index]
        )

        print(
            f"\n{class_name}"
        )

        print(
            f"Correct: "
            f"{class_correct[index]}"
        )

        print(
            f"Total: "
            f"{class_total[index]}"
        )

        print(
            f"Accuracy: "
            f"{accuracy:.2f}%"
        )

# --------------------------------------
# CONFUSION MATRIX
# --------------------------------------

matrix = confusion_matrix(
    all_labels,
    all_predictions
)


display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=class_names
)


fig, ax = plt.subplots(
    figsize=(10, 8)
)


display.plot(
    ax=ax,
    cmap="Blues",
    values_format="d"
)


plt.title(
    "Farmer AI Onion Disease Confusion Matrix"
)


plt.xticks(
    rotation=30,
    ha="right"
)


plt.tight_layout()


# Save confusion matrix
confusion_matrix_path = (
    ML_DIR
    / "models"
    / "onion_confusion_matrix.png"
)


plt.savefig(
    confusion_matrix_path,
    dpi=300
)


print(
    f"\nConfusion matrix saved to:"
)

print(
    confusion_matrix_path
)


plt.show()