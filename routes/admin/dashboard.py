from app import app
from flask import render_template

@app.route('/admin')
def admin_dashboard():
    models = 'dashboard'
    return render_template('admin/dashboard/admin_dash.html', models=models)