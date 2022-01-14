from flask import Flask, render_template, url_for, request, redirect

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True



db = SQLAlchemy(app)

# db = None
# def get_db():
#   global db
#   if not db:
#     db = SQLAlchemy(app)
#   return db


# get_db()

#print(get_db())

class Todo(db.Model):
     id = db.Column( db.Integer, primary_key = True)
     content = db.Column( db.String(200), nullable = False)
     completed =  db.Column( db.Integer , default=0)
     date_created = db.Column( db.DateTime, default=datetime.utcnow )

#  def __init__(self, content, completed):
#         self.content = content
#         self.completed = completed


def __repr__(self):
    return '<Todo %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
          if request.method == 'POST':
              task_content = request.form['content']
              new_task = Todo(content=task_content)
              try:
                db.session.add(new_task)
                db.session.commit()
              except:
                return "There was an issue adding your request."
              return redirect('/')
          else:
              tasks = Todo.query.order_by(Todo.date_created).all()
              return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
              task_to_delete = Todo.query.get_or_404(id)
              try:
                db.session.delete(task_to_delete)
                db.session.commit()
              except:
                return "There was a problem deleting record."
              return redirect('/')

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
              task_to_update = Todo.query.get_or_404(id)
              if request.method == 'POST':
                task_to_update.content = request.form['content']
                  
                try:
                  db.session.commit()
                except:
                  return "There was an issue updating your request."
                return redirect('/')
              else:
                return render_template('update.html', task=task_to_update)
                  


# @app.route('/')
# def index():
#     return render_template('index.html')
    #return "Hello, World!"

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)