import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing hourly load data into the target format.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Rename 'value1'...'value24' to '1:00'...'24:00'.
    3. Format the date into 'cst' column with format '%a %m/%d/%Y'.
    4. Sort chronologically by the original date.
    5. Select and order columns to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # The source format is '%m/%d/%Y' (e.g., '7/3/2011')
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Rename value columns
    # Map value1 -> 1:00, value2 -> 2:00, ..., value24 -> 24:00
    rename_map = {f'value{i}': f'{i}:00' for i in range(1, 25)}
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Create the 'cst' column
    # Format: '%a %m/%d/%Y' (e.g., 'Sat 01/01/2011')
    df['cst'] = df['parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Sort by date to ensure chronological order
    # Sorting by the parsed datetime ensures correct order regardless of string representation
    df = df.sort_values('parsed_date')
    
    # 5. Define target columns in the exact required order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 6. Select the target columns and reset index
    result = df[target_columns].reset_index(drop=True)
    
    return result