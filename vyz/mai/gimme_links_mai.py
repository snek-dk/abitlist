from os import listdir
from os.path import isfile, join


def gimme_links():
    mypath = rf"..\..\vyz\mai"
    names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    names = [x if (x[-2:] != 'py') else False for x in names]
    ed_principle = ''
    form_of_education = ''
    links_budget = []
    links_contract = []
    main_link = 'https://public.mai.ru/priem/rating/data/'
    for i in names:
        if i:
            ed_principle, form_of_education = i.split('+')[1], i.split('+')[2]
            path = mypath + rf'\{i}'
            with open(path, 'rb') as f:
                for j in f.readlines():
                    s = j.decode('utf-8')
                    link = main_link + s.split('"')[1]
                    if ed_principle == 'госбюджет':
                        links_budget.append(
                            (link, s.split('"')[2].replace('>', '').replace('\r', '').replace('\n', ''), i.split('+')[-1]))
                    else:
                        links_contract.append(
                            (link, s.split('"')[2].replace('>', '').replace('\r', '').replace('\n', ''), i.split('+')[-1]))
    return links_budget, links_contract
print(gimme_links()[0])
print(gimme_links()[1])