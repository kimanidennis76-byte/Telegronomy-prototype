import sqlite3
import streamlit as st
from datetime import date


DATABASE = "database/telegronomy.db"


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
# PAGE
# --------------------------------

st.title("🔍 Crop Health")

st.write(
    f"Welcome, {st.session_state.full_name}"
)

st.write(
    "Record what you are observing in your crops."
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
        "You need to add a crop before creating a health assessment."
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


# --------------------------------
# HEALTH ASSESSMENT
# --------------------------------

st.header("Crop Health Assessment")


overall_health = st.selectbox(
    "Overall Crop Health",
    [
        "Healthy",
        "Needs Attention",
        "Poor"
    ]
)


symptoms = st.multiselect(
    "Symptoms Observed",
    [
        "No symptoms",
        "Yellowing leaves",
        "Leaf spots",
        "Wilting",
        "Stunted growth",
        "Pest damage",
        "Discoloration",
        "Leaf curling",
        "Root damage",
        "Fruit damage",
        "Other"
    ]
)


farmer_notes = st.text_area(
    "Farmer Notes",
    placeholder="Describe what you are seeing in the crop..."
)


assessment_date = st.date_input(
    "Assessment Date",
    value=date.today()
)


# --------------------------------
# SAVE ASSESSMENT
# --------------------------------

if st.button("Save Health Assessment"):

    if not symptoms and not farmer_notes:

        st.error(
            "Please record at least one symptom or add a note."
        )

    else:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO crop_health_assessments
            (
                crop_id,
                overall_health,
                symptoms,
                farmer_notes,
                assessment_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                crop_id,
                overall_health,
                ", ".join(symptoms),
                farmer_notes,
                str(assessment_date)
            )
        )

        connection.commit()

        connection.close()

        st.success(
            "Crop health assessment saved successfully!"
        )


# --------------------------------
# DISPLAY ASSESSMENTS
# --------------------------------

st.divider()

st.header("Previous Assessments")


connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        crop_health_assessments.overall_health,
        crop_health_assessments.symptoms,
        crop_health_assessments.farmer_notes,
        crop_health_assessments.assessment_date,
        crops.crop_name,
        crops.variety,
        fields.field_name
    FROM crop_health_assessments

    JOIN crops
        ON crop_health_assessments.crop_id = crops.id

    JOIN fields
        ON crops.field_id = fields.id

    JOIN farms
        ON fields.farm_id = farms.id

    WHERE farms.user_id = ?

    ORDER BY crop_health_assessments.id DESC
    """,
    (user_id,)
)

assessments = cursor.fetchall()

connection.close()


if assessments:

    for assessment in assessments:

        st.subheader(
            f"🌱 {assessment[4]}"
        )

        st.write(
            f"Variety: {assessment[5] or 'Not specified'}"
        )

        st.write(
            f"Field: {assessment[6]}"
        )

        st.write(
            f"Overall Health: {assessment[0]}"
        )

        st.write(
            f"Symptoms: {assessment[1] or 'None recorded'}"
        )

        st.write(
            f"Notes: {assessment[2] or 'No notes'}"
        )

        st.write(
            f"Assessment Date: {assessment[3]}"
        )

        st.divider()

else:

    st.info(
        "No health assessments have been recorded yet."
    )