#!/usr/bin/env python

'''Convert height and weight to metric. NA converted to NULL for SQL '''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file, designates columns to convert to metric and current units")
    parser.add_argument("-f", "--filename", help="name of csv file",
                        required=True, type=str)
    parser.add_argument("-c", "--columns", action='append', help="columns to convert, column per -c",
                        required=True, type=int)
    parser.add_argument("-u", "--units", action='append', help="current units to be converted, 'oz' or 'inch'",
                        required=True, type=str)
    return parser.parse_args()

def inch_to_cm(height):
    '''(str)->float
    This fxn converts inches to cm. Blank columns designated with
    NA will be converted to NULL.
    >>>inch_to_cm('10')
    25.4
    >>>inch_to_cm('NA')
    'NULL'
    '''
    if height != 'NA' and height != 'NULL': #avoid non-numic values
        height=float(height)*2.54 #conversion factor
    elif height == 'NA':
        height = 'NULL'
    return height

def oz_to_kg(weight):
    '''(str)->float
    This fxn converts ounces to kg. Blank columns designated with
    NA will be converted to NULL.
    >>>oz_to_kg('529.11')
    15
    >>>oz_to_kg('NA')
    'NULL'
    '''
    if weight == 'NA':
        weight = 'NULL'
    elif weight != 'NULL': #avoid non-numeric values
        weight=float(weight)/35.274 #conversion factor
    return weight

def convert(file, cols, unit):
    '''(file,list,str) -> file
    This fxn reads in csv, and converts specified columns values to
    metric units. Ounces to kg and inches to cm. NA is also coverted
    to NULL. Uses fxns oz_to_kg and inch_to_cm'''
    # Use original filename & path to build output filename & path
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    ln = 0 # init line count
    # Open original file to edit write changes in new file
    with open(file) as o_data, open(new_file, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',') #split csv into list by columns
            if ln == 1: # header line
                newline = entry # no conversions necessary
            else:
                # Iterate through specified columns to convert
                for i in range(len(cols)):
                    value = entry[cols[i]-1]
                    if unit[i] == 'oz':
                        entry[cols[i]-1] = oz_to_kg(value)
                    elif unit[i] == 'inch':
                        entry[cols[i]-1] = inch_to_cm(value)
                    else:
                        print('Error: invalid units')
            # Convert list back to csv line and write to newfile
            newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None

def main():
    '''runs metric conversion fxns from above using argparse
    provided specifications'''
    args = get_arguments()
    convert(args.filename,args.columns,args.units)
    return None

if __name__ == '__main__':
    main()
