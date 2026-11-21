import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to match the target schema.
    - Renames numeric columns 1..24 to Hr 1..Hr 24.
    - Formats the Date column to %m/%d/%Y.
    - Drops the Class column.
    - Ensures the output has the exact target column names.
    """
    df = source.copy()
    
    # 1. Rename hour columns from '1'...'24' to 'Hr 1'...'Hr 24'
    rename_dict = {str(i): f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 2. Format the Date column
    # Parse to datetime to handle any inconsistencies, then format back to string
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 3. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return the target columns
    # Note: If the source is missing a date that is in the target, this simple transform
    # will not generate it. However, based on the schema mapping, this is the primary transformation.
    # Sorting by Date ensures the order matches the typical target expectation.
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df[target_columns]