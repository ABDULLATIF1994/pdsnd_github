import time
import pandas as pd
import numpy as np
import datetime
pd.set_option('display.max_columns', 500)
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def max_dict(d):
    v_max = -1
    res = None
    for k in d:
        if d[k] > v_max:
            v_max = d[k]
            res = k
    return res

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
    valid_cities = ['chicago', 'new york city', 'washington']
    city = ''
    while city not in valid_cities:
        city = input('Choose a city from chicago, new york city and washington: ').lower()
  

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    month = ''
    while month not in valid_months:
        month = input('Choose a month (from all, january, ...): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in valid_weekdays:
        day = input('Choose a day of the week (from all, monday, ... sunday): ').lower()
    
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

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    month_idx = months.index(month)
    day_idx = weekdays.index(day)
    
    df = pd.read_csv(CITY_DATA[city])
    new_df = []
    for i, row in df.iterrows():
        start_date = row['Start Time']
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        if month_idx != 0 and month_idx != start_date_obj.date().month:
            continue
        if day_idx != 0 and day_idx - 1 != start_date_obj.weekday():
            continue
        new_df.append(row)

    new_df = pd.DataFrame(new_df)
    print("Here is some data: ")
    idx = 0
    while True:
        print(new_df[idx:idx+5].head())
        idx += 5
        if input("Would you like to see more data? (yes/no) ").lower() == "no":
            break
    return new_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    month_counts = {}
    day_counts = {}
    hour_counts = {}
    for i, row in df.iterrows():
        start_date = row['Start Time']
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        month = start_date_obj.date().month
        day = start_date_obj.weekday()
        hour = start_date_obj.hour
        if month in month_counts:
            month_counts[month] += 1
        else:
            month_counts[month] = 1

        if day in day_counts:
            day_counts[day] += 1
        else:
            day_counts[day] = 1

        if hour in hour_counts:
            hour_counts[hour] += 1
        else:
            hour_counts[hour] = 1
            
    # display the most common month
    print('The most common month is:', months[max_dict(month_counts)])
    # display the most common day of week
    print('The most common day of the week is:', weekdays[max_dict(day_counts)])
    # display the most common start hour
    print('The most common start hour is:', max_dict(hour_counts))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_stations = {}
    end_stations = {}
    start_end_combos = {}
    for i, row in df.iterrows():
        start_station = row['Start Station']
        end_station = row['End Station']
        start_end_station = start_station + ', ' + end_station

        if start_station in start_stations:
            start_stations[start_station] += 1
        else:
            start_stations[start_station] = 1

        if end_station in end_stations:
            end_stations[end_station] += 1
        else:
            end_stations[end_station] = 1

        if start_end_station in start_end_combos:
            start_end_combos[start_end_station] += 1
        else:
            start_end_combos[start_end_station] = 1
    # display most commonly used start station
    print('The most commonly used start station is:', max_dict(start_stations))

    # display most commonly used end station
    print('The most commonly used end station is:', max_dict(end_stations))

    # display most frequent combination of start station and end station trip
    print('The most commonly used combination of start and end stations is:', max_dict(start_end_combos))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = 0
    for i, row in df.iterrows():
        total_time += int(row['Trip Duration'])

    # display total travel time
    print('Total travel time:', total_time, 'seconds.')

    # display mean travel time
    print('Mean travel time:', total_time / len(df), 'seconds.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = {}
    genders = {}
    earliest_yob = 10000000
    most_recent_yob = -1
    yob_counts = {}
    for i, row in df.iterrows():
        user_type = str(row['User Type'])
        if 'Gender' in row: 
            gender = str(row['Gender'])
        else:
            gender = ''
        if 'Birth Year' in row:
            yob = str(row['Birth Year'])
        else:
            yob = ''

        if user_type in user_types:
            user_types[user_type] += 1
        elif user_type.strip() != '' and user_type != 'nan':
            user_types[user_type] = 1

        if gender in genders:
            genders[gender] += 1
        elif gender.strip() != '' and gender != 'nan':
            genders[gender] = 1

        if yob in yob_counts:
            yob_counts[yob] += 1
        elif yob.strip() != '' and yob != 'nan':
            yob_counts[yob] = 1

        if yob.strip() != '' and yob != 'nan':
            try:
                yob = int(float(yob))
            except:
                continue
            earliest_yob = min(earliest_yob, yob)
            most_recent_yob = max(most_recent_yob, yob)
            
    # Display counts of user types
    print('Counts of user types:')
    for k in user_types:
        print(k, ':', user_types[k])
    print('-' * 10)  
    # Display counts of gender
    if genders == {}:
        print('No gender data available.')
    else:
        print('Counts of genders:')
        for k in genders:
            print(k, ':', genders[k])
    print('-' * 10)  
    # Display earliest, most recent, and most common year of birth
    if yob_counts == {}:
        print('No birth year data available.')
    else:
        print('Earliest year of birth:', earliest_yob)
        print('Most recent year of birth:', most_recent_yob)
        print('Most common year of birth:', int(float(max_dict(yob_counts))))
    print('-' * 10)  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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


# The main program execution starts here

if __name__ == "__main__":
	main()
