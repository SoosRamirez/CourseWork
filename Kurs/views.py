from django.http import HttpResponse
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'homekurs.html', {})


def orgs(request):
    if request.session["role"] != None:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        a = {}
        container = []
        for i in data["Organisations"]:
            container.append(i)
            a = {"Organisations": container}
    return render(request, 'orgList.html', a)


def emps(request, id):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    a = {}
    container = []
    k = id
    for i in data["Users"]:
        if i["idorg"] == k:
            container.append(i)
            a = {"Users": container}
    return render(request, 'empList.html', a)


def user(request, id):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    a = {}
    container = []
    k = id
    for i in data["Users"]:
        for j in data["Vacations"]:
            if i["id"] == k:
                container.append(i)
                a = {"Users": container}
    return render(request, 'User.html', a)


def vac(request, id):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    a = {}
    container = []
    k = id
    for i in data["Vacations"]:
        if i["id"] == k:
            container.append(i)
            a = {"Vacations": container}
    return render(request, 'vacation.html', a)


@csrf_exempt
def addOrg(request):
    if request.session["role"] != None:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        req = request.POST
        idorg = req.get('idorg')
        name = req.get('name')
        startdate = req.get('startdate')
        description = req.get('description')
        adress = req.get('adress')
        surname = req.get('surname')
        named = req.get('named')
        sec_name = req.get('sec_name')
        birthday = req.get('birthday')
        if id != None and id != "" and name != "" and adress != "":
            a = {
                'idorg': idorg,
                'name': name,
                'startdate': startdate,
                'description': description,
                'adress': adress,
                'boss': {'surname': surname, 'named': named, 'sec_name': sec_name, 'birthday': birthday}
            }
        data['Organisations'].append(a)
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))
    return render(request, 'addOrg.html', {})


@csrf_exempt
def addVac(request):
    if request.session["role"] != None:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        req = request.POST
        id = req.get('id'),
        start = req.get('start'),
        end = req.get('end'),
        long = req.get('long'),
        type = req.get('type'),
        a = {'id': id,
             'start': start,
             'end': end,
             'long': long,
             'type': type}
        data['Vacations'].append(a)
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, 'addVac.html', {})


@csrf_exempt
def moder(request):
    if request.session["role"] != None:
        return render(request, 'Moder.html', {})


@csrf_exempt
def addEmp(request):
    if request.session["role"] != None:
        with open('login.json', 'r', encoding='utf-8') as file:
            data_log = json.load(file)
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        req = request.POST
        id = req.get('id')
        job = req.get('job')
        name = req.get('name')
        surname = req.get('surname')
        sec_name = req.get('sec_name')
        birthday = req.get('birthday')
        idorg = req.get('idorg')
        password = req.get('password')
        login = req.get('login')
        a = {
            'id': id,
            'name': name,
            'job': job,
            'surname': surname,
            'sec_name': sec_name,
            'birthday': birthday,
            'idorg': idorg,
            'login': login,
            'password': password
        }
        b = {
            'login': login,
            'password': password,
            'role': job
        }
        data_log["data"].append(b)
        data['Users'].append(a)
        with open('data_log.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_log, ensure_ascii=False, separators=(',', ': '), indent=2))
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, 'addEmp.html', {})


@csrf_exempt
def login(request):
    with open('login.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
    request.session["role"] = None
    req = request.POST
    request.session["login"] = req.get("login")
    request.session["password"] = req.get("password")
    page = "homekurs.html"
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    a = {}
    container = []
    for i in data["Organisations"]:
        container.append(i)
        a = {"Organisations": container}
    for i in users["data"]:
        if i["login"] == request.session["login"] and i["password"] == request.session["password"]:
            request.session["role"] = i["role"]
            break
    if request.session["role"] == "user":
        page = "orgList.html"
        return render(request, page, a)
    elif request.session["role"] == "moderator":
        page = "Moder.html"
        return render(request, page, a)
    else:
        return render(request, page)
