# calgary_dogs.py
# Destin Saba
#
# A terminal-based application for computing and printing calgary dog breed registration statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.

import pandas as pd
import numpy as np

def main():

    # Import data into DataFrame
    dog_breeds = pd.read_excel('CalgaryDogBreeds.xlsx')

    # Create a multi-index DataFrame
    dog_breeds.set_index(['Breed','Year','Month'],inplace=True)

    print("ENSF 692 Dogs of Calgary")

    # Get user input, continually ask until valid input is entered
    while True:
        try:
            user_input = input("Please enter a dog breed: ")
            # Check if the input matches a dog breed (case insensitive)
            if (user_input.upper() in dog_breeds.index.get_level_values('Breed')):
                breed = user_input.upper()
                break
            else:
                raise KeyError
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

    # Data anaylsis 

    # Create index slice object
    idx = pd.IndexSlice

    # Slice DataFrame to create a DataFrame with only the inputted breed's data
    dog_breed = dog_breeds.loc[idx[breed,:,:],:]
    

    # Find and print all years where the selected breed was listed in the top breeds.
    years = dog_breed.index.get_level_values('Year').unique().tolist()
    print(f"The {breed} was found in the top breeds for years: {' '.join(map(str,years))}")

    # Calculate and print the total number of registrations of the selected breed found in the dataset.
    total_breed_registrations = dog_breed['Total'].sum()
    print(f"There have been {total_breed_registrations} {breed} dogs registered total.")

    # Grouping operation: Calculate total registrations per year for all breeds
    yearly_totals = dog_breeds.groupby('Year')['Total'].sum()

    # Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).
    for year in [2021, 2022, 2023]:
        yearly_total = yearly_totals.get(year,0)

        # Not all dog breeds have data for each year, so only sum if there is data for a given year
        if year in years:
            breed_yearly_total = dog_breed.loc[idx[:, year, :], 'Total'].sum()
        else:
            breed_yearly_total = 0
        yearly_percentage = (breed_yearly_total / yearly_total) * 100
        print(f"The {breed} was {yearly_percentage:.6f}% of top breeds in {year}.")


    # Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
    total_registrations = dog_breeds['Total'].sum()
    total_percentage = total_breed_registrations / total_registrations * 100
    print(f"The {breed} was {total_percentage:.6f}% of top breeds across all years.")


    # Find and print the months that were most popular for the selected breed registrations. Print all months that tie, in alphabetical order.
    most_popular_months = dog_breed.index.get_level_values('Month').value_counts()
    max_occurrences = most_popular_months.max()

    # Use a masking operation to get most popular months 
    popular_months = most_popular_months[most_popular_months == max_occurrences].index.tolist()

    # Sort alphabetically and print
    popular_months.sort()
    print(f"Most popular month(s) for {breed} dogs: {' '.join(popular_months)}")

if __name__ == '__main__':
    main()
