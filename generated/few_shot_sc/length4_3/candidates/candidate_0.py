import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Format the date column
    # Source DT_STRATA is like '7/2/2016', target date is '01/01/2016'
    dt = pd.to_datetime(df['DT_STRATA'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns to 12-hour AM/PM format
    # Mapping logic:
    # Hour 1-11: 1:00 AM - 11:00 AM
    # Hour 12: 12:00 PM (Noon)
    # Hour 13-23: 1:00 PM - 11:00 PM
    # Hour 24: 12:00 AM (Midnight)
    
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        if i == 12:
            tgt_col = '12:00 PM'
        elif i == 24:
            tgt_col = '12:00 AM'
        elif i < 12:
            tgt_col = f'{i}:00 AM'
        else: # i > 12
            tgt_col = f'{i-12}:00 PM'
        
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 3. Define the exact target column order as specified
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    return df[target_columns]