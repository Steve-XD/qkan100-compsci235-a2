import omdb
from csv import writer
from csv import reader
import ast
default_text = 'Some Text'
import requests
url = "http://www.omdbapi.com/"


# Open the input_file in read mode and output_file in write mode
with open('test.csv', 'r') as read_obj, \
        open('test_output.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    for row in csv_reader:
        title = row[1]
        querystring = {"apikey":"15439843","t":title} # your parameters here in query string
        headers = { 'Cache-Control': "no-cache", 'Connection': "keep-alive", 'cache-control': "no-cache" }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(title)
        dict1 = ast.literal_eval(response.text)
        if dict1['Response']=='True'and dict1['Poster']!='N/A':
            # Append the default text in the row / list
            row.append(dict1['Poster'])
            # Add the updated row / list to the output file
            csv_writer.writerow(row)
        else:
            # Append the default text in the row / list
            row.append("None")
            # Add the updated row / list to the output file
            csv_writer.writerow(row)

