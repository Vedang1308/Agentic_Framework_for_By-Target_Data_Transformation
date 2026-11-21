import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Renaming 'Month' to 'month' and expanding abbreviations to full month names.
    2. Renaming 'Daytype' to 'day' and mapping 'WD'/'WE' to 'weekday'/'weekend'.
    3. Renaming hourly columns '1:00'-'24:00' to 'hr1'-'hr24'.
    """
    df = source.copy()
    
    # 1. Define column mappings for the 24 hours
    hour_col_map = {f"{h}:00": f"hr{h}" for h in range(1, 25)}
    
    # 2. Rename columns
    df.rename(columns=hour_col_map, inplace=True)
    df.rename(columns={'Month': 'month', 'Daytype': 'day'}, inplace=True)
    
    # 3. Map Month abbreviations to full names
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
    df['month'] = df['month'].map(month_map)
    
    # 4. Map Daytype codes to full words
    day_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    df['day'] = df['day'].map(day_map)
    
    # 5. Define the target column order
    target_columns = ['month', 'day'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return columns in the correct order
    return df[target_columns]