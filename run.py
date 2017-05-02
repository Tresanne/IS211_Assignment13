#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""web app week 2 """

from flask import Flask,request,redirect, url_for
from flask import render_template
import sqlite3
from datetime import date, datetime

def get_db_conn():
	conn = sqlite3.connect('hw13.db')
	print("Opened database successfully")
	return conn

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET','POST'])
def login_view():
	error_message=None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == 'admin' and password=='password':
			return redirect(url_for('dashboard'))
		error_message = 'Wrong credentials'
	return render_template('login.html', error_message=error_message)

@app.route('/dashboard')
def dashboard():
	conn = get_db_conn()
	c = conn.cursor()
	all_students = c.execute('SELECT * FROM Students').fetchall()
	all_quizzes = c.execute('SELECT * FROM Quizzes').fetchall()
	conn.close()
	return render_template('dashboard.html', all_quizzes=all_quizzes, all_students=all_students)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
	error_message=""
	if request.method == 'POST':
		try:
			firstname = request.form['firstname']
			lastname = request.form['lastname']
			conn = get_db_conn()
			c = conn.cursor()
			all_students = c.execute('SELECT * FROM Students').fetchall()
			id_ = len(all_students)+1
			query_ = "INSERT INTO Students values('%s','%s',%d)" % (firstname, lastname, id_)
			c.execute(query_)
			conn.commit()
			conn.close()
			return redirect(url_for('dashboard'))
		except:
			error_message = 'there were some issues'
	return render_template('addstudent.html', error_message=error_message)	

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
	error_message=""
	if request.method == 'POST':
		try:
			subject = request.form['subject']
			nquestions = request.form['nquestions']
			conn = get_db_conn()
			c = conn.cursor()
			all_quizzes = c.execute('SELECT * FROM Quizzes').fetchall()
			id_ = len(all_quizzes)+1
			today = date.today()
			c.execute('''INSERT INTO Quizzes values(?,?,?,?)''',(id_,subject,nquestions,today,))
			conn.commit()
			conn.close()
			return redirect(url_for('dashboard'))
		except:
			error_message = 'there were some issues'
	return render_template('addquiz.html', error_message=error_message)

@app.route('/result/add', methods=['GET', 'POST'])
def add_result():
	error_message=""
	if request.method == 'POST':
		try:
			student_id = request.form['student']
			quiz_id = request.form['quiz']
			score = request.form['score']
			conn = get_db_conn()
			c = conn.cursor()
			c.execute('''INSERT INTO Results VALUES(?,?,?)''',(student_id, quiz_id, score))
			conn.commit()
			conn.close()
			return redirect(url_for('dashboard'))
		except:
			error_message = 'there were some issues'
	conn = get_db_conn()
	c = conn.cursor()	
	all_quizzes = c.execute('SELECT * FROM Quizzes').fetchall()
	all_students = c.execute('SELECT * FROM Students').fetchall()
	conn.close()
	return render_template('addresult.html', error_message=error_message, all_quizzes=all_quizzes,
	 all_students=all_students)

@app.route('/student/<id>')
def quiz_results(id):
	error_message = ""
	conn = get_db_conn()
	c = conn.cursor()
	quiz_results = c.execute('SELECT * FROM Results where StudentID=(?)',(id,)).fetchall()
	return render_template('quizresults.html',error_message=error_message, quiz_results=quiz_results)

if __name__ == '__main__':
	app.run(debug = True, host='127.0.0.1', port=5000)
