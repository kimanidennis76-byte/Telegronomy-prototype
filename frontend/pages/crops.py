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

st.title("🌱 My Crops")

st.write(
    f"Welcome, {st.session_state.full_name}"
)

st.divider()


# --------------------------------
# GET FARMER'S FIELDS
# --------------------------------

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        fields.id,
        fields.field_name,
        farms.farm_name
    FROM fields
    JOIN farms
        ON fields.farm_id = farms.id
    WHERE farms.user_id = ?
    """,
    (user_id,)
)

fields = cursor.fetchall()

connection.close()


if not fields:

    st.warning(
        "You need to create a field before adding a crop."
    )

    st.stop()


# --------------------------------
# SELECT FIELD
# --------------------------------

field_options = {
    f"{field[2]} → {field[1]}": field[0]
    for field in fields
}

selected_field = st.selectbox(
    "Select Field",
    list(field_options.keys())
)

field_id = field_options[selected_field]


# --------------------------------
# ADD CROP
# --------------------------------

st.header("Add Crop")


crop_name = st.selectbox(
    "Crop",
    [
        "Onion",
        "Maize",
        "Potato",
        "Beans",
        "Cabbage",
        "Tomato",
        "Kale",
        "Chilli Pepper",
        "Other"
    ]
)


if crop_name == "Other":

    crop_name = st.text_input(
        "Enter Crop Name"
    )


variety = st.text_input(
    "Variety"
)


planting_date = st.date_input(
    "Planting Date"
)


expected_harvest_date = st.date_input(
    "Expected Harvest Date"
)


growth_stage = st.selectbox(
    "Growth Stage",
    [
        "Seedling",
        "Vegetative",
        "Flowering",
        "Bulbing",
        "Fruit Development",
        "Maturity",
        "Harvest Ready"
    ]
)


if st.button("Save Crop"):

    if not crop_name:

        st.error(
            "Please select or enter a crop."
        )

    else:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO crops
            (
                field_id,
                crop_name,
                variety,
                planting_date,
                expected_harvest_date,
                growth_stage
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                field_id,
                crop_name,
                variety,
                str(planting_date),
                str(expected_harvest_date),
                growth_stage
            )
        )

        connection.commit()

        connection.close()

        st.success(
            "Crop saved successfully!"
        )


# --------------------------------
# DISPLAY CROPS
# --------------------------------

st.divider()

st.header("My Crops")


connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        crops.crop_name,
        crops.variety,
        crops.planting_date,
        crops.expected_harvest_date,
        crops.growth_stage,
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


if crops:

    for crop in crops:

        st.subheader(
            f"🌱 {crop[0]}"
        )

        st.write(
            f"Variety: {crop[1] or 'Not specified'}"
        )

        st.write(
            f"Farm: {crop[6]}"
        )

        st.write(
            f"Field: {crop[5]}"
        )

        st.write(
            f"Planting Date: {crop[2]}"
        )

        st.write(
            f"Expected Harvest: {crop[3]}"
        )

        st.write(
            f"Growth Stage: {crop[4]}"
        )

        st.divider()

else:

    st.info(
        "No crops have been added yet."
    )