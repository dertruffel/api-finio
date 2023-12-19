import json


class Calculator():

    def next_month(self, current_month):
        if current_month == "january":
            return "february"
        elif current_month == "february":
            return "march"
        elif current_month == "march":
            return "april"
        elif current_month == "april":
            return "may"
        elif current_month == "may":
            return "june"
        elif current_month == "june":
            return "july"
        elif current_month == "july":
            return "august"
        elif current_month == "august":
            return "september"
        elif current_month == "september":
            return "october"
        elif current_month == "october":
            return "november"
        elif current_month == "november":
            return "december"
        elif current_month == "december":
            return "finished"

    def uop(self, data):
        return_data = {
            "january": "0",
            "february": "0",
            "march": "0",
            "april": "0",
            "may": "0",
            "june": "0",
            "july": "0",
            "august": "0",
            "september": "0",
            "october": "0",
            "november": "0",
            "december": "0",
            "total": "0",
        }
        data = data
        if data['type'] != 'uop':
            return "Wrong type"
        pit0 = data['under26']
        monthly_gross = data['monthlyPayGross']
        current_month = "january"
        current_earnings = 0
        current_net = 0
        # retirement = 0.0976
        # disability = 0.015
        # sickness = 0.0245
        # health = 0.0775
        # vat free amount = 30k
        if pit0:
            vat_free_amount = 85528
        else:
            vat_free_amount = 30000
            # under 120000 vat is 12%, over its 32%
        for i in range(12):
            starting = monthly_gross
            starting_const = monthly_gross
            retirement = (monthly_gross * 0.0976)  # retirement
            disability = (monthly_gross * 0.015)  # disability
            sickness = (monthly_gross * 0.0245)  # sickness
            health = (monthly_gross * 0.0775)  # health
            print(starting, retirement, disability, sickness, health)
            starting = starting - retirement - disability - sickness - health
            print(starting)
            if current_earnings >= vat_free_amount:
                apply_vat = True
            else:
                apply_vat = False
            print(starting_const, apply_vat)
            if apply_vat:
                if current_earnings + starting_const > 120000:
                    amount_under_120k = max(0, 120000 - current_earnings)
                    amount_over_120k = max(0, starting - amount_under_120k)
                    vat = amount_under_120k * 0.12 + amount_over_120k * 0.32
                    starting -= vat
                else:
                    vat = starting * 0.12
                    starting -= vat
            else:
                vat = 0
            return_data[current_month] = str(round(starting, 2))
            current_earnings = current_earnings + starting_const
            current_net = current_net + starting
            current_month = self.next_month(current_month)
        return_data['total'] = str(round(current_net, 2))
        return return_data

    def uz(self, data):
        return_data = {
            "january": "0",
            "february": "0",
            "march": "0",
            "april": "0",
            "may": "0",
            "june": "0",
            "july": "0",
            "august": "0",
            "september": "0",
            "october": "0",
            "november": "0",
            "december": "0",
            "total": "0",
        }
        data = data
        if data['type'] != 'uz':
            return "Wrong type"
        pit0 = data['under26']
        monthly_gross = data['monthlyPayGross']
        current_month = "january"
        current_earnings = 0
        current_net = 0
        zus_option = data['zus']
        sickLeave = data['sickLeave']
        # retirement = 0.0976 if zus-my-employeer, if zus-other-employeer 0, if student26 0
        # disability = 0.015, if zus-my-employeer, if zus-other-employeer 0, if student26 0
        # sickness = 0, if zus-my-employeer, if zus-other-employeer 0, if student26 0, if sickLeave 0.0245 for zus-my-employeer, if zus-other-employeer 0, if student26 0.0245
        # health = 0.0775 if zus-my-employeer, if zus-other-employeer 0.09, if student26 0
        # vat free amount = 30k
        if pit0:
            vat_free_amount = 85528
        else:
            vat_free_amount = 30000
            # under 120000 vat is 12%, over its 32%
        for i in range(12):
            starting = monthly_gross
            starting_const = monthly_gross
            if zus_option == "zus-my-employer":
                one = (monthly_gross * 0.0976)
                two = (monthly_gross * 0.015)
                if sickLeave:
                    three = (monthly_gross * 0.0245)
                four = (monthly_gross * 0.0775)
                starting = starting - one - two - four
                if sickLeave:
                    starting = starting - three
            elif zus_option == "zus-other-employer":
                starting = starting - (monthly_gross * 0.09)
            elif zus_option == "student26":
                if sickLeave:
                    starting = starting - (monthly_gross * 0.0245)
            if current_earnings >= vat_free_amount:
                apply_vat = True
            else:
                apply_vat = False
            if apply_vat:
                if current_earnings + starting_const > 120000:
                    # 12% vat for the amount under 120k, and 32% for the amount over 120k
                    if current_earnings < 120000:
                        amount_under_120k = 120000 - current_earnings
                        amount_over_120k = starting - amount_under_120k
                        vat = amount_under_120k * 0.12 + amount_over_120k * 0.32
                        starting = starting - vat
                    else:
                        vat = starting * 0.32
                        starting = starting - vat
                else:
                    vat = starting * 0.12
                    starting = starting - vat
            else:
                vat = 0
            return_data[current_month] = str(round(starting, 2))
            current_earnings = current_earnings + starting_const
            current_net = current_net + starting
            current_month = self.next_month(current_month)
        return_data['total'] = str(round(current_net, 2))
        return return_data

    def uod(self, data):
        return_data = {
            "january": "0",
            "february": "0",
            "march": "0",
            "april": "0",
            "may": "0",
            "june": "0",
            "july": "0",
            "august": "0",
            "september": "0",
            "october": "0",
            "november": "0",
            "december": "0",
            "total": "0",
        }
        data = data
        if data['type'] != 'ud':
            return "Wrong type"
        monthly_gross = data['monthlyPayGross']
        current_month = "january"
        current_earnings = 0
        current_net = 0
        costOfIncome = data['costOfIncome']
        if costOfIncome == 20:
            mult = 0.904
        else:
            mult = 0.94
        for i in range(12):
            starting = monthly_gross * mult
            return_data[current_month] = str(round(starting, 2))
            current_earnings = current_earnings + starting
            current_net = current_net + starting
            current_month = self.next_month(current_month)
        return_data['total'] = str(round(current_net, 2))
        return return_data

    def b2b(self, data):
        return_data = {
            "january": "0",
            "february": "0",
            "march": "0",
            "april": "0",
            "may": "0",
            "june": "0",
            "july": "0",
            "august": "0",
            "september": "0",
            "october": "0",
            "november": "0",
            "december": "0",
            "total": "0",
        }
        data = data
        if data['type'] != 'b2b':
            return "Wrong type"
        monthly_gross = data['monthlyPayGross']
        starting_const = monthly_gross
        current_month = "january"
        current_earnings = 0
        current_net = 0
        zusb2b = data['zusb2b']
        tax = data['tax']
        sickLeave = data['sickLeave']
        if zusb2b == "ulga":
            zusless_months = 6
            lower_zus_months = True
        elif zusb2b == "preference":
            zusless_months = 0
            lower_zus_months = True
        else:
            zusless_months = 0
            lower_zus_months = False
        for i in range(12):
            # zus
            starting = monthly_gross
            if zusless_months > 0:
                zusless_months = zusless_months - 1
                starting = starting * 0.9
            elif lower_zus_months:
                starting = starting * 0.93
                starting = starting - 176.71
                starting = starting - 72.24
                if sickLeave:
                    starting = starting - 15.08

                starting = starting - 22.12
            else:
                one = starting * 0.043491
                two = starting * 0.077
                starting = starting - one - two
                starting = starting - 693.58
                if sickLeave:
                    starting = starting - 87.50
                starting = starting - 59.34
                starting = starting - 87.05
            # tax
            if tax == "19":
                starting = starting * 0.81
            elif tax == "12/32":
                if current_earnings + starting_const > 120000:
                    # 12% vat for the amount under 120k, and 32% for the amount over 120k
                    if current_earnings < 120000:
                        amount_under_120k = 120000 - current_earnings
                        amount_over_120k = starting - amount_under_120k
                        vat = amount_under_120k * 0.12 + amount_over_120k * 0.32
                        starting = starting - vat
                    else:
                        vat = starting * 0.32
                        starting = starting - vat
                else:
                    vat = starting * 0.12
                    starting = starting - vat
            else:
                print("Wrong tax")
            return_data[current_month] = str(round(starting, 2))
            current_earnings = current_earnings + starting_const
            current_net = current_net + starting
            current_month = self.next_month(current_month)
        return_data['total'] = str(round(current_net, 2))
        return return_data
