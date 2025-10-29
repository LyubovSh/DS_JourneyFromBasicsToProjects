def data_types():
    variable_1  = 10
    variable_2 = 'Hi. world'
    variable_3 = 0.01
    variable_4 = True
    variable_5 = list()
    variable_6 = dict()
    variable_7 = tuple()
    variable_8 = set()
    return [elem.__class__.__name__ for elem in locals().values()]

if __name__ == '__main__':
    print(data_types())




