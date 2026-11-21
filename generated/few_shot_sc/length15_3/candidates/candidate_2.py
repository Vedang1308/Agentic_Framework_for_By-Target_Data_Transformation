import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Handle sentinel values
    # 32767 is a common sentinel for missing data in this dataset
    df = df.replace(32767, np.nan)
    
    # 2. Parse timestamp and extract features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['month'] = df['timestamp'].dt.month
    
    # 3. Determine season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['month'].apply(get_season)
    
    # 4. Map source columns to target categories
    # HVAC: AC Compressor, Air Handler, Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    df['HVAC'] = df[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    dwh_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    
    # Major Appliances: Dryer (1-CT), Range, Dishwasher, Primary Fridge, 2nd Fridge, Dryer (2-CTs)
    major_appl_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    
    # Lighting: No explicit column, sample shows 0. 
    # We will initialize to 0.
    df['lighting'] = 0
    
    # Miscellaneous Plug Loads: Pool Pump, Spares, Future Use
    misc_cols = [
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]',
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Future use- WHS (2-CTs)[xpod chB-3,4]',
        'Future use- WHS (2-CTs)[xpod chB-5,6]'
    ]
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # Total: Total Building WHS
    df['Total'] = df['TOTAL BLDG WHS [emon ch1,2]']
    
    # 5. Aggregate
    # Group by season and hour, sum the values
    agg_df = df.groupby(['season', 'hour']).agg({
        'HVAC': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    # 6. Fill NaNs with 0
    agg_df = agg_df.fillna(0)
    
    # 7. Cast types to match target schema
    # season: object (string)
    # hour: int64
    # HVAC: int64
    # domestic_water_heating: int64
    # major_appliances: int64
    # lighting: int64
    # miscellaneous_plug_loads: float64
    # Total: int64
    
    agg_df['hour'] = agg_df['hour'].astype('int64')
    agg_df['HVAC'] = agg_df['HVAC'].astype('int64')
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype('int64')
    agg_df['major_appliances'] = agg_df['major_appliances'].astype('int64')
    agg_df['lighting'] = agg_df['lighting'].astype('int64')
    agg_df['miscellaneous_plug_loads'] = agg_df['miscellaneous_plug_loads'].astype('float64')
    agg_df['Total'] = agg_df['Total'].astype('int64')
    
    # 8. Select and order columns
    target_columns = ['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']
    
    return agg_df[target_columns]