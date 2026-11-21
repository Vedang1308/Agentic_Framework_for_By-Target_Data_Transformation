import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Derive season from MONTH
    def get_season(month):
        if month in [12, 1, 2]:
            return 'WINTER'
        elif month in [3, 4, 5]:
            return 'SPRING'
        elif month in [6, 7, 8]:
            return 'SUMMER'
        else:
            return 'FALL'
    
    source['season'] = source['MONTH'].apply(get_season)
    
    # 2. Derive daytype from PROFILE_CLASS
    def get_daytype(pc):
        if pd.isna(pc):
            return 'UNKNOWN'
        if pc.startswith('WE'):
            return 'WEEKEND'
        else:
            return 'WEEKDAY'
            
    source['daytype'] = source['PROFILE_CLASS'].apply(get_daytype)
    
    # 3. Unpivot the range columns
    # We will create a long dataframe by stacking the 4 possible ranges
    ranges_list = []
    for i in range(1, 5):
        df_range = source.copy()
        df_range['range_index'] = i
        df_range['low_end'] = df_range[f'LOW_{i}']
        df_range['high_end'] = df_range[f'HIGH_{i}']
        df_range['coefficient'] = df_range[f'COEFF_{i}']
        ranges_list.append(df_range)
        
    df_long = pd.concat(ranges_list, ignore_index=True)
    
    # 4. Filter to keep only valid ranges based on NUMBER_OF_RANGES
    # Only keep rows where range_index <= NUMBER_OF_RANGES
    df_valid = df_long[df_long['range_index'] <= df_long['NUMBER_OF_RANGES']].copy()
    
    # 5. Calculate temperature_range
    df_valid['temperature_range'] = df_valid['high_end'] - df_valid['low_end']
    
    # 6. Select and order the target columns
    target_columns = ['season', 'daytype', 'hour', 'temperature_range', 'constant', 'coefficient', 'low_end', 'high_end']
    
    # Ensure hour is float64 as per target schema
    df_valid['hour'] = df_valid['HOUR'].astype(float)
    df_valid['constant'] = df_valid['CONSTANT'].astype(float)
    df_valid['coefficient'] = df_valid['coefficient'].astype(float)
    df_valid['low_end'] = df_valid['low_end'].astype(float)
    df_valid['high_end'] = df_valid['high_end'].astype(float)
    df_valid['temperature_range'] = df_valid['temperature_range'].astype(float)
    
    result = df_valid[target_columns]
    
    # Sort to match typical output order (optional but good for consistency)
    # The sample is sorted by season, daytype, hour.
    result = result.sort_values(by=['season', 'daytype', 'hour']).reset_index(drop=True)
    
    return result