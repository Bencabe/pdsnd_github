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
    # get user input for city (chicago, new york city, washington)
    city = input("Would you like to explore chicago, new york city or washington? ").lower()
    while city != "chicago" and city != "new york city" and city != "washington":
        city = input("Sorry, that isn't a valid city. Please try again: ").lower()
        if city == "chicago" or city == "new york city" or city == "washington":
            break



    # get user input for month (all, january, february, ... , june)
    month = input("If you would like to explore a specific month please pick a month between january and june. If not please type 'all': ").lower()
    months = ['all','january','february','march','april','may','june']
    while month not in months:
        month = input("Sorry, that isn't a valid month. Please try again: ").lower()
        if month in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("If you would like to explore a specific day please pick a day of the week. If not please type 'all': ").lower()
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while day not in days:
        day = input("Sorry, that isn't a valid day. Please try again: ").lower()
        if day in days:
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June'}

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    most_common_month = "The most common month for travel is: {}".format(months[df['month'].mode()[0]])
    print(most_common_month)

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.weekday_name
    most_common_dow = "The most common day for travel is: {}".format(df['day'].mode()[0])
    print(most_common_dow)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = "The most common hour for travel is: {}".format(df['hour'].mode()[0])
    print(most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = "The most common station that journeys started at is: {}.".format(df['Start Station'].mode()[0])
    print(most_common_start)


    # display most commonly used end station
    most_common_end = "The most common station which journeys finished at is: {}.".format(df['End Station'].mode()[0])
    print(most_common_end)

    # display most frequent combination of start station and end station trip
    most_combination = df.groupby(['Start Station','End Station']).size().sort_values(ascending = False).head(1)
    sentence = "the most frequent combination of start and end station and the number of trips between them is:\n{}".format(most_combination)
    print(sentence)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = "The total amount of time spent travelling is: {} hours".format(sum(df['Trip Duration']) / 3600)
    print(total_travel)


    # display mean travel time
    mean_travel = "The average trip duration is: {} minutes".format(df['Trip Duration'].mean() / 60)
    print(mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)

    # Display counts of gender
    try:
        gender_type = df['Gender'].value_counts()
        print(gender_type)
    except:
        print("Sorry we don't have information about the user's gender for this city")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        latest_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print(" The earliest birth year of a user is {}.\nThe latest birth year of a user is {}.\nThe most common birth year among the users is {}.".format(earliest_year,latest_year,most_common_year))
    except:
        print("Sorry we don't have information about the user's birth year for this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Allows the user to explore raw trip data"""
    count = 6
    see_more_data = input("Would you like to see raw trip data?(yes or no) ").lower()
    while see_more_data == "yes":
        print(df.head(count))
        count += 5
        see_more_data = input("Would you like to see more 5 more lines of raw trip data?(yes or no) ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
