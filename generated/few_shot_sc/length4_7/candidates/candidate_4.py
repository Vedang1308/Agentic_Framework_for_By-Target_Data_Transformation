import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and format as MM/DD/YYYY
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    # pd.to_datetime can parse the source format directly.
    dt = pd.to_datetime(df['Date'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Map hourly columns from 24-hour format to 12-hour AM/PM format
    rename_dict = {}
    
    # Hours 1-11 map to 1:00 AM - 11:00 AM
    for h in range(1, 12):
        rename_dict[f'{h}:00'] = f'{h}:00 AM'
        
    # Hour 12 maps to 12:00 PM
    rename_dict['12:00'] = '12:00 PM'
    
    # Hours 13-23 map to 1:00 PM - 11:00 PM
    for h in range(13, 24):
        hour_12 = h - 12
        rename_dict[f'{h}:00'] = f'{hour_12}:00 PM'
        
    # Hour 24 (represented as 24:00:00 in source) maps to 12:00 AM
    rename_dict['24:00:00'] = '12:00 AM'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_cols = ['date']
    
    # AM hours: 1:00 AM to 11:00 AM
    for h in range(1, 12):
        target_cols.append(f'{h}:00 AM')
        
    # 12:00 PM
    target_cols.append('12:00 PM')
    
    # PM hours: 1:00 PM to 11:00 PM
    for h in range(1, 12):
        target_cols.append(f'{h}:00 PM')
        
    # 12:00 AM (Midnight)
    target_cols.append('12:00 AM')
    
    # 4. Return the dataframe with only the target columns
    return df[target_cols]