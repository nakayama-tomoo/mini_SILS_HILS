#include "fan_control.hpp"

#include <cctype>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

namespace {

struct Args {
    fs::path scenarioPath;
    std::string versionId = "fan_control_v1";
};

void printUsage()
{
    std::cout
        << "Usage: run_scenario --scenario <csv_path> "
        << "[--version-id fan_control_v1|fan_control_v2]\n";
}

Args parseArgs(int argc, char** argv)
{
    Args args;

    for (int i = 1; i < argc; ++i) {
        const std::string key = argv[i];

        if (key == "--help" || key == "-h") {
            printUsage();
            std::exit(0);
        }

        if (key == "--scenario") {
            if (i + 1 >= argc) {
                throw std::invalid_argument(
                    "--scenario requires a value"
                );
            }

            args.scenarioPath = argv[++i];
            continue;
        }

        if (key == "--version-id") {
            if (i + 1 >= argc) {
                throw std::invalid_argument(
                    "--version-id requires a value"
                );
            }

            args.versionId = argv[++i];
            continue;
        }

        throw std::invalid_argument(
            "Unknown argument: " + key
        );
    }

    if (args.scenarioPath.empty()) {
        throw std::invalid_argument(
            "--scenario is required"
        );
    }

    return args;
}

std::string trim(const std::string& value)
{
    std::size_t first = 0;

    while (
        first < value.size()
        && std::isspace(static_cast<unsigned char>(value[first]))
    ) {
        ++first;
    }

    std::size_t last = value.size();

    while (
        last > first
        && std::isspace(static_cast<unsigned char>(value[last - 1]))
    ) {
        --last;
    }

    return value.substr(first, last - first);
}

std::string normalizeKey(const std::string& value)
{
    std::string normalized;

    for (unsigned char c : value) {
        if (std::isalnum(c)) {
            normalized.push_back(
                static_cast<char>(std::tolower(c))
            );
        }
    }

    return normalized;
}

std::string upper(const std::string& value)
{
    std::string result;
    result.reserve(value.size());

    for (unsigned char c : value) {
        result.push_back(
            static_cast<char>(std::toupper(c))
        );
    }

    return result;
}

std::vector<std::string> splitCsvLine(const std::string& line)
{
    std::vector<std::string> cells;
    std::string cell;
    bool inQuotes = false;

    for (char c : line) {
        if (c == '"') {
            inQuotes = !inQuotes;
            continue;
        }

        if (c == ',' && !inQuotes) {
            cells.push_back(trim(cell));
            cell.clear();
            continue;
        }

        cell.push_back(c);
    }

    cells.push_back(trim(cell));

    return cells;
}

std::size_t findColumn(
    const std::vector<std::string>& header,
    const std::vector<std::string>& candidates
)
{
    for (std::size_t i = 0; i < header.size(); ++i) {
        const std::string normalizedHeader =
            normalizeKey(header[i]);

        for (const std::string& candidate : candidates) {
            if (normalizedHeader == normalizeKey(candidate)) {
                return i;
            }
        }
    }

    return static_cast<std::size_t>(-1);
}

std::string cellAt(
    const std::vector<std::string>& row,
    std::size_t index
)
{
    if (index >= row.size()) {
        return "";
    }

    return trim(row[index]);
}

std::string csvEscape(const std::string& value)
{
    const bool needsQuote =
        value.find(',') != std::string::npos
        || value.find('"') != std::string::npos
        || value.find('\n') != std::string::npos
        || value.find('\r') != std::string::npos;

    if (!needsQuote) {
        return value;
    }

    std::string escaped = "\"";

    for (char c : value) {
        if (c == '"') {
            escaped += "\"\"";
        } else {
            escaped += c;
        }
    }

    escaped += "\"";
    return escaped;
}

fs::path findRepoRoot(const fs::path& scenarioPath)
{
    fs::path current = fs::absolute(scenarioPath);

    if (fs::is_regular_file(current)) {
        current = current.parent_path();
    }

    while (!current.empty()) {
        if (
            fs::exists(
                current
                / "common"
                / "scenario"
                / "scenario_suite.yaml"
            )
            && fs::exists(
                current
                / "implementations"
                / "cpp_sils"
                / "CMakeLists.txt"
            )
        ) {
            return current;
        }

        const fs::path parent = current.parent_path();

        if (parent == current) {
            break;
        }

        current = parent;
    }

    current = fs::current_path();

    while (!current.empty()) {
        if (
            fs::exists(
                current
                / "common"
                / "scenario"
                / "scenario_suite.yaml"
            )
            && fs::exists(
                current
                / "implementations"
                / "cpp_sils"
                / "CMakeLists.txt"
            )
        ) {
            return current;
        }

        const fs::path parent = current.parent_path();

        if (parent == current) {
            break;
        }

        current = parent;
    }

    throw std::runtime_error(
        "Repository root was not found"
    );
}

}  // namespace

int main(int argc, char** argv)
{
    try {
        const Args args = parseArgs(argc, argv);
        const fs::path scenarioPath =
            fs::absolute(args.scenarioPath);

        if (!fs::exists(scenarioPath)) {
            throw std::runtime_error(
                "Scenario file was not found: "
                + scenarioPath.string()
            );
        }

        const FanControlThresholds thresholds =
            thresholdsForVersion(args.versionId);

        std::ifstream input(scenarioPath);

        if (!input) {
            throw std::runtime_error(
                "Failed to open scenario file: "
                + scenarioPath.string()
            );
        }

        std::string line;

        if (!std::getline(input, line)) {
            throw std::runtime_error(
                "Scenario file is empty: "
                + scenarioPath.string()
            );
        }

        const std::vector<std::string> header =
            splitCsvLine(line);

        const std::size_t timeColumn = findColumn(
            header,
            {
                "time_s",
                "time_sec",
                "time",
                "timestamp_s",
            }
        );

        const std::size_t tempColumn = findColumn(
            header,
            {
                "coolant_temp_c",
                "coolant_temperature_c",
                "temperature_c",
                "temp_c",
            }
        );

        const std::size_t expectedColumn = findColumn(
            header,
            {
                "expected_fan_state",
                "expected_state",
                "expected_fan_command",
                "expected_command",
                "expected",
            }
        );

        const std::size_t notFound =
            static_cast<std::size_t>(-1);

        if (tempColumn == notFound) {
            throw std::runtime_error(
                "Temperature column was not found"
            );
        }

        if (expectedColumn == notFound) {
            throw std::runtime_error(
                "Expected fan state column was not found"
            );
        }

        const fs::path repoRoot = findRepoRoot(scenarioPath);
        const fs::path outputDir =
            repoRoot
            / "implementations"
            / "python_sils"
            / "cpp"
            / "results";

        fs::create_directories(outputDir);

        const std::string scenarioName =
            scenarioPath.stem().string();

        const fs::path outputPath =
            outputDir
            / (scenarioName + "_cpp_results.csv");

        std::ofstream output(outputPath);

        if (!output) {
            throw std::runtime_error(
                "Failed to open output file: "
                + outputPath.string()
            );
        }

        output
            << "time_s,"
            << "coolant_temp_c,"
            << "expected_fan_state,"
            << "actual_fan_state,"
            << "match,"
            << "version_id\n";

        FanState state = FanState::OFF;
        int totalRows = 0;
        int passedRows = 0;

        while (std::getline(input, line)) {
            if (trim(line).empty()) {
                continue;
            }

            const std::vector<std::string> row =
                splitCsvLine(line);

            const std::string timeValue =
                timeColumn == notFound
                    ? std::to_string(totalRows)
                    : cellAt(row, timeColumn);

            const std::string tempValue =
                cellAt(row, tempColumn);

            const std::string expectedValue =
                cellAt(row, expectedColumn);

            if (tempValue.empty()) {
                throw std::runtime_error(
                    "Temperature value is empty"
                );
            }

            if (expectedValue.empty()) {
                throw std::runtime_error(
                    "Expected fan state value is empty"
                );
            }

            const int coolantTempC = std::stoi(tempValue);

            state = decideFanState(
                state,
                coolantTempC,
                thresholds
            );

            const FanState expectedState =
                fanStateFromString(expectedValue);

            const bool match =
                state == expectedState;

            if (match) {
                ++passedRows;
            }

            ++totalRows;

            output
                << csvEscape(timeValue) << ","
                << coolantTempC << ","
                << fanStateToString(expectedState) << ","
                << fanStateToString(state) << ","
                << (match ? "PASS" : "FAIL") << ","
                << csvEscape(args.versionId) << "\n";
        }

        std::cout << "C++ SILS scenario result\n";
        std::cout << " scenario   : " << scenarioPath << "\n";
        std::cout << " version_id : " << args.versionId << "\n";
        std::cout << " output     : " << outputPath << "\n";
        std::cout << " rows       : " << totalRows << "\n";
        std::cout << " passed     : " << passedRows << "\n";
        std::cout << " result     : "
                  << (totalRows == passedRows ? "PASS" : "FAIL")
                  << "\n";

        return totalRows == passedRows ? 0 : 1;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << "\n";
        return 1;
    }
}
