from bs4 import BeautifulSoup
import json


# Parse the HTML with Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table by its ID (or use other selectors)
table = soup.find('table', id='example-table')

# Initialize a list to hold the data
table_data = []

# Iterate over rows in the table body
for row in table.find('tbody').find_all('tr'):
    # Extract all cells in the row
    cells = row.find_all('td')
    # Store data in a dictionary
    row_data = {
        'Date': cells[0].text.strip(),
        'Day': cells[1].text.strip(),
        'Time': cells[2].text.strip(),
        'Status': cells[3].text.strip(),
        'Price': cells[4].text.strip(),
    }
    # Append the row data to the list
    table_data.append(row_data)

# Convert the table data to JSON format
table_json = json.dumps(table_data, indent=4)

# Print the JSON
print(table_json)
