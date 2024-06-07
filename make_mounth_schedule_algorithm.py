import json
import openpyxl


def create_one_day_list(all_s_l, num_d):
    one_d_l = all_s_l.copy()
    for sh in one_d_l.keys():
        one_d_l[sh] = (one_d_l[sh] // num_d) + 1
    return one_d_l


def read_doc_list_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        doc_ls = file.read()
    return json.loads(doc_ls)


def find_search_index(sh):
    if sh == "КТ1":
        return "1", "КТ"
    elif sh == "КТ2":
        return "2", "КТ"
    elif sh == "МРТ1":
        return "1", "МРТ"
    elif sh == "МРТ2":
        return "2", "МРТ"
    else:
        return "", sh


def make_time(dc_di):
    if dc_di.get("ставка") == 1.0:
        end_time = "20:30"
        all_time = 12
    elif dc_di.get("ставка") == 0.75:
        end_time = "17:30"
        all_time = 8
    else:
        end_time = "14:30"
        all_time = 6
    return end_time, all_time


def write_excel(doc_l, shed, path_input, path_output):
    alph = ['G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI',
            'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP']
    doc_l_tab = []
    f_t = 3
    for i in range(len(doc_l)):
        doc_l_tab.append([f_t + n for n in range(4)])
        f_t += 4
    workbook = openpyxl.load_workbook(path_input)
    worksheet = workbook.active
    for data in shed:
        x = alph[data['День'] - 1]
        y = doc_l_tab[data['ФИО'][1] - 1]
        worksheet[x + str(y[0])] = str(data['Рабочее время']['с'])
        worksheet[x + str(y[1])] = str(data['Рабочее время']['по'])
        worksheet[x + str(y[2])] = str(data['Рабочее время']['перерыв'])
        worksheet[x + str(y[3])] = str(data['Рабочее время']['отраб.']) + " (" + str(data['Исследование']) + ")"
    workbook.save(path_output)


def find_one_doc(day_list, doc_l, doc_lst, doc_i, schedule, search, search_index, all_search_lst,
                 one_doc_sh_l, one_day_search_lst, doc_lst_iter, count_doc, day):
    day_list[doc_l.index(doc_lst[doc_i])] -= 1
    schedule.append({'День': day + 1, 'ФИО': [doc_lst[doc_i].get("ФИО"), int((doc_lst[doc_i].get("ФИО")).split('ч')[1])], 'Исследование': search + search_index,
                     'Рабочее время': {'с': '8:00', 'по': make_time(doc_lst[doc_i])[0], 'перерыв': 30,
                                       'отраб.': make_time(doc_lst[doc_i])[1]}})
    all_search_lst[search + search_index] -= one_doc_sh_l.get(search + search_index) * doc_lst[doc_i].get("ставка")
    one_day_search_lst[search + search_index] -= one_doc_sh_l.get(search + search_index) * doc_lst[doc_i].get("ставка")
    doc_elem = doc_lst[doc_i]
    doc_lst_iter.pop(doc_lst_iter.index(doc_elem))
    doc_lst_iter.append(doc_elem)
    doc_lst.pop(doc_i)
    count_doc += 1
    return day_list, schedule, all_search_lst, one_day_search_lst, doc_lst_iter, doc_lst, count_doc


def make_schedule_algorithm(all_search_l, doc_l, one_doc_sh_l, num_day, worked_day):
    all_search_lst = all_search_l.copy()
    one_day_sh_l = create_one_day_list(all_search_l, num_day)
    day_list = [worked_day for _ in range(len(doc_l))]
    doc_lst_iter = doc_l.copy()
    doc_lst_iter = sorted(doc_lst_iter, key=lambda x: x["ставка"], reverse=True)
    schedule = []
    cd = []
    for day in range(num_day):
        count_doc = 0
        one_day_search_lst = one_day_sh_l.copy()
        doc_lst = doc_lst_iter.copy()
        for num in range(len(day_list)):
            for search in all_search_lst.keys():
                search_index = find_search_index(search)[0]
                search = find_search_index(search)[1]
                for doc_i in range(len(doc_lst)):
                    if ((doc_lst[doc_i].get("модальность") == search or
                        search in doc_lst[doc_i].get("дополнительные модальности")) and
                            day_list[doc_l.index(doc_lst[doc_i])] > 0 and
                            all_search_lst.get(search + search_index) > 0 and
                            one_day_search_lst.get(search + search_index) > 0):
                        day_list, schedule, all_search_lst, one_day_search_lst, doc_lst_iter, doc_lst, count_doc = (
                            find_one_doc(day_list, doc_l, doc_lst, doc_i, schedule, search, search_index,
                                         all_search_lst, one_doc_sh_l, one_day_search_lst,
                                         doc_lst_iter, count_doc, day))
                        break
        cd.append(f"День {day + 1} занято {count_doc} врачей")
    return sorted(schedule, key=lambda x: x["ФИО"][1]), all_search_lst, cd


month_search_list = [{'Денситометрия': 1970, 'КТ': 4437, 'КТ1': 508, 'КТ2': 541, 'ММГ': 19061, 'МРТ': 1675, 'МРТ1': 817,
                   'МРТ2': 14, 'РГ': 67021, 'ФЛГ': 40364}, {'Денситометрия': 2089, 'КТ': 4506, 'КТ1': 577, 'КТ2': 570, 'ММГ': 19666, 'МРТ': 1903, 'МРТ1': 833,
                   'МРТ2': 17, 'РГ': 70212, 'ФЛГ': 38880}, {'Денситометрия': 1833, 'КТ': 4058, 'КТ1': 606, 'КТ2': 528, 'ММГ': 17039, 'МРТ': 1748, 'МРТ1': 806,
                   'МРТ2': 14, 'РГ': 61990, 'ФЛГ': 36616}, {'Денситометрия': 1827, 'КТ': 3990, 'КТ1': 635, 'КТ2': 567, 'ММГ': 16623, 'МРТ': 1936, 'МРТ1': 829,
                   'МРТ2': 20, 'РГ': 64422, 'ФЛГ': 31052}, {'Денситометрия': 2196, 'КТ': 4765, 'КТ1': 597, 'КТ2': 610, 'ММГ': 19955, 'МРТ': 1928, 'МРТ1': 821,
                   'МРТ2': 10, 'РГ': 71415, 'ФЛГ': 38298}]
one_doc_search_list = {'Денситометрия': 140, 'КТ': 26, 'КТ1': 16, 'КТ2': 11, 'ММГ': 82, 'МРТ': 20, 'МРТ1': 15,
                       'МРТ2': 10, 'РГ': 82, 'ФЛГ': 300}
doc_list = read_doc_list_file('doc_list.txt')
answer = [make_schedule_algorithm(m_s_l, doc_list, one_doc_search_list, 7, 5) for m_s_l in month_search_list]
answer_month = []
for i in range(len(answer)):
    for j in range(len(answer[i][0])):
        answer[i][0][j]['День'] += 7 * i
for ans in answer:
    for a in ans[0]:
        answer_month.append(a)
write_excel(doc_list, answer_month, 'template_doc_excel_for_month.xlsx', 'doc_excel_for_month.xlsx')

