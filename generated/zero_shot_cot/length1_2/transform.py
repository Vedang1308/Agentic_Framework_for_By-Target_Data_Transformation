import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names verbatim
    target_columns = [
        'cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', 
        '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', 
        '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', 
        '22:00', '23:00', '24:00'
    ]
    
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse the date column
    # The source date format is '%m/%d/%Y' (e.g., '7/3/2011')
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Format the date to the target format '%a %m/%d/%Y' (e.g., 'Sat 01/01/2011')
    # %a gives the abbreviated weekday name (e.g., Sat, Sun)
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename value columns to time columns
    # Map value1 -> 1:00, value2 -> 2:00, ..., value24 -> 24:00
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_map)
    
    # 4. Select and order the columns as required
    # We need 'cst' followed by the time columns in order
    result_df = df[target_columns]
    
    # Ensure the value columns are float64 as per target schema
    for col in target_columns[1:]:
        result_df[col] = result_df[col].astype('float64')
        
    return result_df