import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Make a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse the 'date' column to datetime
    # The format is %m/%d/%Y (e.g., '7/3/2015')
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Format the date to the target format: '%a %m/%d/%Y' (e.g., 'Thu 01/01/2015')
    # %a is the abbreviated weekday name
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Drop the temporary parsed date column and the original date column
    df.drop(columns=['date', 'date_parsed'], inplace=True)
    
    # 4. Rename 'Hour 1'...'Hour 24' to '1:00'...'24:00'
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hour {i}'] = f'{i}:00'
    
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Define the target column order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 6. Return the dataframe with columns in the correct order
    return df[target_columns]