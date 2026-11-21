import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column to datetime
    dt = pd.to_datetime(df['Date'])
    
    # 2. Create 'month' column with full month name (e.g., 'January')
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column ('weekday' or 'weekend')
    # dayofweek: Mon=0, ..., Sat=5, Sun=6
    df['daytype'] = df['Date'].map(lambda _: 'weekend') # Placeholder, will overwrite
    # Correct logic:
    is_weekend = dt.dt.dayofweek >= 5
    df['daytype'] = 'weekday'
    df.loc[is_weekend, 'daytype'] = 'weekend'
    
    # 4. Rename hour columns from 'Hr X' to 'hrX'
    rename_dict = {}
    for i in range(1, 25):
        old_name = f'Hr {i}'
        new_name = f'hr{i}'
        if old_name in df.columns:
            rename_dict[old_name] = new_name
            
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns in exact order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe
    return df[target_columns]