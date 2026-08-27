import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

# see if classifications based on EPA guidlines affect potability
np.random.seed(42)

wp_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_data.xlsx")
wqp_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_data.xlsx")

# define bins and lables (quartiles from wp and wqp excel files, first tab)
bin_ph_wp = [6.115637546, 7.378597016, 8.383761691]
bin_Hardness_wp = [180.323568, 197.5502981, 218.2714214]
bin_Solids_wp =[15360.83507, 21884.53851, 29496.91016]
bin_Cholamines_wp = [6.375449253, 7.625545081, 8.494115369]
bin_Sulfate_wp = [313.5147404, 336.0227531, 364.7327704]
bin_Conductivity_wp = [367.1176961, 431.3272487, 514.4527095]
bin_Organic_carbon_wp = [9.280759847, 13.28583838, 17.25648527]
bin_Trihalomethanes_wp = [60.14968497, 69.45175688, 77.62129994]
bin_Turbidity_wp = [3.647425426, 4.176699214, 4.622223479]

# create arrays to traverse through in loop
categories = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
bins_wp = [bin_ph_wp, bin_Hardness_wp, bin_Solids_wp, bin_Cholamines_wp, bin_Sulfate_wp, bin_Conductivity_wp, bin_Organic_carbon_wp, bin_Trihalomethanes_wp, bin_Turbidity_wp]

for category, base_bins in zip(categories, bins_wp):
    print(f"\n{'='*60}")
    print(f"ANALYZING CATEGORY: {category}")
    print(f"{'='*60}")
    
    # Add -inf and inf to capture all data points (creates 4 bins total)
    bin_edges = [-np.inf] + base_bins + [np.inf]
    bin_labels = ['Q1 (Lowest)', 'Q2 (Low-Mid)', 'Q3 (High-Mid)', 'Q4 (Highest)']
    
    # Use temporary columns for the binned data to prevent overwriting original data
    binned_col = f'{category}_binned'
    wp_df[binned_col] = pd.cut(wp_df[category], bins=bin_edges, labels=bin_labels, include_lowest=True)
    wqp_df[binned_col] = pd.cut(wqp_df[category], bins=bin_edges, labels=bin_labels, include_lowest=True)

    # Count the frequencies of Potable and Non-Potable for each label
    wp_contingency_table = pd.crosstab(wp_df[binned_col], wp_df['Potability'])
    wqp_contingency_table = pd.crosstab(wqp_df[binned_col], wqp_df['Potability'])
    
    print(f"Contingency Table for WP ({category}):")
    print(wp_contingency_table)
    print("\n")
    print(f"Contingency Table for WQP ({category}):")
    print(wqp_contingency_table)
    print("\n")

    # Run the Chi-Square Test of Independence
    wp_chi2_stat, wp_p_value, wp_dof, wp_expected_freq = chi2_contingency(wp_contingency_table.dropna())
    wqp_chi2_stat, wqp_p_value, wqp_dof, wqp_expected_freq = chi2_contingency(wqp_contingency_table.dropna())

    print(f"Chi-squared tests for independence of {category} categories on potability of water:")
    print(">>> WP Chi-Square Test Results")
    print(f"Chi-Square Statistic: {wp_chi2_stat:.4f}")
    print(f"P-value: {wp_p_value:.4e}")
    print(f"Degrees of Freedom: {wp_dof}")
    print("\n")
    
    print(">>> WQP Chi-Square Test Results")
    print(f"Chi-Square Statistic: {wqp_chi2_stat:.4f}")
    print(f"P-value: {wqp_p_value:.4e}")
    print(f"Degrees of Freedom: {wqp_dof}")
    print("\n")

    # Check to see if valid
    # (Expected frequencies should all be >= 5)
    print(f"Expected WP frequencies ({category}):")
    print(wp_expected_freq)
    print(f"\nExpected WQP frequencies ({category}):")
    print(wqp_expected_freq)
    print("\n")
    
    # WP Visualization
    wp_row_percentages = pd.crosstab(wp_df[binned_col], wp_df['Potability'], normalize='index') * 100
    ax = wp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

    plt.title(f'Proportion of Water Potability by {category} (WP)', fontsize=14)
    plt.xlabel(f'{category} Classification', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # WQP Visualization
    wqp_row_percentages = pd.crosstab(wqp_df[binned_col], wqp_df['Potability'], normalize='index') * 100
    ax = wqp_row_percentages.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#e63946', '#457b9d'])

    plt.title(f'Proportion of Water Potability by {category} (WQP)', fontsize=14)
    plt.xlabel(f'{category} Classification', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Potability', labels=['Non-Potable', 'Potable'], bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()