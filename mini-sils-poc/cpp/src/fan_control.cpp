#include "fan_control.hpp"

FanState decideFanState(FanState prevState, int coolantTempC)
{
    if (prevState == FanState::OFF) {
        if (coolantTempC < 95) {
            return FanState::OFF;
        }

        if (coolantTempC < 105) {
            return FanState::LOW;
        }

        return FanState::HIGH;
    }

    if (prevState == FanState::LOW) {
        if (coolantTempC <= 90) {
            return FanState::OFF;
        }

        if (coolantTempC < 105) {
            return FanState::LOW;
        }

        return FanState::HIGH;
    }

    if (prevState == FanState::HIGH) {
        if (coolantTempC <= 90) {
            return FanState::OFF;
        }

        if (coolantTempC <= 100) {
            return FanState::LOW;
        }

        return FanState::HIGH;
    }

    return FanState::OFF;
}
