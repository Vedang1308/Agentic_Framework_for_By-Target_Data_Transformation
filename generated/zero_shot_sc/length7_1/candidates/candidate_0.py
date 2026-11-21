import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with hourly columns into a target DataFrame
    with 'month', 'daytype', and 'hr1'-'hr24' columns.
    """
    df = source.copy()
    
    # 1. Parse the CST column to extract date information
    # Format is '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    df['parsed_date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'April', 'December')
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Determine 'daytype' (weekday vs weekend)
    # weekday() returns 0 for Monday, 6 for Sunday
    # Monday-Friday (0-4) are weekdays, Saturday-Sunday (5-6) are weekends
    df['daytype'] = np.where(df['parsed_date'].dt.weekday < 5, 'weekday', 'weekend')
    
    # 4. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    # Identify the hourly columns
    hour_cols = [col for col in df.columns if col != 'CST' and col != 'parsed_date' and col != 'month' and col != 'daytype']
    
    # Create a mapping for renaming
    # We expect 24 columns. Let's map them sequentially.
    # Note: The source columns might not be in strict order in the DataFrame, 
    # but typically they are. We should map based on the column name content.
    
    rename_map = {}
    for col in hour_cols:
        # Extract the hour number from the column name
        # Examples: '1:00' -> 1, '24:00:00' -> 24
        # Split by ':' and take the first part
        try:
            hour_num = int(col.split(':')[0])
            rename_map[col] = f'hr{hour_num}'
        except ValueError:
            # Fallback or skip if format is unexpected
            pass
            
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Select and order the final columns
    target_columns = ['month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24']
    
    # Ensure all target columns exist and select them
    # If any hour is missing, it will raise an error, which is appropriate for validation
    result = df[target_columns].copy()
    
    # 6. Ensure correct data types
    # month and daytype should be object (string)
    result['month'] = result['month'].astype(str)
    result['daytype'] = result['daytype'].astype(str)
    
    # Hourly columns should be float64
    for col in target_columns[2:]: # Skip first two
        result[col] = result[col].astype(float)
        
    return result[target_columns]