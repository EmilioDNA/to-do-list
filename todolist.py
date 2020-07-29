# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')


Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create all the models
Base.metadata.create_all(engine)


def display_missed_tasks():
    today = datetime.today()
    tasks = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
    print("Missed tasks")
    print_tasks_2(tasks)
    print()


def display_week_tasks(today):
    tasks = session.query(Task).filter(Task.deadline == today.date()).all()
    print(f"{today.strftime('%A')} {today.day} {today.strftime('%b')}")
    print_tasks(tasks)


def display_today_tasks(today):
    tasks = session.query(Task).filter(Task.deadline == today.date()).all()
    print(f"Today {today.day} {today.strftime('%b')}:")
    print_tasks(tasks)


def display_tasks_in_week():
    today = datetime.today()
    for day in range(0, 7):
        day_week = today + timedelta(days=day)
        display_week_tasks(day_week)


def display_all_tasks():
    tasks = session.query(Task).order_by(Task.deadline).all()
    print_tasks_2(tasks)
    return tasks


def add_task():
    print('Enter task')
    task = input()
    print('Enter deadline')
    deadline = input()
    deadline = datetime.strptime(deadline, '%Y-%m-%d')
    new_task = Task(task=task, deadline=deadline)
    session.add(new_task)
    session.commit()
    print('The task has been added!')


def delete_task():
    print("Chose the number of the task you want to delete:")
    tasks = display_all_tasks()
    id_task = input()
    task_to_delete = tasks[int(id_task) - 1]
    session.delete(task_to_delete)
    session.commit()
    print("The task han been deleted!")


def print_main_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


def print_tasks(tasks):
    if len(tasks) == 0:
        print('Nothing to do!')
        print()
    else:
        for count, task in enumerate(tasks):
            print(f'{count + 1}. {task}')
            print()


def print_tasks_2(tasks):
    if len(tasks) == 0:
        print('Nothing to do!')
    else:
        for count, task in enumerate(tasks):
            print(f"{count + 1}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")
    print()


def execute_choice(input_choice):
    if input_choice == '1':
        display_today_tasks(datetime.today())
    elif input_choice == '2':
        display_tasks_in_week()
    elif input_choice == '3':
        display_all_tasks()
    elif input_choice == '4':
        display_missed_tasks()
    elif input_choice == '5':
        add_task()
    elif input_choice == '6':
        delete_task()
    elif input_choice == '0':
        pass


choice = ''
while choice != '0':
    print_main_menu()
    choice = input()
    execute_choice(choice)

