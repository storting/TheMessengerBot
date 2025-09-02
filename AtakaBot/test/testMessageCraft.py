from MessageCraft import Message

def search_data():
        """Поиск данных по заданной дате."""
        found_data = []
        with open('dataBase', encoding='utf-8') as file:
            for line in file:
                data_list = eval(line.strip())
                found_data.append((data_list[1], data_list[2], data_list[4]))
        return found_data

data = search_data()

for i in range(0, 10):
    print(data[i][0], "\t", data[i][1])
    testMessegeClass = Message(data[i][0], data[i][1])
    print(testMessegeClass.final_form_massage())
    