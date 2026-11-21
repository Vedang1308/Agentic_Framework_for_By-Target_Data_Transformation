import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid SettingWithCopyWarning
    df = source.copy()
    
    # Parse the datetime column. 
    # The format is MM/DD/YYYY H:MM or MM/DD/YYYY HH:MM. 
    # pd.to_datetime handles this inference well.
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract the date as string in the target format: MM/DD/YYYY
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract the hour of the day (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to the target column names: value1 (hour 0) ... value24 (hour 23)
    df['value_col'] = 'value' + (df['hour'] + 1).astype(str)
    
    # Group by date and the new value column, then aggregate.
    # Mean is the standard aggregation for sensor readings over a time bin.
    agg = df.groupby(['date', 'value_col'])['cerc_logger_1'].mean()
    
    # Unstack to create wide format with hours as columns
    wide_df = agg.unstack()
    
    # Reset index to bring 'date' back as a column
    wide_df = wide_df.reset_index()
    
    # Define the exact target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Ensure all 24 value columns exist in the dataframe
    # If a day/hour combination had no data, that column might be missing or NaN
    for col in target_columns:
        if col != 'date' and col not in wide_df.columns:
            wide_df[col] = np.nan
            
    # Select and order the columns exactly as required
    result_df = wide_df[target_columns]
    
    # Ensure numeric columns are float64
    for col in result_df.columns:
        if col != 'date':
            result_df[col] = result_df[col].astype(float)
            
    return result_df