import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid SettingWithCopyWarning and modify original
    df = source.copy()
    
    # Mapping for Month abbreviations to full names
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
    
    # Mapping for Daytype abbreviations to full names
    day_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Apply mappings to the categorical columns
    df['month'] = df['Month'].map(month_map)
    df['day'] = df['Daytype'].map(day_map)
    
    # Create a mapping for the hourly columns from 'X:00' to 'hrX'
    hour_rename_map = {}
    for i in range(1, 25):
        hour_rename_map[f'{i}:00'] = f'hr{i}'
        
    # Rename the columns
    df.rename(columns=hour_rename_map, inplace=True)
    
    # Define the target columns in the exact order specified
    target_columns = [
        'month', 'day', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 
        'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 
        'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # Select and return the columns in the correct order
    return df[target_columns]