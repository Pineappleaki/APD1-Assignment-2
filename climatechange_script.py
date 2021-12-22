"""
This program is designed to take in data and return plots and statistical 
summaries which will be presented in a clean, readable format
"""
# Import the modules needed
from datetime import date
from colorama import Fore, Style
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

def snapshotData(data, year, feature_names=[], normalise = True):

    """
    Take data from a specific year for all or some indicators

    Parameters
    ----------
    data : LIST
        list containing pandas dataframe(s).
    year : INT/STRING
        The year to look at.
    feature_names : LIST, optional
        refine for only specific features. The default is [].
    normalise : BOOL, optional
        Whether to normalise values or not. The default is True.

    Returns
    -------
    PANDAS_DATAFRAME
        Data from a specific year including the indicators chosen.

    """
    
    if isinstance(data, list) != True:  # Check data is a list
        return 'Data must be a list!'
    if isinstance(year, int):  # Correct int to a string
        year = str(year)
        
    # Substitute feature names if names are missing
    if feature_names == []:
        for i in range(len(data)):
            feature_names.append(f'Feature {i+1}')
    elif feature_names != range(len(data)):
        missing_names = ((len(data)) - len(feature_names))
        for i in range(missing_names):
            feature_names.append(f'NaN_{i+1}')
        
    snapshot = pd.DataFrame()  # Initalise dataframe
    
    for i in range(len(clean_data)):
        df = clean_data[i]
        if normalise is True:  # mean normalisation
            normalise_df = (df - df.mean() ) / df.std()
            df = normalise_df
        temp = df.loc[year]
        temp = temp.transpose()
        
        col_name = feature_names[i]  # get current feature name
        data = temp.iloc[:, 0]
        
        snapshot[col_name] = data  # adding a column to the df each itn
    
    return snapshot

def plotTimeSeries(data, y1, y2,
                   labels=['Title', 'X-axis', 'Y-axis(left)', 'Y-axis(right)'],
                   asset_set=['Feature_1', 'Feature_1'],
                   color_set=['#2077b4', '#f38043'],
                   save_file=False,
                   produce_summary=False):

    """
    Parameters
    ----------
    data : List
        An array of the desired datasets to plot.
    y1 : String
        Left Y axis value.
    y2 : String
        Right Y axis value.
    labels : List
        list of labels: Title;X;Y1;Y2, enter '' to skip a given element.
    asset_set : List
        set of each currency being plotted.
    color_set : List
        set of two colours.
    save_file : Bool
        Save file as a .png, default = False.
    produce_summary : Bool
        Produces summary stats (Min, Max, Mean) and the spearman between
        y1 & y2, default = True.

    Returns
    -------
    Shows a plot for each respective element in 'data', with option to save
    graphics and produce a summary
    """
    print(f'\n*** {Fore.YELLOW + Style.BRIGHT}STARTING:{Fore.RESET}',
          'plotTimeSeries ***')
    if len(labels) == 2:
        labels.extend([y1, y2])
    else:
        pass
    
    # Unpacking lists
    try:
        gen_title, x_label, y1_label, y2_label = labels
    except:
        print(f"{Fore.RED + Style.BRIGHT}ERROR:{Fore.RESET} Labels is missing",
              f"{(4 - len(labels))} parameters")
        print(f'*** {Fore.YELLOW + Style.BRIGHT}ENDING:{Fore.RESET}',
              'plotTimeSeries ***\n')
        return
    color_a, color_b = color_set

    current_date = date.today().strftime('%d-%m-%Y')

    # Establishing variables
    itn = 0

    for df in data:

        title = f'{asset_set[itn]}: {gen_title}'
        itn += 1

        fig, ax1 = plt.subplots()

        ax1.tick_params(axis='x', rotation=45)
        ax1.title.set_text(title)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y1_label)
        ax1.grid(True)
        ax1.fill_between(df.index, df[y1], alpha=0.25)

        _plt = ax1.plot(df.index, df[y1])

        ax2 = ax1.twinx()
        ax2.set_ylabel(y2_label)

        _plt2 = ax2.plot(df.index, df[y2], color=color_set[1])

        plt.legend([_plt[0], _plt2[0]], [y1_label, y2_label])
        plt.show()

        if save_file is True:
            file_name = (f'./plots/{title}_{current_date}.png')
            print(f'{Fore.MAGENTA + Style.BRIGHT}SAVING:{Fore.RESET} ',
                  f'{file_name}')
            fig.savefig((file_name),
                        format='png',
                        dpi=120,
                        bbox_inches='tight')

        if produce_summary is True:
            print(f'\nProducing Summary for {Fore.YELLOW + Style.BRIGHT}',
                  f'{asset_set[itn-1]}:{Fore.RESET}\n')
            all_features = [y1, y2]
            total_summary = []
            # Basic summary
            for feature in all_features:
                summary = []
                summary.append(np.max(df[feature]))
                summary.append(np.min(df[feature]))
                summary.append(np.mean(df[feature]))

                total_summary.append(summary)
            feature_df = pd.DataFrame(total_summary,
                                      columns=(['Maximum', 'Minimum', 'Mean']),
                                      index=(all_features))
            feature_df = feature_df.transpose()

            spearman = stats.spearmanr(df[y1], df[y2], nan_policy = 'omit')
            print(feature_df)
            print('\nSpearman R Coefficient:\n',
                  f'{Fore.BLUE + Style.BRIGHT}Correlation:{Fore.RESET} ',
                  f'{spearman[0]:.4f}\n',
                  f'{Fore.BLUE + Style.BRIGHT}P-Value:{Fore.RESET} ',
                  f'{spearman[1]}\n')

    print(f'*** {Fore.YELLOW + Style.BRIGHT}ENDING:{Fore.RESET} ',
          'plotTimeSeries ***\n')
    return

def seperateCountry(data, data_name, countries):

    """
    Seperate the country from the data to have country specific df

    Parameters
    ----------
    data : LIST
        list containing pandas dataframe(s)..
    data_name : LIST
        list containing desired features to out into df.
    countries : LIST
        list contraining countries to seperate.

    Returns
    -------
    country_data : LIST
        List containing country specific data in the order of countries.

    """
    
    # Create empty lists
    country_data = []
    country_list = []
    
    for j in range(len(countries)):
        target_country = countries[j]
        country_list.append(target_country)

        for i in range(len(data)):

            df = data[i][target_country]

            if i == 0:  # for the first itn create a df
                temp_df = pd.DataFrame(df)
                temp_df = temp_df.rename(columns = 
                                         ({target_country : data_name[i]}))

            else:  # otherwise, add to the df and then rename the column
                temp_df = pd.DataFrame(temp_df.join(df))
                temp_df = temp_df.rename(columns = 
                                         ({target_country : data_name[i]}))

        country_data.append(temp_df)  # add the df into a list

    return country_data

def multiSummaryStats(data, chosen_features = [], r = 3):

    """
    summary for multiple features 

    Parameters
    ----------
    data : LIST
        list containing pandas df.
    chosen_features : LIST, optional
        features to observe. The default is [] (all).
    r : int, optional
        rounding value. The default is 3.

    Returns
    -------
    summarised_stats : LIST
        returns list of df.

    """

    summarised_stats = []

    itn = 0
    for df in data:

        # Checking to see if specific features have been selected
        if chosen_features == []:
            chosen_features = list(df)
        else:
            pass

        total_summary = []

        for feature in chosen_features:
            summary = []
            # Generating stats
            feature_min = np.round(df[feature].min(), r)
            feature_max = np.round(df[feature].max(), r)
            # Finding dates of min/max and extracting the year only
            min_date = df.index[ df[feature].argmin() ].year
            max_date = df.index[ df[feature].argmax() ].year
            # Finding the mean
            mean = np.round(df[feature].mean(), r)
            
            # Add all elements to list
            summary.extend([min_date, feature_min, max_date, feature_max, 
                            mean])

            # Add to total summary
            total_summary.append(summary)

        feature_df = pd.DataFrame(total_summary, index = chosen_features,
                                  columns = ['Date:', 'Min', 'Date:', 'Max',
                                             'Mean'])
        feature_df.index.name = f'{country_names[itn]}'

        print(f'{Fore.YELLOW + Style.BRIGHT}',
                      f'{country_names[itn]}:{Fore.RESET}\n')
        print(feature_df)

        summarised_stats.append(feature_df)

        itn += 1
    
    return summarised_stats
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

# Taking a look at a heatmap to see any correlations
data_2014 = snapshotData(clean_data, 2014, data_name)
sns.heatmap(data_2014, cmap ='RdYlGn', linewidths = 0.30, annot = True)

# Seperate countries and create new 'data' list
data = seperateCountry(clean_data, data_name, country_names)
world, uk, china, india, brazil, us, norway = data  # extract data 

# Producing summary stats
stat = multiSummaryStats(data, ['CO2 Emissions', 'GDP ($)'])

# Plot time series of GDP v CO2
plotTimeSeries(data, 'GDP ($)', 'CO2 Emissions',
               labels = ['GDP vs CO2', 'Year'],
               asset_set = country_names, produce_summary = True)

# Plotting pairplot to observe any correlations between variables
# sns.pairplot(uk);  # commented out as very intensive to run each time
