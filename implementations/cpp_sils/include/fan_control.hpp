#pragma once

#include <string>

enum class FanState {
    OFF,
    LOW,
    HIGH
};

struct FanControlThresholds {
    int lowOnC;
    int offC;
    int highOnC;
    int highOffC;
};

FanControlThresholds thresholdsForVersion(const std::string& versionId);

FanState decideFanState(FanState prevState, int coolantTempC);

FanState decideFanState(
    FanState prevState,
    int coolantTempC,
    const FanControlThresholds& thresholds
);

std::string fanStateToString(FanState state);

FanState fanStateFromString(const std::string& value);
