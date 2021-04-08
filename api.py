#!/usr/bin/env python
import re
import requests
from bs4 import BeautifulSoup
import datetime
import json
import matplotlib.pyplot as plt

VICENZA_URL = 'http://www.pollnet.it/WeeklyReport_it.aspx?ID=66'

def parse_tr(tr):
    children = tr.findChildren("td" , recursive=False)
    if len(children) < 2:
        return None, None
    values = [row.text.replace(',', '.') for row in children]
    famiglia = values[0]
    dati = [float(value) for value in values[1:-1]]
    return famiglia, dati

def parse_table(table):
    rows = table.findChildren("tr" , recursive=False)
    data = dict()
    for row in rows[1:]:
        famiglia, dati = parse_tr(row)
        if famiglia:
            data[famiglia] = dati
    return data

def get_data():
    with requests.session() as s:
        s.get('http://www.pollnet.it/ReportRegional_it.aspx?ID=10')
        response = s.get(VICENZA_URL)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "valori"})
        return parse_table(table)

def save_plot(data):
    y_axis = data['Betulacee']
    x_axis = range(1, 8)

    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.grid()
    ax.margins(0.05,0)
    ax.set_ylabel('Concentrazione')
    labels = "Lunedì Martedì Mercoledì Giovedì Venerdì Sabato Domenica".split()
    plt.xticks(x_axis, labels)


    ax.axhspan(0.5, 16, facecolor='yellow')
    ax.axhspan(16, 50, facecolor='orange')
    ax.axhspan(50, 70, facecolor='red')

    plt.savefig('plot.png')


data = get_data()
save_plot(data)
