from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


class WorkoutCalendar(HTMLCalendar):
    """All users can preview their trainings due to WorkoutCalendar. 
    It contains training information (user name, date and short description of training). 
    """

    def __init__(self, workouts):
        """Init procedure. As default WorkoutCalendar groups trainings in workout by day. 
        
        :param `workouts`: list of Workout class objects.
        """
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)


    def formatday(self, day, weekday):
        """This method forms appropriate day view. 
        It compares actual date with day passed as argument and sequentially attaches css classes.
        
        :param `day`: number that represents day for which training will be displayed.
        :param `weekday`: number of day in week.
        :return: Day cell with appropriate appearance.
        """
        if day != 0:
            cssclass = self.cssclasses[weekday]
            cssclass += ' day'
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    body.append('<li>')
                    body.append(workout.user.name)
                    body.append (" ")
                    body.append(esc(workout.title))
                    body.append('</li>')
                body.append('</ul>')
                # print("FINAL ccs_class" + " " +  cssclass)
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            # print("FINAL ccs_class" + " " + cssclass)
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        """Method that formats month.
        
        :param year: number that represents year.
        :param month: number that represents month.
        :return: month's calendar as an HTML table.
        """
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        """Method that groups trainings by day.
        
        :param workouts: list of Workout objects.
        :return: List of workouts sorted by day.
        """
        field = lambda workout: workout.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)