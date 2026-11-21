import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with high-frequency time series data 
    into a daily aggregated DataFrame with hourly columns.
    """
    # 1. Parse the date column
    # The format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour components
    # We need to group by day
    df['date_only'] = df['datetime'].dt.date
    
    # Map hours to 1-24 format where 0 (midnight) becomes 24
    # 1:00 -> 1, ..., 23:00 -> 23, 00:00 -> 24
    df['hour'] = df['datetime'].dt.hour
    df['hour'] = df['hour'].apply(lambda h: 24 if h == 0 else h)
    
    # 3. Aggregate by date and hour
    # The sample shows source value 73 and target value 876.
    # 876 / 73 = 12. There are 12 five-minute intervals in an hour.
    # This implies a SUM aggregation.
    agg_df = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 4. Pivot the data
    # Rows: date_only, Columns: hour, Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016_cooling_sp')
    
    # 5. Format the columns to match target verbatim (e.g., '1:00', '2:00', ..., '24:00')
    # Ensure all 24 hours are present in the correct order
    all_hours = list(range(1, 25))
    pivot_df = pivot_df.reindex(columns=all_hours, fill_value=0) # Fill missing hours with 0 if any
    
    # Rename columns to string format "H:00"
    pivot_df.columns = [f"{h}:00" for h in pivot_df.columns]
    
    # 6. Format the date column 'cst'
    # Reset index to bring date_only back as a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'cst'})
    
    # Convert 'cst' to datetime for formatting, then to string
    # Note: 'cst' is currently a date object or datetime depending on pivot. 
    # pd.to_datetime handles date objects.
    pivot_df['cst'] = pd.to_datetime(pivot_df['cst']).dt.strftime('%a %m/%d/%Y')
    
    # 7. Define target columns and reorder
    target_columns = [
        'cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', 
        '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', 
        '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'
    ]
    
    # Ensure only target columns are returned
    result_df = pivot_df[target_columns]
    
    return result_df