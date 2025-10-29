import sys

def auxiliary_lists():
    #Первый список содержит адреса электронной почты ваших клиентов.
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
    #Второй список содержит адреса электронной почты участников вашего последнего мероприятия, 
    #некоторые из которых были вашими клиентами. 
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    #Третий список содержит адреса электронной почты клиентов, 
    #которые просмотрели ваше последнее рекламное письмо.
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    return set(clients), set(participants), set(recipients)

if __name__=='__main__':
    if len(sys.argv) == 2:
        tasks = ['call_center', 'potential_clients', 'loyalty_program']
        try:
            tasks.index(sys.argv[1])
        except IndexError:
            print(f'Задача {sys.argv[1]} недоступна к исполнению')
            exit()
        result = set() 
        if sys.argv[1] == tasks[0]:
            #Поскольку clients-список всех клиентов, а recipients - те, кто уже получили рекламу. Найдя разности множеств, получаем тех клиентов, которые еще не получили рекламную рассылку 
            result = auxiliary_lists()[0] - auxiliary_lists()[2]
        elif sys.argv[1] == tasks[1]:
            #Для поиска  участников, которые не являются вашими клиентами необходимо из списка participants надо извлечь clients, и это будет ответом 
            result = auxiliary_lists()[1] - auxiliary_lists()[0]
        elif sys.argv[1] == tasks[2]:
            #Для поиска клиентов, которые не участвовали в мероприятии необходимо из списка клиентов нужно вычесть тех, кто учавствовал в мероприятии
            result = auxiliary_lists()[0] - auxiliary_lists()[1]
        print(list(result))



        
    

