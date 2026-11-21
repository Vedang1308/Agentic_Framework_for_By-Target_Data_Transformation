import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Handle sentinel value 32767.0 as NaN
    df = df.replace(32767.0, np.nan)
    
    # 2. Parse timestamp and extract month and hour
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month'] = df['timestamp'].dt.month
    df['hour'] = df['timestamp'].dt.hour
    
    # 3. Define column mappings for each target category
    # HVAC: AC Compressor, Air Handler, Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
    # Major Appliances: Dryer (1-CT), Range, Dishwasher, Primary Fridge, 2nd Fridge, Dryer (2-CTs)
    major_appl_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    
    # Lighting: No explicit columns found, initialize to 0
    lighting_cols = []
    
    # Miscellaneous Plug Loads: Pool Pump, Spares, Future Use
    misc_plug_cols = [
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]',
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Future use- WHS (2-CTs)[xpod chB-3,4]',
        'Future use- WHS (2-CTs)[xpod chB-5,6]'
    ]
    
    # Total: Total Building WHS
    total_cols = [
        'TOTAL BLDG WHS [emon ch1,2]'
    ]
    
    # 4. Calculate sums for each category
    # Using sum(axis=1) to sum across columns for each row
    df['HVAC'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    df['lighting'] = 0.0 # No columns mapped
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    df['Total'] = df[total_cols].sum(axis=1)
    
    # 5. Group by month and hour and aggregate (sum)
    # The target has 288 rows (12 months * 24 hours), implying we sum all occurrences of each month/hour pair
    agg_df = df.groupby(['month', 'hour']).agg({
        'HVAC': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    # 6. Select and order columns to match target verbatim
    target_columns = ['month', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']
    
    return agg_df[target_columns]