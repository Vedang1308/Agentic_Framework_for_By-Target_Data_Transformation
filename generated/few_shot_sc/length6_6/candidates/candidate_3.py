import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target schema.
    - Parses and formats the 'date' column to 'Date' with format 'YYYY-MM-DD HH:MM:SS'.
    - Renames 'Hour X' columns to 'Hr X' for X in 1..24.
    """
    df = source.copy()
    
    # 1. Handle Date Column
    # Parse the 'date' column (format M/D/YYYY) to datetime
    dt_series = pd.to_datetime(df['date'])
    # Format to 'YYYY-MM-DD HH:MM:SS' as required by target 'Date'
    df['Date'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename Hour Columns
    # Map 'Hour 1'...'Hour 24' to 'Hr 1'...'Hr 24'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'Hr {i}'
    
    df.rename(columns=rename_dict, inplace=True)
    
    # 3. Select and Order Columns
    # Construct the list of target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    return df[target_columns]