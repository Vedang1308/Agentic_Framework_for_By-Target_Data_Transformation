import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the 'date' column to datetime
    # The format is '%m/%d/%Y' (e.g., '7/3/2015')
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Sort by the parsed datetime to ensure chronological order
    # This matches the target sample which is sorted by date
    df = df.sort_values(by='date_dt').reset_index(drop=True)
    
    # 3. Create the 'cst' column with the format '%a %m/%d/%Y'
    # %a is abbreviated weekday name (e.g., Thu)
    # %m is zero-padded month
    # %d is zero-padded day
    # %Y is 4-digit year
    df['cst'] = df['date_dt'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Rename the Hour columns to the target format 'X:00'
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hour {i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_map)
    
    # 5. Ensure correct data types
    # Hours 9-16 are int64 in the target, others are float64
    # The source already has these types, but we ensure they are preserved
    int_cols = [f'{i}:00' for i in range(9, 17)]
    for col in int_cols:
        if col in df.columns:
            # Convert to int64, handling potential NaNs if any (though sample shows 0)
            # Using 'Int64' nullable integer or standard int64. 
            # Standard int64 cannot hold NaN. If there are NaNs, they become -9223372036854775808 or error.
            # The sample shows 0s. We assume no NaNs in int columns based on sample.
            # If there are NaNs, we might need to fill them or use nullable int.
            # Given the sample values are 0, we'll cast to int64.
            df[col] = df[col].astype('int64')
            
    float_cols = [f'{i}:00' for i in range(1, 9)] + [f'{i}:00' for i in range(17, 25)]
    for col in float_cols:
        if col in df.columns:
            df[col] = df[col].astype('float64')
            
    # 6. Define the target columns in the correct order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 7. Select and return the target columns
    return df[target_columns]