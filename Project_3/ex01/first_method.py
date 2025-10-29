class Research:
    
    def file_reader(self):
        with open('data.csv', 'r', encoding = 'utf-8') as file:
            return file.read() 

if __name__ == '__main__':
    class_instance = Research()
    print(class_instance.file_reader())
