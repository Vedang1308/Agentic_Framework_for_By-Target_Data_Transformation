import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define mappings for categorical columns
    month_map = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
        'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
        'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
    }
    day_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Transform Month column
    df['month'] = df['Month'].map(month_map)
    
    # Transform Daytype column
    df['day'] = df['Daytype'].map(day_map)
    
    # Rename hourly columns from '1:00'...'24:00' to 'hr1'...'hr24'
    hour_rename = {f'{i}:00': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=hour_rename)
    
    # Define the target column order
    target_columns = ['month', 'day'] + [f'hr{i}' for i in range(1, 25)]
    
    # Select and order columns
    df = df[target_columns]
    
    return df