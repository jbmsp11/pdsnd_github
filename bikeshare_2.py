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
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    try:
        city,month,day = str(input("Please enter a city, month(or all), day of week(or all) - separated by commas (example:chicago,june,all):")).split(",",3)
    except (ValueError, RuntimeError, NameError, UnboundLocalError):
        print("Invalid Data. Please restart and re-enter the correct data")


    print('-'*40)
    return (city.lower()).strip(), (month.lower()).strip(), (day.lower()).strip()


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
    try:
        filename=(city+".csv")
        df = pd.read_csv(filename)
    except FileNotFoundError as e:
        print('City file not found. Please select either Chicago, Washington, or New_York_City.\n')
        main()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        try:
            month = months.index(month) + 1
        except ValueError:
            print('please enter either a full month name or all.\n')
            get_filters()

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        try:
            df = df[df['day_of_week'] == day.title()]
        except ValueError:
            print('Data not found. Please enter either the name of the day or all.\n')
            get_filters()
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # use the index of the months list to get the corresponding int
    months = ['january', 'february', 'march', 'april', 'may', 'june']


    # display the most common month
    try:
        cm = months[df['month'].mode()[0] - 1].title()
        cd = df['day_of_week'].mode()[0]
        csh = df['hour'].mode()[0]
    except Exception as e:
        print('Identified the following error: ',e )


    #print('The most common month is: ',months[df['month'].mode()[0] - 1].title())
    print('The most common month is: ',cm)
    # display the most common day of week

    #print('The most common day of the week is: ',df['day_of_week'].mode()[0])
    print('The most common day of the week is: ', cd)

    # display the most common start hour
    #print('The most common start hour: ',df['hour'].mode()[0])
    print('The most common start hour: ',csh)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is: ',df['Start Station'].mode()[0])


    # display most commonly used end station
    print('The most common end station is: ',df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['freq_combination'] = df['Start Station'] + " to " + df['End Station']
    print('The most frequent combination of start/end stataions is :',df['freq_combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print("Total travel time: ", round(df['Trip Duration'].sum()/60,2), " minutes.")

    # display mean travel time
    print("Average (mean) travel time: ",round(df['Trip Duration'].mean()/60,2)," minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby(['User Type'])['User Type'].count()
    print('Counts by user types: \n',user_type,'\n')

    # Display counts of gender
    try:
        gender = df.groupby(['Gender'])['Gender'].count()
    except KeyError:
        print('Gender not available in this file.\n')
    else:
        print('Counts by gender: \n', gender,'\n')


    # Display earliest, most recent, and most common year of birth
    try:
        cbd = df.groupby(['Birth Year'])['Birth Year'].count().reset_index(name='counts').sort_values(['counts'],ascending=False).astype('int').head(1)
        rbd = pd.to_numeric(df['Birth Year'].max())
        ebd = pd.to_numeric(df['Birth Year'].min())
    except KeyError:
        print('Birth year not available in this dataset')
    else:
        print('The most common year of birth is: \n',cbd,'\n')
        print('The most recent year of birth is: ',int(rbd))
        print('The earliest year of birth is: ', int(ebd),'\n')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays the raw data associated with the dataframes."""

    #Collect input from the user to see if they would like to see the raw data. Loop through the data if they want to see more.
    pd.set_option('display.max_columns', 200)
    rd = input('Would you like to see 5 lines of raw data (y/n)?')
    c = 0
    if rd == 'y':
        rd2 = ''
        while rd2.lower() != 'n':
            c += 5
            print(df.iloc[c-5:c,:])
            rd2 = input('Press any key to see more, N to end')

def try_again():
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes' and restart.lower() != 'no':
        print(restart)
        print('Unrecognized value - please re-enter yes/no')
        del restart
        try_again()
    elif restart.lower() == 'no':
        quit()
    elif restart.lower()=='yes':
        main()

def main():
    a=0
    while True:

        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
        except Exception as e:
                print('error: ',e)
                city, month,day = get_filters()
                df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        #restart = input('\nWould you like to restart? Enter yes or no.\n')
        #while restart.lower() != 'yes' or restart.lower() != 'no:':
        #        print('Unrecognized response.\n')
        #        restart = input('\nWould you like to restart? Enter yes or no.\n')
        try_again()




if __name__ == "__main__":
	main()
