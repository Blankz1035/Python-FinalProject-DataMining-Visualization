# Python-FinalProject-DataMining-Visualization
 Final year project for semester 1 of post grad. Analysis and mining performed on Property Price Index in Ireland.

## Introduction
This was a final year project for Semester 1 of my post graduate. The aim of this project was to design and develop an application which would incorporate certain features at each stage of the module. This would range from the following:

1. Initially finding a dataset and creating design plan and reason for choice.
2. Stage 1 - Program with:
    * File input
    * Conditional Structures
    * Repetition Statements
    * Lists and Tuples and Sets
    * Exception Handling
3. Stage 2 - Program with:
    * Include stage 1
    * Functions
    * File output
    * Matplot - Charts, Plots
    * Dictionaries
4. Extensive documentation on the program, features and use cases.

## How to use this application
To use this application you will need to download _separately_ the CSV file from https://www.propertypriceregister.ie/.
You should download the CSV file which incorporates _ALL_ the records in the data source. 

### Data Preparation
* You should scrum the column "Property Size Description" from the file download. This field is redundant due to a large amount of missing data.
* Save the file with the name :

Thats it! The rest is taken care of.

Note: The following code will be responsible for reading and outputing the file results. Ensure you have placed the csv file into the correct location:

`
    with open("PPR_ALL.csv", encoding="utf-8") as csv_in, open("PPR_OUT.csv", "a") as csv_out:
`

## Enhancements and Discoveries
During the development lifecycle of this application, I learnt many different things with regards to performance and efficiency using python. I learnt that in many situations, the use of dictionaries in python are more performant that a list, and even more performant than a repetition statement. Through external research I also learnt that dictionaries do however take more memory in a process, but in a program such as this there is no problems and the performance speed out-weighs the memory use.

I learnt how to efficiently utilize exception based development and functions. In other programs I have built, this is very important to providing the user with meaningful information on a program termination or "dump". 

One of the biggest enhancements that I implemented into this program was the use of dictionary comprehensions vs lists. This played well into some places in the program when pre-processing the data. A good example of this is when I am splitting my data into usable data structures. In multiple places, I loop through lists of "split" data and create dictionaries for frequencies of values. As indexing with dictionaries is a lot faster than indexing in lists, the program speed was enhanced. 

```
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
```

## Sample Output
I designed the program with a strong focus on UX and functionality.  Let us look at some of the output from the program:

```
Program status: File import - Started..
Program status: File successfully split into lines. 438759 lines recognised..

Would you like to process all records? y/n: y
Program status: Pre-processing beginning.. 
Processing Status: 5% complete..
Processing Status: 10% complete..
Processing Status: 20% complete..
Processing Status: 30% complete..
Processing Status: 40% complete..
Processing Status: 50% complete..
Processing Status: 60% complete..
Processing Status: 70% complete..
Processing Status: 80% complete..
Processing Status: 90% complete..
Processing Status: 100% complete..

Calculating frequency of pricing data [27860 unique prices of 438759 sales]..
Processing Status: 5% complete..
Processing Status: 10% complete..
Processing Status: 20% complete..
Processing Status: 30% complete..
Processing Status: 40% complete..
Processing Status: 50% complete..
Processing Status: 60% complete..
Processing Status: 70% complete..
Processing Status: 80% complete..
Processing Status: 90% complete..
Processing Status: 100% complete..

Program status: Beginning further data processing:
Processing status: 1.Data Count - Completed..
Processing status: 2.Maximum Price Determination - Completed.. 
Processing status: 3.Minimum Price Determination - Completed.. 
Processing status: 4.Mean Data Determination - Completed.. 
Processing status: 5.Median Data Determination - Completed.. 
Processing status: 6.Mode Data Determination - Completed.. 
Processing status: 8.Additional Data Determination - Beginning.. 
Processing status: 8. - Yearly Range Statistics - Completed..
Processing Status: 5% complete..
Processing Status: 10% complete..
Processing Status: 20% complete..
Processing Status: 30% complete..
Processing Status: 40% complete..
Processing Status: 50% complete..
Processing Status: 60% complete..
Processing Status: 70% complete..
Processing Status: 80% complete..
Processing Status: 90% complete..
Processing Status: 100% complete..
Processing status: 8. - County Statistics - Completed..
Processing status: 8. - Monthly Statistics - Beginning..
Processing Status: 5% complete..
Processing Status: 10% complete..
Processing Status: 20% complete..
Processing Status: 30% complete..
Processing Status: 40% complete..
Processing Status: 50% complete..
Processing Status: 60% complete..
Processing Status: 70% complete..
Processing Status: 80% complete..
Processing Status: 90% complete..
Processing Status: 100% complete..
Processing status: 8. - Monthly Statistics - Completed..
Processing status: 8.Additional Data Determination - Completed.. 
Processing Status: Ouput file created - PPR_OUT.csv

Program status: pre-processing completed..
File has been imported to program.

You can now analyse the data.

Welcome to Data Processing of PPR_ALL.csv!
You can analyse the property prices since 01/01/2010 - 09/10/2020.
    0 - View menu
    1 - Number of records
    2 - Maximum value
    3 - Minimum value
    4 - Mean value
    5 - Median value
    6 - Mode value 
    7 - Standard Deviation
    8 - Extra Data Mining
    9 - Create Graphical Plots
    10 - Exit

``` 


## Conclusions
The project development was a great success. The program output is able to provide detailed information on all areas I had wanted to analyse and mine from the data source. I learnt a lot in this program and looking forward to the next stages of development with regression, classification  and using ML techniques.

