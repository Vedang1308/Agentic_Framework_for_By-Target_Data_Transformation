import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    # Handle the 24th hour specifically as it has a different format in source
    rename_dict['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_dict)
    
    # 2. Define the target columns in the correct order
    # The Date column remains 'Date'
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 3. Select only the target columns
    # This automatically drops 'Segment' and any other unused columns
    return df[target_columns]