import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process Date Column
    # Parse DT_STRATA and format as MM/DD/YYYY
    dt = pd.to_datetime(df['DT_STRATA'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Map Hourly Columns to 12-hour AM/PM format
    rename_dict = {}
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        if h == 12:
            label = '12:00 PM'
        elif h == 24:
            label = '12:00 AM'
        elif h < 12:
            label = f'{h}:00 AM'
        else:
            label = f'{h - 12}:00 PM'
        
        if src_col in df.columns:
            rename_dict[src_col] = label
            
    df = df.rename(columns=rename_dict)
    
    # 3. Define Target Columns in the exact order specified
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', # Note: 12:00 AM (Midnight) comes before PM hours in the target schema list provided
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 PM'
    ]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]