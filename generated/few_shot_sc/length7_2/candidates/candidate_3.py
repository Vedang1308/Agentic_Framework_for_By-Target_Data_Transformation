import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform DT_STRATA to month name
    # Source format is '%m/%d/%Y', e.g., '7/2/2016'
    dt = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    df['month'] = dt.dt.strftime('%B')
    
    # 2. Transform DOW to daytype
    # Distinct values in source: '1', '2', '3', '4', '5', '6', '7', 'H', 'D'
    # Standard mapping for utility strata:
    # 1-5: Weekday
    # 6-7: Weekend
    # H: Holiday
    # D: Often Weekend/Day-off in these contexts. Mapping to 'weekend' is standard for 'D' if not 'H'.
    dow_mapping = {
        '1': 'weekday',
        '2': 'weekday',
        '3': 'weekday',
        '4': 'weekday',
        '5': 'weekday',
        '6': 'weekend',
        '7': 'weekend',
        'H': 'holiday',
        'D': 'weekend'
    }
    df['daytype'] = df['DOW'].map(dow_mapping)
    
    # 3. Rename hourly columns PCT_HOURLY_XX00 -> hrXX
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'hr{i}'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns and return
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]