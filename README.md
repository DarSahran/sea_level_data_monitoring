# Sea Level Data Processing

This project processes sea level data from NetCDF format to CSV, with the capability to generate synthetic monthly data from annual measurements.

## Features

- Converts NetCDF files to CSV format
- Generates synthetic monthly data from annual measurements
- Uses statistical modeling (ARIMA) for realistic data generation
- Preserves annual averages while creating monthly variations

## Requirements

- Python 3.10+
- Required packages:
  - xarray
  - pandas
  - numpy
  - scipy
  - statsmodels
  - netcdf4

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sea-level-data-processing.git
cd sea-level-data-processing
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Place your NetCDF file in the project directory
2. Run the conversion script:
```bash
python convert_nc_to_csv.py
```

The script will generate a CSV file with monthly data.

## Data Description

The dataset contains sea level measurements from 1900 to 2018, including:
- Global average sea level change
- Contributions from various sources (glaciers, ice sheets, etc.)
- Upper and lower bounds for measurements

## License

MIT License 