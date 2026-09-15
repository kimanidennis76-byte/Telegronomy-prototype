import sqlite3
import streamlit as st
import os


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Farmer Dashboard",
    page_icon="🌱",
    layout="wide"
)


# --------------------------------
# LOGIN CHECK
# --------------------------------

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()


if st.session_state.get("role") != "Farmer":
    st.error("This page is only available to farmers.")
    st.stop()


# --------------------------------
# DATABASE
# --------------------------------

DATABASE = "database/telegronomy.db"

user_id = st.session_state.get("user_id")


# --------------------------------
# GET FARM DATA
# --------------------------------

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


# Number of farms
cursor.execute(
    """
    SELECT COUNT(*)
    FROM farms
    WHERE user_id = ?
    """,
    (user_id,)
)

farm_count = cursor.fetchone()[0]


# Number of fields
cursor.execute(
    """
    SELECT COUNT(*)
    FROM fields
    JOIN farms ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    """,
    (user_id,)
)

field_count = cursor.fetchone()[0]


# Number of crops
cursor.execute(
    """
    SELECT COUNT(*)
    FROM crops
    JOIN fields ON crops.field_id = fields.id
    JOIN farms ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    """,
    (user_id,)
)

crop_count = cursor.fetchone()[0]


# Latest disease assessments
cursor.execute(
    """
    SELECT
        disease_assessments.predicted_disease
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
    LIMIT 1
    """,
    (user_id,)
)

latest_disease = cursor.fetchone()

# Farmer's crops with latest disease
cursor.execute(
    """
    SELECT
        crops.id,
        crops.crop_name,
        crops.variety,
        fields.field_name,
        farms.farm_name,
        
        (   SELECT disease_assessments.predicted_disease
            FROM disease_assessments
            WHERE disease_assessments.crop_id = crops.id
            ORDER BY
                disease_assessments.created_at DESC,
                disease_assessments.id DESC
            LIMIT 1
        )  AS latest_disease

    FROM crops

    JOIN fields
        ON crops.field_id = fields.id

    JOIN farms
        ON fields.farm_id = farms.id

    WHERE farms.user_id = ?

    ORDER BY crops.id DESC
    """,
    (user_id,)
)

farmer_crops = cursor.fetchall()

connection.close()

# --------------------------------
# FARM HEALTH STATUS
# --------------------------------

if latest_disease is None:

    farm_health = "⚪ No Assessment"

elif latest_disease[0] ==  "healthy":

    farm_health = "🟢 Healthy"

else:

    farm_health = "🟠 Needs Attention"




# --------------------------------
# FARMER HEADER
# --------------------------------

st.title("🌱 Telegronomy")

st.subheader(
    f"Welcome, {st.session_state.get('full_name', 'Farmer')}"
)

st.write(
    "Your intelligent agricultural companion."
)

st.divider()


# --------------------------------
# FARM OVERVIEW
# --------------------------------
st.subheader("🏡 Farm Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏡 Farms",
        farm_count
    )

with col2:
    st.metric(
        "🌾 Fields",
        field_count
    )

with col3:
    st.metric(
        "🌱 Crops",
        crop_count
    )

with col4:
    st.metric(
        "❤️ Farm Health",
        farm_health
    )


st.divider()

# -------------------------------
# MY CROPS
# --------------------------------
st.header("🌾 My Crops")

if farmer_crops:

    for crop in farmer_crops:

        crop_id = crop[0]
        crop_name = crop[1]
        variety = crop[2] or "variety not specified"
        field_name = crop[3]
        farm_name = crop[4]
        latest_disease = crop[5]

        with st.container():

            st.subheader(f"🌱 {crop_name}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write(f"**🏡 Farm**") 
                st.write(f"{farm_name}")

            with col2:
                st.write(f"**🌾 Field:**")
                st.write(f"{field_name}")

            with col3:
                st.write(f"**🌱 Variety:**")
                st.write(f"{variety}")

            with col4:
                st.write("**📊 Status**")

                if latest_disease is None:
                    st.write("⚪ No Assessment")

                elif latest_disease == "healthy":

                    st.write("🟢 Healthy")

                else:

                    st.write(f" 🟠{latest_disease.replace('_', ' ').title()}")
                    
    
        st.divider()

else:
    st.info(
        "You have not added any crop yet."
    )

    
# --------------------------------
# MAIN FEATURES
# --------------------------------


st.header("Telegronomy Services")

# ---------------------------------------------------------
# MANAGE YOUR FARM
# ---------------------------------------------------------

st.subheader("🌱 Manage Your Farm")

col1, col2 = st.columns(2)

with col1:
    st.write("### 🏡 My Farm")
    st.write(
        "Manage your farm, fields and crops."
    )

    if st.button(
        "Open My Farm",
        key="open_my_farm"
    ):
        st.switch_page("pages/my_farm.py")


with col2:
    st.write("### 📖 Digital Farm Passport")
    st.write(
        "View your farm history and agricultural records."
    )

    if st.button(
        "Open Farm Passport",
        key="open_farm_passport"
    ):
        st.switch_page("pages/farm_passport.py")


st.divider()


# ---------------------------------------------------------
# MONITOR YOUR FARM
# ---------------------------------------------------------

st.subheader("🔍 Monitor Your Farm")

col1, col2 = st.columns(2)

with col1:
    st.write("### 🌿 Crop Health")
    st.write(
        "Record and monitor the health of your crops."
    )

    if st.button(
        "Check Crop Health",
        key="check_crop_health"
    ):
        st.switch_page("pages/crop_health.py")


with col2:
    st.write("### 🤖 AI Disease Detection")
    st.write(
        "Use AI to analyze a crop photograph."
    )

    if st.button(
        "Analyze Crop Disease",
        key="analyze_crop_disease"
    ):
        st.switch_page("pages/disease_detection.py")


st.divider()


# ---------------------------------------------------------
# GET EXPERT SUPPORT
# ---------------------------------------------------------

st.subheader("👨🏾‍🌾 Get Expert Support")

st.write(
    "Connect with agricultural professionals "
    "when you need additional guidance."
)

if st.button(
    "Consult Agronomist",
    key="consult_agronomist"
):
    st.session_state["show_agronomist_form"] = True


# --------------------------------
# AGRONOMIST CONSULTATION
# --------------------------------

if st.session_state.get("show_agronomist_form", False):

    st.divider()

    st.header("👨🏾‍🌾 Consult an Agronomist")

    st.write(
        "Describe the agricultural issue you are experiencing "
        "and an agronomist can review your request."
    )

    # Crop selection
    if farmer_crops:

        consultation_crop_options = {
            f"{crop[1]} → {crop[3]}": crop[0]
            for crop in farmer_crops
        }

        selected_consultation_crop = st.selectbox(
            "Select Crop",
            list(consultation_crop_options.keys())
        )

        consultation_crop_id = consultation_crop_options[
            selected_consultation_crop
        ]

    else:

        st.warning(
            "Please add a crop to your farm before consulting an agronomist."
        )

        consultation_crop_id = None

    # Issue
    issue = st.selectbox(
        "What do you need help with?",
        [
            "Crop disease",
            "Pest problem",
            "Nutrient deficiency",
            "Crop management",
            "Plant growth problem",
            "Other"
        ]
    )

    # Description
    description = st.text_area(
        "Describe the problem",
        placeholder=(
            "Example: The leaves of my onion plants are developing "
            "purple spots and the plants are becoming weak."
        ),
        height=150
    )

    # Optional photo
    consultation_image = st.file_uploader(
        "Attach a crop photo (optional)",
        type=["jpg", "jpeg", "png"],
        key="agronomist_photo"
    )

    col_submit, col_cancel = st.columns(2)

    with col_submit:

        if st.button("📨 Submit Consultation Request"):

            if consultation_crop_id is None:

                st.error(
                     "Please add a crop before submitting a consultation."
                )

            elif not description.strip():

                st.error(
                    "Please describe the problem before submitting."
                )

            else:

        # -----------------------------
        # SAVE CONSULTATION TO DATABASE
        # -----------------------------

                connection = sqlite3.connect(DATABASE)
                cursor = connection.cursor()

                image_path = None

                # Save photo if one was attached
                if consultation_image:

                    upload_folder = "uploads"
                    os.makedirs(upload_folder, exist_ok=True)

                    image_path = os.path.join(
                        upload_folder,
                        f"consultation_{user_id}_{consultation_image.name}"
                    )

                    with open(image_path, "wb") as file:

                        file.write(
                            consultation_image.getbuffer()
                        )

                cursor.execute(
                    """
                    INSERT INTO agronomist_consultations
                    (
                        user_id,
                        crop_id,
                        issue,
                        description,
                        image_path,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        consultation_crop_id,
                        issue,
                        description.strip(),
                        image_path,
                        "Pending"
                    )
                )

                consultation_id = cursor.lastrowid

                connection.commit()
                connection.close()

                # -----------------------------
                # CONFIRMATION
                # -----------------------------

                st.success(
                    "✅ Consultation request submitted successfully."
                )

                st.write("### Consultation Summary")

                st.write(
                    f"**Consultation:** #{consultation_id:04d}"
                )

                st.write(
                    f"**Crop:** {selected_consultation_crop}"
                )

                st.write(
                    f"**Issue:** {issue}"
                )

                st.write(
                    f"**Description:** {description}"
                )

            st.write(
                    "**Status:** 🟡 Pending"
            )

            if consultation_image:

                st.write(
                    "**Photo:** Attached"
                )

            else:

                st.write(
                    "**Photo:** Not attached"
                )

            st.info(
                "Your consultation request has been received. "
                "An agronomist will review your request and provide "
                "professional agricultural guidance."
            )    
                    

    with col_cancel:

        if st.button("Cancel Consultation"):

            st.session_state["show_agronomist_form"] = False

            st.rerun()
    # --------------------------------
# AGRONOMIST CONSULTATION HISTORY
# --------------------------------

st.divider()

st.header("📋 My Agronomist Consultations")

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
        agronomist_consultations.image_path,
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

consultations = cursor.fetchall()

connection.close()


if consultations:

    for consultation in consultations:

        consultation_id = consultation[0]
        crop_name = consultation[1]
        field_name = consultation[2]
        issue = consultation[3]
        description = consultation[4]
        status = consultation[5]
        created_at = consultation[6]
        image_path = consultation[7]
        agronomist_response = consultation[8]
        management_advice = consultation[9]
        follow_up_required = consultation[10]

       # -------------------------------------------
       # STATUS DISPLAY
       # -------------------------------------------
        if status == "Pending":

            status_display = "🟡 Pending"

        elif status == "Under Review":

            status_display =  "🔎 Under Review"

        elif status == "Responded":

            status_display = "✅ Responded"

        else:

            status_display = status

        # -----------------------------------------
        # CONSULTATION HEADER
        # -----------------------------------------
        with st.expander(
            f"👨🏾‍🌾 Consultation #{consultation_id:04} - {crop_name}"
        ):
            st.write("### 📋 Consultation Details")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**🌱 Crop:** {crop_name}")

                st.write(f"**🌾 Field:** {field_name}")

                st.write(f"**📌 Issue:** {issue}")

            with col2:
                st.write(f"**📊 Status:** {status_display}")

                st.write(f"**📅 Submitted:** {created_at}")

                if image_path:

                    st.write("**📷 Photo:** Attached")

                else:

                    st.write("**📷 Photo:** Not attached")

            st.divider()

            st.write("### 📝 Your Description")

            st.write(description)

            # ------------------------------------
            # AGRONOMIST RESPONSE
            # ------------------------------------
            if status == "Responded":

                st.divider()

                st.subheader("👨🏾‍🌾 Agronomist Response")

                if agronomist_response:

                    st.info(
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
                        "Yes - follow-up is recommended."
                    )

                else:

                    st.success(
                        "No follow-up is currently required."
                    )
else:
    st.info(
        "You have not submitted any agronomist consultation yet."
    )