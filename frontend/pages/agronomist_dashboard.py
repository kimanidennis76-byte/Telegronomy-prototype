import sqlite3
import streamlit as st
import os


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Agronomist Dashboard",
    page_icon="👨🏾‍🌾",
    layout="wide"
)


# --------------------------------
# LOGIN CHECK
# --------------------------------

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()


if st.session_state.get("role") != "Agronomist":
    st.error(
        "This page is only available to agronomists."
    )
    st.stop()


# --------------------------------
# DATABASE
# --------------------------------

DATABASE = "database/telegronomy.db"


# --------------------------------
# HEADER
# --------------------------------

st.title("👨🏾‍🌾 Agronomist Dashboard")

st.subheader(
    f"Welcome, {st.session_state.get('full_name', 'Agronomist')}"
)

st.write(
    "Review farmer consultation requests and provide "
    "professional agricultural guidance."
)

st.divider()


# --------------------------------
# CONSULTATION SUMMARY
# --------------------------------

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


cursor.execute(
    """
    SELECT COUNT(*)
    FROM agronomist_consultations
    WHERE status = 'Pending'
    """
)

pending_count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM agronomist_consultations
    WHERE status = 'Under Review'
    """
)

under_review_count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM agronomist_consultations
    WHERE status = 'Responded'
    """
)

responded_count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM agronomist_consultations
    """
)

total_count = cursor.fetchone()[0]


connection.close()


st.header("📊 Consultation Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Consultations",
        total_count
    )


with col2:

    st.metric(
        "Pending",
        pending_count
    )


with col3:

    st.metric(
        "Under Review",
        under_review_count
    )


with col4:

    st.metric(
        "Responded",
        responded_count
    )


st.divider()


# --------------------------------
# CONSULTATION REQUESTS
# --------------------------------

st.header("📋 Farmer Consultation Requests")


connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


cursor.execute(
    """
    SELECT
        agronomist_consultations.id,
        users.full_name,
        crops.crop_name,
        fields.field_name,
        agronomist_consultations.issue,
        agronomist_consultations.description,
        agronomist_consultations.status,
        agronomist_consultations.created_at,
        agronomist_consultations.image_path
    FROM agronomist_consultations

    JOIN users
        ON agronomist_consultations.user_id = users.id

    JOIN crops
        ON agronomist_consultations.crop_id = crops.id

    JOIN fields
        ON crops.field_id = fields.id

    ORDER BY
        agronomist_consultations.created_at DESC,
        agronomist_consultations.id DESC
    """
)


consultations = cursor.fetchall()

connection.close()


if consultations:

    for consultation in consultations:

        consultation_id = consultation[0]
        farmer_name = consultation[1]
        crop_name = consultation[2]
        field_name = consultation[3]
        issue = consultation[4]
        description = consultation[5]
        status = consultation[6]
        created_at = consultation[7]
        image_path = consultation[8]

        with st.expander(
            f"👨🏾‍🌾 Consultation #{consultation_id:04d} — "
            f"{crop_name} — {status}"
        ):

            st.subheader("📋 Consultation Details")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Farmer:** {farmer_name}"
                )

                st.write(
                    f"**Crop:** {crop_name}"
                )

                st.write(
                    f"**Field:** {field_name}"
                )

                st.write(
                    f"**Issue:** {issue}"
                )

            with col2:

                st.write(
                    f"**Status:** {status}"
                )

                st.write(
                    f"**Submitted:** {created_at}"
                )

            st.divider()

            st.subheader("📝 Farmer's Description")

            st.write(description)

            # --------------------------------
            # ATTACHED PHOTO
            # --------------------------------

            if image_path:

                st.subheader("📷 Crop Photo")

                if os.path.exists(image_path):

                    st.image(
                        image_path,
                        width="stretch"
                    )

                else:

                    st.warning(
                        "The consultation photo could not be found."
                    )

            else:

                st.write(
                    "**Photo:** Not attached"
                )

            st.divider()

            # --------------------------------
            # START REVIEW
            # --------------------------------

            if status == "Pending":

                if st.button(
                    "🔎 Start Review",
                    key=f"review_{consultation_id}"
                ):

                    connection = sqlite3.connect(DATABASE)
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        UPDATE agronomist_consultations
                        SET status = 'Under Review'
                        WHERE id = ?
                        """,
                        (consultation_id,)
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        f"Consultation #{consultation_id:04d} "
                        "is now under review."
                    )

                    st.rerun()

            elif status == "Under Review":

                st.info(
                    "🔎 This consultation is currently under review."
                )

                st.subheader("🧑🏾‍🌾 Agronomist Response")

                agronomist_response = st.text_area(
                    "Professional Response",
                    placeholder=(
                         "Explain your assessment of the farmer's problem."
                    ),
                    height=150,
                    key=f"response_{consultation_id}"
                )


                management_advice = st.text_area(
                    "Management Advice",
                    placeholder=(
                        "Provide practical management recommendations "
                        "for the farmer."
                    ),
                    height=150,
                    key=f"management_{consultation_id}"
                )

                follow_up_required = st.radio(
                    "Follow-up Required?",
                    ["NO", "YES"],
                    horizontal=True,
                    key=f"followup_{consultation_id}"
                )

                if st.button(
                    "📨 Submit Agronomist Response",
                    key=f"submit_response_{consultation_id}"

                ):
                    if not agronomist_response.strip():

                        st.error(
                            "Please provide a professional response."
                        )
                    elif not management_advice.strip():
                        st.error(
                            "Please provide management advice."
                        )
                    else:

                        connection = sqlite3.connect(DATABASE)
                        cursor = connection.cursor()

                        cursor.execute(
                            """
                            UPDATE agronomist_consultations

                            SET
                                agronomist_response = ?,
                                management_advice = ?,
                                follow_up_required = ?,
                                status = 'Responded'

                            WHERE id = ?
                            """,
                            (
                                agronomist_response.strip(),
                                management_advice.strip(),
                                follow_up_required,
                                consultation_id
                            )
                        )

                        connection.commit()
                        connection.close()

                        st.success(
                            f"✅ Response submitted for "
                            f"Consultation #{consultation_id:04d}."
                        )

                        st.rerun()
                        

            elif status == "Responded":

                st.success(
                    "✅ This consultation has been responded to."
                )

            else:

                st.info(
                    "There are no farmer consultation requests yet."
                )