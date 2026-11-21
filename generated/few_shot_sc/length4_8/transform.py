import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # Source format: '7/28/2019 4:50' -> %m/%d/%Y %H:%M
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    # If the above fails due to AM/PM ambiguity in parsing, try standard 24h format if possible, 
    # but the sample '4:50' usually implies 24h or ambiguous. 
    # Let's look at sample: '7/28/2019 4:50'. 
    # pd.to_datetime is flexible. Let's try generic parsing first.
    if df['datetime'].isna().all():
        df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M', errors='coerce')
        
    # 2. Extract calendar date for grouping and final output
    df['cal_date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Map hour to target column names
    # 0 -> 12:00 AM
    # 1-11 -> 1:00 AM - 11:00 AM
    # 12 -> 12:00 PM
    # 13-23 -> 1:00 PM - 11:00 PM
    
    def map_hour_to_label(h):
        if pd.isna(h):
            return np.nan
        h = int(h)
        if h == 0:
            return '12:00 AM'
        elif h == 12:
            return '12:00 PM'
        elif 1 <= h < 12:
            return f'{h}:00 AM'
        elif 13 <= h < 24:
            return f'{h-12}:00 PM'
        return np.nan

    df['hour_label'] = df['hour'].apply(map_hour_to_label)
    
    # 5. Group by calendar date and hour label, then aggregate (mean)
    # We drop rows where datetime parsing failed or hour is invalid
    df_valid = df.dropna(subset=['cal_date', 'hour_label'])
    
    grouped = df_valid.groupby(['cal_date', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 6. Pivot to wide format
    df_pivot = grouped.pivot(index='cal_date', columns='hour_label', values='cerc_logger_1').reset_index()
    
    # 7. Define target columns
    target_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Rename the index column 'cal_date' to 'date'
    df_pivot = df_pivot.rename(columns={'cal_date': 'date'})
    
    # Ensure all target columns exist, filling missing ones with NaN
    for col in target_hour_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # 8. Select and order columns verbatim
    target_columns = ['date'] + target_hour_cols
    
    return df_pivot[target_columns]