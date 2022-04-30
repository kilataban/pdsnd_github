from calendar import day_abbr
import time
import pandas as pd
import numpy as np

CITIES_DATA = {'chi':'chicago.csv', 'nyc': 'new_york_city.csv', 'wash': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze 

    Returns:
        (str) city - name of city to analyze
        (str) month - name of the month to filter by or "all" to apply no month filter.
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter.

    """
    print("Hello! Let's explore some US bikeshare data\n")
    while True:
        city = input("Please pick a city to analyze: 'chi' for Chicago, 'nyc' for New York City and 'wash' for Wahsington.").lower()
        if(city in CITIES_DATA.keys()):
            break
        else:
            print("Sorry, that is an invalid input.\n")

    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']
    while True:
        month = input("Please pick a month (jan, feb, mar, apr, may, jun) or 'all' to filter: \n").lower()
        if (month in months):
            break
        else:
            print("Sorry, that is an invalid input.\n")
            
    days = ['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'all']
    while True:
        day = input("Please pick a day of the week (sat, sun, mon, tue, wed, thu, fri or 'all' to filter.").lower()
        if day in days:
            break
        else:
            print("Sorry, that is an invalid input.\n")
    
    print('*' *80)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city  and filters by month and  day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month -  name of the month to filter by, or "all"
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    
    Returns:
        df - Pandas DataFrame containing city data by month and day
    """

    df = pd.read_csv(CITIES_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month'].str.startswith(month.title())]
    
    if day != 'all':
        df = df[df['day_of_week'].str.startswith(day.title())]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel as per the data
    """
    # The most popular travel times
    print('/nCalculating the Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['month'] = df['Start Time'].dt.month_name()
    most_popular_month = df['month'].mode()[0]
    print("Most popular month for travel is ", most_popular_month)

    # The most popular day of the week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_popular_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week to travel is ', most_popular_day)

    # The most popular hour of travel in the day
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('The most popular hour of the day to travel is ', most_popular_hour)

    print("\nThis process took %s seconds to complete." %(time.time() - start_time))
    print('*' *80)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trips
    """
    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()
    most_comm_start = df['Start Station'].mode()[0]
    print('The most popular start station is ',most_comm_start)

    most_comm_end = df['End Station'].mode()[0]
    print('The most popular end station is', most_comm_end)

    most_popular_trip = 'The most popular trip is the one from ' + df['Start Station'] + " to " + df['End Station'].mode()[0]
    print(most_popular_trip)

    print("\nThis data retrieval process took %s seconds." %(time.time() - start_time))
    print('*' *80)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()
    total_trip_duration = df['Trip Duration'].sum()
    print('The total trip duration is ', total_trip_duration)
    avg_travel_time = df['Trip Duration'].mean()
    print("The average travel time is", avg_travel_time)

    print("\nThis process took %s seconds." % (time.time() - start_time))
    print('*' *80)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """

    print("\nCalculating the User Statistics...\n")
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('These are the user types in our bikeshare system ', user_types)
    try:
        print("The count by Gender is ", df['Gender'].value_counts())
        print("Our earliest birth year in the data is", df['Birth Year'].min())
        print('The latest year of birth is ', df['Birth Year'].max())
        print("The most common birth year in the data is", df['Birth Year'].mode()[0])

    except(RuntimeError, TypeError, NameError):
        print("That filter couldn't be used or found.")

    print("\nThis process took %s seconds." % (time.time() - start_time))
    print('*' *80)


def display_data(df):
    additional_data = input("Would you like to view 5 more rows of data? Enter 'Y' or 'N").upper()
    start_loc = 0
    while (additional_data == 'Y'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        additional_data = input("Would you like to view 5 more rows of data? Enter 'Y' or 'N").upper()

    return df

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        start_over = input("Do you want to start the program again? 'Y' or 'N'?\n").upper()
        if (start_over != 'Y'):
            break

if __name__ == "__main__":
    main()