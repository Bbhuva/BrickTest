import pandas as pd
import re
import os.path
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot

import seaborn as sns


def operationOption():
    print('\nOptions:\n\t 1 - Input a CSV file and convert it to JSON')
    print('\t 2 - Input a CSV file and generate a SQL insert statement')
    print('\t 3 - Input a CSV file and present a data summary')
    print('\t 0 - Quit')


def operationNumber():
    operation_err = "\nYou must enter the number between 1 to 3! Try again."
    while True:
        try:
            operation_number = 0
            operationOption()
            operation_number = int(
                input('Please select the operation number '))
            if operation_number >= 0 and operation_number <= 3:
                print('\nYou have selected operation ' + str(operation_number))
                return int(operation_number)
            else:
                print(operation_err)
        except ValueError:
            print(operation_err)
    else:
        print(operation_err)


def getValidPath(check="", statement="", stype="file"):
    path_err = f"\nYou must enter the valid {stype} path"
    while True:
        try:
            filepath = ''
            filepath = input(statement)
            if (stype == "file" and os.path.isfile(filepath)):
                if check != "" and os.path.splitext(filepath)[-1].lower() != check:
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


print('please select the operation you wants to perfrom from below list\n')
operating = True

while operating:
    operation = 0
    operation_no = int(operationNumber())

    if operation_no == 1:
        filepath = getValidPath(
            check=".csv", statement="please enter csv file path ", stype="file")
        head, tail = os.path.split(filepath)
        savepath = head+'\\'+tail[:-3]+'json'
        df = pd.read_csv(
            filepath, sep=",", index_col=False, header=0)
        df.to_json(savepath, orient='records')

        print(f'File saved at {savepath}')
        # jsonpath = getValidPath(
        #     statement="please enter folder path ", stype="directory")
        # with open(savepath, 'w') as f:
        #     f.write(df.to_json(orient='records')

    elif operation_no == 2:
        filepath = getValidPath(
            check=".csv", statement="please enter csv file path ", stype="file")
        head, tail = os.path.split(filepath)
        savepath = head+'\\'+tail[:-3]+'sql'
        df = pd.read_csv(filepath)

        TableName = "sandbox_installs"
        txt = f'INSERT INTO dbo.{TableName}({",".join(df.columns)}) VALUES\n'

        values_string = ''
        for row in df.itertuples(index=False, name=None):
            values_string += re.sub(r'nan', 'null', str(row))
            values_string += ',\n'

        final = txt + values_string[:-2] + ';'

        with open(savepath, 'w', encoding="utf-8") as f:
            f.write(final)

        print(f'File saved at {savepath}')

    elif operation_no == 3:
        # Read CSV using padas
        df = pd.read_csv("sandbox-installs.csv")

        # drop empty colums with threshold of 60%
        df = df.dropna(thresh=df.shape[0]*0.4, how='all', axis=1)

        # Device OS and User Account Source
        f1 = plt.figure(1, figsize=[10, 6])
        sns.countplot(x='device_os', hue="ua_source", data=df)
        plt.title('User Destribution by OS')
        plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0)
        plt.xlabel('Operating Systems')
        plt.ylabel('User Count')
        plt.savefig('User Destribution by OS.png')

        # Users by Country and Device OS
        f2 = plt.figure(2, figsize=[10, 6])
        sns.countplot(data=df, x='geo_country', hue="device_os",
                      order=pd.value_counts(df['geo_country']).iloc[:15].index)
        plt.title('Application use by country')
        plt.xlabel('Country')
        plt.ylabel('User Count')
        plt.savefig('Application use by country.png')

        # Top Device Brands Used by Users
        f3 = plt.figure(3, figsize=[10, 6])
        sns.countplot(data=df, y='device_brand_name', order=pd.value_counts(
            df['device_brand_name']).iloc[:10].index)
        plt.title('Top Device Brands')
        plt.xlabel('User Count')
        plt.ylabel('Brands')
        plt.savefig('Top Device Brands.png')

        # Users by Device Type
        f4 = plt.figure(4, figsize=[10, 6])
        df['device_category'].value_counts().plot.pie(autopct="%.1f%%")
        plt.title("User base by device type", fontsize=14)
        plt.ylabel('')
        plt.savefig('User base by device type.png')

        # User connection based on dates
        f5 = plt.figure(5, figsize=[10, 6])

        # converting timestamp_raw from string to datetime type
        df['timestamp_raw'] = pd.to_datetime(df['timestamp_raw'])
        df['Date'] = df['timestamp_raw'].apply(lambda x: x.date())

        df['Date'].value_counts().plot.bar().invert_xaxis()
        plt.title('User Account by date')
        plt.xticks(rotation=0)
        plt.xlabel('Dates User Joined')
        plt.ylabel('User Count')
        plt.savefig('User Account by date.png')

        # Users by country on map
        data = dict(
            type='choropleth',
            locations=df['geo_country'].value_counts().index,
            locationmode="country names",
            z=df['geo_country'].value_counts().values,
            text=df['geo_country'],
            colorbar={'title': 'number by country'},
        )
        layout = dict(title='number by country',
                      geo=dict(showframe=False,
                               projection={'type': 'natural earth'})
                      )
        choromap = go.Figure(data=[data], layout=layout)
        plot(choromap, validate=False)

        plt.show()

    else:
        print('\nQuit.')
        break

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
