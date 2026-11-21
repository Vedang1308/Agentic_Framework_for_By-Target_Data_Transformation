import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source time-series dataframe into a daily aggregated wide-format dataframe.
    """
    # 1. Parse the date column into datetime objects
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date string in the target format (%m/%d/%Y)
    source['date_str'] = source['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour (0-23)
    source['hour'] = source['datetime'].dt.hour
    
    # 4. Define mapping from hour integer to target column name
    hour_to_col = {
        0: '12:00 AM',
        1: '1:00 AM',
        2: '2:00 AM',
        3: '3:00 AM',
        4: '4:00 AM',
        5: '5:00 AM',
        6: '6:00 AM',
        7: '7:00 AM',
        8: '8:00 AM',
        9: '9:00 AM',
        10: '10:00 AM',
        11: '11:00 AM',
        12: '12:00 PM',
        13: '1:00 PM',
        14: '2:00 PM',
        15: '3:00 PM',
        16: '4:00 PM',
        17: '5:00 PM',
        18: '6:00 PM',
        19: '7:00 PM',
        20: '8:00 PM',
        21: '9:00 PM',
        22: '10:00 PM',
        23: '11:00 PM'
    }
    
    # 5. Map hours to column names
    source['hour_label'] = source['hour'].map(hour_to_col)
    
    # 6. Group by date and hour_label, calculate mean of cerc_logger_1
    # This aggregates the 10-minute intervals into hourly averages
    grouped = source.groupby(['date_str', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 7. Pivot the table to wide format
    df_pivot = grouped.pivot(index='date_str', columns='hour_label', values='cerc_logger_1')
    
    # 8. Reset index to make date_str a column again
    df_pivot = df_pivot.reset_index()
    
    # 9. Rename the date column to 'date'
    df_pivot = df_pivot.rename(columns={'date_str': 'date'})
    
    # 10. Define the exact target column order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 11. Ensure all target columns exist (fill NaN if a day/hour combo is missing)
    for col in target_columns:
        if col != 'date' and col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # 12. Select and reorder columns to match target verbatim
    df_result = df_pivot[target_columns]
    
    # 13. Ensure numeric columns are float64
    numeric_cols = [col for col in target_columns if col != 'date']
    for col in numeric_cols:
        df_result[col] = df_result[col].astype(float)
        
    return df_result