import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse the date column to datetime
    dt = pd.to_datetime(df['date'])
    
    # Create the 'cst' column with format '%a %m/%d/%Y'
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Rename value columns to hour format '1:00', '2:00', ..., '24:00'
    rename_dict = {f'value{i}': f'{i}:00' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # Sort by date to match the target's chronological order
    # We use the parsed datetime 'dt' for sorting, then drop it
    df['dt_sort_key'] = dt
    df = df.sort_values('dt_sort_key')
    df = df.drop(columns=['dt_sort_key'])
    
    # Define target columns
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # Select only the target columns
    return df[target_cols]