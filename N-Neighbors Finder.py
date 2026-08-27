import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
import os

# Check RMSE for different # neigbhors in KNN and accuracy to identify optimal KNN n_neighbors (based on ph)

# Calculating optimal KNN n_neighbors for WP Potable data:

df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\KNN potable data.xlsx")

# remove missing data from KNN Potable
df_complete = df.dropna().reset_index(drop=True)
k_folds = 5

kf = KFold(n_splits=k_folds, shuffle=True, random_state=10)

k_neighbors_list = range(20, 60)
average_errors = []

for k_neighbors in k_neighbors_list:
    
    # keeps track of the RMSE for each k-fold (5 of them per loop)
    fold_errors = [] 
    
    # Loop through the 5 folds
    for train_idx, test_idx in kf.split(df_complete):
        
        # new copy of the complete data for the fold
        df_missing = df_complete.copy()
        
        # hide ph values for the rows in test fold
        df_missing.loc[test_idx, 'ph'] = np.nan
        
        # scale the data (0 to 1)
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df_missing)
        
        # Impute the data using current k_neighbors
        imputer = KNNImputer(n_neighbors=k_neighbors)
        df_imputed_scaled = imputer.fit_transform(df_scaled)
        
        # reverse the scaling
        df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_scaled), columns=df_complete.columns)
        
        # Check the error only on the hidden fold
        true_values = df_complete.loc[test_idx, 'ph']
        guessed_values = df_imputed.loc[test_idx, 'ph']
        
        rmse = np.sqrt(mean_squared_error(true_values, guessed_values))
        fold_errors.append(rmse)
        
    # average the 5 fold errors together
    average_errors.append(np.mean(fold_errors))

# 4. Plot the accurate Results
plt.figure(figsize=(10, 6))
plt.plot(k_neighbors_list, average_errors, marker='o', linestyle='dashed', color='purple')
plt.title(f'Optimal K-Neighbors for Potable Data')
plt.xlabel('Number of Neighbors (K)')
plt.ylabel('Average Error (RMSE)')
plt.xticks(k_neighbors_list)
plt.grid(True)
plt.show()
print(guessed_values)


# FINDING AVERAGE OPTIMAL n_neighbor VALUE

# Create storage for lowest RMSE knn values
best_knn_values = []

# Run 20 times to get average best n_neighbors value
for i in range(20):
    kf = KFold(n_splits=5, shuffle=True, random_state=i)

    #reset average_errors
    average_errors = []

    for k_neighbors in k_neighbors_list:
    
        fold_errors = [] 

        # Loop through the 5 folds
        for train_idx, test_idx in kf.split(df_complete):
            
            # new copy of the complete data for the fold
            df_missing = df_complete.copy()
            
            # hide ph values for the rows in test fold
            df_missing.loc[test_idx, 'ph'] = np.nan
            
            # scale the data (0 to 1)
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df_missing)
            
            # Impute the data using current k_neighbors
            imputer = KNNImputer(n_neighbors=k_neighbors)
            df_imputed_scaled = imputer.fit_transform(df_scaled)
            
            # reverse the scaling
            df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_scaled), columns=df_complete.columns)
            
            # Check the error only on the hidden fold
            true_values = df_complete.loc[test_idx, 'ph']
            guessed_values = df_imputed.loc[test_idx, 'ph']
            
            rmse = np.sqrt(mean_squared_error(true_values, guessed_values))
            fold_errors.append(rmse)
            
        # average the 5 fold errors together
        average_errors.append(np.mean(fold_errors))
    knn_best_index = np.argmin(average_errors)
    knn_best = k_neighbors_list[knn_best_index]
    best_knn_values.append(knn_best)
    final_average_knn = round(np.mean(best_knn_values))
print(f'The average n_neighbors that yielded the least RMSE for potable data was {final_average_knn}')


# ========================================
# DO SAME FOR NON POTABLE DATA
# ========================================
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\KNN non-potable data.xlsx")

# remove missing data
df_complete = df.dropna().reset_index(drop=True)
k_folds = 5

kf = KFold(n_splits=k_folds, shuffle=True, random_state=10)

k_neighbors_list = range(20, 60)
average_errors = []

for k_neighbors in k_neighbors_list:
    
    fold_errors = [] 
    
    # Loop through the 5 folds
    for train_idx, test_idx in kf.split(df_complete):
        
        # new copy of the complete data for the fold
        df_missing = df_complete.copy()
        
        # hide ph values for the rows in our test fold
        df_missing.loc[test_idx, 'ph'] = np.nan
        
        # scale the data (0 to 1)
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df_missing)
        
        # Impute the data using current k_neighbors
        imputer = KNNImputer(n_neighbors=k_neighbors)
        df_imputed_scaled = imputer.fit_transform(df_scaled)
        
        # reverse the scaling
        df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_scaled), columns=df_complete.columns)
        
        # Check the error only on the hidden fold
        true_values = df_complete.loc[test_idx, 'ph']
        guessed_values = df_imputed.loc[test_idx, 'ph']
        
        rmse = np.sqrt(mean_squared_error(true_values, guessed_values))
        fold_errors.append(rmse)
        
    # average the 5 fold errors together
    average_errors.append(np.mean(fold_errors))

# Plot the accurate Results
plt.figure(figsize=(10, 6))
plt.plot(k_neighbors_list, average_errors, marker='o', linestyle='dashed', color='purple')
plt.title(f'Optimal K-Neighbors for Non-Potable Data')
plt.xlabel('Number of Neighbors (K)')
plt.ylabel('Average Error (RMSE)')
plt.xticks(k_neighbors_list)
plt.grid(True)
plt.show()
print(guessed_values)


# remove missing values
df_complete = df.dropna().reset_index(drop=True)
df_missing = df_complete.copy()

k_neighbors_list = range(20, 60)
best_knn_values = []

# now run 20 times to get average best n_neighbors value
for i in range(20):
    kf = KFold(n_splits=5, shuffle=True, random_state=i)

    #reset average_errors
    average_errors = []

    for k_neighbors in k_neighbors_list:
    
        fold_errors = [] 

        # Loop through the 5 folds
        for train_idx, test_idx in kf.split(df_complete):
            
            # new copy of the complete data for the fold
            df_missing = df_complete.copy()
            
            # hide ph values for the rows in our test fold
            df_missing.loc[test_idx, 'ph'] = np.nan
            
            # scale the data (0 to 1)
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df_missing)
            
            # Impute the data using current k_neighbors
            imputer = KNNImputer(n_neighbors=k_neighbors)
            df_imputed_scaled = imputer.fit_transform(df_scaled)
            
            # reverse the scaling
            df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_scaled), columns=df_complete.columns)
            
            # Check the error only on the hidden fold
            true_values = df_complete.loc[test_idx, 'ph']
            guessed_values = df_imputed.loc[test_idx, 'ph']
            
            rmse = np.sqrt(mean_squared_error(true_values, guessed_values))
            fold_errors.append(rmse)
            
        # average the 5 fold errors together
        average_errors.append(np.mean(fold_errors))
    knn_best_index = np.argmin(average_errors)
    knn_best = k_neighbors_list[knn_best_index]
    best_knn_values.append(knn_best)
    final_average_knn = round(np.mean(best_knn_values))
print(f'The average n_neighbors that yielded the least RMSE for non potable data was {final_average_knn}')