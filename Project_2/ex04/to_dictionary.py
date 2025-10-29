def list_of_tuples():
    list_of_tuples = [
    ('Russia', '25'),
    ('France', '132'),
    ('Germany', '132'),
    ('Spain', '178'),
    ('Italy', '162'),
    ('Portugal', '17'),
    ('Finland', '3'),
    ('Hungary', '2'),
    ('The Netherlands', '28'),
    ('The USA', '610'),
    ('The United Kingdom', '95'),
    ('China', '83'),
    ('Iran', '76'),
    ('Turkey', '65'),
    ('Belgium', '34'),
    ('Canada', '28'),
    ('Switzerland', '26'),
    ('Brazil', '25'),
    ('Austria', '14'),
    ('Israel', '12')
    ]
    return list_of_tuples

if __name__ == '__main__':
    result_dict = dict()
    for elem in list_of_tuples():
        if elem[1] not in result_dict:
            result_dict[elem[1]] = [elem[0]]
        else:
            result_dict[elem[1]].append(elem[0])

    for key, values in result_dict.items():
        for value in values:
            print(f"'{key}' : '{value}'")
