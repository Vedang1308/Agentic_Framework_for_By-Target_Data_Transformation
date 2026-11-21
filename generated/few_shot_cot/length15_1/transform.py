import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse time
    df['time'] = pd.to_datetime(df['time'])
    
    # Extract hour and month
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    
    # Define seasons
    # Winter: 12, 1, 2
    # Spring: 3, 4, 5
    # Summer: 6, 7, 8
    # Autumn: 9, 10, 11 (Excluded based on target row count 72 = 24*3)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'
            
    df['season'] = df['month'].apply(get_season)
    
    # Filter out Autumn to match the 72 row count (3 seasons * 24 hours)
    df = df[df['season'] != 'Autumn']
    
    # Define aggregation columns
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
    
    dwheating_cols = ['electricity_water_systems_kwh']
    
    major_appliances_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    
    misc_plug_cols = [
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
    
    total_cols = ['net_site_electricity_kwh']
    
    # Group by season and hour, sum the values
    grouped = df.groupby(['season', 'hour'])
    
    agg_df = pd.DataFrame()
    agg_df['hvac'] = grouped[hvac_cols].sum().sum(axis=1)
    agg_df['domestic_water_heating'] = grouped[dwheating_cols].sum().sum(axis=1)
    agg_df['major_appliances'] = grouped[major_appliances_cols].sum().sum(axis=1)
    agg_df['lighting'] = grouped[lighting_cols].sum().sum(axis=1)
    agg_df['miscellaneous_plug_loads'] = grouped[misc_plug_cols].sum().sum(axis=1)
    agg_df['total'] = grouped[total_cols].sum().sum(axis=1)
    
    # Reset index to make season and hour columns
    agg_df = agg_df.reset_index()
    
    # Ensure column order and names match target
    target_columns = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    return agg_df[target_columns]