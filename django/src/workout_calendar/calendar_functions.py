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
            cssid = str(self.year) + "-" + self.format_one_digit(self.month) + "-" + self.format_one_digit(day)
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
                return self.day_cell(cssclass, cssid, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, cssid, day)
        return self.day_cell_no_id('noday', '&nbsp;')

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

    def day_cell(self, cssclass, cssid, body):
        """
        Method that formats the div for the day that has id.

        `cssclass`: class name to be applied in this div
        `cssid`: id to be applied in this div
        `body`: content of the div

        Method returns a HTML sample that represents a formatted div.
        """
        return '<td class="%s" id="%s">%s</td>' % (cssclass, cssid, body)

    def day_cell_no_id(self, cssclass, body):
        """
        Method that formats the div for the day with no id.

        `cssclass`: class name to be applied in this div
        `body`: content of the div

        Method returns a HTML sample that represents a formatted div.
        """
        return '<td class="%s">%s</td>' % (cssclass, body)

    def create_day_with_workouts(self, workout):
        """
        Method that adds workout information to the div.

        `workout`: Workout object that should be added to the div

        Method returns a HTML sample that represents a formatted div.
        """
        body = '<div class=workout_info id=' + str(workout.id) + '><ul>'
        body += '<li>' + workout.title
        body += "<li>"
        body += esc(workout.distance) + ' km'
        body += '</li></ul></div>'

        return body

    def format_one_digit(self, string_to_format):
        """
        Method that formats input string to be a valid month string.

        `string_to_format`: a string that represents the month number

        Method returns a formatted string.
        """
        string_to_format = str(string_to_format)
        if len(string_to_format) < 2:
            return '0' + string_to_format
        else:
            return string_to_format
