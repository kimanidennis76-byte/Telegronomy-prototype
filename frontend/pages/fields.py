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

st.title("🌱 Farm Fields")

st.write(
    f"Welcome, {st.session_state.full_name}"
)

st.divider()


# --------------------------------
# GET FARMER'S FARMS
# --------------------------------

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT id, farm_name
    FROM farms
    WHERE user_id = ?
    """,
    (user_id,)
)

farms = cursor.fetchall()

connection.close()


if not farms:

    st.warning(
        "You need to create a farm before adding fields."
    )

    st.stop()


# --------------------------------
# SELECT FARM
# --------------------------------

farm_options = {
    farm[1]: farm[0]
    for farm in farms
}

selected_farm = st.selectbox(
    "Select Farm",
    list(farm_options.keys())
)

farm_id = farm_options[selected_farm]


# --------------------------------
# ADD FIELD
# --------------------------------

st.header("Add Field")

field_name = st.text_input(
    "Field Name"
)

field_size = st.number_input(
    "Field Size",
    min_value=0.1,
    step=0.1
)

size_unit = st.selectbox(
    "Size Unit",
    ["Acres", "Hectares"]
)


if st.button("Save Field"):

    if not field_name:

        st.error(
            "Please enter a field name."
        )

    else:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO fields
            (
                farm_id,
                field_name,
                field_size,
                size_unit
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                farm_id,
                field_name,
                field_size,
                size_unit
            )
        )

        connection.commit()

        connection.close()

        st.success(
            "Field saved successfully!"
        )


# --------------------------------
# DISPLAY FIELDS
# --------------------------------

st.divider()

st.header(
    f"Fields in {selected_farm}"
)


connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        id,
        field_name,
        field_size,
        size_unit
    FROM fields
    WHERE farm_id = ?
    """,
    (farm_id,)
)

fields = cursor.fetchall()

connection.close()


if fields:

    for field in fields:

        st.subheader(
            f"🌱 {field[1]}"
        )

        st.write(
            f"Size: {field[2]} {field[3]}"
        )

        if st.button(
            "Open Field Crops",
            key=f"crops_{field[0]}"
        ):
            st.switch_page("pages/crops.py")

        st.divider()

else:

    st.info(
        "No fields have been added yet."
    )