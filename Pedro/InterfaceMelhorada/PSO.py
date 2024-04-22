import random
import math
import numpy as np


#Define Class Particles
class Particle:
    def __init__ (self,position):
        self.position=position
        self.velocity=np.zeros_like(position)
        self.best_position=position
        self.best_fitness=float('inf')

def PSO(T,X,Y,ObjF,Pop_Size,D,MaxT):

    particles=[]

    #Posotion Initialization
    for i in range(Pop_Size):
      position = np.array([50*random.random(), 100*random.random(), 5000*random.random(),10*random.random()] )
      particle=Particle(position)



      #Fitness Update
      fitness=ObjF(position, T, X, Y)

      if i == 0:
        swarm_best_position=position
        swarm_best_fitness=fitness

      particle.best_position=position
      particle.best_fitness=fitness

      if fitness<swarm_best_fitness:
          swarm_best_fitness=fitness
          swarm_best_position=position

      particles.append(particle)

    #PSO Main Loop
    for itr in range(MaxT):

        for particle in particles:

            #Update Velocity
            w = 0.8
            c1 = 1.2
            c2 = 1.2

            r1=random.random()
            r2=random.random()

            #Velocity Calculation
            particle.velocity = w*particle.velocity+c1*r1*(particle.best_position-particle.position)+c2*r2*(swarm_best_position-particle.position)

            #New Position
            particle.position = particle.position + particle.velocity

            #Evaluate Fitness
            fitness = ObjF(particle.position, T, X, Y)

            #Update PBest
            if fitness<particle.best_fitness:
                particle.best_fitness=fitness
                particle.best_position=particle.position

            #Update GBest
            if fitness<swarm_best_fitness:
                swarm_best_fitness=fitness
                swarm_best_position=particle.position

    return swarm_best_position,swarm_best_fitness

#Define ObjFunction
# X = [0,0.04,0.12,0.19,0.55,1.25,1.65, 2.1,3.06,3.45,4.25,6.31,8.19,10.7,11.8,14.1,17.2,18.9]
# Y = [0,0.02,0.089, 0.13,0.33,0.71, 0.88,1.12, 1.47,1.62,1.83,2.36,2.73,3.06,3.26,3.53,3.83,3.99]
def F1(x,T,X,Y):
  result = 0
  for i in range(len(X)):
    result = result + (Y[i]-x[0]*x[1]*X[i]*math.exp(x[2]*(1/298.15-1/273.15))*(1-Y[i]/x[0])**x[3])**2
  return result
# XCO2 = [0,0.0118,0.061,0.2905,0.861,1.6,3.1,5.25,10.15,14.45,19.35,22.8,26.6,32]
# YCO2 =[0,1.147,2.249,3.659,4.5,5.06,5.58,6.04,6.52,6.92,6.96,7.09,7.22,7.372]
# def F2(x):
#   result = 0
#   for i in range(len(XCO2)):
#     result = result + (YCO2[i]-x[0]*x[1]*XCO2[i]*math.exp(x[2]*(1/298.15-1/273.15))*(1-YCO2[i]/x[0])**x[3])**2
#   return result

Objective_Function ={'F1':F1}

#Parameters
Pop_Size=200
MaxT=200
D=4

# Iterate over each objective function and run PSO
def chamaPSO(T, X, Y):
    return PSO(T, X, Y, F1, Pop_Size, D, MaxT)
    #for funName, ObjF in Objective_Function.items():
    #    Output = "Running Function = " + funName + "\n"
    #    best_position,best_fitness = PSO(T, X, Y, ObjF,Pop_Size,D,MaxT)
    ##    Output += "BEST POSITION : " + str(best_position)+"\n"
     #   Output += "BEST COST : " + str(best_fitness)
     #   Output += "\n"

      #  print("PSO RUN",Output)
      #  return