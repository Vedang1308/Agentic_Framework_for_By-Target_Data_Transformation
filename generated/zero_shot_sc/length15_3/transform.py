import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Clean data: Replace sensor error value 32767 with 0
    # This value appears frequently in spare/future columns and likely indicates no data/overflow
    source_clean = source.replace(32767, 0)
    
    # 2. Parse timestamp
    source_clean['timestamp_dt'] = pd.to_datetime(source_clean['timestamp'])
    source_clean['hour'] = source_clean['timestamp_dt'].dt.hour
    source_clean['month'] = source_clean['timestamp_dt'].dt.month
    
    # 3. Define Season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else: # 9, 10, 11
            return 'Fall'
            
    source_clean['season'] = source_clean['month'].apply(get_season)
    
    # 4. Construct Category Columns
    # HVAC
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    source_clean['HVAC'] = source_clean[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    source_clean['domestic_water_heating'] = source_clean['WATER HEATER WHS [emon ch7,8]']
    
    # Major Appliances
    major_appliance_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    source_clean['major_appliances'] = source_clean[major_appliance_cols].sum(axis=1)
    
    # Lighting (Not explicitly measured, set to 0)
    source_clean['lighting'] = 0
    
    # Miscellaneous Plug Loads (Spare/Future/Pool)
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Future use- WHS (2-CTs)[xpod chB-3,4]',
        'Future use- WHS (2-CTs)[xpod chB-5,6]'
    ]
    source_clean['miscellaneous_plug_loads'] = source_clean[misc_cols].sum(axis=1)
    
    # Total
    source_clean['Total'] = source_clean['TOTAL BLDG WHS [emon ch1,2]']
    
    # 5. Aggregate
    group_cols = ['season', 'hour']
    agg_cols = {
        'HVAC': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'Total': 'sum'
    }
    
    df = source_clean.groupby(group_cols, as_index=False).agg(agg_cols)
    
    # 6. Format Output
    # Ensure correct column names and types
    target_columns = ['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']
    
    # Cast types to match target schema exactly
    df['season'] = df['season'].astype('object')
    df['hour'] = df['hour'].astype('int64')
    df['HVAC'] = df['HVAC'].astype('int64')
    df['domestic_water_heating'] = df['domestic_water_heating'].astype('int64')
    df['major_appliances'] = df['major_appliances'].astype('int64')
    df['lighting'] = df['lighting'].astype('int64')
    df['miscellaneous_plug_loads'] = df['miscellaneous_plug_loads'].astype('float64')
    df['Total'] = df['Total'].astype('int64')
    
    # Select and return
    return df[target_columns]