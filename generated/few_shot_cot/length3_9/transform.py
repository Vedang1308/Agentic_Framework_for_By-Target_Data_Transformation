import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Format the Date column
    # Source 'Date' is like '1/1/2014', Target 'date' is '01/01/2014'
    dt = pd.to_datetime(df['Date'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hour columns
    # Source 'Hr 1'...'Hr 24' -> Target 'Hour 1'...'Hour 24'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'Hour {i}'
    df = df.rename(columns=rename_dict)
    
    # 3. Select target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    return df[target_columns]