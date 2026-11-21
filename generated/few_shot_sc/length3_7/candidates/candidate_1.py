import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and Format Date
    # Source 'Date' is like '7/3/2013'. Target 'date' is '07/03/2013'.
    dt = pd.to_datetime(df['Date'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hourly Columns
    # Source columns are integers 1 to 24. Target columns are 'Hour 1' to 'Hour 24'.
    rename_dict = {}
    for i in range(1, 25):
        # Source columns might be strings or integers in the index
        if str(i) in df.columns:
            rename_dict[str(i)] = f'Hour {i}'
        elif i in df.columns:
            rename_dict[i] = f'Hour {i}'
            
    df = df.rename(columns=rename_dict)
    
    # 3. Define Target Columns Verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Select and Return
    return df[target_columns]