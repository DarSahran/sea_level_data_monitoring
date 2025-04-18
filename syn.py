import pandas as pd
import numpy as np

# Define a broader set of global stations
stations = [
    {"StationID":"ST01","StationName":"North Atlantic Buoy","Region":"North Atlantic","Latitude":40.0,"Longitude":-70.0,"VLM_mm_per_year":-1.2,"GIA_mm_per_year":0.5},
    {"StationID":"ST02","StationName":"Central Pacific Buoy","Region":"Central Pacific","Latitude":0.0,"Longitude":-160.0,"VLM_mm_per_year":0.8,"GIA_mm_per_year":0.3},
    {"StationID":"ST03","StationName":"Mekong Delta Station","Region":"Mekong Delta","Latitude":10.5,"Longitude":104.0,"VLM_mm_per_year":-5.0,"GIA_mm_per_year":0.2},
    {"StationID":"ST04","StationName":"Arctic Ice Buoy","Region":"Arctic","Latitude":75.0,"Longitude":-42.0,"VLM_mm_per_year":0.5,"GIA_mm_per_year":1.0},
    {"StationID":"ST05","StationName":"Southern Ocean Buoy","Region":"Southern Ocean","Latitude":-60.0,"Longitude":30.0,"VLM_mm_per_year":0.2,"GIA_mm_per_year":0.8},
    {"StationID":"ST06","StationName":"Indian Ocean Buoy","Region":"Indian Ocean","Latitude":-20.0,"Longitude":80.0,"VLM_mm_per_year":-0.5,"GIA_mm_per_year":0.4},
    {"StationID":"ST07","StationName":"Mediterranean Station","Region":"Mediterranean","Latitude":35.0,"Longitude":18.0,"VLM_mm_per_year":-2.0,"GIA_mm_per_year":0.1},
    {"StationID":"ST08","StationName":"Baltic Sea Station","Region":"Baltic Sea","Latitude":60.0,"Longitude":20.0,"VLM_mm_per_year":-3.0,"GIA_mm_per_year":0.2},
    {"StationID":"ST09","StationName":"Caribbean Buoy","Region":"Caribbean","Latitude":15.0,"Longitude":-75.0,"VLM_mm_per_year":-1.0,"GIA_mm_per_year":0.3},
    {"StationID":"ST10","StationName":"South Pacific Buoy","Region":"South Pacific","Latitude":-30.0,"Longitude":-140.0,"VLM_mm_per_year":0.3,"GIA_mm_per_year":0.5},
]

# Date range
start, end = '2020-01-01', '2024-12-31'
dates = pd.date_range(start=start, end=end, freq='D')
n = len(dates)

rows = []
for st in stations:
    days = (dates - dates[0]).days.values
    # Generate base factors
    thermal = days * 0.00082 + np.random.normal(0, 0.05, n)
    glacier = days * 0.00055 + np.random.normal(0, 0.02, n)
    icesheet = days * 0.0004 + np.random.normal(0, 0.01, n)
    reservoir = -5 * np.sin(2 * np.pi * days / 365) + np.random.normal(0, 0.2, n)
    vlm = days * st["VLM_mm_per_year"] / 365 + np.random.normal(0, 0.02, n)
    gia = days * st["GIA_mm_per_year"] / 365 + np.random.normal(0, 0.01, n)
    ocean_current = np.random.normal(0, 0.3, n)
    conflict = np.zeros(n); mask = (dates >= "2022-06-01") & (dates <= "2022-12-31")
    conflict[mask] = -0.3 + np.random.normal(0, 0.1, mask.sum())
    
    # Additional factors
    groundwater = -2 * np.sin(2 * np.pi * days / 180) + np.random.normal(0, 0.1, n)
    salinity = np.random.normal(0, 0.05, n)
    atm_pressure = np.random.normal(0, 0.5, n)
    enso = (np.sin(2 * np.pi * days / 365.25) + np.random.normal(0,0.1,n)) * 0.5
    pdo = (np.cos(2 * np.pi * days / (365.25*7)) + np.random.normal(0,0.05,n)) * 0.4
    storm_surge = np.where((dates.month.isin([8,9])) & (np.random.rand(n) < 0.05),
                            np.random.normal(10,3,n), 0)
    sediment = np.random.normal(0, 0.2, n)
    river_discharge = 3 * np.sin(2 * np.pi * (dates.dayofyear) / 365) + np.random.normal(0,0.3,n)
    coastal_eng = np.random.normal(0, 0.1, n)
    
    # Total anomaly and measured level
    sea_mm = (thermal + glacier + icesheet + reservoir + vlm + gia + ocean_current +
              conflict + groundwater + salinity + atm_pressure + enso + pdo +
              storm_surge + sediment + river_discharge + coastal_eng)
    measured_m = sea_mm / 1000.0
    
    for i, dt in enumerate(dates):
        rows.append({
            "StationID": st["StationID"],
            "StationName": st["StationName"],
            "Region": st["Region"],
            "Latitude": st["Latitude"],
            "Longitude": st["Longitude"],
            "Date": dt,
            "ThermalExpansion_mm": thermal[i],
            "GlacierMelt_mm": glacier[i],
            "IceSheetLoss_mm": icesheet[i],
            "ReservoirStorage_mm": reservoir[i],
            "VerticalLandMovement_mm": vlm[i],
            "GIA_mm": gia[i],
            "OceanCurrentVar_mm": ocean_current[i],
            "ConflictImpact_mm": conflict[i],
            "GroundwaterExtraction_mm": groundwater[i],
            "SalinityVar_mm": salinity[i],
            "AtmPressureVar_mm": atm_pressure[i],
            "ENSOImpact_mm": enso[i],
            "PDOImpact_mm": pdo[i],
            "StormSurge_mm": storm_surge[i],
            "SedimentTrapping_mm": sediment[i],
            "RiverDischarge_mm": river_discharge[i],
            "CoastalEngineering_mm": coastal_eng[i],
            "SeaLevelAnomaly_mm": sea_mm[i],
            "MeasuredSeaLevel_m": measured_m[i]
        })

# Create DataFrame and save to CSV
df_extended = pd.DataFrame(rows)
csv_path = 'sea_level_global_extended.csv'
df_extended.to_csv(csv_path, index=False)

# Display preview
import ace_tools as tools; tools.display_dataframe_to_user(name="Extended Global Sea Level Data Preview", dataframe=df_extended.head())
