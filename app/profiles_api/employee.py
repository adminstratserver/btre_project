import datetime
from jbnnb

class Employee:

    salary_increment_rate = 1.04

    def __init__(self, firstname, lastname, company, salary):
        self.firstname = firstname
        self.lastname = lastname
        self.company = company
        self.salary = salary

    def getfullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def salaryincrease(self):
        self.salary = self.salary * self.salary_increment_rate

    @classmethod
    def change_salary_rate(cls, newrate):
        cls.salary_increment_rate = newrate

    @staticmethod
    def check_ifweekend(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return True
        return False


class Developer(Employee):
    def __init__(self, firstname, lastname, company, salary, program_language):
        super().__init__(firstname, lastname, company, salary)
        self.program_language = program_language


empl1 = Developer('David', 'Tang', 'HBI', 100, 'python')
empl2 = Developer('Pintip', 'Ophakawinkul', 'Booking', 200, 'java')


print('1. emp1 name=', empl1.getfullname())
print('2. emp1 program_lang=', empl1.program_language)
print('3. emp2 name=', Developer.getfullname(empl2))
print('3. emp1 program_lang=', empl2.program_language)


'''
print('2. emp2 fullname=', empl2.getfullname())
print('3. emp2 fullname=', Employee.getfullname(empl2))
print('4. emp2 dict', empl2.__dict__)
print('5. emp1 salary', empl1.salary)
# Employee.salaryincrease(empl1)
print('6. emp1 salary', empl1.salary)
Employee.change_salary_rate(1.05)
Employee.salaryincrease(empl1)
print('6. emp1 salary', empl1.salary)
mydate = datetime.date(2019, 11, 30)
print(Employee.check_ifweekend(mydate))
mydate = datetime.date(2019, 12, 1)
print(Employee.check_ifweekend(mydate))
'''
