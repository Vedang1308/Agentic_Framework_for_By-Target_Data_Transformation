import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source time-series data (10-min intervals) into daily hourly aggregated data.
    """
    df = source.copy()
    
    # 1. Parse the date column
    # Format is '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour components
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map pandas hour (0-23) to target hour index (1-24)
    # Hypothesis: 1:00 corresponds to hour 0 (00:00-00:59), ..., 24:00 corresponds to hour 23 (23:00-23:59)
    df['target_hour'] = df['hour'] + 1
    
    # 4. Aggregate by date and target hour
    # Sum the values. Based on sample analysis, summing ~6 readings of ~24 gives ~144, matching target magnitude.
    agg_df = df.groupby(['date_only', 'target_hour'])['cerc_logger_1'].sum().reset_index()
    
    # 5. Pivot the data to wide format
    # Index: date_only, Columns: target_hour, Values: cerc_logger_1
    pivot_df = agg_df.pivot_table(index='date_only', columns='target_hour', values='cerc_logger_1', fill_value=0)
    
    # 6. Ensure all 24 hours are present in columns
    # Create a complete range of hours 1-24
    all_hours = range(1, 25)
    pivot_df = pivot_df.reindex(columns=all_hours, fill_value=0)
    
    # 7. Format the date column for 'cst'
    # Convert date_only back to datetime for formatting, then to string
    # Note: date_only is a date object. We can format it directly or convert to datetime.
    # pd.to_datetime on a date object works.
    pivot_df['cst'] = pd.to_datetime(pivot_df.index).dt.strftime('%a %m/%d/%Y')
    
    # 8. Reset index to make 'date_only' a column (though we replaced it with 'cst')
    pivot_df = pivot_df.reset_index(drop=True)
    
    # 9. Rename hour columns to match target verbatim: '1:00', '2:00', ...
    rename_dict = {h: f'{h}:00' for h in all_hours}
    pivot_df = pivot_df.rename(columns=rename_dict)
    
    # 10. Define target columns and select them
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # Ensure the order is correct
    result_df = pivot_df[target_columns]
    
    return result_df