import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse 'date' column.
    2. Extract 'dt_strata' (MM/DD/YY), 'dow' (1=Mon, 7=Sun), and 'hour'.
    3. Map hours to target column indices:
       - Hour 0 -> 'pct_hourly_2400'
       - Hour 1 -> 'pct_hourly_0100'
       - ...
       - Hour 23 -> 'pct_hourly_2300'
       - 'pct_hourly_2500' is always 0 (or unused).
    4. Aggregate 'zone_016' by summing for each date and hour bucket.
    5. Pivot and format to match target schema.
    """
    
    # 1. Parse Date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Features
    # dt_strata: MM/DD/YY
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # dow: 1=Monday, 7=Sunday. pandas dayofweek: 0=Monday, 6=Sunday.
    df['dow'] = df['datetime'].dt.dayofweek + 1
    
    # hour: 0-23
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Prepare for Aggregation
    # Fill NaNs with 0 for summing
    df['zone_016'] = df['zone_016'].fillna(0)
    
    # 4. Define Hour to Column Name Mapping
    # Based on analysis:
    # Hour 0 (12 AM) -> pct_hourly_2400
    # Hour 1 (1 AM)  -> pct_hourly_0100
    # ...
    # Hour 23 (11 PM) -> pct_hourly_2300
    hour_to_col = {}
    for h in range(24):
        if h == 0:
            col_name = 'pct_hourly_2400'
        else:
            col_name = f'pct_hourly_{h:02d}00'
        hour_to_col[h] = col_name
        
    # 5. Aggregate
    # Group by dt_strata and hour, sum zone_016
    agg_df = df.groupby(['dt_strata', 'hour'])['zone_016'].sum().reset_index()
    
    # 6. Pivot
    # We need to pivot so each hour is a column
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour', values='zone_016')
    
    # Rename columns based on mapping
    pivot_df.rename(columns=hour_to_col, inplace=True)
    
    # Ensure all target hourly columns exist, filling missing with 0
    target_hourly_cols = [
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400',
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800',
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200',
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600',
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000',
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400',
        'pct_hourly_2500'
    ]
    
    for col in target_hourly_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Add dow column
    # We need to map dt_strata back to dow. 
    # Since we grouped by dt_strata, we can get the dow from the original df 
    # by grouping by dt_strata and taking the first dow (since dow is constant for a date).
    dow_map = df.groupby('dt_strata')['dow'].first()
    pivot_df['dow'] = pivot_df['dt_strata'].map(dow_map)
    
    # 8. Select and Order Columns
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
    
    # Ensure dt_strata is string
    pivot_df['dt_strata'] = pivot_df['dt_strata'].astype(str)
    
    # Ensure dow is int
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    
    # Ensure hourly columns are float (except 2500 which is int in target schema, but let's check)
    # Target schema says pct_hourly_2500 is int64, others float64.
    for col in target_hourly_cols:
        if col == 'pct_hourly_2500':
            pivot_df[col] = pivot_df[col].astype(int)
        else:
            pivot_df[col] = pivot_df[col].astype(float)
            
    return pivot_df[target_columns]