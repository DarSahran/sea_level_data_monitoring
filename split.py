import pandas as pd

def split_sea_level_csv(
    input_csv: str = 'sea_level_global_extended.csv',
    output_excel: str = 'sea_level_split.xlsx'
):
    """
    Splits the master sea-level CSV into three Excel sheets:
      1. Metadata & Measured Levels
      2. Natural Factors
      3. Other Factors
    Each sheet keeps 'StationID' as the common key.
    """
    # Load master dataset
    df = pd.read_csv(input_csv)

    # Define column groups
    sheet1_cols = [
        'StationID', 'StationName', 'Region', 'Latitude', 'Longitude',
        'Date', 'SeaLevelAnomaly_mm', 'MeasuredSeaLevel_m'
    ]
    sheet2_cols = [
        'StationID', 'ThermalExpansion_mm', 'GlacierMelt_mm', 'IceSheetLoss_mm',
        'ReservoirStorage_mm', 'VerticalLandMovement_mm', 'GIA_mm', 'OceanCurrentVar_mm'
    ]
    sheet3_cols = [
        'StationID', 'ConflictImpact_mm', 'GroundwaterExtraction_mm', 'SalinityVar_mm',
        'AtmPressureVar_mm', 'ENSOImpact_mm', 'PDOImpact_mm', 'StormSurge_mm',
        'SedimentTrapping_mm', 'RiverDischarge_mm', 'CoastalEngineering_mm'
    ]

    # Write to Excel with three sheets
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df[sheet1_cols].to_excel(writer, sheet_name='Metadata_Measured', index=False)
        df[sheet2_cols].to_excel(writer, sheet_name='Natural_Factors', index=False)
        df[sheet3_cols].to_excel(writer, sheet_name='Other_Factors', index=False)

    print(f"Successfully split '{input_csv}' into '{output_excel}' with sheets:")
    print("  • Metadata_Measured")
    print("  • Natural_Factors")
    print("  • Other_Factors")

if __name__ == '__main__':
    # Adjust paths below if your CSV or desired XLSX names differ
    split_sea_level_csv(
        input_csv='sea_level_global_extended.csv',
        output_excel='sea_level_split.xlsx'
    )
