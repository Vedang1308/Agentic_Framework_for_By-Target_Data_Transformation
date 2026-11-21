import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a daily hourly time-series table into a monthly hourly summary table.
    
    Steps:
    1. Parse dates to extract month.
    2. Melt the 24 hour columns into a long format.
    3. Convert hour strings (e.g., '1:00 AM') to 24-hour integers (0-23).
    4. Aggregate values by month and hour (mean).
    5. Pivot to have hours as rows and months as columns.
    6. Format and return.
    """
    
    # Define target column names
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Month name mapping
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # 1. Prepare the dataframe
    # Drop DSL as it's not needed
    df = source.drop(columns=['DSL'], errors='ignore')
    
    # 2. Parse Date to extract Month
    # Convert date string to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['month_num'] = df['date'].dt.month
    df['month_name'] = df['month_num'].map(month_map)
    
    # 3. Melt the hour columns
    # Identify hour columns (all columns except 'date', 'month_num', 'month_name')
    hour_cols = [col for col in df.columns if col not in ['date', 'month_num', 'month_name']]
    
    df_melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # 4. Convert hour_label to 24-hour integer
    def convert_hour_to_int(hour_label):
        # hour_label is like "1:00 AM"
        # Split by space to get time and period
        parts = hour_label.split()
        time_str = parts[0]
        period = parts[1]
        
        # Extract hour
        hour = int(time_str.split(':')[0])
        
        if period == 'AM':
            if hour == 12:
                return 0
            else:
                return hour
        else: # PM
            if hour == 12:
                return 12
            else:
                return hour + 12
                
    df_melted['hour'] = df_melted['hour_label'].apply(convert_hour_to_int)
    
    # 5. Aggregate by month and hour
    # Calculate mean for each month/hour combination
    aggregated = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    df_pivot = aggregated.pivot(index='hour', columns='month_name', values='value')
    
    # Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # Rename columns to match target exactly (ensure lowercase)
    # The pivot columns are already month names from our map
    df_pivot.columns.name = None # Clear the column axis name
    
    # Ensure all target month columns exist, even if NaN
    for col in target_columns[1:]: # Skip 'hour'
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # Sort by hour to ensure deterministic order
    df_pivot = df_pivot.sort_values(by='hour')
    
    # Select and return target columns
    return df_pivot[target_columns]