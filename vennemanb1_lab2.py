class timeRates:
    #intitialize talk rates
    rates = {
        'c': {'startRate' : 0.20, 'limit' : 300, 'endRate' : 0.10},
        'r': {'startRate' : 0.10, 'limit' : 120, 'endRate' : 0.05},
        's': {'startRate' : 0.15}
        
    }

    @classmethod
    # method for asking what plan type the user has and gets the number of minutes talked and requires an integer for it
    def get_and_validate_talk_time(cls):
        while True:
            # ask for plan
            planType = input("Enter Plan Type: (C/c for Commercial, R/r for Residential, S/s for Student)").lower()
            if planType not in ['C', 'c', 'R', 'r', 'S', 's']:
                print("Invalid plan type, please retry. (C/c for Commercial, R/r for Residential, S/s for Student)")
                continue
            try:
                # ask for minutes
                talkMinutes = int(input("Enter number of minutes used: (Whole number only)"))
                if talkMinutes < 0 or talkMinutes > 10080:
                    print("Invalid minutes. Must be between 0 and 10080")
                    continue
                return planType, talkMinutes
            # if not an integer try again
            except ValueError:
                print("Invalid input. Please enter a whole number for minutes.")

    @classmethod
    # method to calculate talk time based on the plan type
    def calculate_talk_time(cls, planType, talkMinutes):
        finalRate = cls.rates.get(planType, {'startRate': 0.0})
        # calculate rate
        if 'limit' in finalRate and talkMinutes > finalRate['limit']:
            due = finalRate['startRate'] * finalRate['limit'] + finalRate['endRate'] * (talkMinutes - finalRate['limit'])
        else:
            due = finalRate['startRate'] * talkMinutes


        remCredit = max(25.00 - due, 0.00)
        return due, remCredit
        
    @classmethod
    # main method to get and validate the talk time and calculate it and will ask to enter new customers or not
    def main(cls):
        customerID = 0
        while True:
            # call methods
            planType, talkMinutes = cls.get_and_validate_talk_time()
            due, remCredit = cls.calculate_talk_time(planType, talkMinutes)
            customerID += 1
            # give them correct amount back left or due in account
            if due > 25.00:
                print(f"{customerID} {planType} {talkMinutes} Amount due: $ {due:.2f}")
            else:
                print(f"{customerID} {planType} {talkMinutes} Remaining Credit: $ {remCredit:.2f}")
            # ask if they want to enter a new customer or no
            nextCustomer = input("Enter more information for next customer? (yes/no)")
            if nextCustomer.lower() != 'yes':
                break

if __name__ == "__main__":
    timeRates.main()


