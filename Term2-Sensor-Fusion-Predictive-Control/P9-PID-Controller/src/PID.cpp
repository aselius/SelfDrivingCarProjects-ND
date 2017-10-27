#include "PID.h"

using namespace std;


//Constructor
PID::PID() {
    p_error = 0.0;
    i_error = 0.0;
    d_error = 0.0;
}

PID::~PID() {}

void PID::Init(double Kp, double Ki, double Kd) {
    _Kp = Kp;
    _Ki = Ki;
    _Kd = Kd;
}

void PID::UpdateError(double cte) {
    i_error += cte;
    d_error  = cte - p_error;
    p_error  = cte;
}

double PID::TotalError() {
    return (-_Kp * p_error - _Kd * d_error - _Ki * i_error);
}

