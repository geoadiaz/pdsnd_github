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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nEnter the city: Chicago, New York City, Washington: \n").lower()
    while city not in ['chicago','new york city','washington']:
      print('Try again!')
      city = input("\nEnter the city: Chicago, New York City, Washington \n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nEnter the month: all, January, February, March, April, May, June: \n").lower()
    while month not in ['all','january','february','march','april','may','june']:
      print('Try again!')
      month = input("\nEnter the month: all, January, February, March, April, May, June: \n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nEnter the day: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: \n").lower()
    while day not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
      print('Try again!')
      day = input("\nEnter the day: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: \n").lower()

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
    #load city csv
    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time column to date format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and weekday from Start Time to new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by weekday
    if day != 'all':
        # filter by weekday to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is: ", popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common weekday is: ', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    max_Start_Station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is: ', max_Start_Station)

    # TO DO: display most commonly used end station
    max_End_Station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is: ', max_End_Station)

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " and " + df['End Station']
    print('The most frequent combination of start and end stations is: {}'.format((df['combination'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('The total travel time is: ', total_travel_time/3600, " hours")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ', mean_travel_time/60, " minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types counts:\n', user_types)

    # TO DO: Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('User gender count:\n', user_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('The earliest year is:', earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('The most recent year is:', most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('The most common year is:', most_common_year)

    except KeyError:
        print("\nGender Types:\n There is no gender and birth recorded for this filter.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    # Ask the user if they want to see raw data 'yes/no'
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc: start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to   continue?: Enter yes or no:\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data (df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
