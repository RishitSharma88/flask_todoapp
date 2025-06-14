from flask import Flask, request, redirect, url_for, flash, get_flashed_messages
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Database configuration
DATABASE = 'todo.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    """Initialize the database with the tasks table"""
    try:
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

def ensure_db_exists():
    """Ensure database and table exist before any operation"""
    if not os.path.exists(DATABASE):
        print("Database file doesn't exist, creating...")
        init_db()
    else:
        # Check if table exists
        try:
            conn = get_db_connection()
            conn.execute('SELECT 1 FROM tasks LIMIT 1')
            conn.close()
        except sqlite3.OperationalError:
            print("Table doesn't exist, creating...")
            init_db()

def render_template_string(tasks, flash_messages=None):
    """Generate HTML template as a string"""
    if flash_messages is None:
        flash_messages = []
    
    # Generate flash messages HTML
    flash_html = ""
    if flash_messages:
        for category, message in flash_messages:
            flash_html += f'<div class="flash-message flash-{category}">{message}</div>'
    
    # Generate tasks HTML
    tasks_html = ""
    if tasks:
        for task in tasks:
            completed_class = "completed" if task['completed'] else ""
            completed_text_class = "completed" if task['completed'] else ""
            status_class = "status-completed" if task['completed'] else "status-pending"
            status_text = "Completed" if task['completed'] else "Pending"
            
            if task['completed']:
                action_button = f'<a href="/complete/{task["id"]}" class="btn btn-warning">Undo</a>'
            else:
                action_button = f'<a href="/complete/{task["id"]}" class="btn btn-success">Complete</a>'
            
            tasks_html += f'''
                <div class="task-item {completed_class}">
                    <div class="task-content">
                        <div class="task-title {completed_text_class}">
                            {task['title']}
                        </div>
                        <div class="task-date">
                            Created: {task['created_at']}
                        </div>
                    </div>
                    <div class="task-actions">
                        <span class="task-status {status_class}">
                            {status_text}
                        </span>
                        {action_button}
                        <a href="/delete/{task['id']}" 
                           class="btn btn-danger"
                           onclick="return confirm('Are you sure you want to delete this task?')">
                            Delete
                        </a>
                    </div>
                </div>
            '''
    else:
        tasks_html = '<div class="no-tasks"><p>🎉 No tasks yet! Add your first task above.</p></div>'
    
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask To-Do List</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}

        h1 {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}

        .add-task-form {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .form-group {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .form-group input[type="text"] {{
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}

        .form-group input[type="text"]:focus {{
            outline: none;
            border-color: #3498db;
        }}

        .btn {{
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: background-color 0.3s;
        }}

        .btn-primary {{
            background-color: #3498db;
            color: white;
        }}

        .btn-primary:hover {{
            background-color: #2980b9;
        }}

        .btn-success {{
            background-color: #2ecc71;
            color: white;
        }}

        .btn-success:hover {{
            background-color: #27ae60;
        }}

        .btn-danger {{
            background-color: #e74c3c;
            color: white;
        }}

        .btn-danger:hover {{
            background-color: #c0392b;
        }}

        .btn-warning {{
            background-color: #f39c12;
            color: white;
        }}

        .btn-warning:hover {{
            background-color: #e67e22;
        }}

        .task-list {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .task-item {{
            padding: 20px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background-color 0.3s;
        }}

        .task-item:last-child {{
            border-bottom: none;
        }}

        .task-item:hover {{
            background-color: #f8f9fa;
        }}

        .task-item.completed {{
            background-color: #d4edda;
        }}

        .task-content {{
            flex: 1;
        }}

        .task-title {{
            font-size: 18px;
            margin-bottom: 5px;
        }}

        .task-title.completed {{
            text-decoration: line-through;
            color: #6c757d;
        }}

        .task-date {{
            font-size: 12px;
            color: #6c757d;
        }}

        .task-actions {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .task-status {{
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .status-pending {{
            background-color: #fff3cd;
            color: #856404;
        }}

        .status-completed {{
            background-color: #d4edda;
            color: #155724;
        }}

        .flash-messages {{
            margin-bottom: 20px;
        }}

        .flash-message {{
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 10px;
        }}

        .flash-success {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}

        .flash-error {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}

        .no-tasks {{
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-size: 18px;
        }}

        @media (max-width: 600px) {{
            .task-item {{
                flex-direction: column;
                align-items: stretch;
                gap: 15px;
            }}

            .task-actions {{
                justify-content: center;
            }}

            .form-group {{
                flex-direction: column;
            }}

            .form-group input[type="text"] {{
                margin-bottom: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 My To-Do List</h1>
        
        <!-- Flash Messages -->
        <div class="flash-messages">
            {flash_html}
        </div>

        <!-- Add Task Form -->
        <div class="add-task-form">
            <form method="POST" action="/add">
                <div class="form-group">
                    <input type="text" name="title" placeholder="Enter a new task..." required>
                    <button type="submit" class="btn btn-primary">Add Task</button>
                </div>
            </form>
        </div>

        <!-- Task List -->
        <div class="task-list">
            {tasks_html}
        </div>
    </div>
</body>
</html>
    '''

@app.route('/')
def index():
    """Display all tasks on the main page"""
    # Ensure database exists before accessing
    ensure_db_exists()
    
    try:
        conn = get_db_connection()
        tasks = conn.execute(
            'SELECT * FROM tasks ORDER BY created_at DESC'
        ).fetchall()
        conn.close()
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        tasks = []
    
    # Get flash messages properly
    flash_messages = get_flashed_messages(with_categories=True)
    
    return render_template_string(tasks, flash_messages)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task to the database"""
    # Ensure database exists before accessing
    ensure_db_exists()
    
    title = request.form.get('title')
    
    # Validate input
    if not title or not title.strip():
        flash('Task title cannot be empty!', 'error')
        return redirect(url_for('index'))
    
    try:
        # Add task to database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (title) VALUES (?)',
            (title.strip(),)
        )
        conn.commit()
        conn.close()
        
        flash('Task added successfully!', 'success')
    except Exception as e:
        print(f"Error adding task: {e}")
        flash('Error adding task!', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['GET', 'POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    conn = get_db_connection()
    
    # Check if task exists
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        flash('Task not found!', 'error')
        conn.close()
        return redirect(url_for('index'))
    
    # Toggle completion status
    new_status = not task['completed']
    conn.execute(
        'UPDATE tasks SET completed = ? WHERE id = ?',
        (new_status, task_id)
    )
    conn.commit()
    conn.close()
    
    status_text = 'completed' if new_status else 'marked as incomplete'
    flash(f'Task {status_text}!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    """Delete a task from the database"""
    conn = get_db_connection()
    
    # Check if task exists
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        flash('Task not found!', 'error')
        conn.close()
        return redirect(url_for('index'))
    
    # Delete the task
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Force initialize database when app starts
    print("Starting Flask To-Do App...")
    ensure_db_exists()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)