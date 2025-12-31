from app import app
from flask import render_template

@app.get('/admin/layout')
def admin_layout():
    return  render_template('admin/admin_dash.html')