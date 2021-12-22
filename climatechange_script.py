"""
This program is designed to take in data and return plots and statistical 
summaries which will be presented in a clean, readable format
"""
# Import the modules needed
import pandas as pd

"""
*** FUNCTIONS ***
"""

def refineDataframe(df, years):
    
    """
    Refines a given dataframe to the specified years and removes un-required
    data

    Parameters
    ----------
    df : PANDAS_DATAFRAME
        Dataframe to be modified.
    years : LIST
        A list of 2 items, e.g. [lower bound, upper bound].

    Returns
    -------
    refined_df : PANDAS_DATAFRAME
        Returns a refined datatframe that is between the 'years' given.

    """

    # Getting rid of unncessecary columns and rows
    df = df.reset_index(drop = True)
    df = df.transpose()
    df = df.rename(columns=df.iloc[0])
    df = df.reset_index(drop = True)

    df = df.drop([0, 1, 2, 3])
    df = df.reset_index(drop = True)
    
    # creating an empty list to hold the data
    refined_df = []
    
    for i in range(len(df)): 
        if years[0] <= df.iloc[i, 0] <= years[1]:  # if the row is in range:
            refined_df.append(df.iloc[i])  # append the data into refined_df
    
    refined_df = pd.DataFrame(refined_df)  # completed list into a df
    
    # Correctly labeling axis
    refined_df = refined_df.rename(columns={'Country Name': 'Year'})
    refined_df['Year'] = pd.to_datetime(refined_df['Year'], format = '%Y')
    refined_df = refined_df.set_index('Year')
    
    return refined_df


def selectCountries(df, selected_countries):

    """
    Refine the data to select specific countries of intrest

    Parameters
    ----------
    df : PANDAS_DATAFRAME
        Dataframe to be modified.
    selected_countries : LIST
        List of countries to be selected.

    Returns
    -------
    selective_df : PANDAS_DATAFRAME
        Dataframe containing only the selected countries.

    """
    selective_df = [df.iloc[2]]  # initating the selective_df list 
    for i in range(len(df)):
        if (df.iloc[i, 1] in selected_countries) is True:  # Country in list:
            selective_df.append(df.iloc[i])  # Add country to list
        else:
            pass
    return selective_df


"""

*** CODE ***

"""

# Identify file locations
export_file = './data/exports.xls'
arable_land_file = './data/arable_land.xls'
co2_file = './data/co2_per_cap.xls'
gdp_file = './data/gdp_per_cap.xls'
ff_file = './data/fossil_fuel.xls'
renew_file = './data/renewable_energy_use.xls'
urban_pop_file = './data/urban_pop.xls'
pop_file = './data/pop_total.xls'
alt_energy_file = './data/alt_energy.xls'
energy_use_file = './data/energy_use.xls'

# Load data into pandas df
df1 = pd.read_excel(export_file)
df2 = pd.read_excel(arable_land_file)
df3 = pd.read_excel(co2_file)
df4 = pd.read_excel(gdp_file)
df5 = pd.read_excel(ff_file)
df6 = pd.read_excel(renew_file)
df7 = pd.read_excel(urban_pop_file)
df8 = pd.read_excel(pop_file)
df9 = pd.read_excel(alt_energy_file)
df10 = pd.read_excel(energy_use_file)


countries = ['WLD', 'GBR', 'CHN', 'IND', 'BRA', 'USA', 'NOR']
country_names = ['World', 'United Kingdom', 'China', 'India', 'Brazil', 
                 'United States', 'Norway']

# Making sure countries are in line with correct country codes
for i in range(len(countries)):
    print(f'{countries[i]} = {country_names[i]}') 

data = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]
data_name = ['Export of Goods', 'Arable Land', 'CO2 Emissions', 'GDP ($)',
             'Fossil Fuel Use', 'Renewable Use', 'Urban Population',
            'Population', 'Alt Energy', 'Energy Use']
years = [1970, 2020]


# Using a for loop to clean all dfs in 'data'
clean_data = []
for df in data:
    new_df = pd.DataFrame(selectCountries(df, countries))
    new_df = refineDataframe(new_df, years)

    clean_data.append(new_df)
