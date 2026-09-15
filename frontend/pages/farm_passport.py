import sqlite3
import streamlit as st


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Digital Farm Passport",
    page_icon="📖",
    layout="centered"
)


# --------------------------------
# DATABASE
# --------------------------------

DATABASE = "database/telegronomy.db"


# --------------------------------
# LOGIN CHECK
# --------------------------------

if "user_id" not in st.session_state:

    st.error("Please log in first.")
    st.stop()


user_id = st.session_state["user_id"]
user_name = st.session_state.get("full_name", "Farmer")


# --------------------------------
# PAGE HEADER
# --------------------------------

st.title("📖 Digital Farm Passport")

st.write(
    f"Welcome, {user_name}. "
    "This is your digital record of farm activities and crop health."
)

st.divider()


# --------------------------------
# LOAD FARM INFORMATION
# --------------------------------

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        id,
        farm_name,
        location
    FROM farms
    WHERE user_id = ?
    ORDER BY id DESC
    """,
    (user_id,)
)

farms = cursor.fetchall()


# --------------------------------
# LOAD FARM STATISTICS
# --------------------------------

cursor.execute(
    """
    SELECT COUNT(*)
    FROM fields
    JOIN farms
        ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    """,
    (user_id,)
)

field_count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM crops
    JOIN fields
        ON crops.field_id = fields.id
    JOIN farms
        ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    """,
    (user_id,)
)

crop_count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM disease_assessments
    JOIN crops
        ON disease_assessments.crop_id = crops.id
    JOIN fields
        ON crops.field_id = fields.id
    JOIN farms
        ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    """,
    (user_id,)
)

assessment_count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM agronomist_consultations
    WHERE user_id = ?
    """,
    (user_id,)
)

consultation_count = cursor.fetchone()[0]


connection.close()


# --------------------------------
# PASSPORT SUMMARY
# --------------------------------

st.header("📊 Farm Passport Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Farms", len(farms))

with col2:
    st.metric("Fields", field_count)

with col3:
    st.metric("Crops", crop_count)

with col4:
    st.metric("Assessments", assessment_count)


st.divider()


# --------------------------------
# FARM INFORMATION
# --------------------------------

st.header("🏡 My Farms")

if farms:

    for farm in farms:

        farm_id = farm[0]
        farm_name = farm[1]
        location = farm[2] or "Location not specified"

        with st.container():

            st.subheader(f"🏡 {farm_name}")

            st.write(
                f"**Location:** {location}"
            )

            st.write(
                f"**Farm ID:** {farm_id}"
            )

            st.divider()

else:

    st.info(
        "You have not added any farms yet."
    )

    # --------------------------------
# FIELDS AND CROPS
# --------------------------------

st.header("🌾 Fields & Crops")

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        fields.id,
        fields.field_name,
        crops.id,
        crops.crop_name,
        crops.variety
    FROM fields
    JOIN farms
        ON fields.farm_id = farms.id
    LEFT JOIN crops
        ON crops.field_id = fields.id
    WHERE farms.user_id = ?
    ORDER BY fields.id DESC, crops.id DESC
    """,
    (user_id,)
)

field_crops = cursor.fetchall()

connection.close()


if field_crops:

    current_field = None

    for record in field_crops:

        field_id = record[0]
        field_name = record[1]
        crop_id = record[2]
        crop_name = record[3]
        variety = record[4]

        if field_id != current_field:

            st.subheader(
                f"🌱 Field: {field_name}"
            )

            current_field = field_id

        if crop_id:

            st.write(
                f"**Crop:** {crop_name}"
            )

            st.write(
                f"**Variety:** "
                f"{variety or 'Variety not specified'}"
            )

            st.divider()

        else:

            st.info(
                "No crops have been added to this field yet."
            )

else:

    st.info(
        "You have not added any fields yet."
    )

# --------------------------------
# DISEASE ASSESSMENT HISTORY
# --------------------------------

st.header("🔍 Disease Assessment History")

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        disease_assessments.id,
        crops.crop_name,
        fields.field_name,
        disease_assessments.predicted_disease,
        disease_assessments.confidence,
        disease_assessments.model_version,
        disease_assessments.created_at
    FROM disease_assessments
    JOIN crops
        ON disease_assessments.crop_id = crops.id
    JOIN fields
        ON crops.field_id = fields.id
    JOIN farms
        ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    ORDER BY
        disease_assessments.created_at DESC,
        disease_assessments.id DESC
    """,
    (user_id,)
)

assessment_history = cursor.fetchall()

connection.close()


if assessment_history:

    disease_names = {
        "healthy": "Healthy Onion Plant",
        "iris_yellow_virus": "Iris Yellow Virus",
        "leaf_blight": "Leaf Blight",
        "purple_blotch": "Purple Blotch"
    }

    for assessment in assessment_history:

        assessment_id = assessment[0]
        crop_name = assessment[1]
        field_name = assessment[2]
        predicted_disease = assessment[3]
        confidence = assessment[4]
        model_version = assessment[5]
        created_at = assessment[6]

        disease_name = disease_names.get(
            predicted_disease,
            predicted_disease.replace("_", " ").title()
        )

        if confidence >= 80:

            confidence_status = "🟢 High Confidence"

        elif confidence >= 60:

            confidence_status = "🟡 Moderate Confidence"

        else:

            confidence_status = "🔴 Low Confidence"

        with st.expander(
            f"🔍 Assessment #{assessment_id:04d} — {disease_name}"
        ):

            st.write(
                f"**Crop:** {crop_name}"
            )

            st.write(
                f"**Field:** {field_name}"
            )

            st.write(
                f"**Result:** {disease_name}"
            )

            st.write(
                f"**Confidence:** "
                f"{confidence:.2f}% — {confidence_status}"
            )

            st.write(
                f"**AI Model:** {model_version}"
            )

            st.write(
                f"**Assessment Date:** {created_at}"
            )

else:

    st.info(
        "No disease assessments have been recorded yet."
    )

# --------------------------------
# AGRONOMIST CONSULTATION HISTORY
# --------------------------------

st.header("👨🏾‍🌾 Agronomist Consultation History")

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        agronomist_consultations.id,
        crops.crop_name,
        fields.field_name,
        agronomist_consultations.issue,
        agronomist_consultations.description,
        agronomist_consultations.status,
        agronomist_consultations.created_at,
        agronomist_consultations.agronomist_response,
        agronomist_consultations.management_advice,
        agronomist_consultations.follow_up_required
    FROM agronomist_consultations
    JOIN crops
        ON agronomist_consultations.crop_id = crops.id
    JOIN fields
        ON crops.field_id = fields.id
    WHERE agronomist_consultations.user_id = ?
    ORDER BY
        agronomist_consultations.created_at DESC,
        agronomist_consultations.id DESC
    """,
    (user_id,)
)

consultation_history = cursor.fetchall()

connection.close()


if consultation_history:

    for consultation in consultation_history:

        consultation_id = consultation[0]
        crop_name = consultation[1]
        field_name = consultation[2]
        issue = consultation[3]
        description = consultation[4]
        status = consultation[5]
        created_at = consultation[6]
        agronomist_response = consultation[7]
        management_advice = consultation[8]
        follow_up_required = consultation[9]

        if status == "Pending":

            status_display = "🟡 Pending"

        elif status == "Under Review":

            status_display = "🔎 Under Review"

        elif status == "Responded":

            status_display = "✅ Responded"

        else:

            status_display = status

        with st.expander(
            f"👨🏾‍🌾 Consultation #{consultation_id:04d} — {crop_name}"
        ):

            st.write(
                f"**Crop:** {crop_name}"
            )

            st.write(
                f"**Field:** {field_name}"
            )

            st.write(
                f"**Issue:** {issue}"
            )

            st.write(
                f"**Description:** {description}"
            )

            st.write(
                f"**Status:** {status_display}"
            )

            st.write(
                f"**Submitted:** {created_at}"
            )

            if status == "Responded":

                st.divider()

                st.subheader("👨🏾‍🌾 Agronomist Response")

                if agronomist_response:

                    st.write(
                        agronomist_response
                    )

                st.subheader("📋 Management Advice")

                if management_advice:

                    st.write(
                        management_advice
                    )

                st.subheader("🔄 Follow-up Required")

                if follow_up_required == "YES":

                    st.warning(
                        "Yes — follow-up is recommended."
                    )

                else:

                    st.success(
                        "No follow-up is currently required."
                    )

else:

    st.info(
        "No agronomist consultations have been recorded yet."
    )

# --------------------------------
# RECORD SUMMARY
# --------------------------------

st.header("📚 Agricultural Records")

col1, col2 = st.columns(2)

with col1:

    st.write(
        f"🔍 **Disease Assessments:** {assessment_count}"
    )

with col2:

    st.write(
        f"👨🏾‍🌾 **Agronomist Consultations:** {consultation_count}"
    )


st.info(
    "Your Digital Farm Passport will continue to grow "
    "as you add crops, perform health assessments, "
    "and consult agronomists."
)