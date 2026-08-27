import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Define features
features = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']

# Define datasets
datasets = {
    "WP Data": "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Log_Reg_Data.xlsx",
    "WQP Data": "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Log_Reg_Data.xlsx",
    "Combined Data": "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\Combined_Log_Reg_Data.xlsx"
}

# Loop through the dictionary to get name and path
for data_name, file_path in datasets.items():
    print(f"Random Forrest for: {data_name}")

    # Load Data
    df = pd.read_excel(file_path)

    # Define X and y
    X = df[features]
    y = df['Potability']

    # Initialize K-Means (4 custers) to aid model
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Apply SMOTE to training data - SMOTE adds synthetic data to balance out potable and non-potable data
    print("-> Balancing classes using SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    # Scale the Data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_smote)
    X_test_scaled = scaler.transform(X_test)

    # Fit K-Means on the training data
    train_clusters = kmeans.fit_predict(X_train_scaled)

    # Get the Cluster IDs for the test data
    test_clusters = kmeans.predict(X_test_scaled)

    # Adding Cluster IDs as a brand new feature/column to scaled data
    # Reshape the clusters to be a column, then add it to the end of X
    X_train_scaled_wclusters = np.hstack((X_train_scaled, train_clusters.reshape(-1, 1)))
    X_test_scaled_wclusters = np.hstack((X_test_scaled, test_clusters.reshape(-1, 1)))

    # Finding optimal parameters for rf_model

    param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5)
    }

    rf_base = RandomForestClassifier(n_estimators=100, random_state = 42)

    # Use random search to find the best hyperparameters
    rand_search = RandomizedSearchCV(
    rf_base, param_distributions=param_dist,
    n_iter=10, cv=5, scoring='accuracy',
    n_jobs=-1, random_state=42)

    rand_search.fit(X_train_scaled, y_train_smote)

    print('\nThe Best Parameters found are:')
    print(rand_search.best_params_)

    # Create best model:
    rf_model = rand_search.best_estimator_

    # Train the Model
    rf_model.fit(X_train_scaled_wclusters, y_train_smote)

    # Predict potabilities
    y_pred = rf_model.predict(X_test_scaled_wclusters)

    importances = rf_model.feature_importances_

    # Put importances into a new DataFrame
    features_wclusters = features + ['cluster_ID']
    importance_df = pd.DataFrame({
        'Feature': features_wclusters,
        'Importance_Score': importances
    })

    # Sort from most important to least important
    importance_df = importance_df.sort_values(by='Importance_Score', ascending=False)
    print(importance_df)

    y_pred_probs = rf_model.predict_proba(X_test_scaled_wclusters)[:, 1]

    # Set a new (lower) threshold
    custom_threshold = 0.5

    # Generate new predictions based on lower threshold
    y_pred_custom = (y_pred_probs >= custom_threshold).astype(int)

    # Print the new classification report
    print(f"--- Classification Report (Threshold = {custom_threshold}) ---")
    print(classification_report(y_test, y_pred_custom, target_names=['Non-Potable (0)', 'Potable (1)']))

    # Results
    accuracy = accuracy_score(y_test, y_pred_custom)
    print(f"Accuracy: {accuracy * 100:.2f}%\n")
