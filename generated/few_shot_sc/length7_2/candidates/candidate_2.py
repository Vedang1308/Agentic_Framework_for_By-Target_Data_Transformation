import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse DT_STRATA and extract month name
    # Source format: 'M/D/YYYY' e.g., '7/2/2016'
    dt_series = pd.to_datetime(df['DT_STRATA'])
    df['month'] = dt_series.dt.strftime('%B')
    
    # 2. Map DOW to daytype
    # Source DOW values: '1'-'7', 'H', 'D'
    # Standard mapping for energy/load data:
    # 1-5: Weekday, 6-7: Weekend, H: Holiday, D: Day Off
    dow_map = {
        '1': 'weekday',
        '2': 'weekday',
        '3': 'weekday',
        '4': 'weekday',
        '5': 'weekday',
        '6': 'weekend',
        '7': 'weekend',
        'H': 'holiday',
        'D': 'dayoff'
    }
    df['daytype'] = df['DOW'].map(dow_map)
    
    # 3. Rename hourly columns
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: hr1 ... hr24
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'hr{i}'
        rename_dict[src_col] = tgt_col
        
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns in correct order
    target_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 5. Return the transformed dataframe with only target columns
    return df[target_cols]