from pathlib import Path

import torch
import torch.nn as nn

from PIL import Image

from torchvision import transforms, models


# --------------------------------------
# PROJECT PATHS
# --------------------------------------

ML_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = ML_DIR / "models"

MODEL_PATH = (
    MODELS_DIR
    / "telegronomy_onion_model.pth"
)

# --------------------------------------
# DEVICE CONFIGURATION
# --------------------------------------

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# --------------------------------------
# LOAD TRAINED MODEL
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


print(
    "Farmer AI Onion Disease Model Loaded!"
)

print(
    f"Using device: {device}"
)

print(
    f"Disease classes: {class_names}"
)


# --------------------------------------
# IMAGE TRANSFORMATION
# --------------------------------------

IMAGE_SIZE = 224


image_transform = transforms.Compose([

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
# DISEASE RECOMMENDATIONS
# --------------------------------------

DISEASE_INFORMATION = {

# ---------------------------------
# HEALTHY ONION
# ---------------------------------
    "healthy": {
        "name": "Healthy Onion Plant",
        "recommendation": (
            "Your onion plant appears healthy. "
            "Continue good farming practices, regular monitoring, "
            "proper irrigation, and balanced nutrition."
        ),

        "immediate_actions":[
            "Continue monitoring the crop regularly.",
            "Maintain proper irrigation and avoid waterlogging.",
            "Maintain good field sanitation.",
            "Monitor plants for any new symptoms or pest activity."
        ],

        "prevention": [
            "Maintain good field hygiene and remove infected plant debris.",
            "Use healthy planting material.",
            "Avoid excessive irrigation and prolonged leaf wetness.",
            "Monitor the crop regularly for early signs of disease or pests."
        
        ],

        "management_ptions":{
            "cultural":[
                "Monitor crops regularly."
                "Maintain proper irrigation and avoid waterogging.",
                "Maintain good field sanitation.",
                "Remove unhealthy plant debris where appropriate."
            ],

            "integrated":[
                "Monitor regularly for disease and pest symptoms.",
                "Use healthy planting material.",
                "Monitor for thrips and other important onion pests.",
                "Act early if symptoms begin appearing."
            ],

            "chemical":(
                "No disease treatment is recommeded when the plant appears "
                "healthy. Any pesticide application should be  based on an "
                "identified pest or disease problem and appropriate "
                "professional or product-label guidance."
            )

        },

        "agronomist_referral":(
            "Consult an agronomist if new symptoms appear, "
            "plant health begins to decline, or you are unsure "
            "Monitor the crop regularly for early signs of disease or pests."    
        )      
    },

# --------------------------------------
#  IRIS YELLOW VIRUS
# ---------------------------------------

    "iris_yellow_virus": {
        "name": "Iris Yellow Virus",
        "recommendation": (
            "Iris Yellow Virus is commonly spread by thrips. "
            "Monitor and manage thrips, remove severely affected plants, "
            "and consult an agronomist for an appropriate integrated "
            "disease and pest management plan."
        ),

        "immediate_actions":[
            "Inspect the crop for thrips and other signs of pest activity.",
            "Remove and safely dispose of severely affected plants where appropriate.",
            "Monitor nearby onion plants for similar symptoms.",
            "Consult an agronomist before applying disease or pest control products."

        ],

        "prevention":[
            "Monitor regularly for thrips and manage them appropriately.",
            "Maintain good field sanitation.",
            "Remove severely affected plants and crop debris where appropriate.",
            "Use healthy planting material and maintain good crop management practices."
        ],

        "management_options":{
            "cultural":[
                "Remove and safely dispose of severely affected plants where appropriate.",
                "Remove crop debris that may contribute to pest or disease problem.",
                "Maintain good field hygiene.",
                "Avoid unnecessary plant stress."
            ],

            "integrated":[
                "Closely monitor for thrips.",
                "Use appropriate integrated pest-management practices.",
                "Monitor surrounding plants for symptoms.",
                "Consult an agronomist when symptoms are speading."

            ],

            "chemical": (
                "Chemical control should focus on the identified pest where "
                "appropriate, rather than assuming a chemical can cure the "
                "virus. Product selection should be confirmed by an agronomist. "
                "Only use products registered for the intended crop and pest "
                "in Kenya and follow the product label."
            )

        }, 

        "agronomist_referral":(
            "Consult an agronomist if symptoms continue to spread, "
            "thrips populations are difficult to manage, or a significant "
            "portion of the crop becomes affected." 
        )
    },
# ------------------------------------------------
# LEAF BLIGHT
# ------------------------------------------------

    "leaf_blight": {
        "name": "Leaf Blight",
        "recommendation": (
            "Remove heavily affected plant material and avoid excessive "
            "leaf moisture. Improve field sanitation and consult an "
            "agronomist for diagnosis and an appropriate disease "
            "management plan."
        ),

        "immediate_actions": [
            "Remove healthy infected leaves where practical.",
            "Remove infected plant debris from the field. ",
            "Avoid prolonged leaf wetness where possible.",
            "Monitor nearby plants for new or worsening symptoms."
        ],

        "prevention": [
            "Maintain good field sanitation.",
            "Avoid excessive irrigation and prolonged leaf wetness.",
            "Allow adequate spacing and airflow between plants.",
            "Monitor the crop regularly for early symptoms."
        ],

        "management_options": {
             "cultural": [
                "Remove heavily affected leaves where practical.",
                "Remove infected plant debris.",
                "Maintain adequate spacing and airflow.",
                "Avoid prolonged leaf wetness.",
                "Avoid excessive irrigation."
            ],

            "integrated": [
                "Monitor the crop regularly for disease progression.",
                "Remove affected material promptly where appropriate.",
                "Use healthy planting material.",
                "Maintain good field sanitation.",
                "Consult an agronomist if symptoms continue spreading."
            ],

            "chemical": (
                "A suitable fungicide may be considered after confirmation "
                "of the disease and assessment of severity. Product selection "
                "should be confirmed by an agronomist. Use only appropriately "
                "registered products and follow the product label."
            )

        },



        "agronomist_referral":(
            "Consult an agronomist if symptoms continue to spread, "
            "Increase in severity, or affect a significant portion "
            "of the crop."
        )

    },

# -------------------------------------
# PURPLE BLOTCH
# --------------------------------------
    "purple_blotch": {
        "name": "Purple Blotch",
        "recommendation": (
            "Remove heavily infected leaves where practical, improve "
            "field sanitation, avoid prolonged leaf wetness, and consult "
            "an agronomist for an appropriate disease management plan."
        ),

        "immediate_actions": [
            "Remove and safely dispose of severely infected leaves.",
            "Keep the field clean and remove infected plant debris.",
            "Avoid prolonged leaf wetness where possible.",
            "Monitor nearby onion plants for new symptoms."
        ],

        "prevention":[
            "Maintain good field sanitation.",
            "Avoid excessive irrigation that keeps leaves wet for long periods.",
            "Allow adequate spacing and airflow between plants.",
            "Monitor the crop regularly for early symptoms."
        ],

        "management_options": {
            "cultural": [
                "Remove severely infected leaves where practical.",
                "Remove infected crop debris.",
                "Maintain adequate plant spacing and airflow.",
                "Avoid prolonged leaf wetness.",
                "Avoid excessive irrigation."
            ], 

            "integrated": [
                "Monitor regularly for new lesions.",
                "Remove severely affected material where appropriate.",
                "Maintain good field sanitation.",
                "Use healthy planting material.",
                "Monitor neighbouring plants for early symptoms."
            ],

            "chemical": (
                "A suitable fungicide may be considered when disease pressure "
                "warrants it and the diagnosis has been confirmed. Product "
                "selection should be confirmed by an agronomist. Use only "
                "appropriately registered products and follow the product label."
            )
        },


        "agronomist_referral": (
            "Consult an agronomist if symptoms continue to spread, "
            "increase in severity, or affect a significant portion "
        )
    }
}
# --------------------------------------
# PREDICT ONION DISEASE
# --------------------------------------

def predict_image(image_path):

    # Open image
    image = Image.open(
        image_path
    ).convert("RGB")


    # Transform image
    image_tensor = image_transform(
        image
    )


    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(
        0
    )


    # Move image to device
    image_tensor = image_tensor.to(
        device
    )


    # Make prediction
    with torch.no_grad():

        outputs = model(
            image_tensor
        )


        probabilities = torch.softmax(
            outputs,
            dim=1
        )


        confidence, predicted_index = torch.max(
            probabilities,
            1
        )


    predicted_index = predicted_index.item()

    confidence = confidence.item() * 100

# --------------------------------------
# CONFIDENCE STATUS
# --------------------------------------

    if confidence >= 80:

        confidence_status = "High Confidence"

    elif confidence >= 60:

        confidence_status = "Moderate Confidence"

    else:

        confidence_status = "Low Confidence"
# --------------------------------------
# CONFIDENCE WARNING
# --------------------------------------

    if confidence_status == "Low Confidence":

        confidence_warning = (
            "⚠ Low confidence prediction. "
            "Please take another clear photo showing "
            "the affected onion leaves. Ensure there is "
            "good lighting and the image is not blurry. "
            "You may also consult an agronomist."
        )

    elif confidence_status == "Moderate Confidence":

        confidence_warning = (
            "This prediction has moderate confidence. "
            "Consider monitoring the plant and taking "
            "another photo if the symptoms change."
        )

    else:

        confidence_warning = (
            "The model has high confidence in this prediction."
        )



    predicted_disease = class_names[
        predicted_index
    ]
    disease_info = DISEASE_INFORMATION[
        predicted_disease
    ]


    disease_name = disease_info[
        "name"
    ]


    recommendation = disease_info[
        "recommendation"
    ]


    return (
        predicted_disease,
        disease_name,
        confidence,
        confidence_status,
        recommendation,
        confidence_warning
    )


