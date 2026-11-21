import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse DT_STRATA to datetime
    # Format is '%m/%d/%Y'
    df['DT_STRATA'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'January')
    df['month'] = df['DT_STRATA'].dt.strftime('%B')
    
    # 3. Determine 'daytype' based on 'DOW'
    # Mapping inference:
    # 'H' -> 'holiday'
    # '1' (Sun), '7' (Sat) -> 'weekend'
    # '2'-'6' (Mon-Fri) -> 'weekday'
    # 'D' -> 'weekday' (Assuming 'D' stands for a standard day/weekday given the context)
    
    def map_daytype(dow):
        if dow == 'H':
            return 'holiday'
        elif dow in ['1', '7']:
            return 'weekend'
        else:
            # Covers '2', '3', '4', '5', '6', 'D'
            return 'weekday'
            
    df['daytype'] = df['DOW'].apply(map_daytype)
    
    # 4. Rename hourly columns from PCT_HOURLY_XXXX to hrN
    # Source: PCT_HOURLY_0100 -> Target: hr1
    # Source: PCT_HOURLY_2400 -> Target: hr24
    
    def rename_hour_col(col):
        if col.startswith('PCT_HOURLY_'):
            # Extract the hour part, e.g., '0100' -> 1
            hour_str = col.split('_')[-1]
            hour_int = int(hour_str)
            return f'hr{hour_int}'
        return col
        
    df = df.rename(columns=rename_hour_col)
    
    # 5. Define target columns in the exact required order
    target_columns = [
        'month', 'daytype', 
        'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 
        'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 
        'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # 6. Select and return only the target columns
    # Ensure float64 type for hourly columns if necessary, though pandas usually infers correctly from source float64
    result_df = df[target_columns].copy()
    
    # Ensure hourly columns are float64
    for col in result_df.columns[2:]: # Skip 'month' and 'daytype'
        result_df[col] = result_df[col].astype('float64')
        
    return result_df