import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import numpy as np

# Train RF model:

# Define features
features = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
 # 'Chloramines', 'Sulfate' before conductivity, 'Trihalomethanes' before Turbidity
datasets = {
    "Combined Data": "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Combined_Log_Reg_Data.xlsx"
}

# Loop through the dictionary using .items() to get both the name and the path
for data_name, file_path in datasets.items():
    print(f"Random Forest for: {data_name}")

    # Load Data
    df = pd.read_excel(file_path)

    # Define X and y
    X = df[features]
    y = df['Potability']

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Apply SMOTE to training data - SMOTE adds synthetic data to balance out potable and non-potable data
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    # Scale the Data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_smote)
    X_test_scaled = scaler.transform(X_test)

    # Train the Model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train_smote)

    # Predict
    y_pred = rf_model.predict(X_test_scaled)

    importances = rf_model.feature_importances_

    # Put importances into a new DataFrame
    importance_df = pd.DataFrame({
        'Feature': features,
        'Importance_Score': importances
    })

    # Sort from most important to least important
    importance_df = importance_df.sort_values(by='Importance_Score', ascending=False)
    print(importance_df)

    y_pred_probs = rf_model.predict_proba(X_test_scaled)[:, 1]

    # Set a new (lower) threshold
    custom_threshold = 0.5

    # Generate new predictions based on the lower threshold
    y_pred_custom = (y_pred_probs >= custom_threshold).astype(int)

    # Print the new classification report
    print(f"--- Classification Report (Threshold = {custom_threshold}) ---")
    print(classification_report(y_test, y_pred_custom, target_names=['Non-Potable (0)', 'Potable (1)']))

    # Results
    accuracy = accuracy_score(y_test, y_pred_custom)
    print(f"Accuracy: {accuracy * 100:.2f}%\n")

# THIS IS THE NEW CODE FOR EXCEL AFTER TRAINING MODEL:

# Find values for excel simulation values
sim_x_val = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Excel Simulation Values for Model.xlsx")
x_val = sim_x_val[features]
print(sim_x_val)
scaled_x_val = scaler.fit_transform(x_val)
y_pred_excel = rf_model.predict(scaled_x_val)

# Add potability
x_y_val = np.hstack((sim_x_val, y_pred_excel.reshape(-1, 1)))
final_df = pd.DataFrame(x_y_val)

# Put into new excel file
final_df.to_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Excel Simulation Values for Model Output.xlsx",index=False)