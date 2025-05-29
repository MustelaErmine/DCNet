from DC import *

def init_options() -> tuple:
    pass

def choose_category() -> int:
    message = '''\nВыберете категорию:
1 - добавить клиента;
2 - операции на клиенте;
3 - добавить клиента-нарушителя целостности
: '''
    answer = -1
    while answer not in ['1', '2', '3']:
        answer = input(message)
    return int(answer)

def choose_client(dc: DC_Net) -> int:
    message = '''Сейчас существуют следующие клиенты:\n'''
    for index, client in enumerate(dc.clients):
        message += f"{index}: {client.name}\n"
    print(message)

    answer = input('Выберите клиента: ')
    try:
        answer = int(answer)
        if answer < 0 or answer >= len(dc.clients):
            return -1
        return answer
    except ValueError:
        return -1

def operate_clients(dc: DC_Net):
    message = '''\nВведите имя клиента: '''
    new_name = input(message)
    dc.add_client(new_name)
    print('Клиент добавлен!\n')

def operate_violent_clients(dc: DC_Net):
    message = '''\nВведите имя клиента-нарушителя целостности: '''
    new_name = input(message)
    dc.add_violent_client(new_name)
    print('Клиент-нарушитель добавлен!\n')

def operate_client(dc: DC_Net, number: int):
    message = '''Выберите команду:
1 - добавить файл;
2 - запросить файл;
: '''
    operation = -1
    while operation not in ['1', '2']:
        operation = input(message)
    
    if operation == '1':
        name = input('Введите название: ')
        content = input('Введите контент: ')
        dc.clients[number].add_file(name, content)
        print(f'Файл {name}: "{content}" добавлен в клиент {number}\n')
    elif operation == '2':
        name = input('Введите название: ')
        print(f'Запрошен файл {name}.')
        print(dc.clients[number].request_file(name))

def operate_command(dc: DC_Net):
    category: int = choose_category()
    if category == 1: # clients
        operate_clients(dc)
    elif category == 2: # on client
        client_number = choose_client(dc)
        if client_number != -1:
            operate_client(dc, client_number)
    elif category == 3:
        operate_violent_clients(dc)

def main():
    options = init_options()
    dc = DC_Net()
    while True:
        operate_command(dc)

if __name__ == '__main__':
    main()