import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Map Month abbreviations to full month names
    month_map = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
        'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
        'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
    }
    
    # 2. Map Daytype codes to full day names
    daytype_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # 3. Create rename dictionary for hourly columns
    # Source columns are '1:00', '2:00', ..., '24:00'
    # Target columns are 'hr1', 'hr2', ..., 'hr24'
    hourly_rename = {}
    for i in range(1, 25):
        old_col = f"{i}:00"
        new_col = f"hr{i}"
        if old_col in df.columns:
            hourly_rename[old_col] = new_col
            
    # 4. Combine all rename mappings
    rename_dict = {
        'Month': 'month',
        'Daytype': 'day'
    }
    rename_dict.update(hourly_rename)
    
    # 5. Apply column renaming
    df = df.rename(columns=rename_dict)
    
    # 6. Apply value mapping for 'month' and 'day'
    df['month'] = df['month'].map(month_map)
    df['day'] = df['day'].map(daytype_map)
    
    # 7. Define the target column order
    target_columns = [
        'month', 'day', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8',
        'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17',
        'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # 8. Return the DataFrame with columns in the correct order
    return df[target_columns]