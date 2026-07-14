from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- डेटाबेस सेटअप ---
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # यहाँ हमने 'timestamp' नाम का नया कॉलम जोड़ा है जो अपने आप तारीख और समय सेव करेगा
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- 1. होम पेज (सारे टास्क दिखाना) ---
@app.route('/')
# --- 1. होम पेज (सारे टास्क दिखाना और सर्च करना) ---
@app.route('/')
def home():
    # ब्राउज़र के सर्च बार से कीवर्ड उठाना
    search_query = request.args.get('search', '')
    
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    if search_query:
        # अगर यूजर ने कुछ सर्च किया है, तो सिर्फ वही टास्क ढूंढना
        cursor.execute("SELECT * FROM tasks WHERE title LIKE ? ORDER BY id DESC", ('%' + search_query + '%',))
    else:
        # अगर सर्च खाली है, तो हमेशा की तरह सारे टास्क दिखाना
        cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
        
    all_tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=all_tasks, search_query=search_query)

# --- 2. नया टास्क जोड़ना ---
@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form.get('title')
    if task_title:
        # मौजूदा समय को एक अच्छे फॉर्मेट (जैसे: 13-Jul-2026 04:15 PM) में बदलना
        current_time = datetime.now().strftime('%d-%b-%Y %I:%M %p')
        
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        # टास्क के साथ समय को भी डेटाबेस में डालना
        cursor.execute('INSERT INTO tasks (title, timestamp) VALUES (?, ?)', (task_title, current_time))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

# --- 3. टास्क डिलीट करना ---
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# --- 4. टास्क पूरा करना ---
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)