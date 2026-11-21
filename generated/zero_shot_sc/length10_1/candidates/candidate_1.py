import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the 'time' column to datetime and format it
    # Source format: '2012-07-02 00:15:00.000'
    # Target format: '2012-01-01 00:15:00'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map and aggregate columns
    
    # hvac: Sum of heating, cooling, and their associated fans and pumps
    # Note: Central system columns are typically subsets of the main heating/cooling columns
    # and should not be double-counted. We use the base heating/cooling columns and add fans/pumps.
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # water_heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # refrigerator
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # clothes_washer
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # clothes_dryer
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # dishwasher
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # cooking_range
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # pool_spa_pumps: Sum of pool pump and hot tub pump
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # interior_lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # exterior_lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # lighting: Sum of interior and exterior lighting
    df['lighting'] = df['electricity_interior_lighting_kwh'] + df['electricity_exterior_lighting_kwh']
    
    # plug
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # pool_spa_heater: Sum of pool heater and hot tub heater
    df['pool_spa_heater'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 3. Select and order columns to match target schema
    target_columns = [
        'datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return df[target_columns]