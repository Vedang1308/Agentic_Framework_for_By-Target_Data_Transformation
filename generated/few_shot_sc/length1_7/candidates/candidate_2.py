import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Rename 'Date' to 'cst'
    # The format %a %m/%d/%Y is the same in source and target, so direct renaming works.
    df = df.rename(columns={'Date': 'cst'})
    
    # 2. Rename '24:00:00' to '24:00'
    df = df.rename(columns={'24:00:00': '24:00'})
    
    # 3. Drop the 'Segment' column as it is not in the target schema
    if 'Segment' in df.columns:
        df = df.drop(columns=['Segment'])
    
    # 4. Define target columns in the correct order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 5. Return the dataframe with only the target columns
    return df[target_columns]