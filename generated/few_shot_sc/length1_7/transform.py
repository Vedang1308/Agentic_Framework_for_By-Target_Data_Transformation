import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform Date to cst
    # Parse the date string to datetime object
    # The format is 'Day MM/DD/YYYY' (e.g., 'Thu 10/01/2009')
    # We can parse it directly or split. pd.to_datetime handles this format well.
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename columns
    # Source has '24:00:00', target has '24:00'
    rename_map = {'24:00:00': '24:00'}
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns verbatim
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # 4. Select and return only the target columns
    return df[target_columns]