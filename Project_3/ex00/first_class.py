class Must_Read:
    def __init__(self):
        self.read_data()

    @staticmethod
    def read_data():
        with open('data.csv', 'r', encoding = 'utf-8') as file:
            for line in file:
                print(line.strip())

if __name__ == '__main__':
    class_instance = Must_Read()
