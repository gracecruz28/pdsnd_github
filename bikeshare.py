import time
import pandas as pd
import numpy as np
import datetime as dt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze. Choose from chicago, new york city or washington
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)

    m = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    d = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    city = ""
    month = ""
    day = ""

    
    restart = 'yes'
    while restart == 'yes':
        while True:
            try:
                city = str(input("Enter which of these cities you want to analyze: (chicago, new york city, washington)?  \n")).lower()
                
                if city in CITY_DATA.keys():
                    month = str(input("Enter month (all, january, february, march, april, may, june): \n")).lower()
                    if month in m:
                        day = str(input("Enter day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): \n")).lower()
                        
                        if day in d:
                            break
                        else:
                            print("\nYou have entered an invalid day.\n")
                            print("please try again.")
                    else:
                        print("\nYou have entered an invalid month.\n")
                        print("please try again.")

                else:
                    print("\nYou have entered an invalid city.\n")
                    print("please try again.")
            except KeyboardInterrupt:
                print("\n\nJob interrupted by user. Goodbye!\n") 
                break  
            except Exception as e3:
                print("Exception occurred: {}".format(e3))
                break
            finally:
                print("\nYou entered: \n City =", city, "\n Month =", month, "\n Day =", day)  


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
    #print("def_load_data: ", df)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

        
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
    
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
 
        ###print("\ndf inside\n")
        ###print(df.head())
   
   
    ###print("\ndf outside\n")
    ###print(df.head())

    return df


def time_stats(df):
    #print("def_time_stats: ",df)
    """Displays statistics on the most frequent times of travel."""
    #print("\nPrinting df inside time_stats\n", df)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    uniq_m = df['month'].nunique()
    if uniq_m != 1:
        most_popular_month = df['month'].mode()[0]
        print('Most Popular Month: ', most_popular_month, ',  Count: ', df['month'].value_counts()[0])

    # display the most common day of week
    uniq_d = df['day_of_week'].nunique()
    if uniq_d != 1:
        most_popular_day = df['day_of_week'].mode()[0]
        print('Most Popular Day of the Week: ', most_popular_day, ',  Count: ', df['day_of_week'].value_counts()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most Popular Hour (24hr): ', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    ### print("def_station_stats: ",df)
    """Displays statistics on the most popular stations and trip."""
    ###print('-'*40)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_startstation = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', most_popular_startstation, ',  Count: ', df['Start Station'].value_counts()[0])

    # display most commonly used end station
    most_popular_endstation = df['End Station'].mode()[0]
    print('Most Popular End Station: ', most_popular_endstation, ',  Count: ', df['End Station'].value_counts()[0])

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + ' to ' + df['End Station']
    most_popular_startendstation = df['start_end_station'].mode()[0]
    print('Most Popular combination of Start and End Station: ', most_popular_startendstation, ',  Count: ', df['start_end_station'].value_counts()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration_time_seconds = df['Trip Duration'].sum()
    print('Total Travel Duration: ', duration_time_seconds, 'seconds.')


    # display mean travel time
    mean_travel_time = df['Trip Duration'].sum()
    print('Average Trave Time: ', mean_travel_time, 'seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of User Type:')
    print(df['User Type'].value_counts())

    
    # Display counts of gender
    if "Gender" in df.columns:
        print('\nGender Counts:')
        print(df['Gender'].value_counts())
    else:
        print('\nGender\'s data is not available.')


    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_recent_year = df['Birth Year'].mode()[0]
        
        print('\nEarliest Birth Year: ', earliest_year)
        print('Most Recent Birth Year: ', most_recent_year)
        print('Most Commnon Year of Birth: ', most_recent_year)

 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    counter = 0
    counter1 = 5
    d_data = 'yes'

    d_data = str(input("Would you like to view individual trip data? Type 'yes' or 'no' : ")).lower()
    while d_data == 'yes':
        while counter < counter1:
            per_row = df.iloc[counter].to_dict()
            counter = counter + 1
            #counter1 = counter1 + 1
            print("\n", per_row, "\n")
        else:
            counter1 = counter + 5
        
        d_data = str(input("Would you like to view more individual trip data? Type 'yes' or 'no' : ")).lower()
        if d_data.lower() != 'yes':
            break
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
