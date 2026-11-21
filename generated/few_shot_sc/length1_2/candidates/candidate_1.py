import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to datetime objects
    # The source date format is '%m/%d/%Y' (e.g., '7/3/2011')
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # 2. Create the 'cst' column with the required format '%a %m/%d/%Y'
    # Example: 'Sat 01/01/2011'
    df['cst'] = df['date_dt'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename value columns to hour columns
    # value1 -> 1:00, ..., value24 -> 24:00
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'{i}:00'
    
    df.rename(columns=rename_dict, inplace=True)
    
    # 4. Sort the dataframe chronologically based on the parsed date
    # The target sample is sorted by date
    df.sort_values(by='date_dt', inplace=True)
    
    # 5. Define the target columns verbatim
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 6. Select only the target columns and return
    # This automatically drops 'class', 'Description', 'analysis', 'date', 'uom', 'date_dt'
    return df[target_columns]