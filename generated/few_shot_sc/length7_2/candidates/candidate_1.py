import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse DT_STRATA and extract month name
    dt = pd.to_datetime(df['DT_STRATA'])
    df['month'] = dt.dt.strftime('%B')
    
    # 2. Map DOW to daytype
    # Based on standard interpretations of such datasets:
    # 1-5: Weekday, 6-7: Weekend, H: Holiday, D: Weekday (default for ambiguous D)
    dow_map = {
        '1': 'weekday',
        '2': 'weekday',
        '3': 'weekday',
        '4': 'weekday',
        '5': 'weekday',
        '6': 'weekend',
        '7': 'weekend',
        'H': 'holiday',
        'D': 'weekday'
    }
    df['daytype'] = df['DOW'].map(dow_map)
    
    # 3. Rename hourly columns PCT_HOURLY_XX00 -> hrX
    rename_dict = {f'PCT_HOURLY_{i:02d}00': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns and return
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]