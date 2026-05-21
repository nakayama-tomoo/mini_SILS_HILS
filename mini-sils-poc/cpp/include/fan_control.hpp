#pragma once

enum class FanState {
    OFF,
    LOW,
    HIGH
};

FanState decideFanState(FanState prevState, int coolantTempC);
