import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse the time column to extract month and hour
    dt = pd.to_datetime(df['time'])
    df['month'] = dt.dt.month
    df['hour'] = dt.dt.hour
    
    # Define HVAC components
    hvac_components = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_components].sum(axis=1)
    
    # Define other end-use categories
    df['water_heating'] = df['electricity_water_systems_kwh']
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # Pool and Spa Pumps
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Plug loads
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool and Spa Heaters
    df['pool_spa_heater'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # Select and order columns to match target schema verbatim
    target_columns = [
        'month', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return df[target_columns]