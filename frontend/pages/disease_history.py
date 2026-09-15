import sqlite3
import sys
from pathlib import Path

import streamlit as st

# --------------------------------
# IMPORT AI INFORMATION
# --------------------------------

PROJECT_DIR = (
    Path(__file__).resolve()
    .parent.parent.parent
)

INFERENCE_DIR = (
    PROJECT_DIR
    / "ML"
    / "inference"
)

sys.path.insert(
    0,
    str(INFERENCE_DIR)
)

from predict_onion_disease import DISEASE_INFORMATION

# --------------------------------
# DATABASE
# --------------------------------

DATABASE = "database/telegronomy.db"


# --------------------------------
# CHECK LOGIN
# --------------------------------

if "logged_in" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()


if st.session_state.get("role") != "Farmer":

    st.error(
        "This page is only available to farmers."
    )

    st.stop()


user_id = st.session_state.user_id


# --------------------------------
# PAGE TITLE
# --------------------------------

st.title(
    "📋 Disease Assessment History"
)

st.write(
    "View your previous crop disease analyses."
)

st.divider()


# --------------------------------
# GET DISEASE ASSESSMENTS
# --------------------------------

connection = sqlite3.connect(
    DATABASE
)

cursor = connection.cursor()


cursor.execute(
    """
    SELECT

        disease_assessments.id,

        crops.crop_name,

        crops.variety,

        fields.field_name,

        disease_assessments.predicted_disease,

        disease_assessments.confidence,

        disease_assessments.model_version,

        disease_assessments.image_path,

        disease_assessments.created_at

    FROM disease_assessments

    JOIN crops
        ON disease_assessments.crop_id = crops.id

    JOIN fields
        ON crops.field_id = fields.id

    JOIN farms
        ON fields.farm_id = farms.id

    WHERE farms.user_id = ?

    ORDER BY disease_assessments.id DESC
    """,
    (
        user_id,
    )
)


assessments = cursor.fetchall()


connection.close()


# --------------------------------
# NO ASSESSMENTS
# --------------------------------

if not assessments:

    st.info(
        "You have not performed any disease "
        "assessments yet."
    )

    st.stop()


# --------------------------------
# SUMMARY
# --------------------------------

st.subheader("📊 Assessment Summary")

total_assessments = len(assessments)

healthy_count = sum(
    1 for assessment in assessments
    if assessment[4] == "healthy"
)

disease_count = sum(
    1 for assessment in assessments
    if assessment[4] and assessment[4] != "healthy"
)

latest_assessment = assessments[0][8]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Assessments", total_assessments)

with col2:
    st.metric("Healthy Plants", healthy_count)

with col3:
    st.metric("Diseases Detected", disease_count)

with col4:
    st.metric("Latest Assessment", latest_assessment)

st.divider()


# --------------------------------
# DISPLAY ASSESSMENTS
# --------------------------------

for assessment in assessments:

    assessment_id = assessment[0]

    crop_name = assessment[1]

    variety = assessment[2]

    field_name = assessment[3]

    predicted_disease = assessment[4]

    confidence = assessment[5]

    model_version = assessment[6]

    image_path = assessment[7]

    assessment_date = assessment[8]




    with st.expander(

        f"🌱 {crop_name} | "
        f"{predicted_disease or 'Analysis Pending'}"

    ):


        st.write(
            f"**Crop:** {crop_name}"
        )


        st.write(
            f"**Variety:** "
            f"{variety or 'Not specified'}"
        )


        st.write(
            f"**Field:** {field_name}"
        )


        st.divider()

        st.write(
            f"**Assessment Date:** {assessment_date}"
        )


        # --------------------------------
        # DISEASE RESULT
        # --------------------------------
        if predicted_disease:

            disease_names = {
                "healthy": "Healthy Onion Plant",
                "iris_yellow_virus": "Iris Yellow Virus",
                "leaf_blight": "Leaf Blight",
                "purple_blotch": "Purple Blotch"
            }

            disease_name = disease_names.get(
                predicted_disease,
                predicted_disease.replace("_", " ").title()
            )

            st.write(
                f"**Disease Prediction:** "
                f"{disease_name}"
            )

            if confidence >= 80:
                confidence_status = "High Confidence"
            elif confidence >= 60:
                confidence_status = "Moderate Confidence"
            else:
                confidence_status = "Low Confidence"

            st.write(
                f"**Confidence:** "
                f"{confidence:.2f}% — {confidence_status}"
            )

            st.write(
                f"**Model:** "
                f"{model_version}"
            )

            st.write("**Recommendation:**")

            recommendations = {
                "healthy": (
                    "Your onion plant appears healthy."
                    "Continue regular field monitoring,"
                    "good farm hygiene, and proper crop management."
                ),
                "iris_yellow_virus": (
                    "Monitor the crop closely for further symptoms."
                    "Manage thrips and remove severely affected plants"
                    "where appropriate. Consult an agronomist for "
                    "intergrated pest and disease management."
                ),

                "leaf_blight":  (
                    "Remove heavily affected plant material where appropriate."
                    "Avoid prolonged leaf wetness, maintain field sanitation,"
                    "and consult an agronomist for appropriate disease management."                    
                ),

                "purple_blotch": (
                    "Monitor affected plants closely. Remove severely infected "
                    "leaves where appropriate, maintain field sanitation, "
                    "and avoid prolonged leaf wetness. Consult an agronomist "
                    "for appropriate disease management. "
                )
            }

            recommendation = recommendations.get(
                predicted_disease,
                "No recommendation is currently available for this assessment."
            )

            st.info(recommendation)

            st.subheader("Immediate Actions")

            disease_information = DISEASE_INFORMATION.get(
                predicted_disease
            )

            if disease_information:

                immediate_actions = disease_information.get(
                    "immediate_actions",
                    []
                )
                for action in immediate_actions:
                    st.write(f"• {action}")

                st.subheader("Prevention")

                prevention = disease_information.get(
                    "prevention",
                    []
                )
                for item in prevention:
                    st.write(f"• {item}")

                st.subheader("Management Options")

                management_options = disease_information.get(
                     "management_options",
                      {}
                )

                # Cultural Management
                st.write("**Cultural Management**")

                cultural_management = management_options.get(
                    "cultural",
                    []
                )

                for item in cultural_management:
                    st.write(f"• {item}")

                # Integrated Management
                st.write("**Integrated Management**")

                integrated_management = management_options.get(
                    "integrated",
                    []
                )

                for item in integrated_management:
                    st.write(f"• {item}")

                # Chemical Management
                st.write("**Chemical Management**")

                chemical_management = management_options.get(
                    "chemical",
                    ""
                )

                if chemical_management:
                    st.warning(chemical_management)


                st.subheader("When to Consult an Agronomist")

                agronomist_referral = disease_information.get(
                    "agronomist_referral"
                )          

                if agronomist_referral:
                    st.info(agronomist_referral)
        else:

            st.warning(
                "AI analysis is not available "
                "for this assessment."
            )

        st.divider()
        # --------------------------------
        # SHOW IMAGE
        # --------------------------------

        if image_path:

            try:

                st.image(
                    image_path,
                    caption="Analyzed Crop Image",
                    width="stretch"
                )

            except Exception:

                st.warning(
                    "The uploaded image "
                    "could not be displayed."
                )