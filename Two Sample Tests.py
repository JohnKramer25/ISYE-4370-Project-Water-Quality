import pandas as pd
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind

# Mann Whitney U Test and T Test for potable and non potable data in WP and WQP

columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Trihalomethanes']
# separate Organic_carbon and Turbidity (They are the only normal)
org_car_turb = ['Organic_carbon', 'Turbidity']
wppot_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_potable.xlsx")
wpnpot_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_not_potable.xlsx")
wqppot_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_potable.xlsx")
wqpnpot_df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_not_potable.xlsx")

# compare all data (will ignore organic carbon and turbidity because they are normal) for wp
print("\nComparing qualities in potable and non potable WP data (not turbidity or orgnanic carbon) using mann whitney U test:")
for column in columns:
    u_statistic, p_value = mannwhitneyu(wppot_df[column], wpnpot_df[column], alternative='two-sided')
    print(f"U-Statistic for {column}: {u_statistic:.4f}")
    print(f"P-value for {column}:     {p_value:.4f}")

print("\n Independent t test for organic_carbon and turbidity in WP:")
for column in org_car_turb:
    t_statistic, p_value = ttest_ind(wppot_df[column], wpnpot_df[column], equal_var=False)
    print(f"T-Statistic for {org_car_turb}: {t_statistic:.4f}")
    print(f"P-value for {org_car_turb}:     {p_value:.4f}")

# same for wqp but no need for t test as data is not normal (by ks test)
print("\nComparing qualities in potable and non potable WQP data using mann whitney U test")
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for column in columns:
    u_statistic, p_value = mannwhitneyu(wqppot_df[column], wqpnpot_df[column], alternative='two-sided')
    print(f"U-Statistic for {column}: {u_statistic:.4f}")
    print(f"P-value for {column}:     {p_value:.4f}")

