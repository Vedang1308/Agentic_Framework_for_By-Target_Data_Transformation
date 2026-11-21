import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format is likely '%m/%d/%Y' based on sample '7/3/2015'
    # Target format is '%Y-%m-%d %H:%M:%S' based on sample '2015-01-01 00:00:00'
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename Hour columns to value columns
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'value{i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    return df[target_columns]