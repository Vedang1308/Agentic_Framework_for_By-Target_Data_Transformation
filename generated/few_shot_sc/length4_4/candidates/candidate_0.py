import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target schema.
    1. Renames hourly columns from integers 1-24 to 12-hour format strings.
    2. Formats the 'Date' column to 'MM/DD/YYYY'.
    3. Drops the 'Class' column.
    4. Sorts by date.
    5. Returns columns in the specific target order.
    """
    df = source.copy()
    
    # 1. Define the mapping from source hour columns (integers) to target column names
    # Mapping logic:
    # 1-11 -> 1:00 AM - 11:00 AM
    # 12 -> 12:00 PM
    # 13-23 -> 1:00 PM - 11:00 PM
    # 24 -> 12:00 AM
    
    rename_dict = {}
    # 1 AM to 11 AM
    for i in range(1, 12):
        rename_dict[i] = f"{i}:00 AM"
    # 12 PM (Noon)
    rename_dict[12] = "12:00 PM"
    # 1 PM to 11 PM
    for i in range(13, 24):
        hour_12 = i - 12
        rename_dict[i] = f"{hour_12}:00 PM"
    # 12 AM (Midnight)
    rename_dict[24] = "12:00 AM"
    
    # Apply rename
    df = df.rename(columns=rename_dict)
    
    # 2. Format Date
    # Source is 'M/D/YYYY' or similar, parse to datetime then format to 'MM/DD/YYYY'
    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
    
    # 3. Drop unnecessary columns
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])
        
    # 4. Sort by date to match target sample order (chronological)
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # 5. Define target columns in the exact order specified
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    return df[target_columns]