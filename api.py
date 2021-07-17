#!/usr/bin/env python
import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def parse_tr(tr):
    children = tr.findChildren("td" , recursive=False)
    if len(children) < 2:
        return None, None
    values = [row.text.replace(',', '.') for row in children]
    famiglia = values[0]
    dati = [float(value) for value in values[1:-1]]
    return famiglia, dati

def parse_table(soup):
    table = soup.find("table", {"class": "valori"})
    rows = table.findChildren("tr" , recursive=False)
    data = dict()
    for row in rows[1:]:
        famiglia, dati = parse_tr(row)
        if famiglia:
            data[famiglia] = dati
    return data

def parse_title(soup):
    title = soup.find("h3", {"id": "gcStation"})
    station = title.find(text=True, recursive=False)
    settimana = re.sub('\s+', ' ', title.find("div").text)
    return f"{station}\n{settimana}"

def get_data(station_id):
    with requests.session() as s:
        s.get('http://www.pollnet.it/ReportRegional_it.aspx?ID=10')
        response = s.get('http://www.pollnet.it/WeeklyReport_it.aspx?ID={station_id}')
        soup = BeautifulSoup(response.content, "html.parser")
        return parse_title(soup), parse_table(soup)

def save_plot(data):
    y_axis = data
    x_axis = range(1, 8)

    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.grid()
    ax.margins(0.05,0)
    ax.set_ylabel('Concentrazione')
    labels = "Lun Mar Mer Gio Ven Sab Dom".split()
    plt.xticks(x_axis, labels)


    ax.axhspan(0.5, 16, facecolor='yellow')
    ax.axhspan(16, 50, facecolor='orange')
    ax.axhspan(50, 70, facecolor='red')

    plt.savefig('plot.png')

def parse_region(id):
    with requests.session() as s:
        response = s.get(f'http://www.pollnet.it/ReportRegional_it.aspx?ID={id}')

    soup = BeautifulSoup(response.content, "html.parser")
    select = soup.find("select", {"id": "dllStations"})
    options = select.findChildren("option")
    provinces = dict()
    for option in options:
        id = int(option['value'])
        if id != -1:
            province = option.text.strip('- ')
            provinces[province] = id

    return provinces

def get_all_stations():
    regions = {
        'Abruzzo': 13,
        'Alto Adige': 3,
        'Basilicata': 15,
        'Calabria': 19,
        'Campania': 17,
        'Emilia Romagna': 11,
        'Friuli Venezia Giulia': 18,
        'Liguria': 20,
        'Marche': 22,
        'Molise': 23,
        'Piemonte': 21,
        'Puglia': 24,
        'Sardegna': 25,
        'Sicilia': 26,
        'Toscana': 27,
        'Trentino': 14,
        'Umbria': 28,
        "Valle d'Aosta": 29,
        'Veneto': 10
    }

    data = dict()
    for region, id in regions.items():
        data[region] = parse_region(id)
    return data

title, data = get_data()
# save_plot(data)

if __name__ == '__main__':
    # print(title)
    # print(data)
    
    print(get_all_stations())