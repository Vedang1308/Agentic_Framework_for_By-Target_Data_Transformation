import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Define the rename mapping for hourly columns
    # Source: '1:00'...'23:00' and '24:00:00'
    # Target: 'Hr 1'...'Hr 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    rename_dict['24:00:00'] = 'Hr 24'
    
    # Apply renaming
    df = df.rename(columns=rename_dict)
    
    # Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Select and return only the target columns
    return df[target_columns]