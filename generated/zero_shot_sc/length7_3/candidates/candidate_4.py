import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Define mapping for Month abbreviations to full names
    month_map = {
        'Jan': 'January',
        'Feb': 'February',
        'Mar': 'March',
        'Apr': 'April',
        'May': 'May',
        'Jun': 'June',
        'Jul': 'July',
        'Aug': 'August',
        'Sep': 'September',
        'Oct': 'October',
        'Nov': 'November',
        'Dec': 'December'
    }
    
    # Define mapping for Daytype codes to descriptive strings
    daytype_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Apply mappings to categorical columns
    df['month'] = df['Month'].map(month_map)
    df['day'] = df['Daytype'].map(daytype_map)
    
    # Define mapping for hourly columns
    # Source columns: '1:00', '2:00', ..., '24:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr24'
    hour_rename_map = {}
    for i in range(1, 25):
        src_col = f"{i}:00"
        tgt_col = f"hr{i}"
        hour_rename_map[src_col] = tgt_col
        
    # Rename hourly columns
    df = df.rename(columns=hour_rename_map)
    
    # Define target columns in the correct order
    target_columns = ['month', 'day', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24']
    
    # Select and return the required columns
    return df[target_columns]