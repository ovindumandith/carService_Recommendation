# Smart Car Service Booking System

## 🚗 Overview
The **Smart Car Service Booking System** is a web-based platform designed to help users book car maintenance services efficiently. The system leverages **AI-driven recommendations** to suggest optimal service types based on vehicle data, ensuring timely and personalized maintenance.

## 📌 Features
- **User Registration & Car Profile Management**
- **AI-Driven Service Recommendations** using a **Decision Tree Classifier**
- **Service Booking** with available time slots
- **Email Notifications & Updates**
- **Admin Dashboard** for appointment and customer data management
- **Rule-Based Chatbot** for answering car service-related queries

## 🏗 Tech Stack
- **Frontend:** Streamlit (Python-based UI Framework)
- **Backend:** Python
- **Database:** SQLite3
- **AI Model:** Decision Tree Classifier (with potential upgrades to Random Forest, Gradient Boosting, or Neural Networks)
- **Deployment:** Docker (Optional)

## 🛠 Installation & Setup
### 1️⃣ Clone the Repository
```sh
$ git clone https://github.com/your-username/smart-car-service-booking.git
$ cd smart-car-service-booking
```
### 2️⃣ Set Up a Virtual Environment (Optional but Recommended)
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3️⃣ Install Dependencies
```sh
$ pip install -r requirements.txt
```
### 4️⃣ Run the Application
```sh
$ streamlit run main.py
```

## 🔍 AI Integration
The **AI-driven recommendation system** predicts the best service package based on:
- **Mileage**
- **Year of Manufacture**
- **Engine Type** (Petrol, Diesel, Electric, Hybrid)
- **Driving Condition** (City, Highway, Mixed)
- **Last Maintenance Details**

When a user requests a recommendation, their vehicle data is processed through the **Decision Tree Classifier**, and the most suitable service is suggested.

## 💬 Chatbot Feature
The **rule-based chatbot** answers car service-related queries such as:
- "What services does my car need at 50,000 km?"
- "How often should I change my engine oil?"
- "What are the signs of brake failure?"

## 📈 Future Improvements
- **Enhancing AI Accuracy** using Gradient Boosting or Neural Networks
- **Hyperparameter Optimization** via Grid Search or Bayesian Optimization
- **Integrating Live User Feedback** for AI model updates
- **Deploying a Fully Functional Web App** using **Docker & Cloud Services**

## 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a Pull Request

## 📝 License
This project is licensed under the **MIT License**.

## 📧 Contact
For any queries, feel free to reach out:
- **Email:** ovindumandith@gmail.com
- **GitHub Issues:** Open a new issue on this repo

---
⭐ **If you like this project, consider giving it a star on GitHub!** ⭐
