import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date
    dt = pd.to_datetime(df['Date'])
    
    # 2. Extract Month Name
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Determine Day Type (weekday/weekend)
    # dayofweek: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    df['daytype'] = dt.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename numeric columns 1-24 to hr1-hr24
    rename_dict = {i: f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return target columns
    # Sorting by the original date ensures a consistent order if needed, 
    # though the primary requirement is the schema transformation.
    # We sort by the parsed datetime to match typical chronological expectations.
    df = df.sort_values(by=dt).reset_index(drop=True)
    
    return df[target_columns]