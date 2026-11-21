import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Format the date to the target format '%a %m/%d/%Y' (e.g., 'Tue 01/01/2013')
    # and rename the column to 'cst'
    df['cst'] = df['Date'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Create a mapping for the numeric columns 1-24 to 1:00-24:00
    col_mapping = {str(i): f'{i}:00' for i in range(1, 25)}
    
    # 4. Rename the columns
    df = df.rename(columns=col_mapping)
    
    # 5. Drop the original 'Date' and 'Class' columns as they are not in the target
    df = df.drop(columns=['Date', 'Class'])
    
    # 6. Define the exact target column order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 7. Ensure the columns are in the correct order
    df = df[target_columns]
    
    # 8. Optional: Sort by date if necessary, though usually row order is preserved or irrelevant for correctness checks
    # df = df.sort_values('cst').reset_index(drop=True)
    
    return df[target_columns]