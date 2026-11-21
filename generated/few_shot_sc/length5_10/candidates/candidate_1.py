import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Rename 'Date' to 'date'
    df = df.rename(columns={'Date': 'date'})
    
    # 2. Construct rename dictionary for hourly columns
    # Source columns: '1:00'...'23:00', '24:00:00'
    # Target columns: 'value1'...'value24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    rename_dict['24:00:00'] = 'value24'
    
    # 3. Apply renaming
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns verbatim
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 5. Return the DataFrame with only the target columns
    return df[target_columns]