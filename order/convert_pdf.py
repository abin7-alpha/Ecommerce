import pdfplumber

def get_splited_needed_list(pdf):
    data = dict
    number_pages = len(pdf.pages)
    data = []
    for page in range(number_pages):
        # print(page, number_pages)
        if page == 0:
            text = pdf.pages[page].extract_text().splitlines()
            count = 0
            start_line = None
            end_line = None
            for line in text:
                if 'date' in line.lower():
                    start_line = count
                if 'carried over' in line.lower():
                    end_line = count
                count += 1
            text = text[start_line:end_line]
            del text[1]
            data += text
        elif page == number_pages-1:
            text = pdf.pages[page].extract_text().splitlines()
            count = 0
            start_line = None
            end_line = None
            for line in text:
                if 'date' in line.lower():
                    start_line = count
                if 'by closing balance' in line.lower():
                    end_line = count
                count += 1
            text = text[start_line+2:end_line-1]
            data += text
        else:
            text = pdf.pages[page].extract_text().splitlines()
            count = 0
            start_line = None
            end_line = None
            for line in text:
                # print(line)
                if 'date' in line.lower():
                    start_line = count
                if 'carried over' in line.lower():
                    end_line = count
                count += 1
            text = text[start_line+2:end_line]
            data == text

    return data

def split_each_line(list_of_data):
    splited_data = []
    count = 0

    for data in list_of_data:
        splits = data.split()
        if count == 0:
            join_vch_type = " ".join(splits[2:4])
            join_vch_no = " ".join(splits[4:6])
            del splits[2:4]
            del splits[2:4]
            splits.insert(2, join_vch_type)
            splits.insert(3, join_vch_no)
            splited_data.append(splits)
        elif splits[1] == 'To':
            joined_particular = " ".join(splits[1:5])
            del splits[1: 5]
            splits.insert(1, joined_particular)
            splited_data.append(splits)
        elif splits[1] == 'By':
            joined_particular = " ".join(splits[1:5])
            del splits[1: 5]
            splits.insert(1, joined_particular)
            splited_data.append(splits)
        elif splits[1] == 'Local':
            splits.insert(0, None)
            joined_particular = " ".join(splits[1:5])
            del splits[1: 5]
            splits.insert(1, joined_particular)
            splited_data.append(splits)
        count += 1

    return splited_data

def convert_data_to_objects(list_of_data):
    converted_list = []
    for data in list_of_data[1:]:
        obj = {}
        if data[2] == 'Sales':
            obj['Date'] = data[0]
            obj['Particulars'] = data[1]
            obj['Vch Type'] = data[2]
            obj['Vch No.'] = data[3]
            obj['Debit'] = data[4]
            converted_list.append(obj)
        elif data[2] == 'Receipt':
            obj['Date'] = data[0]
            obj['Particulars'] = data[1]
            obj['Vch Type'] = data[2]
            obj['Vch No.'] = data[3]
            obj['Credit'] = data[4]
            converted_list.append(obj)
        elif data[2] == 'Credit':
            obj['Date'] = data[0]
            obj['Particulars'] = data[1]
            obj['Vch Type'] = f"{data[2]} {data[3]}"
            obj['Vch No.'] = data[4]
            obj['Credit'] = data[5]
            converted_list.append(obj)

    return converted_list  

def get_pdf_data(pdf):
    pdf = pdfplumber.open(pdf)
    list_of_data = split_each_line(get_splited_needed_list(pdf))
    final_data = convert_data_to_objects(list_of_data)
    
    return final_data
