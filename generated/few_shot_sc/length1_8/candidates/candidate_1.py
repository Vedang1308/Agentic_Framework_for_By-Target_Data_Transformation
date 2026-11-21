import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source time-series data (10-min intervals) into daily hourly aggregated data.
    Source: date, cerc_logger_1
    Target: cst, 1:00...24:00
    """
    df = source.copy()
    
    # 1. Parse datetime
    # Source format: '%m/%d/%Y %H:%M'
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract grouping keys
    # Group by Calendar Date
    df['date_key'] = df['dt'].dt.date
    
    # Extract Hour (0-23) and map to Target Hour Index (1-24)
    # Hour 0 (00:00-00:59) -> 1:00
    # Hour 1 (01:00-01:59) -> 2:00
    # ...
    # Hour 23 (23:00-23:59) -> 24:00
    df['hour_idx'] = df['dt'].dt.hour + 1
    
    # 3. Aggregate
    # Based on value magnitude analysis (Input ~24, Output ~130-140), 
    # and 6 intervals per hour, Sum is the likely aggregation.
    df_agg = df.groupby(['date_key', 'hour_idx'])['cerc_logger_1'].sum().reset_index()
    
    # 4. Pivot to wide format
    # Create a pivot table with date_key as index, hour_idx as columns
    df_pivot = df_agg.pivot_table(index='date_key', columns='hour_idx', values='cerc_logger_1', aggfunc='sum')
    
    # Fill missing hours with 0 (as seen in target sample for 02/16/2019)
    df_pivot = df_pivot.fillna(0)
    
    # 5. Format Columns
    # Ensure all 24 hours are present and named correctly
    expected_hours = list(range(1, 25))
    df_pivot = df_pivot.reindex(columns=expected_hours, fill_value=0)
    
    # Rename columns to '1:00', '2:00', ..., '24:00'
    rename_dict = {h: f'{h}:00' for h in expected_hours}
    df_pivot = df_pivot.rename(columns=rename_dict)
    
    # 6. Format Index into 'cst' column
    # Convert date_key back to datetime for formatting, then to string
    df_pivot = df_pivot.reset_index()
    # date_key is a date object, convert to datetime to use strftime
    df_pivot['cst'] = pd.to_datetime(df_pivot['date_key']).dt.strftime('%a %m/%d/%Y')
    
    # 7. Select and Order Columns
    target_cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    df_result = df_pivot[target_cols]
    
    # Sort by date if necessary? The target sample isn't strictly sorted by date in the display 
    # (Sat 07/20, Sun 05/13, Sat 11/24...), but typically we preserve order or sort by date.
    # Given the source is likely chronological, we might want to keep that or sort by date.
    # Let's sort by the cst column to ensure deterministic output if order isn't preserved.
    # However, looking at the target sample, it seems random or grouped by something else?
    # Actually, standard practice is to return in the order of the index (date).
    # Let's sort by the date component to be safe and deterministic.
    df_result['sort_date'] = pd.to_datetime(df_result['cst'].str.split(' ').str[-1], format='%m/%d/%Y')
    df_result = df_result.sort_values('sort_date').reset_index(drop=True)
    df_result = df_result.drop(columns=['sort_date'])
    
    return df_result