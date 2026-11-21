import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing dates and setting them as the index.
    2. Renaming hourly columns from 'Hour N' to 'N:00'.
    3. Reindexing to a complete daily date range to handle missing dates (increasing row count).
    4. Filling missing values with 0.
    5. Formatting the date column as 'cst' with format '%a %m/%d/%Y'.
    """
    
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Set date as index for time-series operations
    df = df.set_index('date')
    
    # 3. Define new column names for hours
    # Source columns are 'Hour 1' to 'Hour 24'
    # Target columns are '1:00' to '24:00'
    new_columns = [f"{i}:00" for i in range(1, 25)]
    
    # Map old column names to new column names
    col_map = {f"Hour {i}": f"{i}:00" for i in range(1, 25)}
    df = df.rename(columns=col_map)
    
    # 4. Handle missing dates (Row count increase from 182 to 183)
    # Determine the full date range
    min_date = df.index.min()
    max_date = df.index.max()
    
    # Create a complete daily date range
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # Reindex to include all days in the range
    df = df.reindex(full_date_range)
    
    # Fill missing values with 0
    # Note: This might change int columns to float if not handled, 
    # but we will cast them back later.
    df = df.fillna(0)
    
    # 5. Reset index to bring date back as a column
    df = df.reset_index()
    df = df.rename(columns={'index': 'cst'}) # The index name is 'date' originally? 
    # Actually, set_index('date') names the index 'date'. 
    # Let's correct the reset_index naming.
    
    # Correction: When we do set_index('date'), the index name is 'date'.
    # reset_index() creates a column named 'date'.
    df = df.rename(columns={'date': 'cst'})
    
    # 6. Format the 'cst' column
    df['cst'] = df['cst'].dt.strftime('%a %m/%d/%Y')
    
    # 7. Ensure correct data types
    # Target has int64 for hours 9-16
    int_hours = [f"{i}:00" for i in range(9, 17)]
    for col in int_hours:
        if col in df.columns:
            df[col] = df[col].astype('int64')
            
    # Float hours
    float_hours = [f"{i}:00" for i in range(1, 25) if i not in range(9, 17)]
    for col in float_hours:
        if col in df.columns:
            df[col] = df[col].astype('float64')
            
    # 8. Define target column order
    target_columns = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    # Return the dataframe with the exact target columns
    return df[target_columns]