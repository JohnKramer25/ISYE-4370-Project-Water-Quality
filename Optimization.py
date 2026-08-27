import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.cluster import KMeans
import numpy as np
from scipy.optimize import differential_evolution

# Run RF Model first on combined data

# features (parameters)
features = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']

datasets = {
    "Combined Data": "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Combined_Log_Reg_Data.xlsx"
}

# Random Forest
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

    # Standardize the Data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_smote.values)
    X_test_scaled = scaler.transform(X_test.values)

    # Train the Model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train_smote)

    # Predict
    y_pred = rf_model.predict(X_test_scaled)

    importances = rf_model.feature_importances_

    # Importances into a new DataFrame
    importance_df = pd.DataFrame({
        'Feature': features,
        'Importance_Score': importances
    })

    # Sort from most important to least important
    importance_df = importance_df.sort_values(by='Importance_Score', ascending=False)
    print(importance_df)

    # Probaility that samples are potable
    y_pred_probs = rf_model.predict_proba(X_test_scaled)[:, 1]

    # Threshhold for classifaction of potabilty
    custom_threshold = 0.5

    # Generate new predictions
    y_pred_custom = (y_pred_probs >= custom_threshold).astype(int)

    # Print the new classification report
    print(f"--- Classification Report (Threshold = {custom_threshold}) ---")
    print(classification_report(y_test, y_pred_custom, target_names=['Non-Potable (0)', 'Potable (1)']))

    # Results
    accuracy = accuracy_score(y_test, y_pred_custom)
    print(f"Accuracy: {accuracy * 100:.2f}%\n")


# Now that rf model is made:
# Optimization

# Treatment Costs for 10,000 gallons of water

cost_dict = {
    'ph': 0.15,              # $0.15 to change pH by 1.0
    'Hardness': 0.1,         # $0.1 to change Hardness by 1.0
    'Solids': 0.1,           # $0.10 to remove 1 unit of Solids
    'Chloramines': 10.0,     # $10 to change Chloramines
    'Sulfate': 0.2,          # $0.20 to change Sulfate by one unit
    'Conductivity': 0.76,    # $0.76 to change Conductivity (through desalination) by one unit
    'Organic_carbon': 10.0,  # $10 to remove Organic_carbon by one unit
    'Trihalomethanes': 1.00, # $1 to remove Trihalomethanes
    'Turbidity': 1.7         # $1.70 to reduce Turbidity
}

cost_array = np.array([cost_dict[feat] for feat in features])

# Bounds
bounds = [
    (-6.0, 6.0),     # ph limits
    (-150.0, 150.0), # Hardness limits
    (-20000, 20000), # Solids 
    (-3.0, 3.0),     # Chloramines
    (-10.0, 10.0),   # Sulfate
    (-200, 200),     # Conductivity
    (-10.0, 0),      # Organic Carbon (removal onl)
    (-60.0, 0),      # Trihalomethanes (removal only)
    (-3.0, 0)        # Turbidity (removal only)
]

file_path = "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Combined_Log_Reg_Data.xlsx"
df = pd.read_excel(file_path)
failing_indices = df[df['Potability'] == 0].index
original_water = df.loc[failing_indices[0], features].values

# Objective Function

def cost_function(treatment_plan):
    financial_cost = np.sum(np.abs(treatment_plan) * cost_array)
    
    treated_water = current_water + treatment_plan
    
    treated_water_scaled = scaler.transform([treated_water])
    
    prob_potable = rf_model.predict_proba(treated_water_scaled)[0, 1]
    
    # If the treated water is less than 80% potable, penalty is added (to auto-reject plan)
    if prob_potable < 0.80:
        return financial_cost + 1000000 
    
    # If potable, return the cost
    return financial_cost

# RUN THE GROUP OPTIMIZER
# For 10 samples of non-potable water, find the cheapest one to treat

cost_list = []
plans_list = []
for i in range(10):
    current_water = df.loc[failing_indices[i], features].values

    # A "Treatment Array" gets made here, and is optimized to make the water sample seem potable to the RF model
    result = differential_evolution(
    cost_function, 
    bounds, 
    strategy='best1bin', 
    maxiter=1000, 
    tol=0.01, 
    seed=42
)

    cost_list.append(result.fun)
    plans_list.append(result.x)

# Print least expensive out of 10 water samples to treat
print("The cheapest out of 10 samples to treat and have a probability of potability be greater than or equal to 80% is :")
min_cost = np.min(cost_list)
print('\n', min_cost)

cheapest_index = np.argmin(cost_list)

if min_cost >= 1000000:
    print("Optimization Failed: None of the 10 samples could reach 80% potability.")
else:
    print(f"The cheapest sample to treat to >= 80% potability is Sample #{cheapest_index + 1}!")
    print(f"Total Treatment Cost: ${min_cost:.2f}")
    
    print("\nRequired Treatment for this Sample:")
    winning_plan = plans_list[cheapest_index]
    winning_water = df.loc[failing_indices[cheapest_index], features].values
    final_water = winning_water + winning_plan
    
    for i, feat in enumerate(features):
        change = winning_plan[i]
        if abs(change) > 0.01:
            print(f"  - Change {feat} by {change:+.2f} (New Value: {final_water[i]:.2f})")
