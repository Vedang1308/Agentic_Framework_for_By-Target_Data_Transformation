import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Handle Datetime
    # Source 'time' is like '2012-07-02 00:15:00.000'
    # Target 'datetime' is '2012-01-01 00:15:00'
    # We parse to datetime and then format to string without milliseconds
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map and Aggregate Columns
    
    # HVAC: Sum of heating, cooling, and their associated fans and pumps
    # Note: We assume 'electricity_heating_kwh' and 'electricity_cooling_kwh' are totals 
    # and do not double-count 'central_system' variants which are likely breakdowns.
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # Water Heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # Refrigerator
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # Clothes Washer
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # Clothes Dryer
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # Dishwasher
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # Cooking Range
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # Pool/Spa Pumps: Sum of pool pump and hot tub pump
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Interior Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # Exterior Lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # Total Lighting: Sum of interior and exterior
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Plug Loads
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool/Spa Heater: Sum of pool heater and hot tub heater
    df['pool_spa_heater'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 3. Define Target Columns
    target_columns = [
        'datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # 4. Return the result with exact column order
    return df[target_columns]