import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Format the date column
    # Source DT_STRATA is like '7/2/2016', Target date is '01/01/2016'
    dt = pd.to_datetime(df['DT_STRATA'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Map hourly columns to 12-hour format with AM/PM
    # Target column order: 
    # 1:00 AM .. 11:00 AM (Hours 1-11)
    # 12:00 AM (Hour 24 - Midnight)
    # 1:00 PM .. 11:00 PM (Hours 13-23)
    # 12:00 PM (Hour 12 - Noon)
    
    rename_dict = {}
    
    # Hours 1 to 11 (AM)
    for i in range(1, 12):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'{i}:00 AM'
        rename_dict[src_col] = tgt_col
        
    # Hour 24 (Midnight -> 12:00 AM)
    rename_dict['PCT_HOURLY_2400'] = '12:00 AM'
    
    # Hours 13 to 23 (PM)
    for i in range(13, 24):
        src_col = f'PCT_HOURLY_{i:02d}00'
        hour_12 = i - 12
        tgt_col = f'{hour_12}:00 PM'
        rename_dict[src_col] = tgt_col
        
    # Hour 12 (Noon -> 12:00 PM)
    rename_dict['PCT_HOURLY_1200'] = '12:00 PM'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the exact order specified
    target_cols = [
        'date',
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    return df[target_cols]