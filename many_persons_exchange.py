import random
import statistics


class Person(object):
    # constructor: define all the attributes and what need to do when creating an instance
    def __init__(self, personID, sim):
        self.personID = personID
        self.budget = random.gauss(50, 10)
        self.sim = sim
    def Step(self):
        persons = random.sample(self.sim.personList, 10)
        sumbudget = self.budget #sumbudget is a local variable, so it does not need self.something
        
        for anperson in persons:
            sumbudget = sumbudget + anperson.budget
        
        self.budget = sumbudget/(len(persons) + 1)
        
        #print (self.budget)
            

class Sim(object): #create list of agents
    
    def __init__(self):
        
        self.personList = [Person(x,self)for x in range(100)]     
        
    def Run(self):
        
        for step in range(10):
            print(step)
            
            for anperson in self.personList:            
                anperson.Step()
            for anperson in self.personList:
                arraybudget = []
                #print(anperson.budget)
            for anperson in self.personList:
                arraybudget.append(anperson.budget)
            stdev = statistics.stdev(arraybudget)
            print (stdev)
            
            if stdev < 0.01:
                print ("It breaks at step", step)
                break


                
            
if __name__ == '__main__':
    
    aSim = Sim()
    
    print ("simulation starts...")
    aSim.Run()
