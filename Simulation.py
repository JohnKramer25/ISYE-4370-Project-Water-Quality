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

# Train RF Model on combined data

# Define features
features = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
 # 'Chloramines', 'Sulfate' before conductivity, 'Trihalomethanes' before Turbidity
datasets = {
    "Combined Data": "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Combined_Log_Reg_Data.xlsx"
}

# Read data and create model
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

    # Predict potabilities
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

    # Set a new, lower threshold (e.g., 30% instead of the default 50%)
    custom_threshold = 0.5

    # Generate new predictions based on the lower threshold
    y_pred_custom = (y_pred_probs >= custom_threshold).astype(int)

    # Print new classification report
    print(f"--- Classification Report (Threshold = {custom_threshold}) ---")
    print(classification_report(y_test, y_pred_custom, target_names=['Non-Potable (0)', 'Potable (1)']))

    # Results
    accuracy = accuracy_score(y_test, y_pred_custom)
    print(f"Accuracy: {accuracy * 100:.2f}%\n")

# NOW SIMULATION

print("\n" + "="*60)
print("STARTING VIRTUAL WATER PLANT SIMULATION")
print("="*60)

# Water Sources

# Source A is the combined WP and WQP data
# Source B is only WQP
df_combined = pd.read_excel(datasets['Combined Data'])
df_wqp = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Log_Reg_Data.xlsx")
source_profiles = {
    "Source A (WP and WQP)": {
        'ph': (df_combined['ph'].mean(), df_combined['ph'].std()), 'Hardness': (df_combined['Hardness'].mean(), df_combined['Hardness'].std()), 'Solids': (df_combined['Solids'].mean(), df_combined['Solids'].std()),
        'Chloramines': (df_combined['Chloramines'].mean(), df_combined['Chloramines'].std()), 'Sulfate': (df_combined['Sulfate'].mean(), df_combined['Sulfate'].std()), 'Conductivity': (df_combined['Conductivity'].mean(), df_combined['Conductivity'].std()),
        'Organic_carbon': (df_combined['Organic_carbon'].mean(), df_combined['Organic_carbon'].std()), 'Trihalomethanes': (df_combined['Trihalomethanes'].mean(), df_combined['Trihalomethanes'].std()), 'Turbidity': (df_combined['Turbidity'].mean(), df_combined['Turbidity'].std())
    },
    "Source B (WQP)": {
        'ph': (df_wqp['ph'].mean(), df_wqp['ph'].std()), 'Hardness': (df_wqp['Hardness'].mean(), df_wqp['Hardness'].std()), 'Solids': (df_wqp['Solids'].mean(), df_wqp['Solids'].std()),
        'Chloramines': (df_wqp['Chloramines'].mean(), df_wqp['Chloramines'].std()), 'Sulfate': (df_wqp['Sulfate'].mean(), df_wqp['Sulfate'].std()), 'Conductivity': (df_wqp['Conductivity'].mean(), df_wqp['Conductivity'].std()),
        'Organic_carbon': (df_wqp['Organic_carbon'].mean(), df_wqp['Organic_carbon'].std()), 'Trihalomethanes': (df_wqp['Trihalomethanes'].mean(), df_wqp['Trihalomethanes'].std()), 'Turbidity': (df_wqp['Turbidity'].mean(), df_wqp['Turbidity'].std())
    },
}

# Simulation Parameters
# (Simulation of a water treatment plant)

days_to_simulate = 30           # Simulate 1 month
samples_per_day = 10            # Tests 10 batches of water per day
target_potability = 0.60        # The Random Forrest must be 60% confident to consider a sample potable

# Trackers for final report
total_water_tested = 0
total_failed_batches = 0
total_treatment_cost = 0.0
daily_costs = []

# Indicies of non-potable water
failing_indices = df[df['Potability'] == 0].index

print(f"Simulating {days_to_simulate} days of operation at {samples_per_day} batches/day...\n")

def cost_function(treatment_plan, simulated_water):
    financial_cost = np.sum(np.abs(treatment_plan) * cost_array)

    treated_water = simulated_water + treatment_plan
    
    treated_water_scaled = scaler.transform([treated_water])
    
    prob_potable = rf_model.predict_proba(treated_water_scaled)[0, 1]
    
    # If the treated water is still less than 60% potable, add penalty to reject this plan
    if prob_potable < target_potability:
        return financial_cost + 1000000 
    
    # Return the actual dollar cost
    return financial_cost

cost_dict = {
    'ph': 0.15,              # $0.15 to change pH by 1.0
    'Hardness': 0.1,         # $0.1 to change Hardness by 1.0
    'Solids': 0.1,           # $0.10 to remove 1 unit of Solids
    'Chloramines': 10.0,     # $10 to change Chloramines
    'Sulfate': 0.2,          # $0.20 to change Sulfate by one unit
    'Conductivity': 0.76,    # $0.76 to change Conductivity through desalination by one unit
    'Organic_carbon': 10.0,  # $10 to remove Organic_carbon by one unit
    'Trihalomethanes': 1.00, # $1 to remove Trihalomethanes
    'Turbidity': 1.7         # $1.70 to reduce Turbidity
}

cost_array = np.array([cost_dict[feat] for feat in features])

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

# Run Simulation (Loop)

for day in range(1, days_to_simulate + 1):
    day_cost = 0.0
    
    # Let's say the plant alternates sources each day
    source_name = "Source A (WP and WQP)" if day % 2 != 0 else "Source B (WQP)"
    profile = source_profiles[source_name]
    
    for batch in range(samples_per_day):
        total_water_tested += 1
        
        # Simulate random water sample
        # Draw a random number for each chemical based on the Source's mean and std
        simulated_water = [np.random.normal(loc=profile[feat][0], scale=profile[feat][1]) for feat in features]
        
        # Test with RF model
        scaled_water = scaler.transform([simulated_water])
        prob_potable = rf_model.predict_proba(scaled_water)[0, 1]
        
        # Treatment if fails potability test
        if prob_potable < target_potability:
            total_failed_batches += 1
            
            # Treat the water
            result = differential_evolution(
                cost_function, bounds, args=(simulated_water,), 
                strategy='best1bin', maxiter=50, tol=0.1 # Faster settings to save time in simulation
            )
            
            # Add the cost to the day_cost (not added if above 1000000)
            day_cost += min(result.fun, 1000000) 

    # Add data to trackers        
    daily_costs.append(day_cost)
    total_treatment_cost += day_cost
    
    # Print daily summary
    print(f"Day {day:02d} ({source_name}): ${day_cost:,.2f} spent on treatment.")


# Final Report

print("\n" + "="*60)
print("MONTHLY SIMULATION REPORT")
print("="*60)
print(f"Total Batches Tested:    {total_water_tested}")
print(f"Total Failed Batches:    {total_failed_batches} ({(total_failed_batches/total_water_tested)*100:.1f}% Failure Rate)")
print(f"Total Monthly Budget:    ${total_treatment_cost:,.2f}")
print(f"Average Cost Per Day:    ${(total_treatment_cost/days_to_simulate):,.2f}")