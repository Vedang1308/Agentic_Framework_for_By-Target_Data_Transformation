import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by pivoting hourly
    aggregated cooling setpoints into a wide format.
    
    Steps:
    1. Parse the 'date' column into datetime.
    2. Extract the date string in '%a %m/%d/%Y' format for the 'cst' column.
    3. Extract the hour from the datetime. Map hour 0 to 24 to match target column '24:00'.
    4. Group by 'cst' and the mapped hour.
    5. Sum the 'zone_016_cooling_sp' values for each group.
    6. Pivot the data so that each hour is a column.
    7. Ensure all target columns (1:00 to 24:00) are present, filling missing with 0.
    8. Return the DataFrame with the exact target column names.
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse date
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Format cst column: '%a %m/%d/%Y'
    df['cst'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Extract hour and map 0 -> 24
    df['hour_raw'] = df['datetime'].dt.hour
    df['hour_mapped'] = df['hour_raw'].replace({0: 24})
    
    # 4. Create column name string for pivot
    df['col_name'] = df['hour_mapped'].astype(str) + ':00'
    
    # 5. Group by cst and col_name, and sum the values
    # Based on analysis: 73 * 12 intervals = 876. Sum is the correct aggregation.
    grouped = df.groupby(['cst', 'col_name'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 6. Pivot the table
    pivot = grouped.pivot(index='cst', columns='col_name', values='zone_016_cooling_sp')
    
    # Clean up column names and index
    pivot.columns.name = None
    pivot = pivot.reset_index()
    
    # 7. Define target columns verbatim
    target_columns = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Reindex to ensure all columns are present and in correct order
    # Fill NaNs with 0 if a specific hour is missing for a day
    pivot = pivot.reindex(columns=target_columns).fillna(0)
    
    return pivot