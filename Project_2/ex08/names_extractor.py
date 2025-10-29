import sys

if __name__ == '__main__':
    print(sys.argv[1:])
    file_path = ''.join(sys.argv[1:])
    print("_" * 100)

    print(file_path)
    print("_" * 100)
    with open(file_path, 'r', encoding='utf-8') as file_1, open('employees.tsv', 'w', encoding='utf-8') as file_2:
        for line in file_1:
            tmp_indx_1 = line.index('.')
            name = (line[:tmp_indx_1]).title()
            tmp_indx_2 = line.index('@')
            surname = (line[tmp_indx_1+1:tmp_indx_2]).title()
            added_str = f'{name}\t{surname}\t{line}'
            file_2.write(added_str)
            

