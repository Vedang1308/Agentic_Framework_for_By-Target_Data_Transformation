import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with AM/PM time columns into a target DataFrame
    with 24-hour format time columns and a reformatted date column.
    """
    # Define the mapping from source AM/PM columns to target 24-hour columns
    # Note: 12:00 PM is Noon (12:00), 12:00 AM is Midnight (24:00 in this target schema)
    col_mapping = {
        '1:00 AM': '1:00', '2:00 AM': '2:00', '3:00 AM': '3:00', '4:00 AM': '4:00',
        '5:00 AM': '5:00', '6:00 AM': '6:00', '7:00 AM': '7:00', '8:00 AM': '8:00',
        '9:00 AM': '9:00', '10:00 AM': '10:00', '11:00 AM': '11:00',
        '12:00 PM': '12:00', # Noon
        '1:00 PM': '13:00', '2:00 PM': '14:00', '3:00 PM': '15:00', '4:00 PM': '16:00',
        '5:00 PM': '17:00', '6:00 PM': '18:00', '7:00 PM': '19:00', '8:00 PM': '20:00',
        '9:00 PM': '21:00', '10:00 PM': '22:00', '11:00 PM': '23:00',
        '12:00 AM': '24:00'  # Midnight
    }

    # Rename the time columns
    df = source.rename(columns=col_mapping)

    # Parse the date and format it as required: 'Wed 01/01/2014'
    # Source format is M/D/YYYY, target is %a %m/%d/%Y
    df['cst'] = pd.to_datetime(df['date']).dt.strftime('%a %m/%d/%Y')

    # Define the target column order
    target_time_columns = [f'{i}:00' for i in range(1, 25)]
    target_columns = ['cst'] + target_time_columns

    # Select only the required columns in the correct order
    # This also implicitly drops the 'date' and 'DSL' columns
    df = df[target_columns]

    return df[target_columns]