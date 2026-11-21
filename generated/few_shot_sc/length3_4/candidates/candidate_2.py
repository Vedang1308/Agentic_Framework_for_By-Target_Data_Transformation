import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for the index/column
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names (Hour 1 to Hour 24)
    # Source hour 0 (midnight) -> Target "Hour 1"
    # Source hour 23 (11pm) -> Target "Hour 24"
    df['hour_label'] = 'Hour ' + (df['datetime'].dt.hour + 1).astype(str)
    
    # 4. Pivot the data
    # Index: date_str
    # Columns: hour_label
    # Values: zone_016_cooling_sp
    # Aggfunc: mean (handles multiple 5-min intervals per hour)
    pivoted = df.pivot_table(
        index='date_str',
        columns='hour_label',
        values='zone_016_cooling_sp',
        aggfunc='mean'
    )
    
    # 5. Reset index to make date_str a column
    pivoted = pivoted.reset_index()
    
    # 6. Rename the date column to match target schema
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 7. Define the exact target columns in order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 8. Ensure all hour columns exist (even if empty/NaN) and reorder
    # The pivot_table creates columns only for hours present in data.
    # We need to ensure columns 1-24 exist.
    for col in target_columns[1:]:
        if col not in pivoted.columns:
            pivoted[col] = pd.NA
            
    # 9. Select and return the target columns
    return pivoted[target_columns]