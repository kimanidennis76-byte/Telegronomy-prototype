from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms, models


# --------------------------------------
# PROJECT PATHS
# --------------------------------------

ML_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = ML_DIR / "dataset" / "onion"

TRAIN_DIR = DATASET_DIR / "training"
VALIDATION_DIR = DATASET_DIR / "validation"
TEST_DIR = DATASET_DIR / "test"

MODELS_DIR = ML_DIR / "models"

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------
# IMAGE TRANSFORMATIONS
# --------------------------------------

IMAGE_SIZE = 224


train_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(),

    transforms.RandomRotation(15),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


evaluation_transform = transforms.Compose([

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
# LOAD DATASETS
# --------------------------------------

train_dataset = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

validation_dataset = datasets.ImageFolder(
    VALIDATION_DIR,
    transform=evaluation_transform
)

test_dataset = datasets.ImageFolder(
    TEST_DIR,
    transform=evaluation_transform
)

# --------------------------------------
# DISPLAY DATASET INFORMATION
# --------------------------------------

print("\nTelegronomy Onion Disease Dataset")

print("=" * 40)

print(
    f"Training images: {len(train_dataset)}"
)

print(
    f"Validation images: {len(validation_dataset)}"
)

print(
    f"Test images: {len(test_dataset)}"
)

print("=" * 40)

print("\nDisease Classes:")

for index, class_name in enumerate(
    train_dataset.classes
):

    print(
        f"{index}: {class_name}"
    )

# --------------------------------------
# HANDLE CLASS IMBALANCE
# --------------------------------------

class_counts = []

for class_index in range(
    len(train_dataset.classes)
):

    count = sum(
        1
        for label in train_dataset.targets
        if label == class_index
    )

    class_counts.append(count)


print("\nClass Counts")

for index, count in enumerate(
    class_counts
):

    print(
        f"{train_dataset.classes[index]}: {count}"
    )


# Calculate class weights
class_weights = [

    1 / count

    for count in class_counts
]


# Create a weight for every image
sample_weights = [

    class_weights[label]

    for label in train_dataset.targets
]


sampler = WeightedRandomSampler(
    weights=sample_weights,
    num_samples=len(sample_weights),
    replacement=True
)




# --------------------------------------
# CREATE DATA LOADERS
# --------------------------------------

BATCH_SIZE = 16


train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    sampler=sampler
)


validation_loader = DataLoader(
    validation_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# --------------------------------------
# DISPLAY LOADER INFORMATION
# --------------------------------------

print("\nData Loaders Ready")

print(
    f"Batch size: {BATCH_SIZE}"
)

print(
    f"Training batches: {len(train_loader)}"
)

print(
    f"Validation batches: {len(validation_loader)}"
)

print(
    f"Test batches: {len(test_loader)}"
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
# MODEL CONFIGURATION
# --------------------------------------

NUM_CLASSES = len(
    train_dataset.classes
)


model = models.mobilenet_v3_small(
    weights=models.MobileNet_V3_Small_Weights.DEFAULT
)


model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    NUM_CLASSES
)


model = model.to(device)


print("\nModel Ready")

print(
    f"Number of disease classes: {NUM_CLASSES}"
)
# --------------------------------------
# LOSS FUNCTION
# --------------------------------------

criterion = nn.CrossEntropyLoss()


# --------------------------------------
# OPTIMIZER
# --------------------------------------

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)


print("\nTraining Configuration Ready")

print(
    "Loss function: CrossEntropyLoss"
)

print(
    "Optimizer: Adam"
)

print(
    "Learning rate: 0.001"
)

# --------------------------------------
# TRAINING SETTINGS
# --------------------------------------

EPOCHS = 10
best_validation_accuracy = 0.0


# --------------------------------------
# TRAINING LOOP
# --------------------------------------

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0.0

    correct_predictions = 0

    total_predictions = 0


    for images, labels in train_loader:

        images = images.to(device)

        labels = labels.to(device)


        # Reset previous gradients
        optimizer.zero_grad()


        # Make predictions
        outputs = model(images)


        # Calculate loss
        loss = criterion(
            outputs,
            labels
        )


        # Calculate gradients
        loss.backward()


        # Update model weights
        optimizer.step()


        # Track loss
        running_loss += loss.item()


        # Get predicted class
        _, predicted = torch.max(
            outputs,
            1
        )


        total_predictions += labels.size(0)

        correct_predictions += (
            predicted == labels
        ).sum().item()


    # Calculate epoch results
    epoch_loss = (
        running_loss
        / len(train_loader)
    )


    epoch_accuracy = (
        100
        * correct_predictions
        / total_predictions
    )


    print(
        f"\nEpoch {epoch + 1}/{EPOCHS}"
    )

    print(
        f"Training Loss: {epoch_loss:.4f}"
    )

    print(
        f"Training Accuracy: "
        f"{epoch_accuracy:.2f}%"
    )


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    model.eval()

    validation_loss = 0.0

    validation_correct = 0

    validation_total = 0


    with torch.no_grad():

        for images, labels in validation_loader:

            images = images.to(device)

            labels = labels.to(device)


            # Make predictions
            outputs = model(images)


            # Calculate validation loss
            loss = criterion(
                outputs,
                labels
            )


            validation_loss += loss.item()


            # Get predicted class
            _, predicted = torch.max(
                outputs,
                1
            )


            validation_total += labels.size(0)

            validation_correct += (
                predicted == labels
            ).sum().item()


    # Calculate validation results
    average_validation_loss = (
        validation_loss
        / len(validation_loader)
    )


    validation_accuracy = (
        100
        * validation_correct
        / validation_total
    )


    print(
        f"Validation Loss: "
        f"{average_validation_loss:.4f}"
    )

    print(
        f"Validation Accuracy: "
        f"{validation_accuracy:.2f}%"
    )

    # --------------------------------------
    # SAVE BEST MODEL
    # --------------------------------------

    if validation_accuracy > best_validation_accuracy:

        best_validation_accuracy = validation_accuracy

        model_path = (
            MODELS_DIR
            / "telegronomy_onion_model.pth"
        )

        torch.save(
            {
                "model_state_dict": model.state_dict(),

                "class_names": train_dataset.classes,

                "image_size": IMAGE_SIZE,

                "validation_accuracy": (
                    validation_accuracy
                )
            },
            model_path
        )

        print(
            "Best model saved!"
        )

        print(
            f"Validation Accuracy: "
            f"{validation_accuracy:.2f}%"
        )