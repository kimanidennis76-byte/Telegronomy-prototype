import os
import sys
import sqlite3

from pathlib import Path

import streamlit as st


# --------------------------------
# PROJECT PATH
# --------------------------------

PROJECT_DIR = (
    Path(__file__).resolve()
    .parent.parent.parent
)


# --------------------------------
# AI MODEL PATH
# --------------------------------

INFERENCE_DIR = (
    PROJECT_DIR
    / "ML"
    / "inference"
)


sys.path.insert(
    0,
    str(INFERENCE_DIR)
)


# --------------------------------
# IMPORT AI PREDICTION MODEL
# --------------------------------

from predict_onion_disease import (
    predict_image
)

DATABASE = "database/telegronomy.db"
UPLOAD_FOLDER = "uploads"


# --------------------------------
# CHECK LOGIN
# --------------------------------

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()


if st.session_state.get("role") != "Farmer":
    st.error("This page is only available to farmers.")
    st.stop()


user_id = st.session_state.user_id


# --------------------------------
# CREATE UPLOAD FOLDER
# --------------------------------

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------
# PAGE
# --------------------------------

st.title("🤖 Crop Disease Detection")

st.write(
    f"Welcome, {st.session_state.full_name}"
)

st.write(
    "Upload a photograph of your crop for disease analysis."
)

st.divider()


# --------------------------------
# GET FARMER'S CROPS
# --------------------------------

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        crops.id,
        crops.crop_name,
        crops.variety,
        fields.field_name,
        farms.farm_name
    FROM crops

    JOIN fields
        ON crops.field_id = fields.id

    JOIN farms
        ON fields.farm_id = farms.id

    WHERE farms.user_id = ?
    """,
    (user_id,)
)

crops = cursor.fetchall()

connection.close()


if not crops:

    st.warning(
        "You need to add a crop before using disease detection."
    )

    st.stop()


# --------------------------------
# SELECT CROP
# --------------------------------

crop_options = {
    f"{crop[4]} → {crop[3]} → {crop[1]} "
    f"({crop[2] or 'Variety not specified'})": crop[0]
    for crop in crops
}


selected_crop = st.selectbox(
    "Select Crop",
    list(crop_options.keys())
)

crop_id = crop_options[selected_crop]

selected_crop_data = next(
    crop
    for crop in crops
    if crop[0] == crop_id
)

selected_crop_name = selected_crop_data[1]



# --------------------------------
# IMAGE UPLOAD
# --------------------------------

st.header("Upload Crop Photograph")

uploaded_file = st.file_uploader(
    "Choose a crop image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded Crop Image",
        use_container_width=True
    )


# --------------------------------
# ANALYZE
# --------------------------------

if st.button("Analyze Crop"):

    if uploaded_file is None:

        st.error(
            "Please upload a crop photograph first."
        )

    else:

        if uploaded_file:
            st.image(
                uploaded_file,
                caption="Uploaded Crop Image",
                width="stretch"
            )

        file_name = (
            f"crop_{crop_id}_"
            f"{st.session_state.user_id}_"
            f"{uploaded_file.name}"
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file_name
        )

        with open(file_path, "wb") as file:

            file.write(
                uploaded_file.getbuffer()
            )
          
        # --------------------------------
        # AI DISEASE ANALYSIS
        # --------------------------------

        predicted_disease = None

        disease_name = None

        confidence = None

        confidence_status = None

        recommendation = None

        confidence_warning = None

        model_version = None


        if selected_crop_name.strip().lower() == "onion":

            with st.spinner(
                "Telegronomy is analyzing your onion crop..."
            ):

                (
                    predicted_disease,
                    disease_name,
                    confidence,
                    confidence_status,
                    recommendation,
                    confidence_warning
                ) = predict_image(
                    file_path
                )


            model_version = (
                "Telegronomy Onion AI v1.0"
            )

        # --------------------------------
        # SAVE DISEASE ASSESSMENT
        # --------------------------------

        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO disease_assessments
            (
                crop_id,
                image_path,
                predicted_disease,
                confidence,
                model_version
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                crop_id,
                file_path,
                predicted_disease,
                confidence,
                model_version
            )
        )

        connection.commit()

        connection.close()


        # --------------------------------
        # DISPLAY RESULTS
        # --------------------------------

        st.success(
            "Crop photograph analyzed successfully!"
        )


        if selected_crop_name.strip().lower() == "onion":

            st.subheader(
                "🤖 Telegronomy Results"
            )

            st.write(
                f"**Disease:** {disease_name}"
            )

            st.write(
                f"**Confidence:** "
                f"{confidence:.2f}%"
            )

            st.write(
                f"**Status:** "
                f"{confidence_status}"
            )


            st.divider()


            st.subheader(
                "🌱 Recommendation"
            )

            st.write(
                recommendation
            )


            st.divider()


            st.warning(
                confidence_warning
            )


        else:

            st.info(
                "AI disease detection is currently "
                "available for Onion crops only."
            )