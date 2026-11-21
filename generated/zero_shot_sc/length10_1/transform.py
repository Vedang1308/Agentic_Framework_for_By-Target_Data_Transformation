import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process Datetime
    # Parse the time column, remove timezone if present, and format to 'YYYY-MM-DD HH:MM:SS'
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map Direct Columns
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    df['water_heating'] = df['electricity_water_systems_kwh']
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # 3. Aggregate Columns
    
    # Lighting: Sum of interior and exterior
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Pool/Spa Pumps: Sum of pool pump and hot tub pump
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Pool/Spa Heater: Sum of pool heater and hot tub heater
    df['pool_spa_heater'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # HVAC: Sum of heating, cooling, and associated fans/pumps
    # Including central system components if available
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # 4. Define Target Columns
    target_columns = [
        'datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # 5. Return Result
    return df[target_columns]