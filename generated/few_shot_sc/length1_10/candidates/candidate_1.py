import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create the target date string column 'cst'
    # Format: '%a %m/%d/%Y' e.g., 'Sun 09/30/2018'
    df['cst'] = df['dt'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Determine the target hour column
    # Source hours are 0-23. Target columns are 1:00 to 24:00.
    # Mapping: Hour 0 -> '1:00', Hour 1 -> '2:00', ..., Hour 23 -> '24:00'
    # This corresponds to Hour_Index = dt.hour + 1
    df['hour_idx'] = df['dt'].dt.hour + 1
    df['hour_col'] = df['hour_idx'].apply(lambda h: f'{h}:00')
    
    # 4. Group by 'cst' and pivot/aggregate
    # We group by the date string and the hour column, then aggregate the value
    # Since there are multiple records per hour (5-min intervals), we take the mean
    grouped = df.groupby(['cst', 'hour_col'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: 'cst', Columns: 'hour_col', Values: 'zone_016_cooling_sp'
    pivoted = grouped.pivot(index='cst', columns='hour_col', values='zone_016_cooling_sp')
    
    # 6. Clean up column names and index
    pivoted.columns.name = None
    pivoted = pivoted.reset_index()
    
    # 7. Ensure all 24 columns are present, filling missing with NaN
    target_hours = [f'{i}:00' for i in range(1, 25)]
    for col in target_hours:
        if col not in pivoted.columns:
            pivoted[col] = pd.NA
            
    # 8. Select and order columns verbatim
    target_columns = ['cst'] + target_hours
    result = pivoted[target_columns]
    
    return result