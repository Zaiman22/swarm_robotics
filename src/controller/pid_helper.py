import math
import numpy as np

class PIDController:
    def __init__(self, kp = 0, ki =0 , kd= 0, dt = 0.01, number_of_signals = 1):
        self.kp = np.array(kp)
        self.ki = np.array(ki)
        self.kd = np.array(kd)
        self.dt = dt

        self.setpoint = 0
        self.state = 0
        self.error = 0
        self.cum_error = 0
        self.deriv_error = 0

        self.max_input = 1000
        self.min_input = -1000


        self.control_signal = np.zeros(number_of_signals)

    def setSetPoint(self, setpoint):
        self.setpoint = setpoint


    def setState(self,state):
        self.state = state

    def getError(self):
        prev_error = self.error
        self.error = self.setpoint-self.state
        self.cum_error += self.error*self.dt
        self.deriv_error = (self.error - prev_error)/self.dt

    def setTimeDelta(self, dt):
        self.dt = dt


    def inputBounding(self,input):
        return max(self.min_input, min(input, self.max_input))


    def getInput(self,setpoint,state):
        self.setState(state)
        self.setSetPoint(setpoint)
        self.getError()

        self.control_signal = self.kp*self.error + self.ki*self.cum_error + self.kd*self.deriv_error
        return self.inputBounding(self.control_signal)

