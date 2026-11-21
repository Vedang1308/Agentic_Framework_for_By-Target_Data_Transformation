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
    
    # 2. Map Daytype codes to full descriptions
    daytype_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    df['day'] = df['Daytype'].map(daytype_map)
    
    # 3. Rename hourly columns from '1:00'...'24:00' to 'hr1'...'hr24'
    rename_dict = {}
    for i in range(1, 25):
        old_name = f'{i}:00'
        new_name = f'hr{i}'
        rename_dict[old_name] = new_name
    
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns in the required order
    target_columns = ['month', 'day'] + [f'hr{i}' for i in range(1, 25)]
    
    # 5. Return the selected columns
    return df[target_columns]