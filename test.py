import pandas as pd
import re
import os.path
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot
import seaborn as sns

# function to disply operation option


def operationOption():
    print('\nOptions:\n\t 1 - Input a CSV file and convert it to JSON')
    print('\t 2 - Input a CSV file and generate a SQL insert statement')
    print('\t 3 - Input a CSV file and present a data summary')
    print('\t 0 - Quit')

# function to get desired operation option from user


def operationNumber():
    operation_err = "\nYou must enter the number between 1 to 3! Try again."

    # user can continue only after selecting valid input
    while True:
        try:
            # initiate operation number, default = 0
            operation_number = 0
            # printing operation options
            operationOption()
            operation_number = int(
                input('Please select the operation number '))                   # get operation number from user
            if operation_number >= 0 and operation_number <= 3:
                # showing user what they have selected
                print('\nYou have selected operation ' + str(operation_number))
                # return operation number
                return int(operation_number)
            else:
                print(operation_err)
        except ValueError:
            print(operation_err)
    else:
        print(operation_err)


def getValidPath(check="", statement="", stype="file"):
    """

    function to check wether provided valid file or folder path 

    input
    ----------------------------
    check: takes file extension .csv,.json as input 
    statement: takes message to show users what input is desired 
    stype: selection type either file or directory; default = file

    output
    ----------------------------
    return valid filepath
    """
    path_err = f"\nYou must enter the valid {stype} path"
    while True:
        try:
            filepath = ''
            filepath = input(statement)
            if (stype == "file" and os.path.isfile(filepath)):
                if check != "" and os.path.splitext(filepath)[-1].lower() != check.lower():
                    print(path_err + f'with {check} file extension')
                else:
                    return filepath
            elif (stype == "directory" and os.path.isdir(filepath)):
                return filepath
            else:
                print(path_err)
        except ValueError:
            print(path_err)
    else:
        print(path_err)


# initial statement
print('please select the operation you wants to perfrom from below list\n')
# setting operating state to true
operating = True

# code execute recursively for continues operation
while operating:
    # setting initial operation value to 0
    operation = 0
    # ask user for choice of operation
    operation_no = int(operationNumber())

    # operation 1 - Input a CSV file and convert it to JSON
    if operation_no == 1:
        filepath = getValidPath(
            check=".csv", statement="please enter csv file path ", stype="file")  # getting valid csv file path

        # saparating path and file name from input
        head, tail = os.path.split(filepath)

        # creating path to save json file
        savepath = head+'\\'+tail[:-3]+'json'
        df = pd.read_csv(
            filepath, sep=",", index_col=False, header=0)                       # reading csv file with pandas

        # converting csv file to json file
        df.to_json(savepath, orient='records')

        # providing output path
        print(f'File saved at {savepath}')

        # jsonpath = getValidPath(
        #     statement="please enter folder path ", stype="directory")
        # with open(savepath, 'w') as f:
        #     f.write(df.to_json(orient='records')

    # operation 2 - Input a CSV file and generate a SQL insert statement
    elif operation_no == 2:
        filepath = getValidPath(
            check=".csv", statement="please enter csv file path ", stype="file")  # getting valid csv file path

        # saparating path and file name from input
        head, tail = os.path.split(filepath)

        # creating path to save sql file
        savepath = head+'\\'+tail[:-3]+'sql'

        # reading csv file with pandas
        df = pd.read_csv(filepath)

        TableName = "sandbox_installs"

        # insert statement tablename and column name string
        txt = f'INSERT INTO dbo.{TableName}({",".join(df.columns)}) VALUES\n'

        values_string = ''

        # generating value string by iterating though dataframe
        for row in df.itertuples(index=False, name=None):

            # replacing nan values with null in tuple
            values_string += re.sub(r'nan', 'null', str(row))

            # adding comma at the end of tuple
            values_string += ',\n'

        # creating final input statement
        final = txt + values_string[:-2] + ';'

        # open sql file to write query in write mode
        with open(savepath, 'w', encoding="utf-8") as f:
            f.write(final)

        # providing output path
        print(f'File saved at {savepath}')

    # operation 2 - Input a CSV file and present a data summary
    elif operation_no == 3:

        # Read CSV using padas
        df = pd.read_csv("sandbox-installs.csv")

        # drop empty colums with threshold of 60%
        df = df.dropna(thresh=df.shape[0]*0.4, how='all', axis=1)

        # Device OS and User Account Source
        f1 = plt.figure(1, figsize=[10, 6])
        # countplot of device os and user account source
        sns.countplot(x='device_os', hue="ua_source", data=df)
        # set title of graph
        plt.title('User Destribution by OS')
        # for adjusting ledgend outside of chart box
        plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0)
        # define x axis label
        plt.xlabel('Operating Systems')
        # define y axis label
        plt.ylabel('User Count')
        # saving plot as image
        plt.savefig('User Destribution by OS.png')

        # Users by Country and Device OS
        f2 = plt.figure(2, figsize=[10, 6])
        sns.countplot(data=df, x='geo_country', hue="device_os",
                      order=pd.value_counts(df['geo_country']).iloc[:15].index)  # top 15 countries by install and device os
        plt.title('Application use by country')
        plt.xlabel('Country')
        plt.ylabel('User Count')
        plt.savefig('Application use by country.png')

        # Top Device Brands Used by Users
        f3 = plt.figure(3, figsize=[10, 6])
        sns.countplot(data=df, y='device_brand_name', order=pd.value_counts(
            df['device_brand_name']).iloc[:10].index)                           # selecting top 10 device brands on which sandbox installs happend
        plt.title('Top Device Brands')
        plt.xlabel('User Count')
        plt.ylabel('Brands')
        plt.savefig('Top Device Brands.png')

        # Users by Device Type
        f4 = plt.figure(4, figsize=[10, 6])
        df['device_category'].value_counts().plot.pie(
            autopct="%.1f%%")        # device types to focus on
        plt.title("User base by device type", fontsize=14)
        plt.ylabel('')
        plt.savefig('User base by device type.png')

        # User connection based on dates
        f5 = plt.figure(5, figsize=[10, 6])
        # converting timestamp_raw from string to datetime type
        df['timestamp_raw'] = pd.to_datetime(df['timestamp_raw'])
        df['Date'] = df['timestamp_raw'].apply(lambda x: x.date())

        df['Date'].value_counts().plot.bar().invert_xaxis(
        )                    # installation by date
        plt.title('User Account by date')
        # turn ticks from vertical to horizontal in pandas visualization
        plt.xticks(rotation=0)
        plt.xlabel('Dates User Joined')
        plt.ylabel('User Count')
        plt.savefig('User Account by date.png')

        # Users by country on map

        # preparing data for plotly choropleth map
        data = dict(
            type='choropleth',
            locations=df['geo_country'].value_counts().index,
            locationmode="country names",
            z=df['geo_country'].value_counts().values,
            text=df['geo_country'],
            colorbar={'title': 'number by country'},
        )
        # preapring layout for map and selecting projection type
        layout = dict(title='number by country',
                      geo=dict(showframe=False,
                               projection={'type': 'natural earth'})
                      )

        # preparing figure with attributes
        choromap = go.Figure(data=[data], layout=layout)
        # generate local map
        plot(choromap, validate=False)
        print(
            f'Get Visualisation files at {os.path.dirname(os.path.abspath(__file__))}')

        plt.show()

    # performing quit operation on other selection
    else:
        print('\nQuit.')
        break

    # getting input if user want to continue or quit
    cont = input(
        'Would you like to continue performing other operations? please enter Y/N')
    if cont.upper() == 'Y':
        operation = 0
    elif cont.upper() == 'N':
        print('\nThank you!')
        break
    else:
        print('\nBye!.')
        break

operating = False
