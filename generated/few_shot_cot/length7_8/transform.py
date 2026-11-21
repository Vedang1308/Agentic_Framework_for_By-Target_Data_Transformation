import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column to datetime
    dt = pd.to_datetime(df['Date'])
    
    # 2. Create 'month' column with full month name (e.g., 'January')
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column ('weekday' or 'weekend')
    # dayofweek: Monday=0, ..., Sunday=6. Weekend is 5 (Sat) or 6 (Sun).
    is_weekend = dt.dt.dayofweek.isin([5, 6])
    df['daytype'] = is_weekend.map({True: 'weekend', False: 'weekday'})
    
    # 4. Rename hour columns from 'Hr 1'...'Hr 24' to 'hr1'...'hr24'
    rename_dict = {f'Hr {i}': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns in the exact required order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe with only the target columns
    return df[target_columns]