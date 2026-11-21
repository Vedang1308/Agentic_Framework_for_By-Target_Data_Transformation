import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    # dt_strata: MM/DD/YY
    dt_strata = dt.dt.strftime('%m/%d/%y')
    
    # dow: Sunday=0, Monday=1, ..., Saturday=6
    # pandas dayofweek: Monday=0, ..., Sunday=6
    # Formula: (dayofweek + 1) % 7
    dow = (dt.dt.dayofweek + 1) % 7
    
    # hour: 0-23
    hour = dt.dt.hour
    
    # 3. Map hour to target column names
    # Hour 0 -> pct_hourly_0100
    # Hour 1 -> pct_hourly_0200
    # ...
    # Hour 23 -> pct_hourly_2400
    # We will create a column name string for each row
    hour_idx = hour + 1
    hour_col_name = 'pct_hourly_' + hour_idx.astype(str).str.zfill(4)
    
    # 4. Prepare data for grouping
    # We need to group by date (to get dt_strata and dow) and hour_col_name
    # To preserve the date for dt_strata and dow, we can group by the datetime object itself or dt_strata
    # Since dt_strata is unique per day in this context, we can group by dt_strata and hour_col_name
    
    df_work = pd.DataFrame({
        'dt_strata': dt_strata,
        'dow': dow,
        'hour_col': hour_col_name,
        'value': source['zone_016_cooling_sp']
    })
    
    # 5. Aggregate
    # Group by dt_strata and hour_col, sum the values
    agg_df = df_work.groupby(['dt_strata', 'hour_col'], as_index=False)['value'].sum()
    
    # 6. Pivot
    # Pivot so that hour_col becomes columns
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour_col', values='value')
    
    # 7. Reset index to make dt_strata a column
    pivot_df.reset_index(inplace=True)
    
    # 8. Get dow for each dt_strata
    # We can compute dow from dt_strata or just join it back
    # Since dt_strata is MM/DD/YY, we can parse it back to get dow, or just use the original grouping
    # Let's create a mapping from dt_strata to dow from the original data
    dow_map = df_work.drop_duplicates(subset=['dt_strata'])[['dt_strata', 'dow']].set_index('dt_strata')['dow']
    pivot_df['dow'] = pivot_df['dt_strata'].map(dow_map)
    
    # 9. Ensure all target columns exist
    target_hour_cols = [f'pct_hourly_{h:04d}' for h in range(1, 26)] # 0100 to 2500
    
    # Fill missing columns with 0
    for col in target_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 10. Select and order columns
    target_columns = ['dt_strata', 'dow'] + target_hour_cols
    
    # Reorder columns
    pivot_df = pivot_df[target_columns]
    
    # 11. Convert types
    pivot_df['dow'] = pivot_df['dow'].astype('int64')
    for col in target_hour_cols:
        pivot_df[col] = pivot_df[col].astype('int64')
        
    # 12. Sort? The sample is not strictly sorted by date, but let's keep the order of appearance or sort by date?
    # The sample target seems to be in reverse chronological order or random.
    # Usually, deterministic output requires sorting. Let's sort by dt_strata descending or just return as is.
    # Given the sample isn't strictly sorted, we might just return the grouped result.
    # However, to be safe and deterministic, let's sort by dt_strata descending (as sample seems to have newer dates first? 10/25, 10/18, 10/05... no, 10/25, 10/18, 10/05, 10/15, 10/14... it's not sorted).
    # Let's just return the dataframe. The groupby might preserve order of first appearance.
    
    return pivot_df