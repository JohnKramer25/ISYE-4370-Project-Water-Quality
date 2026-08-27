import pandas as pd
import os
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

# Spearman rank test for Potable and Non potable data in WP and WQP, and generate graphs to reveal correlation between categories and potability

# For WP Potable

# import csv
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_potable.xlsx")

# Run Spearman rank correlation (excel proved via correlations that data had no linear relationships)
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
correlations = []
correlation_statement=[]

print('For potable data in WP:')
for i in range(len(columns)):
    for j in range(len(columns)):
        if i<j:
            var1 = df.loc[:,columns[i]]
            var2 = df.loc[:,columns[j]]
            # Calculate the Spearman correlation
            spearman_corr = var1.corr(var2, method='spearman')
            
            correlations.append(spearman_corr)
            correlation_statement.append(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')
            print(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')

# make graphs to visualize possible correlations
sns.pairplot(df[columns], corner=True, plot_kws={'alpha': 0.3, 's': 10})
plt.show()

# SAME THING FOR NOT POTABLE DATA WP

# import csv
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_not_potable.xlsx")

# Run Spearman rank correlation (excel proved via correlations that data had no linear relationships)
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
correlations = []
correlation_statement=[]

print('For non-potable data in WP:')
for i in range(len(columns)):
    for j in range(len(columns)):
        if i<j:
            var1 = df.loc[:,columns[i]]
            var2 = df.loc[:,columns[j]]
            # Calculate the Spearman correlation
            spearman_corr = var1.corr(var2, method='spearman')
            
            correlations.append(spearman_corr)
            correlation_statement.append(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')
            print(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')

# make graphs to visualize possible correlations
sns.pairplot(df[columns], corner=True, plot_kws={'alpha': 0.3, 's': 10})
plt.show()

# SAME THING FOR POTABLE DATA in WQP

# import csv
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_potable.xlsx")

# Run Spearman rank correlation (excel proved via correlations that data had no linear relationships)
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
correlations = []
correlation_statement=[]

print('For potable data in WQP:')
for i in range(len(columns)):
    for j in range(len(columns)):
        if i<j:
            var1 = df.loc[:,columns[i]]
            var2 = df.loc[:,columns[j]]
            # Calculate the Spearman correlation
            spearman_corr = var1.corr(var2, method='spearman')
            
            correlations.append(spearman_corr)
            correlation_statement.append(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')
            print(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')

# make graphs to visualize possible correlations
sns.pairplot(df[columns], corner=True, plot_kws={'alpha': 0.3, 's': 10})
plt.show()

# SAME FOR NON POT IN WQP

# import csv
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_not_potable.xlsx")

# Run Spearman rank correlation (excel proved via correlations that data had no linear relationships)
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
correlations = []
correlation_statement=[]

print('For non-potable data in WQP:')
for i in range(len(columns)):
    for j in range(len(columns)):
        if i<j:
            var1 = df.loc[:,columns[i]]
            var2 = df.loc[:,columns[j]]
            # Calculate the Spearman correlation
            spearman_corr = var1.corr(var2, method='spearman')
            
            correlations.append(spearman_corr)
            correlation_statement.append(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')
            print(f'Correlation Coeff of {columns[i]} and {columns[j]} is {spearman_corr}')

# make graphs to visualize possible correlations
sns.pairplot(df[columns], corner=True, plot_kws={'alpha': 0.3, 's': 10})
plt.show()

# Generate combined wp pairplot to check potable vs non potable distributions and visible patterns
df_potable = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_potable.xlsx")
df_not_potable = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_not_potable.xlsx")

df_potable['Potability'] = 'Potable'
df_not_potable['Potability'] = 'Non-Potable'

df_combined = pd.concat([df_potable, df_not_potable], ignore_index=True)

columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity', 'Potability']

print("Generating combined WP pairplot...")
sns.pairplot(df_combined[columns], hue='Potability', corner=True, palette='Set1', plot_kws={'alpha': 0.3, 's': 10})
plt.show()


# Generate combined WP pairplot to check potable vs non potable distributions and visible patterns
df_potable = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_potable.xlsx")
df_not_potable = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_not_potable.xlsx")

df_potable['Potability'] = 'Potable'
df_not_potable['Potability'] = 'Non-Potable'

df_combined = pd.concat([df_potable, df_not_potable], ignore_index=True)

columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity', 'Potability']

# Plot the combined data, colored by Potability
print("Generating combined WQP pairplot...")
sns.pairplot(df_combined[columns], hue='Potability', corner=True, palette='Set1', plot_kws={'alpha': 0.3, 's': 10})
plt.show()