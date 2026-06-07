from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    note = data['note']

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved successfully"})


@app.route('/get_notes')
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    )

    notes = cursor.fetchall()

    conn.close()

    return jsonify(notes)


@app.route('/update_note/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.get_json()
    updated_note = data['note']

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET content=? WHERE id=?",
        (updated_note, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note updated successfully"})


@app.route('/delete_note/<int:id>', methods=['DELETE'])
def delete_note(id):

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)