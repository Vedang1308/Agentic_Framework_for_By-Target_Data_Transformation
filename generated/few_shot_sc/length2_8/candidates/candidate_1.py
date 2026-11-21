import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse Date
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create Target Date Column (MM/DD/YY)
    df['dt_strata'] = df['dt'].dt.strftime('%m/%d/%y')
    
    # 3. Create Day of Week Column (1=Mon, ..., 7=Sun)
    df['dow'] = df['dt'].dt.dayofweek + 1
    
    # 4. Map Hour to 1-24 scale
    # Hour 0 (Midnight) -> 24
    # Hour 1-23 -> 1-23
    df['target_hour'] = df['dt'].dt.hour
    df.loc[df['target_hour'] == 0, 'target_hour'] = 24
    
    # 5. Group by Date and Target Hour, Sum the values
    # We group by dt_strata and target_hour to aggregate the high-frequency data
    grouped = df.groupby(['dt_strata', 'target_hour'])['cerc_logger_1'].sum().reset_index()
    
    # 6. Pivot to create hourly columns
    pivot_df = grouped.pivot(index='dt_strata', columns='target_hour', values='cerc_logger_1')
    
    # 7. Ensure all hours 1-24 are present and fill NaN with 0
    all_hours = list(range(1, 25))
    pivot_df = pivot_df.reindex(columns=all_hours, fill_value=0)
    
    # 8. Rename columns to pct_hourly_HH00 format
    rename_dict = {h: f'pct_hourly_{h:02d}00' for h in all_hours}
    pivot_df = pivot_df.rename(columns=rename_dict)
    
    # 9. Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 10. Add the dummy column pct_hourly_2500
    pivot_df['pct_hourly_2500'] = 0
    
    # 11. We need 'dow' column. Since 'dow' is determined by 'dt_strata', 
    # we can compute it from 'dt_strata' or merge it. 
    # Computing from dt_strata is safer as we have the string.
    # Parse dt_strata back to datetime to get dow
    dt_parsed = pd.to_datetime(pivot_df['dt_strata'], format='%m/%d/%y')
    pivot_df['dow'] = dt_parsed.dt.dayofweek + 1
    
    # 12. Select and order columns
    target_cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 25)] + ['pct_hourly_2500']
    
    # 13. Sort by dt_strata to ensure deterministic output (optional but good practice)
    pivot_df = pivot_df.sort_values('dt_strata').reset_index(drop=True)
    
    return pivot_df[target_cols]