from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


class WorkoutCalendar(HTMLCalendar):
    """
    All users can preview their trainings due to WorkoutCalendar.
    It contains training information (user name, date and short description of training).
    """

    def __init__(self, workouts):
        """
        Init procedure. As default WorkoutCalendar groups trainings in workout by day.

        `workouts`: list of Workout class objects.
        """
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)


    def formatday(self, day, weekday):
        """
        This method forms appropriate day view.
        It compares actual date with day passed as argument and sequentially attaches css classes.


        `day`: number that represents day for which training will be displayed.
        `weekday`: number of day in week.

        Method returns day cell with appropriate appearance.
        """
        if day != 0:
            cssclass = self.cssclasses[weekday]
            cssclass += ' day'
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<div class=\"container"><div class=\"filler\"></div>']
                for workout in self.workouts[day]:
                    body.append(self.create_day_with_workouts(workout))
                body.append('<div hidden class=\'training\'>Click to see the trainings!</div>')
                body.append('</div>')
                # print("FINAL ccs_class" + " " +  cssclass)
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            # print("FINAL ccs_class" + " " + cssclass)
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        """
        Method that formats month.

        `year`: number that represents year.
        `month`: number that represents month.

        Method returns month's calendar as an HTML table.
        """
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        """
        Method that groups trainings by day.

        `workouts`: list of Workout objects.

        Method returns list of workouts sorted by day.
        """
        field = lambda workout: workout.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def create_day_with_workouts(self, workout):
        body = '<div class=workout_info><ul>'
        body += '<li>User: ' + (workout.user.name)
        body += "</li><li>"
        body += 'Workout: ' + esc(workout.title)
        body += '</li></ul></div>'

        return body