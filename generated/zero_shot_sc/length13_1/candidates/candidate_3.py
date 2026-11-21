import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing detailed electricity usage data
    into a target DataFrame with aggregated categories.
    """
    df = source.copy()
    
    # 1. Handle Datetime
    # Parse the 'time' column and format to '%Y-%m-%d %H:%M:%S'
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Calculate 'lighting'
    # Sum of interior and exterior lighting
    df['lighting'] = (df['electricity_interior_lighting_kwh'] + 
                      df['electricity_exterior_lighting_kwh'])
    
    # 3. Calculate 'domestic_water_heating'
    # Direct mapping from water systems
    df['domestic_water_heating'] = df['electricity_water_systems_kwh']
    
    # 4. Calculate 'major_appliances'
    # Sum of refrigerator, clothes washer, clothes dryer, cooking range, dishwasher
    df['major_appliances'] = (df['electricity_refrigerator_kwh'] + 
                              df['electricity_clothes_washer_kwh'] + 
                              df['electricity_clothes_dryer_kwh'] + 
                              df['electricity_cooking_range_kwh'] + 
                              df['electricity_dishwasher_kwh'])
    
    # 5. Calculate 'miscellaneous_plug_loads'
    # Includes plug loads, various fans, and pool/hot tub equipment
    df['miscellaneous_plug_loads'] = (df['electricity_plug_loads_kwh'] + 
                                      df['electricity_house_fan_kwh'] + 
                                      df['electricity_range_fan_kwh'] + 
                                      df['electricity_bath_fan_kwh'] + 
                                      df['electricity_ceiling_fan_kwh'] + 
                                      df['electricity_pool_heater_kwh'] + 
                                      df['electricity_pool_pump_kwh'] + 
                                      df['electricity_hot_tub_heater_kwh'] + 
                                      df['electricity_hot_tub_pump_kwh'])
    
    # 6. Calculate 'hvac'
    # Includes heating, cooling, and associated fans/pumps
    heating_cols = [
        'electricity_heating_kwh', 
        'electricity_central_system_heating_kwh',
        'electricity_fans_heating_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh'
    ]
    
    cooling_cols = [
        'electricity_cooling_kwh', 
        'electricity_central_system_cooling_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    hvac_cols = heating_cols + cooling_cols
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # 7. Calculate 'total'
    # Direct mapping from net site electricity
    df['total'] = df['net_site_electricity_kwh']
    
    # 8. Define target columns and return
    target_columns = ['datetime', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    return df[target_columns]