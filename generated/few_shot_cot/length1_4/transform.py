import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column to datetime
    df['dt'] = pd.to_datetime(df['Date'])
    
    # 2. Create the 'cst' column with the required format: '%a %m/%d/%Y'
    # Example: 'Tue 01/01/2013'
    df['cst'] = df['dt'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename hourly columns from integers (1..24) to strings ('1:00'..'24:00')
    rename_dict = {str(i): f'{i}:00' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 4. Sort by the datetime to ensure the output order matches the target (chronological)
    df = df.sort_values('dt')
    
    # 5. Define target columns verbatim
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 6. Return the DataFrame with only the target columns
    return df[target_columns]