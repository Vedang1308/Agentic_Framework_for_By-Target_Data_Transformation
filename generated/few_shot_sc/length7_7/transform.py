import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Extract 'month' (full name) and 'daytype' ('weekday'/'weekend').
    3. Rename 'Hour X' columns to 'hrX'.
    4. Select and order the columns as per target schema.
    """
    df = source.copy()
    
    # 1. Parse date
    df['date_parsed'] = pd.to_datetime(df['date'])
    
    # 2. Extract month (e.g., "January")
    df['month'] = df['date_parsed'].dt.strftime('%B')
    
    # 3. Extract daytype ("weekday" or "weekend")
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = df['date_parsed'].dt.dayofweek.apply(lambda d: 'weekday' if d < 5 else 'weekend')
    
    # 4. Rename Hour columns
    rename_dict = {f'Hour {i}': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return
    return df[target_columns]