import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def display_most_common(var_name, value):
    """
    Displays most common value.
    
    Args:
        (str) var_name: variable name
        (str) value: the value of variable name to display
    Returns:
        None
    """
    print(f'+ Most common {var_name}: {value}')

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
    city = input("Would you like to see data for chicago, new york city, or washington?\n")
    city = city.lower()
    while city not in CITY_DATA:
        city = input("Invalid city! Try again\n")
        city = city.lower()
    
    # TO DO: get user input for month (all, january, february, ... , june)
    valid_months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    month = input('\nWhich month? all, january, february, march, april, may, or june?\n')
    month = month.lower()
    while month not in valid_months:
        month = input("Invalid month! Try again\n")
        month = month.lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday')
    day = input('\nWhich day of week? all, monday, tuesday, ..., sunday?\n')
    day = day.lower()
    while day not in valid_days:
        day = input("Invalid day! Try again\n")
        day = day.lower()

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    display_most_common('month', common_month)

    # TO DO: display the most common day of week
    common_dayofweek = df['day_of_week'].mode()[0]
    display_most_common('day of week', common_dayofweek)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    display_most_common('start hour', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    display_most_common('Start Station', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    display_most_common('End Station', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    trips = df[['Start Station', 'End Station']].apply(tuple, axis=1)
    display_most_common('trip', trips.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('+ Total travel time:', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('+ Mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    for user_type in user_types.index:
        print(f'+ {user_type}:', user_types[user_type])

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print()
        gender_count = df['Gender'].value_counts()
        for gender in gender_count.index:
            print(f'+ {gender}:', gender_count[gender])

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print()
        print('+ Earliest year of birth:', df['Birth Year'].min())
        print('+ Most recent year of birth:', df['Birth Year'].max())
        print('+ Most common year of birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def validate_yes_no_input(user_input: str):
    """Validate user input, require reentering if not in ['yes', 'no']
    
    """
    while user_input.lower() not in ['yes', 'no']:
        user_input = input("Please enter 'yes' or 'no'!\n")
    
    return user_input

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Display raw data
        is_display = input("Would you like to see 5 lines of raw data?\n")
        is_display = validate_yes_no_input(is_display)
        
        # Initialize index
        idx = 0
        
        while is_display.lower() == 'yes':
            
            # Total of rows
            n_rows = df.shape[0]
            
            # Display 5 rows
            print(df.iloc[idx:idx+5])
            
            idx += 5
            if idx >= n_rows:
                break
            is_display = input("Would you like to see more raw data?\n")
            is_display = validate_yes_no_input(is_display)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        restart = validate_yes_no_input(restart)
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
