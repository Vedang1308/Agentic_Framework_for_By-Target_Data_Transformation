import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column to extract month and day of week.
    2. Map the 24 hourly time columns to hr1...hr24.
    3. Create 'month' column with full month names.
    4. Create 'daytype' column ('weekday' or 'weekend').
    5. Assemble the final DataFrame with the correct column order.
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse Date
    # Format is '%m/%d/%Y'
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract Month Name
    df['month'] = df['parsed_date'].dt.month_name()
    
    # 3. Determine Day Type
    # dayofweek: Monday=0, ..., Sunday=6
    # Weekdays are 0-4, Weekends are 5-6
    df['daytype'] = np.where(df['parsed_date'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 4. Map Hour Columns
    # Source columns are like '1:00 AM', '12:00 PM', etc.
    # We need to map them to hr1 (midnight/12 AM) through hr24 (11 PM)
    
    hour_mapping = {
        '12:00 AM': 'hr1',
        '1:00 AM': 'hr2',
        '2:00 AM': 'hr3',
        '3:00 AM': 'hr4',
        '4:00 AM': 'hr5',
        '5:00 AM': 'hr6',
        '6:00 AM': 'hr7',
        '7:00 AM': 'hr8',
        '8:00 AM': 'hr9',
        '9:00 AM': 'hr10',
        '10:00 AM': 'hr11',
        '11:00 AM': 'hr12',
        '12:00 PM': 'hr13',
        '1:00 PM': 'hr14',
        '2:00 PM': 'hr15',
        '3:00 PM': 'hr16',
        '4:00 PM': 'hr17',
        '5:00 PM': 'hr18',
        '6:00 PM': 'hr19',
        '7:00 PM': 'hr20',
        '8:00 PM': 'hr21',
        '9:00 PM': 'hr22',
        '10:00 PM': 'hr23',
        '11:00 PM': 'hr24'
    }
    
    # Rename the hour columns
    df = df.rename(columns=hour_mapping)
    
    # 5. Define Target Columns
    target_columns = [
        'month', 'daytype', 
        'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 
        'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 
        'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # 6. Select and Return
    # Drop helper columns if any (parsed_date) and select target columns
    result_df = df[target_columns]
    
    # Ensure numeric types for hr columns are float
    for col in target_columns[2:]:
        result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
        
    return result_df