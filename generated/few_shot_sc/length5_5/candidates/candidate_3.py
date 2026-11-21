import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with minute-level sensor data into a daily
    DataFrame with 24 columns representing the average value for each hour of the day.
    """
    df = source.copy()
    
    # 1. Parse the date column to datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract the date string in the target format '%m/%d/%Y'
    df['target_date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Determine the hour bucket (1-24)
    # Hour 0 (00:xx) -> value1
    # Hour 1 (01:xx) -> value2
    # ...
    # Hour 23 (23:xx) -> value24
    df['hour_bucket'] = df['dt'].dt.hour + 1
    
    # 4. Aggregate data by date and hour bucket
    # We use 'mean' to aggregate the sensor values for each hour.
    # If no data exists for an hour, it will result in NaN.
    pivot_df = df.pivot_table(
        index='target_date',
        columns='hour_bucket',
        values='zone_016_cooling_sp',
        aggfunc='mean'
    )
    
    # 5. Rename columns to match target schema: 1 -> value1, ..., 24 -> value24
    pivot_df.columns = [f'value{int(col)}' for col in pivot_df.columns]
    
    # 6. Reset index to make 'target_date' a regular column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'target_date': 'date'}, inplace=True)
    
    # 7. Define the target columns in the correct order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 8. Ensure all target columns exist (some hours might be missing if no data for that hour in entire dataset, though unlikely for 24h)
    # If some value columns are missing because no data ever existed for that hour in the source, 
    # we should add them as NaN to maintain schema consistency.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # 9. Select and return the final dataframe
    return pivot_df[target_columns]