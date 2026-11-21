import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date for grouping and hour for bucketing
    df['date_key'] = df['datetime'].dt.date
    df['hour_num'] = df['datetime'].dt.hour
    
    # 3. Map 0-23 hours to 1:00-24:00 labels
    # Hour 0 (midnight) -> 1:00
    # Hour 23 (11pm) -> 24:00
    df['hour_label'] = (df['hour_num'] + 1).astype(str) + ':00'
    
    # 4. Group by date and hour, aggregate using mean
    # We assume mean is the appropriate aggregation for sensor data like this
    grouped = df.groupby(['date_key', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot to get one row per date with hourly columns
    df_pivot = grouped.pivot(index='date_key', columns='hour_label', values='cerc_logger_1').reset_index()
    
    # 6. Fill missing hours with 0 (based on the all-zero row in the sample)
    # Reindex to ensure all 24 columns exist
    target_hours = [f'{h}:00' for h in range(1, 25)]
    df_pivot = df_pivot.reindex(columns=['date_key'] + target_hours, fill_value=0)
    
    # 7. Format the date column 'cst' as '%a %m/%d/%Y'
    # Convert date_key (which is a date object) back to datetime for formatting, or use strftime on date
    # date objects support strftime
    df_pivot['cst'] = df_pivot['date_key'].apply(lambda x: x.strftime('%a %m/%d/%Y'))
    
    # 8. Select and order the final columns
    target_columns = ['cst'] + target_hours
    
    return df_pivot[target_columns]