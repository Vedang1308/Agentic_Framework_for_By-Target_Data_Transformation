import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from wide format with time-based columns
    to a target DataFrame with standardized 'value1'...'value24' columns
    and formatted dates.
    """
    
    # Define the chronological order of the source time columns
    # value1 corresponds to 12:00 AM (Midnight), value2 to 1:00 AM, etc.
    chronological_columns = [
        '12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM',
        '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM',
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'
    ]
    
    # Define the target column names for the values
    target_value_columns = [f'value{i}' for i in range(1, 25)]
    
    # Create a mapping from source time columns to target value columns
    col_map = dict(zip(chronological_columns, target_value_columns))
    
    # Select the date column and the time columns in chronological order
    # Ensure we only pick columns that exist in source to avoid KeyError
    existing_time_cols = [col for col in chronological_columns if col in source.columns]
    
    # Create the new DataFrame with selected and reordered columns
    df = source[['date'] + existing_time_cols].copy()
    
    # Rename the time columns to value1...value24
    df.rename(columns=col_map, inplace=True)
    
    # Parse the date column from 'M/D/YYYY' format
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Format the date column to '%Y-%m-%d %H:%M:%S' as a string
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the final target columns
    target_columns = ['date'] + target_value_columns
    
    # Return the DataFrame with the exact target schema
    return df[target_columns]