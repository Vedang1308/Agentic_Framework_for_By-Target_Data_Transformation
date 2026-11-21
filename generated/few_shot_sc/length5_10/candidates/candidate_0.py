import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Rename 'Date' to 'date'
    df = df.rename(columns={'Date': 'date'})
    
    # Create mapping for hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # Define target columns in order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    return df[target_columns]