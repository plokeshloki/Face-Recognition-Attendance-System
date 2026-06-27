from flask import Flask, render_template_string
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

ATTENDANCE_DIR = "attendance"

@app.route("/")
def index():
    date = datetime.now().strftime("%Y-%m-%d")
    attendance_file = os.path.join(ATTENDANCE_DIR, f"attendance_{date}.csv")

    if os.path.exists(attendance_file):
        df = pd.read_csv(attendance_file)
        rows = df.to_dict(orient="records")
    else:
        rows = []

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Attendance System</title>
        <style>
            body { font-family: Arial; background: #f0f0f0; padding: 30px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 60%; background: white; }
            th { background: #4CAF50; color: white; padding: 10px; }
            td { padding: 10px; border: 1px solid #ddd; text-align: center; }
            .present { color: green; font-weight: bold; }
            .absent { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>📋 Attendance - {{ date }}</h1>
        {% if rows %}
        <table>
            <tr><th>Name</th><th>Time</th><th>Status</th></tr>
            {% for row in rows %}
            <tr>
                <td>{{ row['Name'] }}</td>
                <td>{{ row['Time'] }}</td>
                <td class="{{ row['Status'].lower() }}">{{ row['Status'] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No attendance data found for today.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, rows=rows, date=date)

if __name__ == "__main__":
    app.run(debug=True)