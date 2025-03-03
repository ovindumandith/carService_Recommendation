import os
from datetime import date
import pandas as pd
import sqlite3
import streamlit as st
from datetime import datetime
from database import get_db_connection, init_db
from ai_model import train_model, recommend_services
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import plotly.express as px


# Initialize Database
init_db()

# Train AI Model
model, label_encoders = train_model()

# Correct the path to faq.json inside the app directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
FAQ_FILE = os.path.join(BASE_DIR, "faq.json")  # Ensure correct path

# Load FAQ data once using caching to improve performance
@st.cache_resource
def load_faq_data():
    """
    Loads predefined FAQ data from a JSON file.
    """
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"❌ Failed to load FAQ data: {e}")
        return []

# Function to find the best response using similarity search
def get_best_response(user_input, faq_data):
    """
    Finds the most similar question from the FAQ data and returns the answer.
    """
    if not faq_data:
        return "I'm sorry, I don't have any answers available at the moment."

    questions = [item["question"] for item in faq_data]

    # Compute TF-IDF similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(questions + [user_input])
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])  # Compare user input with predefined questions

    best_match_idx = similarities.argmax()  # Get index of best match
    best_match_score = similarities[0, best_match_idx]  # Get similarity score

    if best_match_score > 0.3:  # Set a threshold for relevant matches
        return faq_data[best_match_idx]["answer"]
    else:
        return "I'm sorry, I don't understand that question. Please try asking something else."

# Chatbot UI
def chatbot_interface():
    st.title("🚗 Car Service Chatbot")
    st.write("Ask me anything about car services or mechanics!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Load FAQ data
    faq_data = load_faq_data()

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Get user input
    user_input = st.chat_input("Ask a question...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        chatbot_response = get_best_response(user_input, faq_data)
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})

        # Display latest messages
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            st.write(chatbot_response)

# Streamlit App
st.set_page_config(page_title="AutoMate", page_icon="🚗", layout="wide")

# Custom CSS for UI/UX improvements
# Custom CSS for UI/UX improvements
# Custom CSS for UI/UX improvements
st.markdown("""
    <style>
    /* Import Roboto font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    /* General Styling */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #F0F4F8;  /* Light blue-gray background */
        color: #333333;  /* Dark gray text */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #4CAF50;  /* Calm green for headings */
        font-weight: 700;  /* Bold headings */
    }
    .stButton button {
        background-color: #4CAF50;  /* Calm green for buttons */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45A049;  /* Darker green for button hover */
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stDateInput {
        margin-bottom: 20px;
    }

     .stCard {
        background-color: #F0F4F8;  /* Light blue-gray background */
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #4CAF50;  /* Green left border */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stCard:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .stCard h4 {
        color: #1B3A5C;  /* Dark blue for headings */
        margin-bottom: 16px;
    }
    .stCard p {
        font-size: 1rem;
        color: #333333;  /* Dark gray text */
        line-height: 1.6;
    }
    .stCard button {
        background-color: #4CAF50;  /* Calm green for buttons */
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stCard button:hover {
        background-color: #45A049;  /* Darker green for button hover */
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.title("AutoMate 🚗")
menu = st.sidebar.selectbox("Menu", ["Home", "Register", "Login", "Add Car", "Service Recommendations", "Book Service", "User Profile", "Admin Dashboard", "Chatbot"])

# Global session variables
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Logout Button in Sidebar
if st.session_state.user_id or st.session_state.is_admin:
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.session_state.is_admin = False
        st.success("✅ Logged out successfully!")
        st.rerun()  # Refresh the page to reflect the logout


import os
import base64
import streamlit as st

# Function to find and load the video
def load_video(video_name):
    # Get the base directory of the script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the video
    video_path = os.path.join(base_dir, "videos", video_name)
    
    # Check if the video exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found at {video_path}")
    
    return video_path

# Home Page
if menu == "Home":
    try:
        # Load the video dynamically
        video_path = load_video("hero.mp4")
        
        # Header Section with Background Gradient
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1B3A5C 0%, #48CAE4 100%); padding: 40px 20px; border-radius: 12px; margin-bottom: 30px;">
            <h1 style="color: white; margin: 0; font-size: 3rem; text-align: center;">Welcome to AutoMate 🚗</h1>
            <p style="color: white; font-size: 1.2rem; text-align: center; margin-top: 10px;">
                Your smart car service and recommendation system powered by AI
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Main content in two columns
        left_col, right_col = st.columns([2, 1])

        with left_col:
            # Display the video with looping functionality
            video_file = open(video_path, 'rb')
            video_bytes = video_file.read()
            video_file.close()

            # Use HTML video tag with autoplay and loop attributes
            st.markdown(
                f"""
                <video autoplay loop muted controls style="width: 100%;">
                    <source src="data:video/mp4;base64,{base64.b64encode(video_bytes).decode()}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                """, 
                unsafe_allow_html=True
            )

            # Feature Cards in a grid
            st.markdown("<h2 style='color: #1B3A5C; margin-top: 30px;'>What We Offer</h2>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <div class="stCard" style="border-left: 4px solid #48CAE4;">
                    <h4 style="color: #1B3A5C; display: flex; align-items: center;">
                        <span style="background-color: #CAF0F8; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">🔍</span>
                        Smart Recommendations
                    </h4>
                    <p>AI-powered service suggestions based on your vehicle's make, model, and usage patterns.</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="stCard" style="border-left: 4px solid #00B4D8;">
                    <h4 style="color: #1B3A5C; display: flex; align-items: center;">
                        <span style="background-color: #CAF0F8; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">📅</span>
                        Easy Booking
                    </h4>
                    <p>Schedule services with just a few clicks and get instant confirmation.</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="stCard" style="border-left: 4px solid #0077B6;">
                    <h4 style="color: #1B3A5C; display: flex; align-items: center;">
                        <span style="background-color: #CAF0F8; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">🔔</span>
                        Timely Reminders
                    </h4>
                    <p>Never miss an important service with our smart notification system.</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="stCard" style="border-left: 4px solid #023E8A;">
                    <h4 style="color: #1B3A5C; display: flex; align-items: center;">
                        <span style="background-color: #CAF0F8; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">💬</span>
                        Expert Support
                    </h4>
                    <p>Get answers to all your car maintenance questions with our intelligent chatbot.</p>
                </div>
                """, unsafe_allow_html=True)

        with right_col:
            # Call to action card
            st.markdown("""
            <div class="stCard" style="border-left: 4px solid #48CAE4; background-color: #F8FCFF;">
                <h3 style="color: #1B3A5C; text-align: center;">Ready to Get Started?</h3>
                <p style="text-align: center;">Join thousands of car owners who trust AutoMate for their vehicle maintenance needs.</p>
                <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
                    <a href="#register" style="text-decoration: none;">
                        <button style="background-color: #48CAE4; color: white; width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: 500; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            Create an Account
                        </button>
                    </a>
                    <a href="#login" style="text-decoration: none;">
                        <button style="background-color: transparent; color: #48CAE4; width: 100%; padding: 12px; border: 2px solid #48CAE4; border-radius: 8px; font-size: 16px; font-weight: 500; cursor: pointer; transition: all 0.3s ease;">
                            Login
                        </button>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Quick Stats Card
            st.markdown("""
            <div class="stCard" style="margin-top: 20px; border-left: 4px solid #1B3A5C; background-color: #F5F7FA;">
                <h4 style="color: #1B3A5C; text-align: center;">Why AutoMate?</h4>
                <div style="display: flex; justify-content: space-between; text-align: center; margin-top: 15px;">
                    <div>
                        <h2 style="color: #48CAE4; margin: 0; font-size: 2rem;">5k+</h2>
                        <p style="margin: 0; color: #3A506B;">Happy Users</p>
                    </div>
                    <div>
                        <h2 style="color: #48CAE4; margin: 0; font-size: 2rem;">98%</h2>
                        <p style="margin: 0; color: #3A506B;">Satisfaction</p>
                    </div>
                    <div>
                        <h2 style="color: #48CAE4; margin: 0; font-size: 2rem;">24/7</h2>
                        <p style="margin: 0; color: #3A506B;">Support</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Chatbot Preview
            st.markdown("""
            <div class="stCard" style="margin-top: 20px; border-left: 4px solid #023E8A; background-color: #F5F7FA;">
                <h4 style="color: #1B3A5C;">Quick Question?</h4>
                <p>Try our chatbot for instant answers about car maintenance.</p>
                <a href="#chatbot" style="text-decoration: none;">
                    <button style="background-color: #023E8A; color: white; width: 100%; padding: 10px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer;">
                        Chat Now
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

        # Testimonials Section
        st.markdown("<h2 style='color: #1B3A5C; margin-top: 40px; text-align: center;'>What Our Customers Say</h2>", unsafe_allow_html=True)

        testimonial_cols = st.columns(3)

        testimonials = [
            {"name": "John D.", "rating": "⭐⭐⭐⭐⭐", "text": "AutoMate has simplified my car maintenance routine. The AI recommendations are spot on!"},
            {"name": "Sarah M.", "rating": "⭐⭐⭐⭐⭐", "text": "I love how easy it is to book services and get reminders. Never missed an oil change since."},
            {"name": "Mike T.", "rating": "⭐⭐⭐⭐", "text": "The chatbot answered all my questions about my car issues. Saved me an unnecessary trip to the mechanic."}
        ]

        for i, col in enumerate(testimonial_cols):
            with col:
                st.markdown(f"""
                <div class="stCard" style="height: 220px; border-left: 4px solid #48CAE4; background-color: #F8FCFF;">
                    <div style="margin-bottom: 10px; color: #FFD700;">{testimonials[i]['rating']}</div>
                    <p style="font-style: italic;">"{testimonials[i]['text']}"</p>
                    <p style="text-align: right; font-weight: 500; margin-top: 15px; color: #1B3A5C;">- {testimonials[i]['name']}</p>
                </div>
                """, unsafe_allow_html=True)

        # How It Works Section
        st.markdown("<h2 style='color: #1B3A5C; margin-top: 40px; text-align: center;'>How It Works</h2>", unsafe_allow_html=True)

        steps_cols = st.columns(4)

        steps = [
            {"icon": "👤", "title": "Create Account", "desc": "Sign up and add your vehicle details"},
            {"icon": "🚗", "title": "Add Your Car", "desc": "Enter your car's make, model, and details"},
            {"icon": "🔍", "title": "Get Recommendations", "desc": "Receive AI-powered service suggestions"},
            {"icon": "📅", "title": "Book Services", "desc": "Schedule maintenance with just a few clicks"}
        ]

        for i, col in enumerate(steps_cols):
            with col:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px 10px;">
                    <div style="background-color: #CAF0F8; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto; font-size: 24px;">
                        {steps[i]['icon']}
                    </div>
                    <h4 style="color: #1B3A5C; margin-top: 15px;">{steps[i]['title']}</h4>
                    <p style="font-size: 0.9rem;">{steps[i]['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

        # Bottom CTA
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1B3A5C 0%, #48CAE4 100%); padding: 30px; border-radius: 12px; margin-top: 40px; text-align: center;">
            <h2 style="color: white; margin: 0;">Ready to Experience Smart Car Care?</h2>
            <p style="color: white; margin: 10px 0 20px;">Join AutoMate today and keep your vehicle in perfect condition.</p>
            <a href="#register" style="text-decoration: none;">
                <button style="background-color: white; color: #1B3A5C; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                    Get Started Now
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError as e:
        st.error(str(e))

# Register User
if menu == "Register":
    st.subheader("🔑 Register")
    with st.form("register_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email")
        phone = st.text_input("Phone", placeholder="Enter your phone number")
        password = st.text_input("Password", type="password", placeholder="Enter a password")
        submit_button = st.form_submit_button("Register")

        if submit_button:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)', 
                             (name, email, phone, password))
                conn.commit()
                st.success("✅ Registration successful!")
            except sqlite3.IntegrityError:
                st.error("❌ Email already registered!")
            except Exception as e:
                st.error(f"❌ Registration failed: {str(e)}")
            finally:
                conn.close()        

# Login User
elif menu == "Login":
    st.subheader("🔐 Login")
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        admin_key = st.text_input("Admin Key (optional)", type="password", placeholder="Enter admin key")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
            admin = conn.execute('SELECT * FROM admins WHERE email = ? AND password = ? AND admin_key = ?', 
                                 (email, password, admin_key)).fetchone()
            conn.close()

            if user:
                st.session_state.user_id = user["id"]
                st.session_state.is_admin = False
                st.success("✅ Login successful!")
            elif admin:
                st.session_state.is_admin = True
                st.success("✅ Admin login successful!")
            else:
                st.error("❌ Invalid credentials!")

# Add Car
elif menu == "Add Car":
    if st.session_state.user_id is None:
        st.error("❌ Please log in first!")
    else:
        st.subheader("🚘 Add Car")
        with st.form("add_car_form"):
            make = st.text_input("Make", placeholder="Enter car make")
            model_name = st.text_input("Model", placeholder="Enter car model")
            year = st.number_input("Year", min_value=1900, max_value=datetime.now().year)
            mileage = st.number_input("Mileage", min_value=0)
            engine_type = st.selectbox("Engine Type", ["Gasoline", "Diesel", "Hybrid", "Electric"])
            driving_condition = st.selectbox("Driving Habits", ["Fair", "Good", "Excellent"])
            submit_button = st.form_submit_button("Add Car")

            if submit_button:
                conn = get_db_connection()
                conn.execute('''
                    INSERT INTO cars (user_id, make, model, year, mileage, engine_type, driving_condition)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (st.session_state.user_id, make, model_name, year, mileage, engine_type, driving_condition))
                conn.commit()
                conn.close()
                st.success("🚀 Car added successfully!")

# AI-Driven Service Recommendations
elif menu == "Service Recommendations":
    if st.session_state.user_id is None:
        st.error("❌ Please log in first!")
    else:
        st.subheader("🔍 AI-Driven Service Recommendations")
        conn = get_db_connection()
        cars = conn.execute('SELECT * FROM cars WHERE user_id = ?', (st.session_state.user_id,)).fetchall()
        conn.close()
        
        # Create a dictionary of car options for the dropdown
        car_options = {f"{car['make']} {car['model']} ({car['year']})": car for car in cars}
        selected_car = st.selectbox("Select Your Car", list(car_options.keys()))

        if st.button("Get Recommendations"):
            # Show a loading spinner while processing
            with st.spinner("🤖 Generating recommendations..."):
                try:
                    # Get details of the selected car
                    car_details = car_options[selected_car]

                    # Prepare car data for the AI model
                    car_data = {
                        'mileage': car_details['mileage'],
                        'year': car_details['year'],
                        'driving_condition': car_details['driving_condition']  # Ensure this matches the model's features
                    }

                    # Get the recommendation from the AI model
                    recommendation = recommend_services(model, label_encoders, car_data)

                    # Display the recommendation
                    st.toast("✅ Recommendation generated successfully!", icon="🎉")
                    st.write(f"📌 Recommended Service: **{recommendation}**")

                    # Display car details used for the recommendation
                    st.write("### Car Details Used:")
                    st.write(f"- **Make**: {car_details['make']}")
                    st.write(f"- **Model**: {car_details['model']}")
                    st.write(f"- **Year**: {car_details['year']}")
                    st.write(f"- **Mileage**: {car_details['mileage']} miles")
                    st.write(f"- **Engine Type**: {car_details['engine_type']}")
                    st.write(f"- **Driving Condition**: {car_details['driving_condition']}")

                    # Display maintenance history (if available)
                    if 'last_maintenance_date' in car_details and 'last_maintenance_type' in car_details:
                        st.write("### Maintenance History:")
                        st.write(f"- **Last Maintenance Date**: {car_details['last_maintenance_date']}")
                        st.write(f"- **Last Maintenance Type**: {car_details['last_maintenance_type']}")

                except Exception as e:
                    st.error(f"❌ Failed to generate recommendations: {e}")

# Book a Service
elif menu == "Book Service":
    if st.session_state.user_id is None:
        st.error("❌ Please log in first!")
    else:
        st.subheader("📅 Book a Service")
        conn = get_db_connection()
        cars = conn.execute('SELECT * FROM cars WHERE user_id = ?', (st.session_state.user_id,)).fetchall()
        conn.close()

        car_options = {f"{car['make']} {car['model']} ({car['year']})": car for car in cars}
        selected_car = st.selectbox("Select Your Car", list(car_options.keys()))
        service_type = st.selectbox("Service Type", ["Oil Change", "Tire Rotation", "Battery Check", "Brake Inspection"])
        booking_date = st.date_input("Booking Date")
        time_slot = st.selectbox("Time Slot", ["Morning", "Afternoon", "Evening"])

        if st.button("Book Service"):
            if booking_date < date.today():
                st.error("❌ Booking date cannot be in the past!")
            else:
                car_details = car_options[selected_car]
                conn = get_db_connection()
                conn.execute('''
                    INSERT INTO bookings (user_id, car_id, service_type, appointment_date, time_slot, status)
                    VALUES (?, ?, ?, ?, ?, 'Pending')
                ''', (st.session_state.user_id, car_details["id"], service_type, booking_date.strftime("%Y-%m-%d"), time_slot))
                conn.commit()
                conn.close()
                st.toast("✅ Your booking has been implemented successfully!", icon="🎉")

# User Profile
elif menu == "User Profile":
    if st.session_state.user_id is None:
        st.error("❌ Please log in first!")
    else:
        st.subheader("👤 User Profile")
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (st.session_state.user_id,)).fetchone()
        cars = conn.execute('SELECT * FROM cars WHERE user_id = ?', (st.session_state.user_id,)).fetchall()
        bookings = conn.execute('SELECT * FROM bookings WHERE user_id = ?', (st.session_state.user_id,)).fetchall()
        conn.close()

        st.write(f"### Welcome, {user['name']}!")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Phone:** {user['phone']}")

        # Update User Details Form
        st.write("### Update Your Profile")
        with st.form("update_profile_form"):
            new_name = st.text_input("Full Name", value=user['name'], placeholder="Enter your full name")
            new_email = st.text_input("Email", value=user['email'], placeholder="Enter your email")
            new_phone = st.text_input("Phone", value=user['phone'], placeholder="Enter your phone number")
            update_button = st.form_submit_button("Update Profile")

            if update_button:
                if not new_name or not new_email or not new_phone:
                    st.error("❌ Please fill in all fields!")
                else:
                    conn = get_db_connection()
                    try:
                        conn.execute('''
                            UPDATE users
                            SET name = ?, email = ?, phone = ?
                            WHERE id = ?
                        ''', (new_name, new_email, new_phone, st.session_state.user_id))
                        conn.commit()
                        st.success("✅ Profile updated successfully!")
                    except sqlite3.IntegrityError:
                        st.error("❌ Email already registered!")
                    except Exception as e:
                        st.error(f"❌ Failed to update profile: {str(e)}")
                    finally:
                        conn.close()

        st.write("### Your Cars 🚗")
        if cars:
            for car in cars:
                with st.container():
                    st.markdown(f"""
                    <div class="stCard">
                        <h4 style="color: #4CAF50;">{car['make']} {car['model']} ({car['year']})</h4>
                        <p><b>Mileage:</b> {car['mileage']} miles</p>
                        <p><b>Engine Type:</b> {car['engine_type']}</p>
                        <p><b>Driving Condition:</b> {car['driving_condition']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No cars added yet.")

        st.write("### Your Bookings 📅")
        if bookings:
            for booking in bookings:
                with st.container():
                    st.markdown(f"""
                    <div class="stCard">
                        <h4 style="color: #4CAF50;">Booking ID: {booking['id']}</h4>
                        <p><b>Service:</b> {booking['service_type']}</p>
                        <p><b>Date:</b> {booking['appointment_date']}</p>
                        <p><b>Time Slot:</b> {booking['time_slot']}</p>
                        <p><b>Status:</b> {booking['status']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No bookings found.")

# Admin Dashboard
elif menu == "Admin Dashboard":
    if not st.session_state.is_admin:
        st.error("❌ Admin access required!")
    else:
        # Stylish Welcome Header with Dark Theme
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1B3A5C 0%, #48CAE4 100%); padding: 20px; border-radius: 12px; text-align: center;">
            <h1 style="color: white; margin: 0;">Welcome, Admin! 👋</h1>
            <p style="color: white; font-size: 1.1rem;">Manage bookings, approve services, and oversee system analytics.</p>
        </div>
        """, unsafe_allow_html=True)

        conn = get_db_connection()
        bookings = conn.execute('SELECT * FROM bookings').fetchall()
        conn.close()

        # Convert bookings to DataFrame
        bookings_df = pd.DataFrame(bookings, columns=["ID", "User ID", "Car ID", "Service Type", "Appointment Date", "Time Slot", "Status"])

        # Booking Status Pie Chart
        status_counts = bookings_df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_status = px.pie(status_counts, names="Status", values="Count", title="Booking Status Distribution", 
                            color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark")

        # Service Type Bar Chart
        service_counts = bookings_df["Service Type"].value_counts().reset_index()
        service_counts.columns = ["Service Type", "Count"]
        fig_services = px.bar(service_counts, x="Service Type", y="Count", title="Most Requested Services", 
                              color="Count", color_continuous_scale="viridis", template="plotly_dark")

        # Display charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_status, use_container_width=True)
        with col2:
            st.plotly_chart(fig_services, use_container_width=True)

        # Dark Table Styling
        st.markdown("""
        <style>
            .dark-table {
                background-color: #1B3A5C;
                color: #ffffff;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #48CAE4;
                text-align: center;
            }
            .dark-table th {
                background-color: #2C3E50;
                padding: 8px;
            }
            .dark-table td {
                padding: 8px;
                border-bottom: 1px solid #48CAE4;
            }
            .dark-table tr:nth-child(even) {
                background-color: #34495E;
            }
        </style>
        """, unsafe_allow_html=True)

        # Convert table to HTML with custom styling
        table_html = bookings_df.to_html(classes="dark-table", index=False, escape=False)
        st.markdown("### 📋 All Bookings Overview", unsafe_allow_html=True)
        st.markdown(table_html, unsafe_allow_html=True)

        # Display bookings in a card layout with Dark Mode
        st.markdown("## 📌 Recent Bookings")
        for booking in bookings:
            st.markdown(f"""
            <div style="background-color: #2C3E50; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 6px solid #48CAE4;">
                <h4 style="color: #48CAE4;">📍 Booking ID: {booking['ID']}</h4>
                <p style="color: #ffffff;"><b>👤 User ID:</b> {booking['user_iD']}</p>
                <p style="color: #ffffff;"><b>🚗 Service:</b> {booking['service_type']}</p>
                <p style="color: #ffffff;"><b>📅 Date:</b> {booking['appointment_date']}</p>
                <p style="color: #ffffff;"><b>⏰ Time Slot:</b> {booking['time_slot']}</p>
                <p><b>📌 Status:</b> <span style="color: {'#f39c12' if booking['status'] == 'Pending' else '#27ae60'};">{booking['status']}</span></p>
                <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 14px; cursor: pointer;">
                    ✅ Approve {booking['ID']}
                </button>
            </div>
            """, unsafe_allow_html=True)

        # Booking approval logic
        for booking in bookings:
            if st.button(f"✅ Approve {booking['ID']}"):
                conn = get_db_connection()
                conn.execute("UPDATE bookings SET Status = 'Approved' WHERE ID = ?", (booking['ID'],))
                conn.commit()
                conn.close()
                st.success(f"✅ Booking {booking['ID']} approved!")
                st.rerun()  # Refresh page
# Chatbot Section
elif menu == "Chatbot":
    chatbot_interface()