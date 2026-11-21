import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse DT_STRATA to extract the month name.
    2. Map DOW codes to daytype categories (weekday, weekend, holiday, dst).
    3. Rename hourly percentage columns to hr1...hr24.
    4. Select and order the final columns.
    """
    df = source.copy()
    
    # 1. Extract Month from DT_STRATA
    # Format is %m/%d/%Y
    df['DT_STRATA'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    df['month'] = df['DT_STRATA'].dt.strftime('%B')
    
    # 2. Map DOW to daytype
    # Based on standard conventions:
    # 1-5: Weekday
    # 6-7: Weekend
    # H: Holiday
    # D: DST transition
    def map_daytype(dow):
        if dow in ['1', '2', '3', '4', '5']:
            return 'weekday'
        elif dow in ['6', '7']:
            return 'weekend'
        elif dow == 'H':
            return 'holiday'
        elif dow == 'D':
            return 'dst'
        else:
            return 'unknown'
            
    df['daytype'] = df['DOW'].apply(map_daytype)
    
    # 3. Rename and Select Hourly Columns
    # Source columns: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target columns: hr1 ... hr24
    
    hour_mapping = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:04d}'
        tgt_col = f'hr{i}'
        hour_mapping[src_col] = tgt_col
        
    df = df.rename(columns=hour_mapping)
    
    # 4. Define Target Columns and Select
    target_columns = [
        'month', 'daytype', 
        'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 
        'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 
        'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # Ensure we only return the required columns
    # Note: The source has 5673 rows, target has 5673 rows. 
    # No aggregation is needed, just reshaping/renaming.
    
    return df[target_columns]