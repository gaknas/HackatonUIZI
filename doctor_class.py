class doctor:
    def __init__(self,id,abilities, working_rate,graphic_of_work, available_days, is_used ):
        self.id = id
        self.abilities = abilities
        self.working_rate = working_rate
        self.graphic_of_work = graphic_of_work
        #self.available_days = available_days[:]
        self.available_days =[]
        for d in available_days:
            self.available_days.append(d[:])
        self.is_used = is_used
        self.amount_of_hours = []          #количество рабочих часов в неделю, тоэже вроде безполезный параметр

        self.time_schedule = []
        self.time_out  = []
        for week_schedule in available_days:
            if sum(week_schedule) == 3:
                self.time_schedule.append(1.4)
                self.amount_of_hours.append(12 * working_rate)
            if sum(week_schedule) == 4:
                self.time_schedule.append(1.2)
                self.amount_of_hours.append(10 * working_rate)
            if sum(week_schedule) == 5:
                self.time_schedule.append(1)
                self.amount_of_hours.append(8 * working_rate)
        for pereriv in self.amount_of_hours:
            if pereriv > 8:
                self.time_out.append(1)
            else:
                self.time_out.append(0.5)


    def get_pereriv(self,week):
        return self.time_out[week]
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


    def get_used(self):
        return self.is_used

    def get_available_week_schedule(self, week):
        return self.available_days[week]

    def get_available_day_schedule(self, week, day):
        return self.available_days[week][day]

    def get_week_schedule(self, week):
        return self.time_schedule[week]

    def get_schedule(self):
        return self.time_schedule

    def set_new_day_schedule(self, week, day, new_schedule):
        self.available_days[week][day] = new_schedule

    def set_new_week_schedule(self, week, new_schedule):
        self.available_days[week] = new_schedule

    def set_new_available_days(self, new_schedule):
        self.available_days = new_schedule

    def set_used(self, flag):
        self.is_used = flag

    def set_new_abilities(self,abilities):
        self.abilities = abilities

    def set_new_working_rate(self,rate):
        self.working_rate = rate


    def vivod(self):
        print(str(self.id) + "  " + str(self.abilities) + "  " + str(self.working_rate) + "  " + str(self.graphic_of_work) + "  " + str(self.available_days) + "  " + str(self.amount_of_hours))
