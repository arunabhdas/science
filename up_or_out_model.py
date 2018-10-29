import random  # used to generate random numbers; often needed when initilizing agents
from random import randint
import statistics
from scipy import stats
from enum import Enum
import uuid


class EmployeeStatus(Enum):
    NEW_HIRE = 1
    WORKING = 2
    PROMOTE = 3
    FIRED = 4
    QUIT = 5


class Person(object):
    def __init__(self, is_new_hire = True):
        self.person_id = uuid.uuid4()
        self.performance = 0
        years_at_work = 0 if is_new_hire else randint(1, 9)        
        self.status = EmployeeStatus.NEW_HIRE if years_at_work == 0 else EmployeeStatus.WORKING
        self.status_history = [EmployeeStatus.WORKING for year in range(years_at_work)]

        
    def step(self, status, new_status=EmployeeStatus.WORKING):
        #self.years_at_work += 1
        self.status = new_status
        self.should_quit()
        self.status_history.append(status)        
            
    def should_quit(self, status_history):
        if status_history[-3:].count(EmployeeStatus.WORKING) >= 3 and not self.status != EmployeeStatus.PROMOTE:
            self.status = EmployeeStatus.QUIT


    def calculate_performance(self, universal_cases):
        cases_assigned = (random(1, (universal_cases)))
        cases_won = (random(0, (self.cases_assigned)))
        self.performance = cases_won/cases_assigned

        
        
class Firm(object):
    # constructor: define all the attributes and what need to do when creating an instance
    def __init__(self, market):
        self.market = market
        self.universal_cases = random.gauss(100, 10)
        self.persons = [self.market.get_person_from_market(False) for i in range(100)]

    def step(self):
        # 1. work
        for person in self.persons:
            person.calculate_performance() # TODO assign cases to person not universal cases (or everyone can do everything)
        # 2. evaluate
        # TODO promote tied people.
        top_performers = self.get_top_performers()
        for person in self.persons:
            if person in top_performers: # TODO if 10 people left always promoted
                new_status = EmployeeStatus.PROMOTE
            person.step(new_status)
            self.should_fire_person(person)
        # 3. hire
        self.hire_new_people()
        
    def is_top_performer(self, person):
        return person in self.get_top_performers()

    def get_top_performers(self):
        ranked_persons = sorted(self.persons, key = lambda x: x.performance, reverse= True)
        return ranked_persons[:10]
    
    def get_bottom_performers(self): # TODO remaining bottom performers
        ranked_persons = sorted(self.persons, key = lambda x: x.performance, reverse= True)
        remaining_people = [person for person in ranked_persons if person.status != EmployeeStatus.QUIT]
        return remaining_people[-10:]

    def should_fire_person(self, person):
        if person in self.get_bottom_performers():
            person.status = EmployeeStatus.FIRED
            person.status_history[-1] = EmployeeStatus.FIRED
            return True
        return False
            
    def hire_new_people(self):
        n_fired = len([person for person in self.persons if person.status == EmployeeStatus.FIRED])
        # remoive fired and quit
        new_persons = [person for person in self.persons if person.status not in [EmployeeStatus.FIRED, EmployeeStatus.QUIT] ]
        # hire new
        new_persons.extend([self.market.get_person_from_market() for i in range(n_fired)])
        self.persons = new_persons
   
        
class Sim(object):
    def __init__(self, n_simulations=100):
        self.n_simulations = n_simulations 
        self.firm = Firm(self) #firm object inherits all attributes of Firm class
        self.persons = {0: []} #persons list of every simulation iteration, it starts at element zero, then appends array/list of persons for every iteration
        self.current_simulation = 0 #we are starting at zero simulation

    def get_person_from_market(self, is_new_hire):
        person = Person(is_new_hire)
        self.persons[self.current_simulation].append(person) #for the persons population marked by [index] of current simulation, append this new person
        return person(self.firm, is_new_hire)

    def step(self):
        self.current_simulation += 1
        if not self.current_simulation in self.persons:
            self.persons[self.current_simulation] = []
        self.firm.step()

    def Run(self):
        for step in range(self.n_simulations):
            self.step()
        
    
if __name__ == '__main__':
    
    aSim = Sim()
    print ("simulation starts...")
    aSim.Run()                    
    
