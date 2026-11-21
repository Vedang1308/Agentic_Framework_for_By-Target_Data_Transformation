import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the datetime column
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # 2. Extract Date string in format '%m/%d/%Y'
    df['Date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract Hour (0-23) and map to target column names 'Hr 1' to 'Hr 24'
    # Hour 0 -> 'Hr 1', Hour 1 -> 'Hr 2', ..., Hour 23 -> 'Hr 24'
    df['Hour_Col'] = df['parsed_date'].dt.hour + 1
    df['Hour_Col'] = df['Hour_Col'].apply(lambda h: f'Hr {h}')
    
    # 4. Group by Date and Hour_Col, aggregate zone_016
    # Using mean to handle multiple minute-records per hour
    aggregated = df.groupby(['Date', 'Hour_Col'])['zone_016'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: Date, Columns: Hour_Col, Values: zone_016
    df_wide = aggregated.pivot_table(index='Date', columns='Hour_Col', values='zone_016', aggfunc='mean')
    
    # 6. Ensure all expected hour columns exist (Hr 1 to Hr 24)
    expected_hours = [f'Hr {i}' for i in range(1, 25)]
    for col in expected_hours:
        if col not in df_wide.columns:
            df_wide[col] = float('nan')
            
    # 7. Reorder columns to match target schema exactly
    df_wide = df_wide[expected_hours]
    
    # 8. Reset index to make Date a column
    df_wide = df_wide.reset_index()
    
    # 9. Sort by Date descending to match the sample output order (01/02 before 01/01)
    # Note: String sorting of '%m/%d/%Y' works correctly for dates within the same year/month structure.
    df_wide = df_wide.sort_values('Date', ascending=False).reset_index(drop=True)
    
    # 10. Define target columns verbatim
    target_columns = ['Date'] + expected_hours
    
    return df_wide[target_columns]