# Additional third party modules which are used
import time
import pandas as pd
import numpy as np

# Definition of data files which are supported by Udacity to do the analysis
CITY_DATA = { 'chicago':       'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington':    'washington.csv' }

# Definitions of lists of possible data selections
pos_city = list(CITY_DATA)
pos_month = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
pos_day = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Additional function to match user input to valid selections.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """


    # Function to match user input to valid selections
    def searcher(list, string):
        str_match = [s for s in list if string in s]
        if not str_match:
            str_match = '  nothing!  '
        return str_match

    print('-'*65)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*65)

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = 'nothing!'
    # Loop for repeating input in case of invalid input
    while city == 'nothing!' or len(city) > 15:
        print('\n -- Possible city selections: ', pos_city)
        city = input('Please enter valid city you want to analyze! ').lower()
        city = str(searcher(pos_city, city))[2:-2]
        print('--> Your choice matches to: ', city)

    # TO DO: get user input for month (all, january, february, ... , june)
    print('\n -- Possible month selections: ', pos_month)
    month = input('Which month do you want to analyze? ').lower()
    month = str(searcher(pos_month, month))[2:-2]
    print('--> Your choice matches to: ', month)

    # if statement in case of invalid input
    if month == 'nothing!' or len(month) > 10:
        month = 'all'
        print('--> Because there is no clear match about your choice, the automated selection is: ', month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('\n -- Possible day selections: ', pos_day)
    day = input('Which day do you want to analyze? ').lower()
    day = str(searcher(pos_day, day))[2:-2]
    print('--> Your choice matches to: ', day)
    # if statement in case of user selection is not clear
    if day == 'nothing!' or len(day) < 3 or len(day) > 11:
        day = 'all'
        print('--> Because there is no clear match about your choice, the automated selection is: ', day)

    # Output final parameters for analyzing
    print('-'*65)
    print('Final Selections: City: {}, Month: {}, Day: {}'.format(city, month, day).title())
    print('-'*65)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Input:   Dataframe df
    Outputs: Prints statistics of day, month and hour with counts
    Returns: None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    counter = list(df['month'].value_counts())[0]
    print('The most common month is:           {} (counts: {})'.format((pos_month[popular_month].title()), counter))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    counter = list(df['day_of_week'].value_counts())[0]
    print('The most common day is:             {} (counts: {})'.format(popular_day, counter))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['hour'].mode()[0]
    counter = list(df['hour'].value_counts())[0]
    print('The most common start hour is:      {} (counts: {})'.format(popular_start_hour, counter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*65)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Input:   Dataframe df
    Outputs: Print statistics of popular stations and trips with counts
    Returns: None
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    counter = df['Start Station'].value_counts()[0]
    print('The most common start station is:   {} (counts: {})'.format(popular_start_station, counter))


    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    counter = df['End Station'].value_counts()[0]
    print('The most common end station is:     {} (counts: {})'.format(popular_end_station, counter))


    # TO DO: display most frequent combination of start station and end station trip
    # building trips
    df['Trip Stations'] = df['Start Station'] + '  ----->  ' + df['End Station']

    # determining most frequent trip
    popular_trip_stations = df['Trip Stations'].mode()[0]
    counter = df['Trip Stations'].value_counts()[0]
    print('The most frequent trip is:          {} (counts: {})'.format(popular_trip_stations, counter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*65)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Input:   Dataframe df
    Outputs: Displays statistics of trip duration
    Returns: None
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is:         ', total_travel_time, ' in s, ', total_travel_time/3600, ' in h')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is:          ', mean_travel_time, ' in s')

    # display max travel time
    max_travel_time = df['Trip Duration'].max()
    print('The max travel time is:           ', max_travel_time, ' in s')

    # display min travel time
    min_travel_time = df['Trip Duration'].min()
    print('The min travel time is:           ', min_travel_time, ' in s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*65)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Input:   Dataframe df
    Outputs: Displays statistics of users
    Returns: None
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts(dropna=False))

    # TO DO: Display counts of gender only if in dataset
    if 'Gender' in df:
        print('\nCounts of genders:')
        print(df['Gender'].value_counts(dropna=False))
    else:
        print('\nSorry, but there are no data about genders in this dataset :-(')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nBirth year statistics:')
        print('The earliest birth year is:       ', df['Birth Year'].min())
        print('The most recent birth year is:    ', df['Birth Year'].max())
        print('The mean birth year is:           ', df['Birth Year'].mean())
        print('The most common birth year is:     {} (counts: {})'.format(df['Birth Year'].mode()[0], list(df['Birth Year'].value_counts())[0]))

    else:
        print('\nSorry, but there are no data about birth year in this dataset :-(')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*65)


def display_raw_data(df):
    """
    Display raw data if user wants
    Input:   Dataframe df
    Outputs: Displays raw data in parts of 5 rows
    Returns: None
    """

    startpoint = 0
    endpoint = 5
    display = True
    while display:
        display = input('\nDo you want to see raw data? Enter "yes" or anything else for no. ')

        # Displaying data as long as the user wants
        if display == 'yes':
            display = 'True'
            print('\n')
            print(df[startpoint:endpoint])
            startpoint += 5
            endpoint += 5
        else:
            print('Thank you for joining the survey.')
            break

    print('-'*65)

def main():
    while True:
        city, month,day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter "yes" or anything else for no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
