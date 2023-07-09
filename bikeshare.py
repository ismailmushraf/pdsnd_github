import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = time_filter = None
    month = day = 'all'
    while True:
        city = input('Would you like to see data for Chicago, New york city or Washington?\n').lower()
        if city in CITY_DATA.keys():
            break 
    
    while True:
        time_filter = input('Would you like to filter the data by month, day or both, or not at all? Type "none" for no time filter.\n').lower()
        if time_filter in ["month", "day", "both", "none"]:
            break
    
    # get user input for month (all, january, february, ... , june)
    while True and (time_filter == 'month' or time_filter == 'both'):
        month = input('Which month? January, February, March, April, May, June or All?\n').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break 

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True and (time_filter == 'day' or time_filter == 'both'):
        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?.\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break 

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    # removing unnecessary column
    df = df.drop('Unnamed: 0', axis=1)
    # convert date columns to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        print("Most popular month:", df['month'].mode()[0])

        # display the most common day of week
        print("Most popular day of the week:", df['day_of_week'].mode()[0])

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        print("Most popular start hour:", df['hour'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError as ke:
        print('key is not available', ke)
    except Exception as e:
        print(e)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        print('Most Popular Start station:', df['Start Station'].mode()[0])

        # display most commonly used end station
        print('Most Popular End station:', df['End Station'].mode()[0])

        # display most frequent combination of start station and end station trip
        df['Trip'] = (df['Start Station'] + ' to ' + df['End Station'])
        print('Most Popular Trip:', df['Trip'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError as ke:
        print('key is not available', ke)
    except Exception as e:
        print(e)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    try:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        print('Total Travel duration:', df['Trip Duration'].sum())

        # display mean travel time
        print('Average Travel duration:', df['Trip Duration'].mean())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError as ke:
        print('key is not available', ke)
    except Exception as e:
        print(e)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type_count = df.groupby('User Type')['User Type'].count()
        print('User Types')
        for key in user_type_count.index:
            print(key + ':', user_type_count[key], end=' ')
        print()

        # Display counts of gender
        gender_count = df.groupby('Gender')['Gender'].count()
        print('Gender')
        for key in gender_count.index:
            print(key + ':', gender_count[key], end=' ')
        print()

        # Display earliest, most recent, and most common year of birth
        print('Birthdays')
        print('Earliest:', df['Birth Year'].min(), end=' ')
        print('Most recent:', df['Birth Year'].max(), end=' ')
        print('Most common:', df['Birth Year'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError as ke:
        print('key is not available', ke)
    except Exception as e:
        print(e)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        index = 0
        step = 5
        while True:
            show_data = input('\nWould you like to see 5 lines of data? Enter yes or no.\n')
            if show_data.lower() != 'yes':
                break
            else:
                print(df[index:index+step])
                index += step

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
