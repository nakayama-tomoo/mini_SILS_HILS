#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cstring>

#include "fan_control.hpp"

namespace fs = std::filesystem;

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

FanState fromString(const std::string& value)
{
    if (value == "OFF") {
        return FanState::OFF;
    }

    if (value == "LOW") {
        return FanState::LOW;
    }

    if (value == "HIGH") {
        return FanState::HIGH;
    }

    return FanState::OFF;
}

int runScenario(const fs::path& scenarioPath)
{
    std::ifstream input(scenarioPath);

    if (!input.is_open()) {
        std::cerr << "Failed to open: " << scenarioPath << std::endl;
        return 1;
    }


    std::string scenarioName =
        scenarioPath.stem().string();

    fs::path outputPath =
        fs::path("results") / (scenarioName + "_cpp_results.csv");

    std::ofstream output(outputPath);

    output << "time_s,coolant_temp_c,expected_fan_state,actual_fan_state,match\n";

    std::string line;

    std::getline(input, line);

    FanState prevState = FanState::OFF;

    while (std::getline(input, line)) {
        std::stringstream ss(line);

        std::string timeStr;
        std::string tempStr;
        std::string expectedStr;

        std::getline(ss, timeStr, ',');
        std::getline(ss, tempStr, ',');
        std::getline(ss, expectedStr, ',');

        int coolantTemp = std::stoi(tempStr);

        FanState expected = fromString(expectedStr);

        FanState actual = decideFanState(prevState, coolantTemp);

        bool match = (expected == actual);

        output
            << timeStr << ","
            << coolantTemp << ","
            << expectedStr << ","
            << toString(actual) << ","
            << (match ? "PASS" : "FAIL")
            << "\n";

        prevState = actual;
    }

    std::cout << "Completed: " << scenarioName << std::endl;
    std::cout << "Output   : " << outputPath << std::endl;

    return 0;
}

int main(int argc, char* argv[])
{
    if (argc < 3) {
        std::cerr
            << "Usage: "
            << argv[0]
            << " --scenario <scenario.csv>"
            << std::endl;

        return 1;
    }

    std::string option = argv[1];

    if (option != "--scenario") {
        std::cerr
            << "Unknown option: "
            << option
            << std::endl;

        return 1;
    }

    fs::path scenarioPath = argv[2];

    return runScenario(scenarioPath);
}

