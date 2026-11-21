import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse DT_STRATA to extract month names.
    2. Map DOW codes to daytype categories ('weekday', 'weekend', 'holiday').
    3. Rename hourly columns from PCT_HOURLY_XXXX to hrN.
    4. Select and order the final columns.
    """
    df = source.copy()
    
    # 1. Extract month name from DT_STRATA
    # Format is '%m/%d/%Y'
    df['month'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y').dt.month_name()
    
    # 2. Map DOW to daytype
    # Based on standard conventions and sample data:
    # 1-5: Weekdays
    # 6-7: Weekends
    # H, D: Holidays
    dow_mapping = {
        '1': 'weekday',
        '2': 'weekday',
        '3': 'weekday',
        '4': 'weekday',
        '5': 'weekday',
        '6': 'weekend',
        '7': 'weekend',
        'H': 'holiday',
        'D': 'holiday'
    }
    df['daytype'] = df['DOW'].map(dow_mapping)
    
    # 3. Rename hourly columns
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: hr1 ... hr24
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:04d}'
        tgt_col = f'hr{i}'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns in order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 5. Return the transformed dataframe with only the target columns
    return df[target_columns]