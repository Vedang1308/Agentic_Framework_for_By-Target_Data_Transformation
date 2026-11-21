import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define the mapping from source 12-hour format columns to target 24-hour format columns
    column_mapping = {
        '1:00 AM': '1:00',
        '2:00 AM': '2:00',
        '3:00 AM': '3:00',
        '4:00 AM': '4:00',
        '5:00 AM': '5:00',
        '6:00 AM': '6:00',
        '7:00 AM': '7:00',
        '8:00 AM': '8:00',
        '9:00 AM': '9:00',
        '10:00 AM': '10:00',
        '11:00 AM': '11:00',
        '12:00 PM': '12:00',
        '1:00 PM': '13:00',
        '2:00 PM': '14:00',
        '3:00 PM': '15:00',
        '4:00 PM': '16:00',
        '5:00 PM': '17:00',
        '6:00 PM': '18:00',
        '7:00 PM': '19:00',
        '8:00 PM': '20:00',
        '9:00 PM': '21:00',
        '10:00 PM': '22:00',
        '11:00 PM': '23:00',
        '12:00 AM': '24:00'
    }
    
    # Rename the hourly columns
    df = source.rename(columns=column_mapping)
    
    # Drop the DSL column as it is not in the target
    if 'DSL' in df.columns:
        df = df.drop(columns=['DSL'])
        
    # Parse the date column and format it as required
    # Source format: '%m/%d/%Y'
    # Target format: '%a %m/%d/%Y' (e.g., 'Wed 01/01/2014')
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['cst'] = df['date'].dt.strftime('%a %m/%d/%Y')
    
    # Remove the original date column
    df = df.drop(columns=['date'])
    
    # Define the exact target column order
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', 
                      '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', 
                      '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
                      
    # Ensure all target columns exist and reorder
    # Note: The source might not have all columns if they are missing, but based on the schema they should be there.
    # We select the columns in the specific order required by the target.
    df = df[target_columns]
    
    return df