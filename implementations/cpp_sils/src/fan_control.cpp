#include "fan_control.hpp"

#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <string>

namespace {

std::string normalizeStateName(const std::string& value)
{
    std::string normalized;
    normalized.reserve(value.size());

    for (unsigned char c : value) {
        if (c == ' ' || c == '\t' || c == '\r' || c == '\n') {
            continue;
        }

        normalized.push_back(
            static_cast<char>(std::toupper(c))
        );
    }

    return normalized;
}

}  // namespace

FanControlThresholds thresholdsForVersion(const std::string& versionId)
{
    if (versionId == "fan_control_v1" || versionId == "v1") {
        return FanControlThresholds{
            95,
            90,
            105,
            100,
        };
    }

    if (versionId == "fan_control_v2" || versionId == "v2") {
        return FanControlThresholds{
            94,
            89,
            104,
            99,
        };
    }

    throw std::invalid_argument(
        "Unsupported fan control version_id: " + versionId
    );
}

FanState decideFanState(FanState prevState, int coolantTempC)
{
    return decideFanState(
        prevState,
        coolantTempC,
        thresholdsForVersion("fan_control_v1")
    );
}

FanState decideFanState(
    FanState prevState,
    int coolantTempC,
    const FanControlThresholds& thresholds
)
{
    if (prevState == FanState::OFF) {
        if (coolantTempC < thresholds.lowOnC) {
            return FanState::OFF;
        }

        if (coolantTempC < thresholds.highOnC) {
            return FanState::LOW;
        }

        return FanState::HIGH;
    }

    if (prevState == FanState::LOW) {
        if (coolantTempC <= thresholds.offC) {
            return FanState::OFF;
        }

        if (coolantTempC < thresholds.highOnC) {
            return FanState::LOW;
        }

        return FanState::HIGH;
    }

    if (prevState == FanState::HIGH) {
        if (coolantTempC <= thresholds.offC) {
            return FanState::OFF;
        }

        if (coolantTempC <= thresholds.highOffC) {
            return FanState::LOW;
        }

        return FanState::HIGH;
    }

    return FanState::OFF;
}

std::string fanStateToString(FanState state)
{
    if (state == FanState::OFF) {
        return "OFF";
    }

    if (state == FanState::LOW) {
        return "LOW";
    }

    if (state == FanState::HIGH) {
        return "HIGH";
    }

    return "OFF";
}

FanState fanStateFromString(const std::string& value)
{
    const std::string normalized = normalizeStateName(value);

    if (normalized == "OFF") {
        return FanState::OFF;
    }

    if (normalized == "LOW") {
        return FanState::LOW;
    }

    if (normalized == "HIGH") {
        return FanState::HIGH;
    }

    throw std::invalid_argument(
        "Unsupported fan state: " + value
    );
}
