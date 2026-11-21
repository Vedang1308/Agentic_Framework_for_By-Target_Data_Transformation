import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by renaming columns,
    formatting dates, and reordering columns to match the target schema.
    """
    # 1. Copy the source to avoid modifying the original
    df = source.copy()
    
    # 2. Handle the Date column
    # Parse the date string to datetime to handle formatting consistently (e.g., zero-padding)
    # Source format is '%m/%d/%Y' (e.g., '7/3/2013')
    # Target format is '%m/%d/%Y' (e.g., '01/01/2013')
    if 'Date' in df.columns:
        df['date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 3. Define the mapping from source numeric columns (1-24) to target time columns
    # Source 1-11 -> 1:00 AM - 11:00 AM
    # Source 12 -> 12:00 PM (Noon)
    # Source 13-23 -> 1:00 PM - 11:00 PM
    # Source 24 -> 12:00 AM (Midnight)
    
    col_mapping = {}
    
    # 1:00 AM to 11:00 AM
    for i in range(1, 12):
        col_mapping[str(i)] = f"{i}:00 AM"
        
    # 12:00 PM (Noon) corresponds to hour 12
    col_mapping['12'] = '12:00 PM'
    
    # 1:00 PM to 11:00 PM
    for i in range(13, 24):
        pm_hour = i - 12
        col_mapping[str(i)] = f"{pm_hour}:00 PM"
        
    # 12:00 AM (Midnight) corresponds to hour 24
    col_mapping['24'] = '12:00 AM'
    
    # 4. Rename the numeric columns
    df = df.rename(columns=col_mapping)
    
    # 5. Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    # 6. Select and reorder columns. 
    # Note: We drop the original 'Date' and 'Class' columns as they are not in the target schema.
    # We only keep 'date' and the renamed time columns.
    
    # Ensure we only select columns that exist in the dataframe
    existing_target_cols = [col for col in target_columns if col in df.columns]
    
    # If there are missing columns (e.g. if source didn't have all 24 hours), 
    # we might need to handle NaNs, but assuming schema consistency:
    df = df[existing_target_cols]
    
    # Return the DataFrame with the exact target column names
    return df[target_columns]