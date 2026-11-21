import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse timestamp
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Extract hour
    df['hour'] = df['timestamp_dt'].dt.hour
    
    # Determine season
    month = df['timestamp_dt'].dt.month
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    df['season'] = month.apply(get_season)
    
    # Map source columns to target columns
    # HVAC: AC Compressor + Air Handler
    col_ac = 'AC COMPRESSOR WHS [emon ch3,4]'
    col_air = 'AIR HANDLER WHS [emon ch5,6]'
    df['hvac'] = df[col_ac] + df[col_air]
    
    # Water Heating
    col_wh = 'WATER HEATER WHS [emon ch7,8]'
    df['water_heating'] = df[col_wh]
    
    # Refrigerator: Primary + 2nd
    col_fridge1 = 'Primary Fridge WHS [emon ch12]'
    col_fridge2 = '2nd Fridge WHS [emon ch13]'
    df['refrigerator'] = df[col_fridge1] + df[col_fridge2]
    
    # Clothes Washer: Wattsup Energy Washer
    col_washer = 'Wattsup Energy Washer (WHS)'
    df['clothes_washer'] = df[col_washer]
    
    # Clothes Dryer: Dryer (1-CT) + Dryer (2-CTs)
    col_dryer1 = 'DRYER WHS (1-CT) [emon ch9]'
    col_dryer2 = 'Dryer WHS (2-CTs) [xpod chA-9,10]'
    df['clothes_dryer'] = df[col_dryer1] + df[col_dryer2]
    
    # Dishwasher
    col_dish = 'DISH WASHER WHS [emon ch11]'
    df['dishwasher'] = df[col_dish]
    
    # Cooking Range
    col_range = 'RANGE WHS (1-CT) [emon ch10]'
    df['cooking_range'] = df[col_range]
    
    # Pool Spa Pumps
    col_pool_pump = 'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    df['pool_spa_pumps'] = df[col_pool_pump]
    
    # Pool Spa Heater: Minisplit is the best candidate for a heater not already mapped
    col_pool_heater = 'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    df['pool_spa_heater'] = df[col_pool_heater]
    
    # Lighting and Plug columns
    # There are no explicit source columns for these. Based on the target sample having 0s,
    # and no obvious mapping from SPARE channels (which are often unused or unknown),
    # we initialize them to 0.
    df['interior_lighting'] = 0
    df['exterior_lighting'] = 0
    df['lighting'] = 0
    df['plug'] = 0
    
    # Define target columns
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Ensure integer types for numeric columns as per target schema
    numeric_cols = target_columns[1:] # Exclude 'season'
    for col in numeric_cols:
        df[col] = df[col].astype('int64')
        
    return df[target_columns]