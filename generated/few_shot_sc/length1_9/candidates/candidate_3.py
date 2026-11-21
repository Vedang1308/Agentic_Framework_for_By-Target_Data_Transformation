import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create the 'cst' column with format '%a %m/%d/%Y'
    df['cst'] = df['dt'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Map the source hour to the target column name
    # Logic derived from sample:
    # Source Hour 0 (0:00-0:59) -> Target Column '24:00'
    # Source Hour 1 (1:00-1:59) -> Target Column '1:00'
    # ...
    # Source Hour 23 (23:00-23:59) -> Target Column '23:00'
    def map_hour(hour):
        if hour == 0:
            return '24:00'
        else:
            return f'{hour}:00'
            
    df['hour_col'] = df['dt'].dt.hour.apply(map_hour)
    
    # 4. Aggregate by day ('cst') and mapped hour ('hour_col')
    # Summing the zone_016 values (likely minute-level to hour-level aggregation)
    grouped = df.groupby(['cst', 'hour_col'])['zone_016'].sum().reset_index()
    
    # 5. Pivot the table to have hours as columns
    pivoted = grouped.pivot(index='cst', columns='hour_col', values='zone_016')
    
    # 6. Ensure all expected hour columns exist and fill missing with 0
    target_hours = [f'{i}:00' for i in range(1, 25)]
    for col in target_hours:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # Fill any remaining NaNs with 0 (for days/hours with no data)
    pivoted = pivoted.fillna(0)
    
    # 7. Reset index to make 'cst' a column
    pivoted = pivoted.reset_index()
    
    # 8. Select and order the columns verbatim
    target_columns = ['cst'] + target_hours
    return pivoted[target_columns]