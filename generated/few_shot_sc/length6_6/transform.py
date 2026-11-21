import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'date' column and format it to 'YYYY-MM-DD HH:MM:SS'
    # The source format is '%m/%d/%Y' (e.g., '7/3/2015')
    # The target format is '%Y-%m-%d %H:%M:%S' (e.g., '2015-07-03 00:00:00')
    dt = pd.to_datetime(df['date'])
    df['Date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename hourly columns from 'Hour X' to 'Hr X'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'Hr {i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Sort by Date to match the chronological order in the target sample
    # Although the source sample is sorted, explicit sorting ensures consistency.
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    # 5. Return only the target columns
    return df[target_columns]