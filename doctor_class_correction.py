class doctor:
    def __init__(self,id,abilities, working_rate,graphic_of_work, available_days, raspisanie, amount_of_hours, starting_time, is_used ):
        self.id = id                                #@ айдишник врача
        self.abilities = abilities                  #@ что врач может делать
        self.working_rate = working_rate            #@ ставка врача
        self.graphic_of_work = graphic_of_work      #@ график работы, типо 1\1, или 2\2, или 5\2
        self.available_days = []                    # расписание врача
        self.amount_of_hours = []                   # количество рабочих часов в смену
        self.starting_time = []                     # когда смена начиналась  у врача
        self.activities_per_day = []                # количество оставшейся энергии врача
        self.new_available_days = []                # новое расписание на каждый день в месяце
        self.work_per_day = []                      # какие ивенты врач выполнял за день
        self.is_used = is_used
        self.koef = []                              # коэффициент работы врача, типо 1 из 1 - стандартное кол-во деталей в смену
        self.raspisanie = raspisanie
        day_schet = 0
        for week in range(0,len(raspisanie)):
            self.available_days.append([])
            self.work_per_day.append([])
            self.new_available_days.append([])
            self.activities_per_day.append([])
            self.amount_of_hours.append([])
            self.starting_time.append([])
            self.koef.append([])

            for day in range(0, len(raspisanie[week])):
                self.available_days[week].append(available_days[day_schet] )
                self.work_per_day[week].append([])
                self.new_available_days[week].append(0)
                self.amount_of_hours[week].append(amount_of_hours[day_schet])
                self.activities_per_day[week].append(300 * available_days[day_schet]  * amount_of_hours[day_schet] / 8)
                self.starting_time[week].append(starting_time[day_schet])
                self.koef[week].append(available_days[day_schet] * amount_of_hours[day_schet]/8)

                day_schet+=1
        i = 0
        self.time_out = []
        for week in self.amount_of_hours:
            self.time_out.append([])
            for pereriv in week:
                if pereriv > 8:
                    self.time_out[i].append(1)
                else:
                    self.time_out[i].append(0.5)
            i += 1

    def get_id(self):
        return self.id
    def get_abilities(self):
        return self.abilities
    def get_working_rate(self):
        return self.working_rate

    def get_graphic_of_work(self):
        return self.graphic_of_work

    def get_available_days(self):
        return self.available_days

    def get_available_day(self, week, day):
        return self.available_days[week][day]

    def get_work_per_day(self, week, day):
        return self.work_per_day[week][day]

    def get_new_available_days(self, week, day):
        return self.new_available_days[week][day]
    def get_amount_of_hours(self, week, day):
        return self.amount_of_hours[week][day]

    def get_starting_time(self, week, day):
        return self.starting_time[week][day]

    def get_activities_per_day(self, week, day):
        return self.activities_per_day[week][day]

    def get_koef(self, week, day):
        return self.koef[week][day]

    def get_used(self):
        return self.is_used

    def set_work_per_day(self, schedule,  week, day):
        self.work_per_day[week][day] = schedule

    def set_new_available_days(self, schedule, week, day):
        self.new_available_days[week][day] = schedule

    def set_amount_of_hours(self, schedule, week, day):
        self.amount_of_hours[week][day] = schedule

    def set_starting_time(self, schedule, week, day):
        self.starting_time[week][day] = schedule

    def set_activities_per_day(self, schedule, week, day):
        self.activities_per_day[week][day] = schedule

    def set_koef(self, schedule, week, day):
        self.koef[week][day] = schedule

    def set_used(self, flag):
        self.is_used = flag

    def vivod(self):
        print(str(self.id) + "  " + str(self.abilities) + "  " +  str(self.working_rate) + "  " + str(self.graphic_of_work) + "  " + str(self.available_days) + "  " + str(self.raspisanie) + "  " + str(self.amount_of_hours) + "  " + str(self.starting_time) + "  " + str(self.is_used))

    def get_pereriv(self,week):
        return self.time_out[week]

    def set_pereriv(self, shedule, week):
        self.time_out[week] = shedule






























