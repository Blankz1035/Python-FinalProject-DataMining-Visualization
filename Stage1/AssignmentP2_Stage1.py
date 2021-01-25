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
    
    File Input:  
        CSV File PPR_ALL.csv

    Columns:
        Date of Sale (dd/mm/yyyy),Address,Postal Code,County,Price (�),Not Full Market Price,VAT Exclusive,
        Description of Property,Property Size Description
"""


from string import ascii_letters
import math

########################## Pre-Processing starts here ##########################
try:
    with open("6_Lect_Exercises/PPR_ALL.csv", encoding="utf-8") as csv_in, open("6_Lect_Exercises/PPR_OUT.csv", "a") as csv_out:

        # discard first line of headers:
        _ = csv_in.readline()

        # User Message:
        print("Program status: File import - Started..")
        # Read data from csv file into a variable which will accept the list returned from readLines()
        data = csv_in.readlines()
        
        # User Message:
        print(f"Program status: File successfully split into lines. {len(data)} lines recognised..")

        # declare variables for us in program with the file input.
        dos = []
        address = []
        pobox = []
        county = []
        fullmarketprice = []
        vatexcl = []
        description = []
        priceList = []

        # Frequency of pricing
        pricefrequency = []

        # index variable -> Program status control
        index = 0
        rows_to_process = len(data)
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

        # User Message:
        print("Program status: Pre-processing beginning.. ")

        for line in data:
            index += 1
            # if index == 1:
            #     continue
            
            # Unnecessary assignment to line variable now that i have removed a column from the data source -> Size of property.
            # Removed as the majority of the data is missing from data source anyway!

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
            
            # Price -> Strip commas (keep decimals). 
            price = valuesquotes[3]
            # Need to further check and remove any invalid characters not in ASCII
            # if ',' in price:
            price = price.replace(',', "")
                
            # Full_Market_Price, Vat_Excl and Description:
            # During our initial split on quotes, we now have values in index 4 of valuesquotes that has 4 values split by commas.
            # However we only require the last 3 values for our data analysis. As split requires parameters matching, we can use _ to discard
            # data again and act as a placeholder.
            # We also need to remove spaces from in front of the values too (using strip())
            _, f, v, descr = valuesquotes[4].split(',')

            f = f.strip()
            v = v.strip()
            descr = descr.strip()

            # Pricing Validation -> Need to convert to a number for analysis
            for character in price:    
                # Check character validity -> issue solved with diamond questionmark invalid character throwing error 
                # as cast to float fails!
                if not character.isascii() and not character.isalpha() and not character.isdigit() or character == '€':
                    price = price.replace(character, "")
                    continue
                
            # After processing the line, make ammendments to the number values:
            try:
                price = float(price)
            except ValueError:
                print(f"Problem converting price ({price}) to a float value. Line: 105 and index{index}")

            # Once we have the line split completely, we need to now append to our lists.
            dos.append(d), address.append(a), pobox.append(
                p),  county.append(c), fullmarketprice.append(f)
            vatexcl.append(v), description.append(
                descr), priceList.append(price)

            # Loading % for user - data preparation
            if int(rows_to_process * 0.25) == index:
                print("Processing Status: 25% complete..")
            if int(rows_to_process * 0.50) == index:
                print("Processing Status: 50% complete..")
            if int(rows_to_process * 0.75) == index:
                print("Processing Status: 75% complete..")
            if int(rows_to_process) == index:
                print("Processing Status: 100% complete..")
            
            if index == rows_to_process:
                break
        else:
            print("Completed..")

        # price frequency - > get a shortened version of list for later MODE check. Original way was counting for every single element 
        # even duplicates.
        # Issue being faced here is the runtime when counting. We are performing a county on every single element in pricelist n times.
        # Possible more efficient to remove the element after looping over it or have a more filtered looping approach.
        index = 0  # set index again to 0 for progress for pricing
        uniquePrice = set(priceList)     
        checkedPrice = []
        temporary_price_list = sorted(list(priceList))

        counter = 0
        print()
        print(f"Calculating frequency of pricing data [{len(uniquePrice)} unique prices of {len(priceList)} sales]..")
        for prc in sorted(uniquePrice):  
            index +=1
            checkedPrice.append(prc)    # Use to index set price. Cannot index set values.

            for pl in temporary_price_list:
                if prc == pl:
                    counter += 1
                else:
                    break
            
             # Now remove the price from the temporary list. We want to do this as the price has now been checked, so we dont want to keep repeating the process for max length
            if counter != 0:            
                pricefrequency.append(counter)
                temporary_price_list = temporary_price_list[counter:]
                counter = 0

            #temporary_price_list = [x for x in temporary_price_list if x != prc]

            # Loading % for user - pricing frequency preparation
            if int(len(uniquePrice) * 0.05) == index:
                print("Processing Status: 5% complete..")
            if int(len(uniquePrice) * 0.10) == index:
                print("Processing Status: 10% complete..")
            if int(len(uniquePrice) * 0.20) == index:
                print("Processing Status: 20% complete..")
            if int(len(uniquePrice) * 0.30) == index:
                print("Processing Status: 30% complete..")
            if int(len(uniquePrice) * 0.40) == index:
                print("Processing Status: 40% complete..")
            if int(len(uniquePrice) * 0.50) == index:
                print("Processing Status: 50% complete..")
            if int(len(uniquePrice) * 0.60) == index:
                print("Processing Status: 60% complete..")
            if int(len(uniquePrice) * 0.70) == index:
                print("Processing Status: 70% complete..")
            if int(len(uniquePrice) * 0.80) == index:
                print("Processing Status: 80% complete..")
            if int(len(uniquePrice) * 0.90) == index:
                print("Processing Status: 90% complete..")
            if len(uniquePrice) == index:
                print("Processing Status: 100% complete..")
        else:
            print("Completed..")
        # User Message:
        print()
        print("Program status: Beginning further data processing:")

        ################# Begin processing for User Menu Data: #################
        ################# Option 1 -> Number of Records
        length_of_pricelist = len(priceList)
        sum_of_pricelist = sum(priceList)
        # User Message:
        print("Processing status: 1.Data Count - Completed..")
        ################# Option 2 -> Max of Pricelist
        max_of_pricelist = max(priceList)
        # User Message:
        print("Processing status: 2.Maximum Price Determination - Completed.. ")
        ################# Option 3 -> Min of Pricelist
        min_of_pricelist = min(priceList)
        # User Message:
        print("Processing status: 3.Minimum Price Determination - Completed.. ")
        ################# Option 4 - > Mean of pricelist
        # Mean value for this data set is based on the sum of the prices (total) / the total number of months or years
        # Date format is dd/mm/yyyy
        # We want to take the first and last value in the DOS list.
        # We can then do a substring on this value, convert to integer and get perform a calculation to get the total amounts
        # for months and years. We can plug these values into our calculations.
        total_months = 0
        total_years = 0

        first_dos = dos[0]
        last_dos = dos[len(dos)-1]

        # Now we have the string values of first and last dos. Split these into month and year.
        first_dos_mon = int(first_dos[3:5])
        first_dos_year = int(first_dos[6:])

        last_dos_mon = int(last_dos[3:5])
        last_dos_year = int(last_dos[6:])

        # Determine how many months are used in the first year: Eg. starting in may (month 5 -> So we need to take 5 away from total but add any month after final year)
        total_years = last_dos_year - first_dos_year

        if total_years > 0:
            total_months = (12 * total_years) + last_dos_mon - first_dos_mon  # eg: 2020 - 2010 = 10yrs  + 9 months -(months of 1st year)
        else:
            total_months = last_dos_mon - first_dos_mon

        # User Message:
        print("Processing status: 4.Mean Data Determination - Completed.. ")

        ################# Option 5 -> Median of Pricelist
        # Find the mid-point of the list
        mid_index = int(length_of_pricelist / 2) 

        if length_of_pricelist % 2 == 1:
            mid_pricelist = priceList[mid_index]
        else:
            mid_pricelist = (priceList[mid_index -1] + priceList[mid_index]) / 2
        
        # User Message:
        print("Processing status: 5.Median Data Determination - Completed.. ")
        ################# Option 6 -> MODE of PriceList
        # pricefrequency calculated above already.
        freq_index = pricefrequency.index(max(pricefrequency))

        # User Message:
        print("Processing status: 6.Mode Data Determination - Completed.. ")

        ################# Option 7
        # Because we have done mean values based on year, month and pricing, we should include this here.
        # Deviations:
        price_deviations = [ ((x - (sum_of_pricelist / length_of_pricelist)) **2) for x in priceList]

        # If months is not = 0
        if total_months > 0:
            month_deviations = [ ((x - (sum_of_pricelist / total_months)) **2) for x in priceList]
            month_std_dev = math.sqrt(sum(month_deviations)/(total_months -1))

        # Year: Only if total years is > 0 do we caculate.
        if total_years > 0:
            year_deviations = [ ((x - (sum_of_pricelist / total_years)) **2) for x in priceList]
            year_std_dev = math.sqrt(sum(year_deviations)/(total_years -1))


        # Calculate deviation for price
        price_std_dev = math.sqrt(sum(price_deviations)/(length_of_pricelist -1))

        ################# Option 8 -> EXTRA PROCESSING INFORMATION
        # User Message:
        print("Processing status: 8.Additional Data Determination - Beginning.. ")
        yearly_house_sales = []
        yearly_range = list(range(first_dos_year, last_dos_year +1))
        indexes = []
        # Yearly Range Indexes for amount of sales per year.
        for year in yearly_range:
            amount_per_year = len([i for i in dos if str(year) in i])         
            yearly_house_sales.append(amount_per_year)
            
            if len(yearly_house_sales) == 1:
                starting = 0
                indexes.append(sum(priceList[starting:amount_per_year-1]))
                starting = amount_per_year
            else:
                indexes.append(sum(priceList[starting:amount_per_year-1]))
                starting = amount_per_year

        # User Message:
        print("Processing status: 8. - Yearly Range Statistics - Completed..")
        # Countys -> Create unique list of countys from data and then an index of total sold for each county
        unique_countys = set(county) 
        countys = list(sorted(unique_countys))    
        county_sales_index = list()

        for c in countys:
            county_sales_index.append([len([i for i in county if str(c) in i])])

        # User Message:
        print("Processing status: 8. - County Statistics - Completed..")

        # User Message:
        print("Processing status: 8. - Monthly Statistics - Beginning..")
        # Months -> Most Common Month
        unique_dates = set(dos)  # unique amounts of dates across all records.
        dates_index = list()
        checked_dates = list()

        index = 0
        counter = 0

        for u_date in unique_dates:
            # Set the date checking to only contain the month. Not interested in a specific day.
            u_date = u_date[3:]
            
            if u_date not in checked_dates:
                # try to split the search to not have to search all elements in the dos list -> that is an ordered list.     
                for date in dos:
                    if u_date in date[3:]:
                        counter += 1

                    if u_date[3:] != date[6:]:
                        break
                
                dates_index.append(counter)
                checked_dates.append(u_date)
                
                counter = 0
            
            index += 1

            # Loading % for user - months mode preparation
            if int(len(unique_dates) * 0.25) == index:
                print("Processing Status: 25% complete..")
            if int(len(unique_dates) * 0.50) == index:
                print("Processing Status: 50% complete..")
            if int(len(unique_dates) * 0.75) == index:
                print("Processing Status: 75% complete..")
            if len(unique_dates) == index:
                print("Processing Status: 100% complete..")

        # User Message:
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
        out_data = [sum_of_pricelist, max_of_pricelist, min_of_pricelist, (sum_of_pricelist/length_of_pricelist), (checkedPrice[freq_index], max(pricefrequency)), price_std_dev]
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
print(f"You can analyse the property prices since {first_dos} - {last_dos}.")
print('''    0 - View menu
    1 - Number of records
    2 - Maximum value
    3 - Minimum value
    4 - Mean value
    5 - Median value
    6 - Mode value 
    7 - Standard Deviation
    8 - Extra Data Mining
    10 - Exit''')

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
            
            if pick < 0 or pick > 8:
                raise ValueError
            print()
        except ValueError:
            print("You entered an invalid choice.")
            continue
        
        # Handle user selection with processing based on choice.
        if pick == 0:
            print('''    0 - View menu
        1 - Number of records
        2 - Maximum value
        3 - Minimum value
        4 - Mean value
        5 - Median value
        6 - Mode value 
        7 - Standard Deviation
        8 - Extra Data Mining
        10 - Exit''')
        elif pick == 1:  # Number of records
            print(f"Number of records   :    {length_of_pricelist}")
            print(f"Total Euros :   €{sum_of_pricelist:.2f}")
        elif pick == 2:  # Max value
            print(f"Maximum value of    :   €{max_of_pricelist:.2f}")
        elif pick == 3:  # Min value
            print(f"Minimum value of    :   €{min_of_pricelist:.2f}")
        elif pick == 4:  # Mean value
            print(f"You are checking the mean values between {first_dos} and {last_dos}")

            # Check for 0 divisble numbers: -> If 0, then we are only checking 1 month values. There is no average of months available.
            if total_months == 0:
                print(f"Mean value (1 month(s)) of   :    €{sum_of_pricelist:.2f}") 
            else:
                print(f"Mean value ({total_months} month) of   :    €{sum_of_pricelist / total_months:.2f}") 
            
            # If total years is = 0, then we are only viewing sales in 1 year (12 months) -> No output necessary
            if total_years > 0:
                print(f"Mean value (per year) of    :   €{sum_of_pricelist / total_years:.2f}") 
            
            # Give an average value of sale based on the amount of sales and the total cost 
            print(f"Mean value (per sale)[sum/total sales] of    :   €{sum_of_pricelist / length_of_pricelist:.2f}") 
        elif pick == 5:  # Median value
            print("Median value of  : €", mid_pricelist , " at index: ", mid_index)
        elif pick == 6:  # Mode value
            #freq = [priceList.count(x) for x in priceList]
            # display the frequencies of each value:
            print("Mode Value:")
            print("Price        |       Frequency")
            print(f"€{checkedPrice[freq_index]}     |       {max(pricefrequency)}")
        elif pick == 7:  # Standard deviation
            print(f"Deviations of from Mean for Prices: {sum(price_deviations)/(length_of_pricelist):.2f}")
            print(f"Standard Deviation for price lists: {price_std_dev:.2f}")
            print()
            if total_months > 0:
                print(f"Deviations based on monthly mean.: {sum(month_deviations)/(total_months):.2f}")
                print(f"Standard Deviation for price (monthly): {month_std_dev:.2f}")
                print()
            if total_years > 0:
                print(f"Deviations based on yearly mean: {sum(year_deviations)/(total_years):.2f}")
                print(f"Standard Deviation for price (yearly): {year_std_dev:.2f}")
        else: 
            print("Extra Data Mining:")
            print(f"{yearly_range}")
            print(f"{yearly_house_sales}")
            print(f"Year of most houses sold: {yearly_range[yearly_house_sales.index(max(yearly_house_sales))]}")
            print(f"Year of least houses sold: {yearly_range[yearly_house_sales.index(min(yearly_house_sales))]}")
            print(f"Month/Year most houses sold: {checked_dates[dates_index.index(max(dates_index))]}")
            print(f"Month/Year least houses sold: {checked_dates[dates_index.index(min(dates_index))]}")
            print(f"Highest Money Price Paid - Year / Price: {(year_month_most_sales_dos)} €{max_of_pricelist:.2f} - (Address/Description: {address[year_month_most_sales_index]}, {countys[county_sales_index.index(max(county_sales_index))]} / {description[year_month_most_sales_index]})")
            print(f"Lowest Money Price Paid - Year / Price: {(year_month_least_sales_dos)} €{min_of_pricelist:.2f} - (Address/Description: {address[year_month_least_sales_index]}, {countys[county_sales_index.index(min(county_sales_index))]} / {description[year_month_least_sales_index]})")
            print()
            print(f"Counties with House Sales:\n{countys}\n")
            print(f"County with most properties sold: {countys[county_sales_index.index(max(county_sales_index))]} with {max(county_sales_index)}")
            print(f"County with least properties sold: {countys[county_sales_index.index(min(county_sales_index))]} with {min(county_sales_index)}")

    except KeyboardInterrupt:
        print("Program stopped by user key interrupt.")
        pick = 10

else:
    print("\nThank you for reviewing the data. Program finished.")

print()

########################## Data Processing ENDS here ##########################
