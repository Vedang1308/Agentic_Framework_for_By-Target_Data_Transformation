import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format datetime
    # Source 'time' is like '2012-07-02 00:15:00.000'
    # Target 'datetime' is like '2012-01-01 00:15:00'
    dt = pd.to_datetime(df['time'])
    df['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Calculate hvac
    # Sum of heating, cooling, and associated fans/pumps
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
    
    # 3. Calculate domestic_water_heating
    df['domestic_water_heating'] = df['electricity_water_systems_kwh']
    
    # 4. Calculate major_appliances
    appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    df['major_appliances'] = df[appliance_cols].sum(axis=1)
    
    # 5. Calculate lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    df['lighting'] = df[lighting_cols].sum(axis=1)
    
    # 6. Calculate miscellaneous_plug_loads
    misc_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # 7. Set total
    df['total'] = df['net_site_electricity_kwh']
    
    # Define target columns
    target_columns = [
        'datetime', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    return df[target_columns]