import pandas as pd

# Load the original annual data (adjust the file name/path as needed)
df = pd.read_csv('sea_level_data.csv')

# Create a list to hold the synthetic monthly records.
monthly_records = []

# Loop through each year from the first row up to the penultimate row.
# For each year, calculate monthly values using linear interpolation.
for idx in range(len(df) - 1):
    current_year = int(df.loc[idx, 'Year'])
    current_level = df.loc[idx, 'Sea_Level']
    next_level = df.loc[idx + 1, 'Sea_Level']
    
    # For each month in the year (months 1 through 12)
    for month in range(1, 13):
        # Calculate the fraction of the interval (e.g., Jan corresponds to 0/12, Feb 1/12, etc.)
        fraction = (month - 1) / 12.0
        synthetic_level = current_level * (1 - fraction) + next_level * fraction
        monthly_records.append({
            'Year': current_year,
            'Month': month,
            'Sea_Level': synthetic_level
        })

# For the last year (2018), replicate the annual value across all 12 months.
last_year = int(df.loc[len(df) - 1, 'Year'])
last_level = df.loc[len(df) - 1, 'Sea_Level']
for month in range(1, 13):
    monthly_records.append({
        'Year': last_year,
        'Month': month,
        'Sea_Level': last_level
    })

# Convert list of records to a DataFrame
monthly_df = pd.DataFrame(monthly_records)

# Save the updated CSV file
monthly_df.to_csv('/synthetic_sea_level_data.csv', index=False)

print("Synthetic monthly sea level data saved to '/synthetic_sea_level_data.csv'")
