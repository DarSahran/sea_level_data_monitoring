import xarray as xr
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# Open the NetCDF file
ds = xr.open_dataset('global_timeseries_measures.nc')

# Print the structure of the dataset
print("Dataset structure:")
print(ds)

# Print the time variable to see its format
print("\nTime variable:")
print(ds.time)

# Convert to pandas DataFrame
df = ds.to_dataframe().reset_index()

# Convert the time column to datetime and format it
df['time'] = pd.to_datetime(df['time'])
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month

def generate_monthly_data(annual_data, years):
    # Convert annual data to time series
    ts = pd.Series(annual_data, index=pd.date_range(start=f'{years[0]}-01-01', 
                                                   end=f'{years[-1]}-12-31', 
                                                   freq='Y'))
    
    # Decompose the time series to get trend, seasonal, and residual components
    try:
        decomposition = seasonal_decompose(ts, model='additive', period=1)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
    except:
        # If decomposition fails, use simpler approach
        trend = ts.rolling(window=3, center=True).mean()
        seasonal = pd.Series(np.sin(np.linspace(0, 2*np.pi, len(ts))) * 0.1 * ts.mean(), 
                           index=ts.index)
        residual = ts - trend - seasonal
    
    # Fit ARIMA model to residuals
    try:
        model = ARIMA(residual.dropna(), order=(1,1,1))
        model_fit = model.fit()
    except:
        # If ARIMA fails, use normal distribution
        mu, std = stats.norm.fit(residual.dropna())
    
    # Generate monthly data
    monthly_data = []
    for year in years:
        # Get the trend value for this year
        year_trend = trend[ts.index.year == year].mean()
        if pd.isna(year_trend):
            year_trend = ts[ts.index.year == year].mean()
        
        # Generate monthly values
        monthly_values = []
        for month in range(1, 13):
            # Base value from trend
            value = year_trend
            
            # Add seasonal component
            seasonal_factor = np.sin((month - 6) * np.pi / 6) * 0.1 * year_trend
            value += seasonal_factor
            
            # Add random component
            try:
                # Use ARIMA to generate random component
                random_component = model_fit.forecast(1)[0]
            except:
                # Fallback to normal distribution
                random_component = np.random.normal(mu, std/2)
            
            value += random_component
            monthly_values.append(value)
        
        # Adjust to match annual average
        monthly_values = np.array(monthly_values)
        annual_avg = ts[ts.index.year == year].mean()
        monthly_values = monthly_values - np.mean(monthly_values) + annual_avg
        
        monthly_data.extend(monthly_values)
    
    return np.array(monthly_data)

# Create a new DataFrame with all months
new_rows = []
years = df['year'].values

# Generate synthetic data for each numeric column
for col in df.columns:
    if col not in ['time', 'year', 'month'] and pd.api.types.is_numeric_dtype(df[col]):
        print(f"Processing {col}...")
        monthly_values = generate_monthly_data(df[col].values, years)
        
        # Create rows for each month
        for i, year in enumerate(years):
            for month in range(1, 13):
                new_row = {'year': year, 'month': month}
                new_row[col] = monthly_values[i*12 + month-1]
                new_rows.append(new_row)

# Create the new DataFrame
monthly_df = pd.DataFrame(new_rows)

# Group by year and month to combine all columns
monthly_df = monthly_df.groupby(['year', 'month']).mean().reset_index()

# Sort by year and month
monthly_df = monthly_df.sort_values(['year', 'month'])

# Print dataset dimensions
print("\nDataset dimensions:")
print(f"Number of rows: {len(monthly_df)}")
print(f"Number of columns: {len(monthly_df.columns)}")
print("\nColumns:")
for i, col in enumerate(monthly_df.columns, 1):
    print(f"{i}. {col}")

# Save to CSV
monthly_df.to_csv('sea_level_data_monthly.csv', index=False)
print("\nConversion completed successfully! Monthly data saved to sea_level_data_monthly.csv") 