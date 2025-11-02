import math


class PIDController:
    def __init__(self, kp = 0, ki =0 , kd= 0, dt = 0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt

        self.setpoint = 0
        self.state = 0
        self.error = 0
        self.cum_error = 0
        self.deriv_error = 0

        self.max_input = 1000
        self.min_input = -1000

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

        control_signal = self.kp*self.error + self.ki*self.cum_error + self.kd*self.deriv_error
        return self.inputBounding(control_signal)

