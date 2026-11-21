import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'Date' column to datetime.
    2. Extract 'month' as the full month name (e.g., 'January').
    3. Determine 'daytype' as 'weekday' or 'weekend' based on the day of the week.
    4. Rename columns '1' through '24' to 'hr1' through 'hr24'.
    5. Select and order the columns to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse Date
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Extract Month Name
    df['month'] = df['Date'].dt.strftime('%B')
    
    # 3. Determine Day Type
    # dayofweek: Monday=0, ..., Friday=4, Saturday=5, Sunday=6
    df['daytype'] = df['Date'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename Hour Columns
    # Source columns are strings '1' to '24'
    # Target columns are 'hr1' to 'hr24'
    rename_dict = {str(i): f'hr{i}' for i in range(1, 25)}
    df.rename(columns=rename_dict, inplace=True)
    
    # 5. Define Target Columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and Return
    # Ensure we only return the required columns in the correct order
    return df[target_columns]