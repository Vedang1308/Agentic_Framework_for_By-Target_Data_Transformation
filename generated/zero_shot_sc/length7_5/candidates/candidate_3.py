import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Extract 'month' as the full month name.
    3. Determine 'daytype' ('weekday' or 'weekend') based on the day of the week.
    4. Rename the 24 hourly columns from their AM/PM format to hr1-hr24 based on chronological order.
    5. Select and order columns to match the target schema.
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse date
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract month name
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Determine daytype
    # dayofweek: Monday=0, ..., Sunday=6
    # Weekend is Saturday (5) or Sunday (6)
    df['daytype'] = df['parsed_date'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # 4. Rename hourly columns
    # Mapping from source column names to target column names
    # Chronological order of the day:
    # 12:00 AM (Midnight) -> hr1
    # 1:00 AM -> hr2
    # ...
    # 11:00 AM -> hr12
    # 12:00 PM (Noon) -> hr13
    # 1:00 PM -> hr14
    # ...
    # 11:00 PM -> hr24
    
    col_mapping = {
        '12:00 AM': 'hr1',
        '1:00 AM': 'hr2',
        '2:00 AM': 'hr3',
        '3:00 AM': 'hr4',
        '4:00 AM': 'hr5',
        '5:00 AM': 'hr6',
        '6:00 AM': 'hr7',
        '7:00 AM': 'hr8',
        '8:00 AM': 'hr9',
        '9:00 AM': 'hr10',
        '10:00 AM': 'hr11',
        '11:00 AM': 'hr12',
        '12:00 PM': 'hr13',
        '1:00 PM': 'hr14',
        '2:00 PM': 'hr15',
        '3:00 PM': 'hr16',
        '4:00 PM': 'hr17',
        '5:00 PM': 'hr18',
        '6:00 PM': 'hr19',
        '7:00 PM': 'hr20',
        '8:00 PM': 'hr21',
        '9:00 PM': 'hr22',
        '10:00 PM': 'hr23',
        '11:00 PM': 'hr24'
    }
    
    df = df.rename(columns=col_mapping)
    
    # 5. Define target columns in exact order
    target_columns = ['month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24']
    
    # Select and return the final DataFrame
    return df[target_columns]