import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with minute-level time series data 
    into a daily aggregated DataFrame with 24 hourly columns.
    """
    # 1. Parse the date column to datetime
    df = source.copy()
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract the calendar date and the hour of the day
    # We use the date part for grouping and the hour for pivoting
    df['date_key'] = df['date_dt'].dt.date
    df['hour'] = df['date_dt'].dt.hour
    
    # 3. Group by date and hour, and aggregate the values
    # We use mean to aggregate multiple minutes within the same hour
    # If there's only one minute, mean returns that value.
    # If there are NaNs, mean ignores them (unless all are NaN)
    grouped = df.groupby(['date_key', 'hour'])['zone_016'].mean()
    
    # 4. Unstack the hour level to create columns for each hour (0-23)
    # This creates a DataFrame with index=date_key and columns=0..23
    pivoted = grouped.unstack('hour')
    
    # 5. Rename the columns to match the target schema: value1...value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    pivoted.columns = [f'value{i+1}' for i in pivoted.columns]
    
    # 6. Reset index to make 'date_key' a column
    pivoted = pivoted.reset_index()
    
    # 7. Format the date column to MM/DD/YYYY
    # The date_key is a Python date object, we convert to string
    pivoted['date'] = pivoted['date_key'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Drop the temporary date_key column
    pivoted = pivoted.drop(columns=['date_key'])
    
    # 9. Define the target columns in the correct order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Ensure all target columns exist (in case some hours are missing entirely in the dataset)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # 11. Sort by date to ensure deterministic output order (optional but good practice)
    pivoted = pivoted.sort_values('date').reset_index(drop=True)
    
    # 12. Return the DataFrame with the exact target columns
    return pivoted[target_columns]