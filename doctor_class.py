class doctor:
    def __init__(self,id,abilities, working_rate,graphic_of_work, available_days, amount_of_hours, is_used ):
        self.id = id
        self.abilities = abilities
        self.working_rate = working_rate
        self.graphic_of_work = graphic_of_work
        self.available_days = []
        for d in available_days:
            self.available_days.append(d[:])
        self.is_used = is_used
        self.amount_of_hours = []          #количество рабочих часов в неделю, тоэже вроде безполезный параметр

        self.time_schedule = []             #параметр для вычисления продуктивности, тип 8 часов - 1, 10 часов в смене - 1.2
        self.time_out = []
        i = 0
        for week in self.available_days:
            self.amount_of_hours.append([])
            self.time_schedule.append([])
            for day in week:

                self.amount_of_hours[i].append(amount_of_hours[i]* day  * self.working_rate )
                self.time_schedule[i].append(amount_of_hours[i] * day * self.working_rate / 8)
            i+=1
        #print(self.time_schedule)
        i = 0
        for week in self.amount_of_hours:
            self.time_out.append([])
            for pereriv in week:
                if pereriv > 8:
                    self.time_out[i].append(1)
                else:
                    self.time_out[i].append(0.5)
            i += 1

        self.activities_per_day = []              #количество оставшейся энергии врача
        self.new_available_days = []              #новое расписание на каждый день в месяце
        self.work_per_day = []                    #какие ивенты врач выполнял за день

        i = 0

        for week in available_days:
            self.activities_per_day.append([])
            self.new_available_days.append([])
            self.work_per_day.append([])
            j = 0
            for day in week:
                if day > 0:
                    self.activities_per_day[i].append( 300 *self.time_schedule[i][j])
                else:
                    self.activities_per_day[i].append(0)
                self.new_available_days[i].append(0)
                self.work_per_day[i].append([])
                j+=1
            i += 1

    def set_new_available_days(self, new_schedule, week, day):
        self.new_available_days[week][day] = new_schedule

    def get_new_available_days(self):

        return self.new_available_days

    def get_work_per_day(self):
        return self.work_per_day

    def get_activities_per_day(self,week,day):
        return self.activities_per_day[week][day]

    def set_work_per_day(self, new_schedule, week, day):
        self.work_per_day[week][day].append(new_schedule)

    def set_activities_per_day(self, new_schedule, week, day):
        self.activities_per_day[week][day] = new_schedule

    def get_pereriv(self,week):
        return self.time_out[week]

    def set_pereriv(self, shedule, week):
        self.time_out[week] = shedule

    def get_pereriv_per_day(self,week,day):
        return self.time_out[week][day]

    def set_pereriv_per_day(self, shedule, week, day):
        self.time_out[week][day] = shedule

    def get_id(self):
        return self.id

    def get_abilities(self):
        return self.abilities

    def get_working_rate(self):
        # print(self.working_rate)
        return self.working_rate

    def get_available_days(self):
        return self.available_days

    def get_graphic_of_work(self):
        return self.graphic_of_work

    def get_amount_of_hours(self,week):
        return self.amount_of_hours[week]
    def get_amount_of_hours_per_day(self,week,day):
        return self.amount_of_hours[week][day]

    def get_used(self):
        return self.is_used

    def get_available_week_schedule(self, week):
        return self.available_days[week]

    def get_available_day_schedule(self, week, day):
        return self.available_days[week][day]

    def get_week_schedule(self, week):
        return self.time_schedule[week]

    def get_day_schedule(self, week, day):
        return self.time_schedule[week][day]

    def get_schedule(self):
        return self.time_schedule

    def set_new_day_schedule(self, week, day, new_schedule):
        self.available_days[week][day] = new_schedule

    def set_new_week_schedule(self, week, new_schedule):
        self.available_days[week] = new_schedule

    def set_available_days(self, new_schedule):
        self.available_days = new_schedule

    def set_used(self, flag):
        self.is_used = flag

    def set_new_abilities(self,abilities):
        self.abilities = abilities

    def set_new_working_rate(self,rate):
        self.working_rate = rate



    def vivod(self):
        pass
        #print(str(self.id) + "  " + str(self.abilities) + "  " + str(self.working_rate) + "  " + str(self.graphic_of_work) + "  " + str(self.available_days) + "  " + str(self.amount_of_hours))
