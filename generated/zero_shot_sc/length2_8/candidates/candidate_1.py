import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by aggregating 
    hourly sensor readings into daily summaries.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    df['dow'] = df['datetime'].dt.dayofweek + 1  # 1-indexed: Mon=1, Sun=7
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate by date and hour
    # We group by dt_strata and hour. dow is dependent on dt_strata, so we can group by both 
    # or just dt_strata and then map dow later. Grouping by both ensures consistency.
    grouped = df.groupby(['dt_strata', 'dow', 'hour'])['cerc_logger_1'].sum().reset_index()
    
    # 4. Pivot the data to get hourly columns
    # Index: dt_strata, Columns: hour, Values: cerc_logger_1
    pivoted = grouped.pivot_table(index='dt_strata', columns='hour', values='cerc_logger_1', aggfunc='sum')
    
    # 5. Map hours to target column names
    # Target columns: pct_hourly_0100 to pct_hourly_2400, plus pct_hourly_2500
    # Mapping:
    # Hour 1 -> 0100
    # ...
    # Hour 23 -> 2300
    # Hour 0 -> 2400 (Midnight)
    
    col_mapping = {}
    for h in range(1, 24):
        col_mapping[h] = f'pct_hourly_{h:02d}00'
    col_mapping[0] = 'pct_hourly_2400'
    
    pivoted = pivoted.rename(columns=col_mapping)
    
    # 6. Ensure all expected hourly columns exist and fill missing with 0
    expected_hourly_cols = [f'pct_hourly_{h:02d}00' for h in range(1, 24)] + ['pct_hourly_2400']
    for col in expected_hourly_cols:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # 7. Add the constant 0 column for pct_hourly_2500
    pivoted['pct_hourly_2500'] = 0
    
    # 8. Reset index to make dt_strata a column
    pivoted = pivoted.reset_index()
    
    # 9. Merge dow back if it wasn't preserved in pivot (it was in the groupby, but pivot drops it from index)
    # Actually, since dow is functionally dependent on dt_strata, we can just re-derive it or keep it from the groupby.
    # The pivot table index is only dt_strata. We need to bring dow back.
    # Let's get unique dt_strata and dow mapping from the grouped data
    dow_map = grouped[['dt_strata', 'dow']].drop_duplicates().set_index('dt_strata')['dow']
    pivoted['dow'] = pivoted['dt_strata'].map(dow_map)
    
    # 10. Define the final column order
    target_columns = [
        'dt_strata', 'dow',
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400',
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800',
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200',
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600',
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000',
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400',
        'pct_hourly_2500'
    ]
    
    # 11. Select and order columns
    result = pivoted[target_columns]
    
    # 12. Fill any remaining NaNs with 0
    result = result.fillna(0)
    
    # 13. Ensure correct data types
    result['dow'] = result['dow'].astype('int64')
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    # Convert hourly columns to float64
    for col in result.columns:
        if col.startswith('pct_hourly_'):
            if col != 'pct_hourly_2500':
                result[col] = result[col].astype('float64')
                
    return result[target_columns]