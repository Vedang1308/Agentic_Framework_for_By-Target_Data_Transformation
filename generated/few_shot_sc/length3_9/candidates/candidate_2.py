import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'Date' column and format it to 'MM/DD/YYYY'
    # The source format is M/D/YYYY or MM/DD/YYYY
    dt = pd.to_datetime(df['Date'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns from 'Hr X' to 'Hour X'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'Hour {i}'
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]