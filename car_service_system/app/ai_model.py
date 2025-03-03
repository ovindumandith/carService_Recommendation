import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
def load_dataset():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "car_maintenance.csv")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    df = pd.read_csv(data_path, encoding="ISO-8859-1")

    # Drop rows with missing values in the 'maintenance_labels' column
    df = df.dropna(subset=['maintenance_labels'])

    # Check if the dataset is empty after dropping rows
    if df.empty:
        raise ValueError("Dataset is empty after removing rows with missing 'maintenance_labels'.")

    return df

# Preprocess dataset
def preprocess_data(df):
    # Encode categorical features
    label_encoders = {}
    categorical_cols = ['make', 'model', 'engine_type', 'driving_condition', 'maintenance_labels']
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Features and labels
    features = ['mileage', 'year', 'driving_condition']
    X = df[features]
    y = df['maintenance_labels']

    return X, y, label_encoders

# Train AI model
def train_model():
    df = load_dataset()
    X, y, label_encoders = preprocess_data(df)
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model, label_encoders

# Get service recommendation
def recommend_services(model, label_encoders, car_details):
    # Validate input data
    required_features = ['mileage', 'year', 'driving_condition']
    for feature in required_features:
        if feature not in car_details:
            raise ValueError(f"Missing required feature: {feature}")
        if pd.isna(car_details[feature]):
            raise ValueError(f"Invalid value for feature: {feature}")

    # Encode categorical features
    car_details_encoded = {}
    for key, value in car_details.items():
        if key in label_encoders:
            try:
                car_details_encoded[key] = label_encoders[key].transform([value])[0]
            except ValueError:
                # Handle unseen categories by assigning a default value
                car_details_encoded[key] = -1  # Use a value not seen during training
        else:
            car_details_encoded[key] = value

    # Define feature order and create a DataFrame
    features = ['mileage', 'year', 'driving_condition']
    input_data = pd.DataFrame([car_details_encoded], columns=features)

    # Predict maintenance label
    prediction = model.predict(input_data)
    maintenance_label = label_encoders['maintenance_labels'].inverse_transform(prediction)[0]
    
    return maintenance_label