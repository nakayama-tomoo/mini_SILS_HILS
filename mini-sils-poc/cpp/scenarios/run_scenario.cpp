#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

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

int runScenario(const std::string& scenarioName)
{
    std::string inputPath =
        "scenarios/fan_control/" + scenarioName + ".csv";

    std::ifstream input(inputPath);

    if (!input.is_open()) {
        std::cerr << "Failed to open: " << inputPath << std::endl;
        return 1;
    }

    std::string outputPath =
        "cpp/results/" + scenarioName + "_cpp_results.csv";

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

    return 0;
}

int main()
{
    fs::path scenarioDir = "scenarios/fan_control";

    std::vector<std::string> scenarioNames;

    for (const auto& entry : fs::directory_iterator(scenarioDir)) {
        if (!entry.is_regular_file()) {
            continue;
        }

        if (entry.path().extension() != ".csv") {
            continue;
        }

        scenarioNames.push_back(
            entry.path().stem().string()
        );
    }

    std::sort(
        scenarioNames.begin(),
        scenarioNames.end()
    );

    int overallResult = 0;

    for (const auto& scenarioName : scenarioNames) {
        overallResult |= runScenario(scenarioName);
    }

    return overallResult;
}
