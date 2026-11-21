import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform Date Column
    # Parse DT_STRATA and format as MM/DD/YYYY
    df['date'] = pd.to_datetime(df['DT_STRATA']).dt.strftime('%m/%d/%Y')
    
    # 2. Map Hourly Columns
    # Source columns: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target columns order: 
    # 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 AM, 1:00 PM, ..., 11:00 PM, 12:00 PM
    
    target_hourly_cols = []
    rename_dict = {}
    
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        
        if i < 12:
            tgt_col = f'{i}:00 AM'
        elif i == 12:
            tgt_col = '12:00 AM'
        elif i < 24:
            tgt_col = f'{i-12}:00 PM'
        else: # i == 24
            tgt_col = '12:00 PM'
            
        rename_dict[src_col] = tgt_col
        target_hourly_cols.append(tgt_col)
        
    df = df.rename(columns=rename_dict)
    
    # 3. Select Final Columns
    # The target schema requires 'date' first, followed by the hourly columns in the specific order
    target_columns = ['date'] + target_hourly_cols
    
    return df[target_columns]