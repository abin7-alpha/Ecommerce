from pprint import pprint

def get_count(file):
    count = 0
    
    for lines in file:
        count += 1

    return count

def convert(sheet, columns):
    data = []
    no_lines = get_count(sheet)

    #start line number for the columns values
    count = 7
    while count <= no_lines:
        obj = {}
        #start line number for the column headers
        num = 6
        for column in columns:
            obj[sheet[f'{column}{num}'].value] = sheet[f'{column}{count}'].value
        data.append(obj)
        count += 1

    return data

def xlsx_data(sheet):
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']

    response_data = {}

    try:
        response_data = {
            "data": convert(sheet, columns)
        }
    except:
        response_data = {
            "error": "failed to parse data"
        }

    # pprint(response_data)
    return response_data
