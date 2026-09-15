import sqlite3
import hashlib
import streamlit as st


DATABASE = "database/telegronomy.db"


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def find_user(email, password, role):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id, full_name, email, role
        FROM users
        WHERE email = ?
        AND password = ?
        AND role = ?
        """,
        (email, password_hash, role)
    )

    user = cursor.fetchone()

    connection.close()

    return user


st.set_page_config(
    page_title="Telegronomy",
    page_icon="🌱",
    layout="centered"
)


st.title("🌱 Telegronomy")

st.subheader(
    "AI-Powered Agricultural Intelligence"
)

st.write(
    "Welcome to Telegronomy — your intelligent agricultural companion."
)

st.divider()


option = st.radio(
    "Choose an option",
    ["Login", "Create Account"]
)


# ==========================================
# LOGIN
# ==========================================

if option == "Login":

    st.header("Login")

    role = st.selectbox(
        "Select your role",
        ["Farmer", "Agronomist", "Admin"]
    )

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if not email or not password:

            st.error(
                "Please enter your email and password."
            )

        else:

            user = find_user(
                email,
                password,
                role
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.full_name = user[1]
                st.session_state.email = user[2]
                st.session_state.role = user[3]

                st.success(
                    f"Welcome, {user[1]}!"
                )

            else:

                st.error(
                    "Invalid email, password, or role."
                )


# ==========================================
# CREATE ACCOUNT
# ==========================================

if option == "Create Account":

    st.header(
        "Create Telegronomy Account"
    )

    full_name = st.text_input(
        "Full Name"
    )

    phone = st.text_input(
        "Phone Number"
    )

    email = st.text_input(
        "Email"
    )

    location = st.text_input(
        "Location"
    )

    role = st.selectbox(
        "Role",
        ["Farmer", "Agronomist"]
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )


    if st.button("Create Account"):

        if (
            not full_name
            or not phone
            or not email
            or not location
        ):

            st.error(
                "Please complete all required fields."
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        elif not password:

            st.error(
                "Please enter a password."
            )

        else:

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()

            password_hash = hash_password(
                password
            )

            try:

                cursor.execute(
                    """
                    INSERT INTO users
                    (
                        full_name,
                        phone,
                        email,
                        location,
                        role,
                        password
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        full_name,
                        phone,
                        email,
                        location,
                        role,
                        password_hash
                    )
                )

                connection.commit()

                # clear any existing login session
                for key in [
                    "logged_in",
                    "user_id",
                    "full_name",
                    "email",
                    "role"
                ]:
                    st.session_state.pop(key, None)

                st.success(
                    "Account created successfully"
                )

                st.info(
                    "Your account has been created. "
                    "Please select Login and sign in using your new account."
                )

            except sqlite3.IntegrityError:

                st.error(
                    "An account with this email already exists."
                )

            finally:

                connection.close()