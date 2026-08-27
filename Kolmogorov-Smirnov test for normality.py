import numpy as np
from scipy import stats
import pandas as pd
from statsmodels.stats.diagnostic import lilliefors

# Testing data for normaility using Kolmogorov-Smirnov test

# for WP potable:

# Sample data:
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_potable.xlsx")
print("\nWP potable:")

# Perform the KS test against a normal distribution with mean and variance the same as given column
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for column in columns:
    # lilliefors is a more accurate version of the KS test in this case as it recognizes that parameters are from sample, not population
    ks_statistic, p_value = lilliefors(df[column], dist='norm', pvalmethod='table')
    print(f"KS Statistic for {column}: {ks_statistic}")
    print(f"P-value: {p_value}")

# for WP non-potable

# Sample data:
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wp_Spearman_test_data_not_potable.xlsx")
print("\nWP not-potable:")

# Perform the KS test against a normal distribution with mean and variance the same as given column
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for column in columns:
    # lilliefors is a more accurate version of the KS test in this case as it recognizes that parameters are from sample, not population
    ks_statistic, p_value = lilliefors(df[column], dist='norm', pvalmethod='table')
    print(f"KS Statistic for {column}: {ks_statistic}")
    print(f"P-value: {p_value}")

# for WQP potable

# Sample data:
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_potable.xlsx")
print("\nWQP potable:")

# Perform the KS test against a normal distribution with mean and variance the same as given column
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for column in columns:
    # lilliefors is a more accurate version of the KS test in this case as it recognizes that parameters are from sample, not population
    ks_statistic, p_value = lilliefors(df[column], dist='norm', pvalmethod='table')
    print(f"KS Statistic for {column}: {ks_statistic}")
    print(f"P-value: {p_value}")

# for WQP non-potable

# Sample data:
df = pd.read_excel("C:\\Users\\kramej4\\Downloads\\ISYE-4370 Project Data Files\\ISYE_WaterQualityProject\\wqp_Spearman_test_data_not_potable.xlsx")
print("\nWP not-potable:")

# Perform the KS test against a normal distribution with mean and variance the same as given column
columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for column in columns:
    # lilliefors is a more accurate version of the KS test in this case as it recognizes that parameters are from sample, not population
    ks_statistic, p_value = lilliefors(df[column], dist='norm', pvalmethod='table')
    print(f"KS Statistic for {column}: {ks_statistic}")
    print(f"P-value: {p_value}")