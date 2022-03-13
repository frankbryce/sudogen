from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import numpy as np
import sudoku

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TODO - wtf is this?'
socketio = SocketIO(app)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def jsEnc(data):
    return json.dumps(data, cls=NpEncoder)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('grid')
def onrandom(difficulty):
    grid = sudoku.Grid.New(difficulty)
    emit('json', {
        'start': jsEnc([[grid.cells[r][c].val for c in range(9)] for r in range(9)]),
        'solution': jsEnc(grid.solution),
    })

@socketio.on('connect')
def onconnect():
    print('client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('client disconnected')

if __name__ == '__main__':
    app.run(debug=True)
