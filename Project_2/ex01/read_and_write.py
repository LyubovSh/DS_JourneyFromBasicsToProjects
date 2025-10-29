if __name__ == '__main__':
    with open('ds.csv', 'r', encoding='utf-8') as file_1, open('ds.tsv', 'w', encoding='utf-8') as file_2:
        for line in file_1:
            counter = 0
            new_line = ""
            for elem in line:
                if elem == '"':
                    counter += 1
                if counter % 2 == 0 and elem == ',':
                    new_line += '\t'
                else:
                    new_line += elem
            file_2.write(new_line)