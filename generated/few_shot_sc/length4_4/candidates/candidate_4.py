import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Identify numeric columns (hours 1-24)
    numeric_cols = [str(i) for i in range(1, 25)]
    
    # Group by Date and aggregate. 
    # Using mean as the aggregation function for the hourly values.
    # We drop 'Class' as it's not in the target.
    agg_dict = {col: 'mean' for col in numeric_cols}
    
    # Perform groupby and aggregation
    df_agg = df.groupby('Date', as_index=False)[numeric_cols].agg(agg_dict)
    
    # Format the Date column
    df_agg['date'] = pd.to_datetime(df_agg['Date']).dt.strftime('%m/%d/%Y')
    
    # Define the target column names for the hours in the exact order provided
    target_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Map source columns (1-24) to target column names
    rename_dict = {str(i): target_hour_cols[i-1] for i in range(1, 25)}
    
    # Rename the numeric columns
    df_agg = df_agg.rename(columns=rename_dict)
    
    # Define the final target columns
    target_columns = ['date'] + target_hour_cols
    
    # Return the dataframe with the correct columns
    return df_agg[target_columns]