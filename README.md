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
During the development lifecycle of this application, I learnt many different things with regards to performance and efficiency using python.



