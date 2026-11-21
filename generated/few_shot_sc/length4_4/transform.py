import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and set as index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    
    # 2. Handle Row Count Increase (182 -> 183) by reindexing to full date range
    # This fills any missing dates within the min-max range of the source data.
    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(date_range)
    
    # 3. Define Column Mapping
    # Source columns are integers 1 to 24.
    # Target columns are 12-hour format strings.
    # Mapping logic:
    # Source 1-11 -> 1:00 AM - 11:00 AM
    # Source 12 -> 12:00 PM
    # Source 13-23 -> 1:00 PM - 11:00 PM
    # Source 24 -> 12:00 AM
    
    rename_dict = {}
    
    # 1:00 AM to 11:00 AM
    for i in range(1, 12):
        rename_dict[str(i)] = f'{i}:00 AM'
        
    # 12:00 PM
    rename_dict['12'] = '12:00 PM'
    
    # 1:00 PM to 11:00 PM (Source 13 to 23)
    for i in range(13, 24):
        hour_12 = i - 12
        rename_dict[str(i)] = f'{hour_12}:00 PM'
        
    # 12:00 AM (Source 24)
    rename_dict['24'] = '12:00 AM'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Reset index to get 'Date' back as a column
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})
    
    # 5. Format date column
    df['date'] = df['date'].dt.strftime('%m/%d/%Y')
    
    # 6. Define target columns in the exact order specified
    target_cols = [
        'date',
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 PM'
    ]
    
    # 7. Select and return
    return df[target_cols]