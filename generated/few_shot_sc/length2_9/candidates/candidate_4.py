import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour components
    df['date_only'] = df['dt'].dt.normalize()
    df['hour'] = df['dt'].dt.hour
    
    # 3. Aggregate: Sum zone_016 for each date and hour
    # We dropna on zone_016 before summing to ignore NaNs
    agg_df = df.groupby(['date_only', 'hour'])['zone_016'].sum().reset_index()
    
    # 4. Pivot the data to get hours as columns
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016')
    
    # 5. Rename columns to match target schema
    # Mapping: Hour 0 -> 2400, Hour 1 -> 0100, ..., Hour 23 -> 2300
    col_map = {}
    for h in range(24):
        if h == 0:
            col_map[h] = 'pct_hourly_2400'
        else:
            col_map[h] = f'pct_hourly_{h:02d}00'
    
    pivot_df = pivot_df.rename(columns=col_map)
    
    # 6. Ensure all expected hour columns exist, filling missing ones with 0
    expected_hours = [f'pct_hourly_{i:02d}00' for i in range(1, 24)] + ['pct_hourly_2400']
    for col in expected_hours:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 7. Create dt_strata and dow
    # dt_strata format: MM/DD/YY
    pivot_df['dt_strata'] = pivot_df.index.strftime('%m/%d/%y')
    
    # dow: Monday=1, ..., Sunday=7
    pivot_df['dow'] = pivot_df.index.dayofweek + 1
    
    # 8. Add pct_hourly_2500 = 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 9. Select and order columns
    target_columns = ['dt_strata', 'dow'] + expected_hours + ['pct_hourly_2500']
    
    # 10. Sort by date descending to match sample order (01/02 before 01/01)
    pivot_df = pivot_df.sort_values(by='dt_strata', ascending=False)
    
    # 11. Reset index to clean up
    pivot_df = pivot_df.reset_index(drop=True)
    
    return pivot_df[target_columns]