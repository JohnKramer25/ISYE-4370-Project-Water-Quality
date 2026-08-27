import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# see if classifications based on EPA guidlines affect potability
np.random.seed(42)

wp_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_data.xlsx")
wqp_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_data.xlsx")

# define bins and lables
bin_edges = [0, 6.5, 8.5, 14] 
bin_labels = ['Acidic', 'Neutral', 'Basic']

# bin ph data into categories
wp_df['ph'] = pd.cut(wp_df['ph'], bins=bin_edges, labels=bin_labels, include_lowest=True)
wqp_df['ph'] = pd.cut(wqp_df['ph'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# count the frequencies of Potable and Non-Potable for each ph label
wp_contingency_table = pd.crosstab(wp_df['ph'], wp_df['Potability'])
wqp_contingency_table = pd.crosstab(wqp_df['ph'], wqp_df['Potability'])
print("for WP:")
print(wp_contingency_table)
print("\n")
print("for WQP")
print(wqp_contingency_table)
print("\n")

# run the Chi-Square Test of Independence
wp_chi2_stat, wp_p_value, wp_dof, wp_expected_freq = chi2_contingency(wp_contingency_table)
wqp_chi2_stat, wqp_p_value, wqp_dof, wqp_expected_freq = chi2_contingency(wqp_contingency_table)

print("Chi-squared tests for independence of categories of acidic, neutral, and basic, on potability of water:")
print("wp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wp_chi2_stat:.4f}")
print(f"P-value: {wp_p_value:.4e}")
print(f"Degrees of Freedom: {wp_dof}")
print("\n")
print("Chi-squared tests for independence of categories of acidic, neutral, and basic, on potability of water:")
print("wqp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wqp_chi2_stat:.4f}")
print(f"P-value: {wqp_p_value:.4e}")
print(f"Degrees of Freedom: {wqp_dof}")


# check to see if valid
print("expected wp frequencies")
print(wp_expected_freq)
print("\nexpected wqp frequencies")
print(wqp_expected_freq)


import matplotlib.pyplot as plt

# visualization for correlation between category and potability for wp
wp_row_percentages = pd.crosstab(wp_df['ph'], wp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by ph for wp', fontsize=14)
plt.xlabel('EPA ph Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# visualization for correlation between category and potability for wqp
wqp_row_percentages = pd.crosstab(wqp_df['ph'], wqp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wqp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by ph for wqp', fontsize=14)
plt.xlabel('EPA ph Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()






# NOW SAME THING FOR ORGANIC CARBON



# define bins and lables
bin_edges = [0, 10, max(max(wp_df['Organic_carbon']),max(wqp_df['Organic_carbon']))] 
bin_labels = ['Acceptable', 'Unacceptable']

# bin Organic_carbon data into categories
wp_df['Organic_carbon'] = pd.cut(wp_df['Organic_carbon'], bins=bin_edges, labels=bin_labels, include_lowest=True)
wqp_df['Organic_carbon'] = pd.cut(wqp_df['Organic_carbon'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# count the frequencies of Potable and Non-Potable for each ph label
wp_contingency_table = pd.crosstab(wp_df['Organic_carbon'], wp_df['Potability'])
wqp_contingency_table = pd.crosstab(wqp_df['Organic_carbon'], wqp_df['Potability'])

print("\n\nOrganic_carbon:\n")
print("for WP:")
print(wp_contingency_table)
print("\n")
print("for WQP")
print(wqp_contingency_table)
print("\n")

# run the Chi-Square Test of Independence
wp_chi2_stat, wp_p_value, wp_dof, wp_expected_freq = chi2_contingency(wp_contingency_table)
wqp_chi2_stat, wqp_p_value, wqp_dof, wqp_expected_freq = chi2_contingency(wqp_contingency_table)

print("Chi-squared tests for independence of categories of Acceptable and Unacceptable levels of Organic_Carbon in water:")
print("wp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wp_chi2_stat:.4f}")
print(f"P-value: {wp_p_value:.4e}")
print(f"Degrees of Freedom: {wp_dof}")
print("\n")
print("Chi-squared tests for independence of categories of Acceptable and Unacceptable levels of Organic_Carbon in water:")
print("wqp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wqp_chi2_stat:.4f}")
print(f"P-value: {wqp_p_value:.4e}")
print(f"Degrees of Freedom: {wqp_dof}")


# check to see if valid
print("expected wp frequencies")
print(wp_expected_freq)
print("\nexpected wqp frequencies")
print(wqp_expected_freq)


import matplotlib.pyplot as plt

# visualization for correlation between category and potability for wp
wp_row_percentages = pd.crosstab(wp_df['Organic_carbon'], wp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by Organic Carbon for wp', fontsize=14)
plt.xlabel('EPA Organic Carbon Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# visualization for correlation between category and potability for wqp
wqp_row_percentages = pd.crosstab(wqp_df['Organic_carbon'], wqp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wqp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by Organic Carbon for wqp', fontsize=14)
plt.xlabel('EPA Organic Carbon Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Acceptable', 'Not Acceptable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()




# NOW SAME THING FOR HARDNESS

# define bins and lables
bin_edges = [0, 180, max(max(wp_df['Hardness']),max(wqp_df['Hardness']))] 
bin_labels = ['Not Very Hard', 'Very Hard']

# bin Organic_carbon data into categories
wp_df['Hardness'] = pd.cut(wp_df['Hardness'], bins=bin_edges, labels=bin_labels, include_lowest=True)
wqp_df['Hardness'] = pd.cut(wqp_df['Hardness'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# count the frequencies of Potable and Non-Potable for each ph label
wp_contingency_table = pd.crosstab(wp_df['Hardness'], wp_df['Potability'])
wqp_contingency_table = pd.crosstab(wqp_df['Hardness'], wqp_df['Potability'])

print("\n\nHardness:\n")
print("for WP:")
print(wp_contingency_table)
print("\n")
print("for WQP")
print(wqp_contingency_table)
print("\n")

# run the Chi-Square Test of Independence
wp_chi2_stat, wp_p_value, wp_dof, wp_expected_freq = chi2_contingency(wp_contingency_table)
wqp_chi2_stat, wqp_p_value, wqp_dof, wqp_expected_freq = chi2_contingency(wqp_contingency_table)

print("Chi-squared tests for independence of categories of not very hard and very hard in water:")
print("wp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wp_chi2_stat:.4f}")
print(f"P-value: {wp_p_value:.4e}")
print(f"Degrees of Freedom: {wp_dof}")
print("\n")
print("Chi-squared tests for independence of categories of not very hard and very hard in water:")
print("wqp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wqp_chi2_stat:.4f}")
print(f"P-value: {wqp_p_value:.4e}")
print(f"Degrees of Freedom: {wqp_dof}")


# check to see if valid
print("expected wp frequencies")
print(wp_expected_freq)
print("\nexpected wqp frequencies")
print(wqp_expected_freq)


import matplotlib.pyplot as plt

# visualization for correlation between category and potability for wp
wp_row_percentages = pd.crosstab(wp_df['Hardness'], wp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by hardness for wp', fontsize=14)
plt.xlabel('EPA Hardness Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# visualization for correlation between category and potability for wqp
wqp_row_percentages = pd.crosstab(wqp_df['Hardness'], wqp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wqp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by hardness for wqp', fontsize=14)
plt.xlabel('EPA Hardness Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Not very hard', 'Very Hard'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()






# NOW SAME THING FOR CHLOROAMINES

# define bins and lables
bin_edges = [0, 4, max(max(wp_df['Chloramines']),max(wqp_df['Chloramines']))] 
bin_labels = ['Low', 'High']

# bin Organic_carbon data into categories
wp_df['Chloramines'] = pd.cut(wp_df['Chloramines'], bins=bin_edges, labels=bin_labels, include_lowest=True)
wqp_df['Chloramines'] = pd.cut(wqp_df['Chloramines'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# count the frequencies of Potable and Non-Potable for each ph label
wp_contingency_table = pd.crosstab(wp_df['Chloramines'], wp_df['Potability'])
wqp_contingency_table = pd.crosstab(wqp_df['Chloramines'], wqp_df['Potability'])

print("\n\Chloramines:\n")
print("for WP:")
print(wp_contingency_table)
print("\n")
print("for WQP")
print(wqp_contingency_table)
print("\n")

# run the Chi-Square Test of Independence
wp_chi2_stat, wp_p_value, wp_dof, wp_expected_freq = chi2_contingency(wp_contingency_table)
wqp_chi2_stat, wqp_p_value, wqp_dof, wqp_expected_freq = chi2_contingency(wqp_contingency_table)

print("Chi-squared tests for independence of categories of low and high amounts of Chloramines in water:")
print("wp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wp_chi2_stat:.4f}")
print(f"P-value: {wp_p_value:.4e}")
print(f"Degrees of Freedom: {wp_dof}")
print("\n")
print("Chi-squared tests for independence of categories of low and high amounts of Chloramines in water:")
print("wqp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wqp_chi2_stat:.4f}")
print(f"P-value: {wqp_p_value:.4e}")
print(f"Degrees of Freedom: {wqp_dof}")


# check to see if valid
print("expected wp frequencies")
print(wp_expected_freq)
print("\nexpected wqp frequencies")
print(wqp_expected_freq)


import matplotlib.pyplot as plt

# visualization for correlation between category and potability for wp
wp_row_percentages = pd.crosstab(wp_df['Chloramines'], wp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by Chloramine level for wp', fontsize=14)
plt.xlabel('EPA Chloramine Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# visualization for correlation between category and potability for wqp
wqp_row_percentages = pd.crosstab(wqp_df['Chloramines'], wqp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wqp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by Chloramines for wqp', fontsize=14)
plt.xlabel('EPA Chloramines Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()



# NOW SAME THING FOR SOLIDS

# define bins and lables
bin_edges = [0, 1000, 10000, max(max(wp_df['Solids']),max(wqp_df['Solids']))] 
bin_labels = ['Drinkable', 'Brakish', 'Saline/Hypersaline']

# bin Organic_carbon data into categories
wp_df['Solids'] = pd.cut(wp_df['Solids'], bins=bin_edges, labels=bin_labels, include_lowest=True)
wqp_df['Solids'] = pd.cut(wqp_df['Solids'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# count the frequencies of Potable and Non-Potable for each ph label
wp_contingency_table = pd.crosstab(wp_df['Solids'], wp_df['Potability'])
wqp_contingency_table = pd.crosstab(wqp_df['Solids'], wqp_df['Potability'])

print("\n\Solids:\n")
print("for WP:")
print(wp_contingency_table)
print("\n")
print("for WQP")
print(wqp_contingency_table)
print("\n")

# run the Chi-Square Test of Independence
wp_chi2_stat, wp_p_value, wp_dof, wp_expected_freq = chi2_contingency(wp_contingency_table)
wqp_chi2_stat, wqp_p_value, wqp_dof, wqp_expected_freq = chi2_contingency(wqp_contingency_table)

print("Chi-squared tests for independence of categories for Solids in water:")
print("wp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wp_chi2_stat:.4f}")
print(f"P-value: {wp_p_value:.4e}")
print(f"Degrees of Freedom: {wp_dof}")
print("\n")
print("Chi-squared tests for independence of categories of Solids in water:")
print("wqp Chi-Square Test Results")
print(f"Chi-Square Statistic: {wqp_chi2_stat:.4f}")
print(f"P-value: {wqp_p_value:.4e}")
print(f"Degrees of Freedom: {wqp_dof}")


# check to see if valid
print("expected wp frequencies")
print(wp_expected_freq)
print("\nexpected wqp frequencies")
print(wqp_expected_freq)


import matplotlib.pyplot as plt

# visualization for correlation between category and potability for wp
wp_row_percentages = pd.crosstab(wp_df['Solids'], wp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by Solids level for wp', fontsize=14)
plt.xlabel('EPA Solids Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# visualization for correlation between category and potability for wqp
wqp_row_percentages = pd.crosstab(wqp_df['Solids'], wqp_df['Potability'], normalize='index') * 100

# Plotting the stacked bar chart
ax = wqp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

plt.title('Proportion of Water Potability by Solids for wqp', fontsize=14)
plt.xlabel('EPA Solids Classification', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=0)

plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()



