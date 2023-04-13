import pdfplumber
# from pprint import pprint

def get_splited_needed_list(pdf):
    number_pages = len(pdf.pages)
    data = []
    user_data = {}
    for page in range(number_pages):
        if page == 0:
            text = pdf.pages[page].extract_text().splitlines()
            count = 0
            start_line = None
            end_line = None
            for line in text:
                if 'Customer' in line.split():
                    user_data['Name'] = line.split()[3:4]
                    user_data['Customer_Number'] = line.split()[2:3]
                if 'Card Number' in line:
                    user_data['Card_Number'] = line.split()[2:3]
                    s = line.split()[3:len(line.split())-1]
                    user_data['Address'] = ' '.join([str(elem) for elem in s])
                if 'Pay Date' in line:
                    user_data['Payment_Date'] = line.split()[2:5]
                if line.split()[0] == 'Amount':
                    user_data['Amount'] = line.split()[1:2][0].split('$')[1]
                if 'TOTAL' in line.split():
                    end_line = count
                if 'Date' in line.split():
                    start_line = count
                count += 1
            tex = text[start_line:end_line]
            data += tex
    return data, user_data

def split_each_line(list_of_data):
    splited_data = []
    count = 0

    for data in list_of_data:
        splits = data.split()
        if count == 0:
            splited_data.append(splits)
        else:
            joined_particular = " ".join(splits[4:len(splits)-2])
            joined_date = " ".join(splits[0:4])
            del splits[4: len(splits)-2]
            del splits[0: 4]
            splits.insert(0, joined_particular)
            splits.insert(0, joined_date)
            splited_data.append(splits)
        count += 1

    return splited_data

def convert_data_to_objects(list_of_data):
    converted_list = []
    for data in list_of_data[1:]:
        obj = {}
        obj['Date'] = data[0]
        obj['Description'] = data[1]
        obj['Bonus'] = float(data[2].split("$")[1])
        obj['Amount'] = float(data[3].split("$")[1])
        converted_list.append(obj)
    return converted_list

def merge_duplicate_data(converted_list):
    new_data = {}
    for data in converted_list:
        if new_data.get(data['Description']):
            new_data[data['Description']].append(data)
        else:
            new_data[data['Description']] = [data]

    return new_data

def get_extracted_data(file):
    pdf = pdfplumber.open(file)
    vendor_data, user_data = get_splited_needed_list(pdf)
    list_of_data = split_each_line(vendor_data)
    converted_list = convert_data_to_objects(list_of_data)
    new_data = merge_duplicate_data(converted_list)
    return user_data, new_data

# pdf = pdfplumber.open('creditcard.pdf')
# get_extracted_data(pdf)