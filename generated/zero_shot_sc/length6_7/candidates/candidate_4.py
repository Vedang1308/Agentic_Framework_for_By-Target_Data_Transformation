import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define the mapping from source column names to target column names
    col_mapping = {
        '1:00': 'Hr 1',
        '2:00': 'Hr 2',
        '3:00': 'Hr 3',
        '4:00': 'Hr 4',
        '5:00': 'Hr 5',
        '6:00': 'Hr 6',
        '7:00': 'Hr 7',
        '8:00': 'Hr 8',
        '9:00': 'Hr 9',
        '10:00': 'Hr 10',
        '11:00': 'Hr 11',
        '12:00': 'Hr 12',
        '13:00': 'Hr 13',
        '14:00': 'Hr 14',
        '15:00': 'Hr 15',
        '16:00': 'Hr 16',
        '17:00': 'Hr 17',
        '18:00': 'Hr 18',
        '19:00': 'Hr 19',
        '20:00': 'Hr 20',
        '21:00': 'Hr 21',
        '22:00': 'Hr 22',
        '23:00': 'Hr 23',
        '24:00:00': 'Hr 24'
    }
    
    # Create a copy to avoid modifying the original source dataframe
    df = source.copy()
    
    # Rename the columns based on the mapping
    df = df.rename(columns=col_mapping)
    
    # Drop the Segment column as it is not in the target schema
    if 'Segment' in df.columns:
        df = df.drop(columns=['Segment'])
    
    # Define the exact target column order
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # Return the dataframe with only the target columns in the correct order
    return df[target_columns]