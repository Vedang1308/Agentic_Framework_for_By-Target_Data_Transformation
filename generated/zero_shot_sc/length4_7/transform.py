import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Define the target column order verbatim
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
        '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]

    # 2. Parse and Format Date
    # Source format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    # Target format: '01/01/2003' -> '%m/%d/%Y'
    df = source.copy()
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 3. Map Source Hour Columns to Target Hour Columns
    # Source: 1:00 (1 AM) ... 12:00 (12 PM/Noon) ... 23:00 (11 PM) ... 24:00:00 (12 AM/Midnight)
    mapping = {}
    
    # 1:00 to 11:00 -> 1:00 AM to 11:00 AM
    for h in range(1, 12):
        mapping[f'{h}:00'] = f'{h}:00 AM'
        
    # 12:00 -> 12:00 PM (Noon)
    mapping['12:00'] = '12:00 PM'
    
    # 13:00 to 23:00 -> 1:00 PM to 11:00 PM
    for h in range(13, 24):
        pm_h = h - 12
        mapping[f'{h}:00'] = f'{pm_h}:00 PM'
        
    # 24:00:00 -> 12:00 AM (Midnight)
    mapping['24:00:00'] = '12:00 AM'

    # 4. Rename columns and drop unused columns
    df = df.rename(columns=mapping)
    
    # Drop Segment and original Date column
    cols_to_drop = ['Segment', 'Date']
    df = df.drop(columns=cols_to_drop, errors='ignore')

    # 5. Ensure correct column order
    # Verify all target columns are present
    for col in target_columns:
        if col not in df.columns:
            raise ValueError(f"Target column {col} not found in transformed dataframe")
            
    df = df[target_columns]
    
    return df