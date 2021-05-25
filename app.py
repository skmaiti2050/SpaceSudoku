import json
import numpy as np
import sudoku_gen as sg
import sudoku_solver as ss
from flask import Flask, request, render_template, url_for, Response

app = Flask(__name__)


def row_list(item):
    items = item.replace('[', '')
    items = items.replace(']', '')
    items = items.replace('"', '')
    items = items.split(',')
    row = list(map(int, items))
    return row


def json_gen(fname):
    dict1 = {}
    a_list = list(map(chr, range(65, 74)))
    for (idx, val) in enumerate(fname, 1):
        for num in list(range(0, 9)):
            nkey = 'cell_' + str(a_list[idx - 1]) + str(num + 1)
            dict1[nkey] = int(val[num])
    return dict1


@app.route('/', methods=['POST', 'GET'])
def Index():
    if request.method == 'POST':
        level = request.form.get('level')
        ng = sg.main(level)
        jdict = json_gen(ng)
        return Response(json.dumps(jdict), mimetype='application/json')
    else:
        return render_template('index.html')


@app.route('/solvesudoku', methods=['POST'])
def SolveSudoku():
    row1 = row_list(request.form['row1'])
    row2 = row_list(request.form['row2'])
    row3 = row_list(request.form['row3'])
    row4 = row_list(request.form['row4'])
    row5 = row_list(request.form['row5'])
    row6 = row_list(request.form['row6'])
    row7 = row_list(request.form['row7'])
    row8 = row_list(request.form['row8'])
    row9 = row_list(request.form['row9'])
    grid = np.array([row1, row2, row3, row4, row5, row6, row7, row8, row9])
    sol = ss.main(grid)
    jdict = json_gen(sol)
    return Response(json.dumps(jdict), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
