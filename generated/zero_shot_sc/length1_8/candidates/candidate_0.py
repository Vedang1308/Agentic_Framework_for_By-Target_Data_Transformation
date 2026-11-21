import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target wide-format DataFrame.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Extract the date part for grouping and the hour part for pivoting.
    3. Map the 24-hour clock (0-23) to the target 1-24 hour format (1-24).
       Assumption: Hour 0 (00:00-00:59) maps to column '1:00', Hour 1 to '2:00', ..., Hour 23 to '24:00'.
    4. Group by date and mapped hour, summing the 'cerc_logger_1' values.
    5. Pivot the table to have dates as rows and hours as columns.
    6. Format the date index as 'cst' column with format '%a %m/%d/%Y'.
    7. Ensure all target columns are present and ordered correctly.
    """
    
    # 1. Parse dates
    # The source format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['dt_date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column index (1-24)
    # Hour 0 -> 1:00
    # Hour 1 -> 2:00
    # ...
    # Hour 23 -> 24:00
    df['target_hour'] = df['hour'] + 1
    
    # 4. Aggregate
    # Group by date and target_hour, sum the values
    agg_df = df.groupby(['dt_date', 'target_hour'])['cerc_logger_1'].sum().reset_index()
    
    # 5. Pivot
    # Index: dt_date, Columns: target_hour, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='dt_date', columns='target_hour', values='cerc_logger_1')
    
    # Fill NaNs with 0 (if some hours have no data)
    pivot_df = pivot_df.fillna(0)
    
    # 6. Rename columns to match target format '1:00', '2:00', ... '24:00'
    pivot_df.columns = [f"{int(col)}:00" for col in pivot_df.columns]
    
    # 7. Format the date index into the 'cst' column
    # Target format: '%a %m/%d/%Y' (e.g., 'Sat 07/20/2019')
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%a %m/%d/%Y')
    
    # Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'cst'})
    
    # 8. Define target columns
    target_columns = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Ensure all target columns exist (some might be missing if no data for that hour ever)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    return result_df