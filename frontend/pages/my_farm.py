import sqlite3
import streamlit as st


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

st.title("🌱 My Farm")

st.write(
    f"Welcome, {st.session_state.full_name}"
)

st.divider()


# --------------------------------
# ADD FARM
# --------------------------------

st.header("Add Your Farm")

farm_name = st.text_input(
    "Farm Name"
)

location = st.text_input(
    "Farm Location"
)

farm_size = st.number_input(
    "Farm Size",
    min_value=0.1,
    step=0.1
)

size_unit = st.selectbox(
    "Size Unit",
    ["Acres", "Hectares"]
)


if st.button("Save Farm"):

    if not farm_name or not location:

        st.error(
            "Please enter the farm name and location."
        )

    else:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO farms
            (
                user_id,
                farm_name,
                location,
                farm_size,
                size_unit
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                farm_name,
                location,
                farm_size,
                size_unit
            )
        )

        connection.commit()

        connection.close()

        st.success(
            "Farm saved successfully!"
        )


# --------------------------------
# DISPLAY FARMS
# --------------------------------

st.divider()

st.header("My Farms")


connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        id,
        farm_name,
        location,
        farm_size,
        size_unit
    FROM farms
    WHERE user_id = ?
    """,
    (user_id,)
)

farms = cursor.fetchall()

connection.close()


if farms:

    for farm in farms:

        st.subheader(
            f"🌱 {farm[1]}"
        )

        st.write(
            f"Location: {farm[2]}"
        )

        st.write(
            f"Size: {farm[3]} {farm[4]}"
        )

        if st.button(
            "Open Farm fields",
            key=f"fields_{farm[0]}"
        ):
            st.switch_page("pages/fields.py")

        st.divider()

else:

    st.info(
        "You haven't added a farm yet."
    )