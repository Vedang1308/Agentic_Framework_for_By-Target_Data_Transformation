import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour for grouping
    df['cal_date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Group by date and hour, summing the zone_016 values
    # We dropna=False to ensure groups with all NaNs are not silently dropped if we wanted to preserve structure,
    # but typically sum ignores NaN. We will fillna(0) after pivot.
    aggregated = df.groupby(['cal_date', 'hour'], as_index=False)['zone_016'].sum()
    
    # 4. Pivot the table
    # Index: cal_date, Columns: hour, Values: zone_016
    pivoted = aggregated.pivot_table(index='cal_date', columns='hour', values='zone_016', fill_value=0)
    
    # 5. Ensure all hours 0-23 are present and sort them
    # Reindex columns to 0-23, filling missing with 0
    pivoted = pivoted.reindex(columns=range(0, 24), fill_value=0)
    
    # 6. Rename columns to match target format: 0 -> '24:00', 1..23 -> '1:00'..'23:00'
    col_rename_map = {0: '24:00'}
    for h in range(1, 24):
        col_rename_map[h] = f'{h}:00'
    
    pivoted.rename(columns=col_rename_map, inplace=True)
    
    # 7. Format the index (date) into 'cst' column
    # Convert index to datetime again for formatting
    pivoted.index = pd.to_datetime(pivoted.index)
    pivoted['cst'] = pivoted.index.strftime('%a %m/%d/%Y')
    
    # 8. Reset index to make 'cst' a column and remove the old index name
    pivoted.reset_index(drop=True, inplace=True)
    
    # 9. Define target columns in the exact order required
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 24)] + ['24:00']
    
    # 10. Select and return
    return pivoted[target_cols]