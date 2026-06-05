#include <iostream>

#include "fan_control.hpp"

const char* toString(FanState state)
{
    switch (state) {
        case FanState::OFF:
            return "OFF";

        case FanState::LOW:
            return "LOW";

        case FanState::HIGH:
            return "HIGH";
    }

    return "UNKNOWN";
}

int main()
{
    FanState result = decideFanState(FanState::OFF, 96);

    std::cout << "Result: " << toString(result) << std::endl;

    return 0;
}
