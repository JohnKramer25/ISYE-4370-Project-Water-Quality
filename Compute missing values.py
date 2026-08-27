import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer

df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\KNN potable data.xlsx")

# pipeline using optimized knn value (from N-Neighbors Finder.py)
impute_pipe = Pipeline(steps=[
    ('scaler', MinMaxScaler()),
    ('imputer', KNNImputer(n_neighbors=31)) # note: 31
])

# run pipeline
predicted_data_array = impute_pipe.fit_transform(df)

# rescale and put names back
df_new = pd.DataFrame(impute_pipe.named_steps['scaler'].inverse_transform(predicted_data_array), columns=df.columns)

print("Missing values left:", df_new.isna().sum().sum())
print(df_new)
output_file = "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\water_potability_potable_filled_data.xlsx"
df_new.to_excel(output_file, index = False)


# DO AGATIN FOR NON POTABLE DATA


df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\KNN non-potable data.xlsx")

# pipeline using this optimized knn value
impute_pipe = Pipeline(steps=[
    ('scaler', MinMaxScaler()),
    ('imputer', KNNImputer(n_neighbors=37)) # note: 37
])

# run pipeline
predicted_data_array = impute_pipe.fit_transform(df)

# rescale and put names back
df_new = pd.DataFrame(impute_pipe.named_steps['scaler'].inverse_transform(predicted_data_array), columns=df.columns)

print("Missing values left:", df_new.isna().sum().sum())
print(df_new)
output_file = "C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\water_potability_non_potable_filled_data.xlsx"
df_new.to_excel(output_file, index = False)