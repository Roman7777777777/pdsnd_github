'''

Author: Roman Sprute
Date: 2022-12-28

'''


import time
import pandas as pd
import numpy as np



def spacer():

    """ Prints some spacing characters. """

    print('\n')
    print('#'*60)
    print('\n')

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze. Month and day are only requested when user stated to want to filter on them.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    spacer()

    validity_city = False
    validity_month = False
    validity_day = False
    validity_filter = False

    while validity_city is False:
        city = input('Please enter a city (chicago|new york city|washington) you are interested in: ')
        city_dics = {'cicago': 'chicago', 'chiago': 'chicago', 'chikago': 'chicago', 'chicago': 'chicago', 'schicago': 'chicago', 'new york city': 'new york city', 'newyorkcity': 'new york city', 'washington': 'washington'}

        try:
            city = str(city)
            city = city.lower()
            if city not in city_dics.keys():
                print('Please state one of the three given city names!')
                continue
            else:
                city = city_dics[city]
                validity_city = True
        except:
            print("Please enter a valid city string.")
            continue

    while validity_filter is False:
        filter = input('Do you wanna filter the data by month, day, or not at all? (month|day|both|no) ' )
        filter_dics = {'month':'month', 'day':'day', 'no': 'no', 'none': 'no', 'both': 'both'}

        try:
            filter = str(filter)
            filter = filter.lower()
            if filter not in filter_dics.keys():
                print('Please enter one of the four options!')
                continue
            else:
                filter = filter_dics[filter]
                validity_filter = True
        except:
            print('Please enter a valid filter!')
            continue

    if filter == 'month' or filter == 'both':

        while validity_month is False:
            month = input('Please enter a month (jan-jun|all) you are interested in: ' )
            month_dics = {'jan': 'jan', 'feb': 'feb', 'mar': 'mar', 'apr': 'apr', 'may': 'may', 'jun': 'jun', 'all': 'all'}

            try:
                month = str(month)
                month = month.lower()
                if month not in month_dics.keys():
                    print('Please state your month correctly. Month is given with three characters only!')
                    continue
                else:
                    month = month_dics[month]
                    validity_month = True
            except:
                print("Please enter a valid month string.")
                continue
        if filter == 'month':
            day = 'all'
    if filter == 'day' or filter == 'both':

        while validity_day is False:
            day = input('Please enter a day (mon-sun|all) you are interested in: ')
            day_dics = {'mon': 'mon', 'tue': 'tue', 'wed': 'wed', 'thu': 'thu', 'fri': 'fri', 'sat': 'sat', 'sun': 'sun', 'all': 'all'}

            try:
                day = str(day)
                day = day.lower()
                if day not in day_dics.keys():
                    print('Please state your day correctly. The day is given with three characters only!')
                    continue
                else:
                    day = day_dics[day]
                    validity_day = True
            except:
                print("Please enter a valid day string.")
                continue
        if filter == 'day':
            month = 'all'
    if filter == 'no':
        month = 'all'
        day = 'all'

    spacer()
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

    city_data = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }

    df = pd.read_csv(city_data[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'],)
    df['End Time'] = pd.to_datetime(df['End Time'],)

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['route'] = df['Start Station'] + ' to ' + df['End Station']

    if month != 'all':
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        day = days.index(day)

        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):

    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # display the most common month

    months = ['Janury', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    common_month = np.bincount(df['month']).argmax()
    print('Most common month: ' + str(months[common_month - 1]))
    # display the most common day of week

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    common_day = np.bincount(df['day_of_week']).argmax()
    print('Most common day: ' + str(days[common_day]))
    # display the most common start hour

    common_hour = np.bincount(df['hour']).argmax()
    print('Most common start hour: ' + str(common_hour))

    spacer()

def station_stats(df):

    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station

    common_start = df['Start Station'].value_counts().idxmax()
    print('Most common start: ' + common_start)
    # display most commonly used end station

    common_end = df['End Station'].value_counts().idxmax()
    print('Most common end: ' + common_end)
    # display most frequent combination of start station and end station trip

    common_route = df['route'].value_counts().idxmax()
    print('Most common route: ' + common_route)

    spacer()

def trip_duration_stats(df):

    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating Trip Duration...\n')

    # display total travel time

    total_travel = df['Trip Duration'].sum()
    print('Total travel time: ' + str(total_travel)+'s')
    # display mean travel time

    mean_travel = df['Trip Duration'].mean()
    mean_travel = round(mean_travel, 2)
    print('Mean travel time: ' + str(mean_travel)+'s')

    spacer()

def user_stats(df, city):

    """
    Displays statistics on bikeshare users. Gender and Birth Day analysis can't be done for washington.

    Args:
        (str) city - name of the city to prevent not possible analysis on washington
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating User Stats...\n')

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print('Follwing users traveled:')
    print(user_types)
    print('\n')
    # Display counts of gender
    if city != 'washington':
        gender_types = df['Gender'].value_counts()
        print('Follwing genders traveled:')
        print(gender_types)
        print('\n')

    # Display earliest, most recent, and most common year of birth

        earliest_year = min(df['Birth Year'])
        latest_year = max(df['Birth Year'])
        common_year = df['Birth Year'].value_counts().idxmax()
        print('The earliest year: ' + str(int(earliest_year)))
        print('The latest year: ' + str(int(latest_year)))
        print('The common year: ' + str(int(common_year)))
    else:
        print('Gender and Birth Dates couldn\'nt be calculated due to choosen city washington.\n')
    spacer()

def get_ending():

    """
    Asks user if he wants to do further analysis.

    Returns:
        (boolean) - returns True when the User stated that he wants to make further analysis. Else returns false.
    """

    validity_valid = False
    while validity_valid is False:
        validin = input('Do you want to start again with analysis? (y|n)')
        validin_dics = {'y': 'yes', 'ye': 'yes', 'yes': 'yes', 'n': 'no', 'no': 'no'}

        try:
            validin = str(validin)
            validin = validin.lower()
            if validin not in validin_dics.keys():
                print('Please enter y or n!')
                continue
            else:
                validin = validin_dics[validin]
                validity_valid = True
        except:
            print('Please enter y or n!')
            continue
    if validin == 'yes':
        return True
    else:
        return False

def want_raw_data(df):

    """
    Prints 5 lines of raw data to user after request is confirmed as often as it is confirmed.

    Args:
        df - Pandas DataFrame containing filtered city data
    """
    validity_raw = False
    counter = 0
    while validity_raw is False:
        raw = input('Do you want to see more raw data? (y|n)')
        raw_dics = {'y': 'yes', 'ye': 'yes', 'yes': 'yes', 'n': 'no', 'no': 'no'}

        try:
            raw = str(raw)
            raw = raw.lower()
            if raw not in raw_dics.keys():
                print('Please enter y or n!')
                continue
            else:
                raw = raw_dics[raw]
        except:
            print('Please enter y or n!')
            continue

        if raw == 'yes' and (len(df) - 5 > counter):
            for i in range(5):
                print(df.iloc[counter])
                counter += 1
        elif len(df) - 5 < counter:
            print('You saw everything interesting.')
            validity_raw = True
        else:
            validity_raw = True

def main():
    print('Hello! My name is Roman. We are going to look on some biking data. Will be quite a good ride I hope! :D')

    valid = True
    while valid:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        want_raw_data(df)
        valid = get_ending()

    print('Bye bye. I wish you a happy new year.')

if __name__ == "__main__":
	main()
