import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Map Month abbreviations to full names
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
    df['month'] = df['Month'].map(month_map)
    
    # 2. Map Daytype to full day type strings
    daytype_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    df['day'] = df['Daytype'].map(daytype_map)
    
    # 3. Rename hourly columns from 'H:00' to 'hrH'
    rename_dict = {}
    for h in range(1, 25):
        old_col = f'{h}:00'
        new_col = f'hr{h}'
        if old_col in df.columns:
            rename_dict[old_col] = new_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns in the exact order specified
    target_columns = ['month', 'day'] + [f'hr{i}' for i in range(1, 25)]
    
    # 5. Return the transformed dataframe
    return df[target_columns]