residence_limit = 90  # 45, 60
schengen_constraint = 180

#  вынесли в функцию самую часто используемую операцию
#  в которой не хотелось бы ошибиться


def date_difference(leave, arrive):
    result = leave - arrive + 1
    return result


#  сделали работу с длиной визитов более удобной
def visit_length(visit):
    return date_difference(visit[1], visit[0])


#  функции надо объявлять до того как вы их вызовите
def get_days_for_visits(visits):
    days_for_visits = []
    for visit in visits:
        days_for_visit = 0
        for past_visit in visits:
            if visit[0] - schengen_constraint < past_visit[0] < visit[0]:
                days_for_visit += visit_length(past_visit)
        days_for_visit += visit_length(visit)
        days_for_visits.append(days_for_visit)
    return days_for_visits


def print_days_future_visit(visits, date_in_future):
    visits_for_future = visits + [[date_in_future, date_in_future]]
    #  используем объявленную функцию
    days_for_future_visits = get_days_for_visits(visits_for_future)
    days_in_es = residence_limit - days_for_future_visits[len(days_for_future_visits) - 1] + 1
    print('Если въедем %s числа, сможем провести в шенгене %s дней' % (date_in_future, days_in_es))


def print_residence_limit_violation(visits):
    days_for_visits = get_days_for_visits(visits)

    for visit, total_days in zip(visits, days_for_visits):
        if total_days > residence_limit:
            overstay_time = total_days - residence_limit
            print('Во время визита', visit, 'количество время пребывания превышено на', overstay_time, 'дней')
            # выходим если есть превышение времени визита
            break
        

def add_visit():
    print('Начало:')
    start = int(input())
    print('Конец:')
    end = int(input())
    visits.append([start, end])
    print_residence_limit_violation(visits)
    # перезаписываем файл визитов
    write_visit(visits)


def func_next_visit():
    print('дата следующего визита:')
    next_visit = int(input())
    print_days_future_visit(visits, next_visit)


def exit_script():
    write_visit(visits)
    return True


# функция записи визитов в файл
def write_visit(visits):
    with open('visit_in.txt', 'w') as f:
        for line in visits:
            f.write( str(line[0])+' '+str(line[1])+'\n' )
            

# функция чтения визитов из файла
def read_visit(visits):
    with open('visit_in.txt') as f:
        for line in f:
            visits += [list(map(int, line.split()))]
    print('\nВизиты: ', visits)

#  visits = [[1, 10], [61, 90], [101, 140], [141, 160], [271, 290]]
#  бесконечный цикл
exit_while = False
while exit_while is False:
    visits = []
    read_visit(visits)
    print('\nвыберите режим:')
    print('v - добавить визит')
    print('p - ввести дату следующего визита')
    print('q - выход')
       
    user_input = input()

    if user_input == 'v':
        add_visit()
        pass

    elif user_input == 'p':
        func_next_visit()

    elif user_input == 'q':
        exit_while = exit_script()

