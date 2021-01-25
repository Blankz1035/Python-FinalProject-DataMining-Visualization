# Program to read and analysis a given CSV file -> Property Price Index of Ireland.
# Created by Andy Blankley

"""Purpose of this Program:
    This program reads in a CSV file (the property price register) and processes the data for user analysis.

    Capabilities: 
        The program provides a user the ability to check the following features from the dataset:
        1. Number of records from the CSV file (excluding header) & Total Euros used 
        2. Maximum Price Value of a House
        3. Minimum Price Value of a House
        4. Mean Value of a House ( Split by: Sale, Month, Year)
        5. Median Value of all houses bought.
        6. Mode Value - Most common price of a house in Ireland.
        7. Standard Deviation
        8. Extra Processing:
            i. Yearly Range.
            ii. Count of Sales Per Year in Yearly Range.
            iii. Year Most / Least houses sold.
            iv. Month / Year Most / Least houses sold.
            v. Highest / Lowest Price paid including Address, County and Description
            vi. All counties with House Sales.
            vii. Counties with Most / Least Properties sold.
        9. Create Graphical Plots:
            i. Scatter Plot - Sales Over Years
            ii, Bar Chart - Sales Over Counties
            iii, Bar Chart - Sales Per Month (Specify Year / All)
            iv, Pie Chart - Sales Over Years
    
    File Input:  
        CSV File PPR_ALL.csv

    Columns:
        Date of Sale (dd/mm/yyyy),Address,Postal Code,County,Price (�),Not Full Market Price,VAT Exclusive,
        Description of Property,Property Size Description
"""
from sys import exit
import math
import matplotlib.pyplot as plt

############## Function Definition: ################
def print_processing_status(index: int, max_rows: int):
    """Function to output processing status for loop statements.

    Args:
        index (int): [Current loop index value]
        max_rows (int): [Maximum loop size]
    """
    

     # Loading % for user - data preparation
    if int(max_rows * 0.05) == index:
        print("Processing Status: 5% complete..")
    if int(max_rows * 0.10) == index:
        print("Processing Status: 10% complete..")
    if int(max_rows * 0.20) == index:
        print("Processing Status: 20% complete..")
    if int(max_rows * 0.30) == index:
        print("Processing Status: 30% complete..")
    if int(max_rows * 0.40) == index:
        print("Processing Status: 40% complete..")
    if int(max_rows * 0.50) == index:
        print("Processing Status: 50% complete..")
    if int(max_rows * 0.60) == index:
        print("Processing Status: 60% complete..")
    if int(max_rows * 0.70) == index:
        print("Processing Status: 70% complete..")
    if int(max_rows * 0.80) == index:
        print("Processing Status: 80% complete..")
    if int(max_rows * 0.90) == index:
        print("Processing Status: 90% complete..")
    if max_rows == index:
        print("Processing Status: 100% complete..")
        return True

    return False

def select_rows_for_processing(max_length:int):
    """Function to allow user to specify rows for processing from CSV file.

    Args:
        max_length (int): [maximum length that can be processed -> Length of data file ]
        Max_Length is set to be rows_to_process. The user can choose to change this or keep the same.

    Returns:
        rows_to_process [int]: [Rows to process in the program.]
    """
    rows_to_process = max_length
    while True:
        choice = input("Would you like to process all records? y/n: ")
        
        if choice.lower() == "y":
            break
        elif choice.lower() == "n":
            try:
                rows_to_process = int(input("Enter a maximum row: "))

                if rows_to_process < 2:
                    print("Rows cannot be less than 2! Try again..")
                    continue
                break
            except ValueError:
                print("Error in user input (value). Try again..")
            except TypeError:
                print("Error in user input (Type). Try again..")
        else:
            print("Invalid input: ", choice)

    return rows_to_process

def validate_price(prc:str):
    """Function to validate the price string split from the data file line.

    Args:
        prc (str): [price string value from the import and split of the line from csv file.]
        The string will be checked to validate the characters will be valid for casting to float value.
    Returns:
        prc [float]: [prc transformed from string to float value.]
    """
    try:    
        if not prc:
            # Should not happen. Price should be filled. If not, then we can raise an error or assign value of 0
                print(f"Problem converting price. Price is null. Assigning 0 value. Line: 105 and index{index}")
                prc = "0"
                
        # Remove the commas in the string price
        prc = prc.replace(',', "")

        # Pricing Validation -> Need to convert to a number for analysis
        for character in prc:    
            # Check character validity -> issue solved with diamond questionmark invalid character throwing error 
            # as cast to float fails!
            if not character == "." and not character.isdigit() or character == '€':
                prc = prc.replace(character, "")
                continue
            
        # After processing the line, make ammendments to the number values:
        
            prc = float(prc)
    except ValueError:
        print(f"Problem converting price ({prc}) to a float value. Line: 105 and index{index}")

    return prc

def calculate_price_frequency(pricelist:list):
    """Function to calculate the mode of the pricelist.

        For output to the user, we inform them of how many unique values are in the price list. This is done using the python set()
        The price list is then looped over to create a dictionary. If the value is located we add 1 to the key/value pair for the frequency.

    Args:
        pricelist (list): [List created from the splitting of input file for the price values.]

    Returns:
        pricefreq_dict[dictionary]: [Dictionary containing unqiue price keys with frequency of appearence as values.]
    """
    index = 0
    uniquePrice = set(priceList)     
    pricefreq_dict = dict()

    print()
    print(f"Calculating frequency of pricing data [{len(uniquePrice)} unique prices of {len(priceList)} sales]..")
    for prc in pricelist: 
        index +=1

        if prc in pricefreq_dict.keys():
           pricefreq_dict[prc] = pricefreq_dict[prc] + 1
        else:
            pricefreq_dict[prc] = 1
        
        # Loading % for user - pricing frequency preparation
        if print_processing_status(index, len(priceList)):
            break
    else:
        print("Completed..")

    return pricefreq_dict

def total_price_values(priceList:list):
    """Function to populate total_price_values from the pricelist.

    Args:
        priceList (list): [List created from the splitting of input file for the price values.]

    Returns:
        Sum, Length , Maximum Value and Minimum Value tuple returned for processing.
    """
    return sum(priceList), len(priceList), max(priceList), min(priceList)

def get_date_values(dos: list):
    """Function to populate key date values for processing in the application.
    Parts of the program rely on splitting the data by the dates to locate specify values.
    Instead of having multiple lists / variables with the key values, it is more performant to have a dictionary with the specified 
    keys with the corresponding values.

    Args:
        dos (list): [List containing the Dates Of Sales that have been split in the csv file.]

    Returns:
        date_values[dictionary]: [Dictionary containing the essential key date splits for use in the program.]
    """
    first_dos = dos[0]
    last_dos = dos[len(dos)-1]

    date_values = {"Total Months": 0, "Total Years":  0, "First Dos": dos[0] , "First Dos Month": int(first_dos[3:5]), "First Dos Year": int(first_dos[6:]), 
    "Last Dos":  dos[len(dos)-1], "Last Dos Month":  int(last_dos[3:5]), "Last Dos Year": int(last_dos[6:]),}
    
    # Determine how many months are used in the first year: Eg. starting in may (month 5 -> So we need to take 5 away from total but add any month after final year)
    date_values["Total Years"] = date_values["Last Dos Year"] - date_values["First Dos Year"]

    if date_values["Total Years"] > 0:
        date_values["Total Months"] = (12 * date_values["Total Years"]) + date_values["Last Dos Month"] - date_values["First Dos Month"]  # eg: 2020 - 2010 = 10yrs  + 9 months -(months of 1st year)
    else:
        date_values["Total Months"] = date_values["Last Dos Month"] - date_values["First Dos Month"]

    return date_values

def mean_of_pricelist(priceList:list, number:int):
    """Function to calculate the mean of the pricelist.
    Number represents the total months or total years. This is used to visualize the data in different dimensions for the mean over the months and years.

    Args:
        priceList (list): [List created from the splitting of input file for the price values.]
        number (int): [Length to calculate the mean with.]

    Returns:
        Sum of pricelist / number IF number is more than 1. Otherwise the mean is the sum of the list
    """
    if number <=1:
        return sum(priceList)
    
    return sum(priceList) / number

def calculate_median_of_pricelist(length_of_pricelist:int, priceList:list):
    """Function to calculate the median of the pricelist.

    Calculating the mid point of the pricelist with variation if the length is an even number. If the length is an even number,
     we first must take the value of the pricelist at the mid_index -1 , add this to the value at the mid index and then divide this value
     by 2 . This will give the median value.

    Args:
        length_of_pricelist (int): [Length of the current pricelist.]
        priceList (list): [List created from the splitting of input file for the price values.]

    Returns:
        mid_index[int]: [middle index point of the pricelist.]
        mid_pricelist[int]: [Median Value of the pricelist.]
    """
    mid_index = int(length_of_pricelist / 2) 

    if length_of_pricelist % 2 == 1:
        mid_pricelist = priceList[mid_index]
    else:
        mid_pricelist = (priceList[mid_index -1] + priceList[mid_index]) / 2
    return mid_index, mid_pricelist

def calculate_standard_deviation(pricelist:list, sumlist = 0, lengthlist = 0, total_months = 0, total_years = 0):
    """[Function to Calculate the Standard Deviation By Month, Year and Overall]

    Args:
        pricelist (list): [List created from the splitting of input file for the price values.]
        sumlist (int, optional): [Optional Parameter. Can be passed to access total months and total year deviation]. Defaults to 0.
        lengthlist (int, optional): [Optional Parameter. Can be passed to access total months and total year deviation]. Defaults to 0.
        total_months (int, optional): [Optional Parameter. Can be passed to access total months and total year deviation]. Defaults to 0.
        total_years (int, optional): [Optional Parameter. Can be passed to access total months and total year deviation]. Defaults to 0.

    Returns:
        std_dev[float]: [Standard deviation based on mean of whole price list]
        month_std_dev[float]: [Standard deviation based on mean of (sum of pricelist / total months)]
        year_std_dev[float]: [Standard deviation based on mean of (sum of pricelist / total years)]
    """
    std_dev = 0
    month_std_dev = 0
    year_std_dev = 0

    if (sumlist > 0) and (lengthlist > 1):
        price_deviations = [ ((x - (sumlist / lengthlist)) **2) for x in priceList]

        # If months is not = 0
        if total_months > 0:
            month_deviations = [ ((x - (sumlist / total_months)) **2) for x in priceList]
            month_std_dev = math.sqrt(sum(month_deviations)/(total_months -1))

        # Year: Only if total years is > 0 do we caculate.
        if total_years > 0:
            year_deviations = [ ((x - (sumlist / total_years)) **2) for x in priceList]
            year_std_dev = math.sqrt(sum(year_deviations)/(total_years -1))


        # Calculate deviation for price
        std_dev = math.sqrt(sum(price_deviations)/(length_of_pricelist -1))
    elif len(pricelist) > 0:
        l_mean = sum(pricelist) / len(pricelist)
        squared_deviations = [ (x - l_mean) ** 2 for x in pricelist ]
        std_dev =  math.sqrt(sum(squared_deviations) / (len(pricelist) - 1))

    else:
        print("Invalid parameters been passed. No calculation completed.")

    return std_dev, month_std_dev, year_std_dev

def calculate_yearly_house_sales(priceList:list, dos:list, date_values:dict):
    """Function to calculate yearly house sales.
    This function utilizes the dates of sale and also the date values dictionary with essential key values.

    Loop over each DOS, slice the value from the year value only of dd/mm/yyyy. cast this to a int.
    check this value against a newly created dictionary year_dict with key values from first DOS to Last DOS.

    Args:
        priceList (list): [List created from the splitting of input file for the price values.]
        dos (list): [List created from the splitting of input file for the date of sale values.]
        date_values (dict): [Dictionary created by Get_Date_Values() function with essential key values for processing.]

    Returns:
        Return year_dict (dictionary) with each year and total sales for that year, the yearly_range list, the year with most houses sold and
        year with least houses sold.
    """
    # Create list between first DOS and Last DOS. eg. 2010, 2011, 2012... 2020
    yearly_range = list(range(date_values["First Dos Year"], date_values["Last Dos Year"] +1))
    # Create a dictionary with Each Year as a Key and set the value to 0.
    year_dict = {year: 0 for year in yearly_range}

    for d in dos:
        d = int(d[6:])
        if d in year_dict.keys():
            year_dict[d] = year_dict[d] + 1
        else:
            year_dict[d] = 1
       
    year_most_houses_sold = max(year_dict, key=year_dict.get)
    year_least_houses_sold = min(year_dict, key=year_dict.get)

    return year_dict, yearly_range, year_most_houses_sold, year_least_houses_sold

def calculate_most_month_of_sale(dos:list):
    """Function to calculate the month with most sales across the rows processed.
    Get the length of DOS and store this (More performant to store this instead of calculating each time)
    Loop over each date and slice from month values eg. mm/2020.
    Build dictionary with the values as keys (unique) and the values as the frequency.
    Display processing status to the user based on length of DOS and the current index.
    Args:
        dos (list): [List created from the splitting of input file for the date of sale values.]

    Returns:
        dates_dict[Dictionary]: [Dictionary containing the dates mm/yyyy and their frequencies.]
    """
    dos_length = len(dos)
    index = 0
    dates_dict = dict()
    
    for u_date in dos:
        # Set the date checking to only contain the month. Not interested in a specific day.
        u_date = u_date[3:]
        
        if u_date in dates_dict.keys():
           dates_dict[u_date] = dates_dict[u_date] + 1
        else:
            dates_dict[u_date] = 1
      
        index += 1

        # Loading % for user - months mode preparation
        if print_processing_status(index, dos_length):
            break

    return dates_dict

def calculate_county_sales(county:list):
    """Function to calculate county sales.
    Get the length of county and store this (More performant to store this instead of calculating each time)
    Loop over each county.
    Build dictionary with the values as keys (unique) and the values as the frequency.
    Display processing status to the user based on length of county and the current index.
    Args:
        county (list): [List of counties that have been sliced from the input file during import.]

    Returns:
        county_dict[dictionary]: [Dictionary containing unique counties and also their frequencies]
    """
    county_dict = dict()
    county_len = len(county)
    index = 0
    for c in county:
        index += 1
        if c in county_dict.keys():
            county_dict[c] = county_dict[c] + 1
        else:
            county_dict[c] = 1
        
        print_processing_status(index, county_len)
            
    return county_dict # return a dictionary -> Contains unqiue counties and also frequency

def create_plots():
    """Function to create use plots. 
    This function is used handle the user plot module. 
    The function will display a menu for the user to choose a plot from. This will loop until an exit value has been reached.
    The choice the user enters determines the program flow and what plot will be created / saved.

    Raises:
        ValueError: [Raising value error to capture the errors from invalid user input. Use this to print error message and continue in 
        the loop statement.]
    """
    print('''    Welcome to User Graphical Plots.
          You can choose from the following options for plots for sales:''')
    print_user_plot_menu()
    
    pick = 1
    while pick != 10:
        # Take user input : Handle incorrect choice to ensuer program does not terminate
        try:
            pick = int(input("Enter your choice: "))
            if pick == 10:
                continue # contine as loop will break
            
            if pick < 0 or pick > 4:
                raise ValueError
        except ValueError:
            print("You entered an invalid choice.")
            continue
        
        # Handle user selection with processing based on choice.
        if pick == 0:
            print_user_plot_menu()
        elif pick == 1:     # Scatter Plot - Sales over Years
            create_scatter_plot(1)
        elif pick == 2:     # Bar chart - Sales over Years
            create_scatter_plot(2)
        elif pick == 3:                # Bar chart Plot - Sales over Counties
            create_scatter_plot(3)
        else:
            create_scatter_plot(4) # pie chart - Sales Over Years
            
def create_multi_bar(year:str, to_output):
    """Function to generate multiple / single bar charts 
    Parameters are dynamic but linked to TotalSalesPerMonthIn bar chart.

    Args:
        year (str): [Year / Beginning year that is being reviewed at the point in time]
        to_output ([type]): [to_output is a dictionary containing values to be used in the bar chart]
    """
    fig2, ax = plt.subplots()
    fig2.suptitle("Bar Chart")
    
    # Dynamic Name
    figure_name = "TotalSalesPerMonthIn" + year  
    ax.set_title(figure_name)    
    # Bar Chart
    y_pos = [ i for i in range(len(to_output))]
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(to_output.keys())            
    ax.set_ylabel("Date")
    ax.set_xlabel("Total Sales")         
    ax.barh(y_pos, to_output.values(), align="center")
    # Plot the axes
    plt.show()         
    # Dynamic Name
    fig2.savefig(str(figure_name), bbox="tight") 
    print("Plot saved to local directory.")

def create_pie_chart():
    """Function to generate pie chart 

    Pie chart to represent the Sales Over Years and to display percentage on the chart to 2 decimal places for accuracy.
    """
    fig, ax = plt.subplots()
    ax.set_title("Sales Over All Years")

    ax.pie(year_dict.values(), labels = year_dict.keys(), autopct="%.2f%%")
    
    plt.show()
    fig.savefig("SalesOverYearsPieChart", bbox="tight") 
    print("Plot saved to local directory.")

def create_scatter_plot(option: int):

    """Function to handle user input to decide plots to generate.

    """
    # Figures that are permitted are Sales Over Years and Sales Over Counties. 
    # We can utilize the already created dictionaries.
    
    if option == 1:
        # Initialize figure and axes
        fig, ax = plt.subplots()
        fig.suptitle("Scatter Plot")
        ax.set_title("Total Sales over Years")
        ax.set_xlabel("Years")
        ax.set_ylabel("Sales")
        
        ax.scatter(list(year_dict.keys()), list(year_dict.values()), marker=".")
        
        # Plot the axes
        plt.show()
        
        fig.savefig("ScatterSalesAndYears", bbox="tight")
        print("Plot saved to local directory.")
    
    elif option == 2:
        # Initialize figure and axes
        fig2, ax = plt.subplots()
        fig2.suptitle("Bar Chart")
        
        ax.set_title("Total Sales over Counties")
       
        # Bar Chart
        y_pos = [ i for i in range(len(county_dict))]
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(county_dict.keys())
        
        ax.set_ylabel("Counties")
        ax.set_xlabel("Total Sales")
       
        ax.barh(y_pos, county_dict.values(), align="center")
        # Plot the axes
        plt.show()
        
        fig2.savefig("BarChartSalesAndCounties", bbox="tight")
        print("Plot saved to local directory.")
    
    elif option == 3:
        # Initialize figure and axes
        try:    
            year = input("Enter a year / ALL: ")
            
            if year.lower() == "all":
                for yr in yearly_range:            
                    to_output = {k:v for k,v in dates_dict.items() if str(yr) in k}
                    
                    if len(to_output)>0:     
                        create_multi_bar(str(yr), to_output)  
            else:
                # Check for year len to ensure it is 4 characters long:
                if len(year) == 4:                    
                    to_output = {k:v for k,v in dates_dict.items() if year in k}
                    if len(to_output)>0:       
                        create_multi_bar(year, to_output)
                    else:
                        print("No dates which match selection.")
                else:
                    print("Please enter a year in the format of yyyy.")

        except ValueError:
            print("You entered an incorrect year.")     

    elif option == 4:
        create_pie_chart()
    else:
        print("Something went wrong. Option not valid..")
        print("Location: create_scatter_plot()")

def print_user_menu():
    """Function to print user menu for main program.

    """

    print('''    0 - View menu
    1 - Number of records
    2 - Maximum value
    3 - Minimum value
    4 - Mean value
    5 - Median value
    6 - Mode value 
    7 - Standard Deviation
    8 - Extra Data Mining
    9 - Create Graphical Plots
    10 - Exit''')

def print_user_plot_menu():
    """Function to generate user plot menu when processing the plot module.
    """

    print('''    0 - View menu
    1 - Scatter Plot - Sales over Years
    2 - Bar Chart - Sales over Counties
    3 - Bar Chart - Sales Per Month (Specify Year)
    4 - Pie Chart - Sales Per Year 
    10 - Exit''')

############## END OF  Function Definition: ################


########################## Pre-Processing starts here ##########################
try:
    with open("PPR_ALL.csv", encoding="utf-8") as csv_in, open("PPR_OUT.csv", "a") as csv_out:

        # discard first line of headers:
        _ = csv_in.readline()

        # User Message:
        print("Program status: File import - Started..")
        # Read data from csv file into a variable which will accept the list returned from readLines()
        data = csv_in.readlines()
        
        # User Message:
        print(f"Program status: File successfully split into lines. {len(data)} lines recognised..")

        # declare variables for us in program with the file input.
        dos, address, pobox, county, fullmarketprice, vatexcl = [],[],[],[],[],[]
        description, priceList = [],[]

        # index variable -> Program status control
        index = 0
        rows_to_process = select_rows_for_processing(len(data))
       
        # User Message:
        print("Program status: Pre-processing beginning.. ")

        for line in data:
            index += 1

            d = ""
            a = ""
            p = ""
            c = ""
            f = ""
            v = ""
            descr = ""
            price = ""
            
            # Split into an array based on "
            valuesquotes = line.strip().split('"') # strip \n and split on ""
            
            # Date -> Strip the commas from the date value
            d = valuesquotes[0].strip(',') # Remove commas from date value -> needed for analysis.

            # Address -> Processing complete after split()
            a = valuesquotes[1]  

            # Postcode and County Values:
            # Needs splitting -> Contains 4 values , , , , -> only need value 2 and 3
            # County also contains an additional space before the word eg , Kildare,. Need to remove this.
            # Tip: _ character is used as a discard character. We can assign data to this to discard at runtime.
            pob_county = valuesquotes[2] 
            _, p, c, _ = pob_county.split(',')
            c = c.strip()
            
            # Price -> Strip commas (keep decimals) -> Validate Price incase of special characters
            price = valuesquotes[3]
            price = validate_price(price)

            # Full_Market_Price, Vat_Excl and Description:
            # During our initial split on quotes, we now have values in index 4 of valuesquotes that has 4 values split by commas.
            # However we only require the last 3 values for our data analysis. As split requires parameters matching, we can use _ to discard
            # data again and act as a placeholder.
            # We also need to remove spaces from in front of the values too (using strip())
            _, f, v, descr = valuesquotes[4].split(',')
            f = f.strip()
            v = v.strip()
            descr = descr.strip()

            # Once we have the line split completely, we need to now append to our lists.
            dos.append(d), address.append(a), pobox.append(
                p),  county.append(c), fullmarketprice.append(f)
            vatexcl.append(v), description.append(
                descr), priceList.append(price)
            
            # Processing Status Information
            if print_processing_status(index, rows_to_process):
                break

        else:
            print("Completed..")


        # Calculate Price Frequency
        pricefreq_dict  = calculate_price_frequency(priceList)

        # User Message:
        print()
        print("Program status: Beginning further data processing:")
        ################# Begin processing for User Menu Data: #################
        ################# Option 1, 2, 3 -> Number of Records, Max of Pricelist, Min of Pricelist
        sum_of_pricelist, length_of_pricelist, max_of_pricelist, min_of_pricelist = total_price_values(priceList)
        print("Processing status: 1.Data Count - Completed..")
        print("Processing status: 2.Maximum Price Determination - Completed.. ")
        print("Processing status: 3.Minimum Price Determination - Completed.. ")

        ################# Option 4 - > Mean of pricelist
        # Mean value for this data set is based on the sum of the prices (total) / the total number of months or years
        # Date format is dd/mm/yyyy
        # We want to take the first and last value in the DOS list.
        # We can then do a substring on this value, convert to integer and get perform a calculation to get the total amounts
        # for months and years. We can plug these values into our calculations.
        date_values = get_date_values(dos)
        mean_months = mean_of_pricelist(priceList, date_values['Total Months'])
        mean_years = mean_of_pricelist(priceList, date_values['Total Years'])
        print("Processing status: 4.Mean Data Determination - Completed.. ")

        ################# Option 5 -> Median of Pricelist
        # Find the mid-point of the list
        mid_index, mid_pricelist = calculate_median_of_pricelist(length_of_pricelist, priceList)
        print("Processing status: 5.Median Data Determination - Completed.. ")

        ################# Option 6 -> MODE of PriceList
        # pricefrequency calculated above already by calculate_price_frequency()
        print("Processing status: 6.Mode Data Determination - Completed.. ")

        ################# Option 7
        # Because we have done mean values based on year, month and pricing, we should include this here.
        price_std_dev, month_std_dev, year_std_dev = calculate_standard_deviation(priceList, sum_of_pricelist, length_of_pricelist, date_values["Total Months"], date_values["Total Years"]) 

        ################# Option 8 -> EXTRA PROCESSING INFORMATION
        print("Processing status: 8.Additional Data Determination - Beginning.. ")
        year_dict, yearly_range, year_most_houses_sold, year_least_houses_sold = calculate_yearly_house_sales(priceList, dos, date_values) 
        print("Processing status: 8. - Yearly Range Statistics - Completed..")
        
        # Countys -> Create dictionary of countys from data and freq of total sold for each county 
        county_dict = calculate_county_sales(county)
        
        print("Processing status: 8. - County Statistics - Completed..")

        # User Message:
        print("Processing status: 8. - Monthly Statistics - Beginning..")
        # Months -> Most Common Month
        dates_dict = calculate_most_month_of_sale(dos)
        print("Processing status: 8. - Monthly Statistics - Completed..")
        print("Processing status: 8.Additional Data Determination - Completed.. ")

        # With all price amounts split into 
        year_month_most_sales_index = priceList.index(max_of_pricelist)
        year_month_least_sales_index = priceList.index(min_of_pricelist)
        # After we have the index with the most / least expensive amount,we can return the date of this sale:
        year_month_most_sales_dos = dos[year_month_most_sales_index]
        year_month_least_sales_dos = dos[year_month_least_sales_index]

        ################################################################
        # Finally, output some data to a file of the mentioned results:
        out_header = ["Total Sales €", "Max Sale €", "Min Sales €", "Mean Sales €", "Mode Sales €", "Standard Dev Of Price €"]
        out_data = [sum_of_pricelist, max_of_pricelist, min_of_pricelist, (sum_of_pricelist/length_of_pricelist), (max(pricefreq_dict, key=pricefreq_dict.get), max(pricefreq_dict)), price_std_dev]
        csv_out.write("Data Processing -> Rows processed: " + str(rows_to_process) + "\n")
        csv_out.write(str(out_header) + "\n")
        csv_out.write(str(out_data) + "\n")
        csv_out.write("\n")

        print("Processing Status: Ouput file created - PPR_OUT.csv")
        # User Message:
        print()
        print("Program status: pre-processing completed..")

except FileNotFoundError:
    print("Opps. File not found. Check location.")
    exit(0)
except FileExistsError:
    print("File not found. Check location.")
    exit(0)
except IsADirectoryError:
    print("Path is a directory and NOT a file.")
    exit(0)
except PermissionError:
    print(PermissionError)
    exit(0)
except ValueError:
    print(ValueError)
    print("Error occurring during assignment of value. See index: ", index)
    print(valuesquotes)
    exit(0)
except TypeError:
    print("Type assignment error. Error: ", TypeError)
    exit(0)
except KeyboardInterrupt:
    print("Program stopped by user key interrupt.")
    exit(0)
except ZeroDivisionError:
    print("Program has run into an error.")
    print(ZeroDivisionError)
    exit(0)
else:
    print("File has been imported to program.")
    print()
finally:
    print("You can now analyse the data.")

########################## Pre-Processing ENDS here ##########################


########################## Data Processing starts here ##########################
# User Menu:
print()
print("Welcome to Data Processing of PPR_ALL.csv!")
print(f"You can analyse the property prices since {date_values['First Dos']} - {date_values['Last Dos']}.")
print_user_menu()

# Setting a default value for pick for control loop.
pick = 1
while pick != 10:
    try:
        # Take user input : Handle incorrect choice to ensuer program does not terminate
        try:
            print()
            pick = int(input("Enter your choice: "))
            if pick == 10:
                continue # contine as loop will break
            
            if pick < 0 or pick > 9:
                raise ValueError
        except ValueError:
            print("You entered an invalid choice.")
            continue
        
        # Handle user selection with processing based on choice.
        if pick == 0:
            print_user_menu()
        elif pick == 1:  # Number of records
            print(f"Number of records   :    {length_of_pricelist}")
            print(f"Total Euros :   €{sum_of_pricelist:.2f}")
        elif pick == 2:  # Max value
            print(f"Maximum value of    :   €{max_of_pricelist:.2f}")
        elif pick == 3:  # Min value
            print(f"Minimum value of    :   €{min_of_pricelist:.2f}")
        elif pick == 4:  # Mean value
            print(f"You are checking the mean values between {date_values['First Dos']} and {date_values['Last Dos']}")
            # Check for 0 divisble numbers: -> If 0, then we are only checking 1 month values. There is no average of months available.
            if mean_months == sum_of_pricelist:
                print(f"Mean value (1 month(s)) of   :    €{mean_months:.2f}") 
            else:
                print(f"Mean value ({date_values['Total Months']} months) of   :    €{mean_months:.2f}") 
            
            # If total years is = 0, then we are only viewing sales in 1 year (12 months) -> No output necessary
            if date_values['Total Years'] > 0:
                print(f"Mean value ({date_values['Total Years']} years) of    :   €{mean_years:.2f}") 
            
            # Give an average value of sale based on the amount of sales and the total cost 
            print(f"Mean value (per sale)[sum/total sales] of    :   €{sum_of_pricelist / length_of_pricelist:.2f}") 
        elif pick == 5:  # Median value
            print("Median value of  : €", mid_pricelist , " at index: ", mid_index)
        elif pick == 6:  # Mode value
            print("Mode Value:")
            print("Price        |       Frequency")
            print(f"€{max(pricefreq_dict, key=pricefreq_dict.get)}     |       {max(pricefreq_dict.values())}")
        elif pick == 7:  # Standard deviation
            print(f"Standard Deviation for price lists: {price_std_dev:.2f}")
            if date_values['Total Months'] > 0:
                print(f"Standard Deviation for price (monthly): {month_std_dev:.2f}")
            if date_values['Total Years'] > 0:
                print(f"Standard Deviation for price (yearly): {year_std_dev:.2f}")
        elif pick == 8: # Extra Data Mining
            print("Extra Data Mining:")
            print("Years with Sales  / Total Sales / Year:")
            print(f"{yearly_range}")
            print(f"{year_dict}")
            print(f"Year of most houses sold: {year_most_houses_sold}")
            print(f"Year of least houses sold: {year_least_houses_sold}")
            print(f"Month/Year most houses sold: {max(dates_dict, key=dates_dict.get)} with {max(dates_dict.values())}")
            print(f"Month/Year least houses sold: {min(dates_dict, key=dates_dict.get)} with {min(dates_dict.values())}")
            print(f"Highest Money Price Paid - Year / Price: {(year_month_most_sales_dos)} €{max_of_pricelist:.2f} - (Address/Description: {address[year_month_most_sales_index]}, {county[year_month_most_sales_index]}/ {description[year_month_most_sales_index]})")
            print(f"Lowest Money Price Paid - Year / Price: {(year_month_least_sales_dos)} €{min_of_pricelist:.2f} - (Address/Description: {address[year_month_least_sales_index]}, {county[year_month_least_sales_index]} / {description[year_month_least_sales_index]})")
            print()
            print(f"Counties with House Sales:\n{sorted(county_dict)}\n")
            print(f"County with most properties sold: {max(county_dict, key=county_dict.get)} with {max(county_dict.values())}")
            print(f"County with least properties sold: {min(county_dict, key=county_dict.get)} with {min(county_dict.values())}")
        else: # Visualization using Plots
            create_plots()
            print_user_menu()
            
    except KeyboardInterrupt:
        print("Program stopped by user key interrupt.")
        pick = 10

else:
    print("\nThank you for reviewing the data. Program finished.")

print()

########################## Data Processing ENDS here ##########################
