#include <gtest/gtest.h>

#include <stdexcept>
#include <vector>

#include "fan_control.hpp"

TEST(FanControlVersionTest, V1ThresholdsAreBaseline)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v1");

    EXPECT_EQ(thresholds.lowOnC, 95);
    EXPECT_EQ(thresholds.offC, 90);
    EXPECT_EQ(thresholds.highOnC, 105);
    EXPECT_EQ(thresholds.highOffC, 100);
}

TEST(FanControlVersionTest, V2ThresholdsAreCandidate)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    EXPECT_EQ(thresholds.lowOnC, 94);
    EXPECT_EQ(thresholds.offC, 89);
    EXPECT_EQ(thresholds.highOnC, 104);
    EXPECT_EQ(thresholds.highOffC, 99);
}

TEST(FanControlVersionTest, UnknownVersionIsRejected)
{
    EXPECT_THROW(
        thresholdsForVersion("fan_control_unknown"),
        std::invalid_argument
    );
}

TEST(FanControlTest, OffToOff)
{
    EXPECT_EQ(
        decideFanState(FanState::OFF, 94),
        FanState::OFF
    );
}

TEST(FanControlTest, OffToLow)
{
    EXPECT_EQ(
        decideFanState(FanState::OFF, 95),
        FanState::LOW
    );
}

TEST(FanControlTest, OffToHigh)
{
    EXPECT_EQ(
        decideFanState(FanState::OFF, 105),
        FanState::HIGH
    );
}

TEST(FanControlTest, LowToLow)
{
    EXPECT_EQ(
        decideFanState(FanState::LOW, 91),
        FanState::LOW
    );
}

TEST(FanControlTest, LowToOff)
{
    EXPECT_EQ(
        decideFanState(FanState::LOW, 90),
        FanState::OFF
    );
}

TEST(FanControlTest, LowToHigh)
{
    EXPECT_EQ(
        decideFanState(FanState::LOW, 105),
        FanState::HIGH
    );
}

TEST(FanControlTest, HighToHigh)
{
    EXPECT_EQ(
        decideFanState(FanState::HIGH, 101),
        FanState::HIGH
    );
}

TEST(FanControlTest, HighToLow)
{
    EXPECT_EQ(
        decideFanState(FanState::HIGH, 100),
        FanState::LOW
    );
}

TEST(FanControlTest, HighToOff)
{
    EXPECT_EQ(
        decideFanState(FanState::HIGH, 90),
        FanState::OFF
    );
}

TEST(FanControlTest, RapidHeatup)
{
    EXPECT_EQ(
        decideFanState(FanState::OFF, 120),
        FanState::HIGH
    );
}

TEST(FanControlV2Test, OffToOffBelowLowOn)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    EXPECT_EQ(
        decideFanState(FanState::OFF, 93, thresholds),
        FanState::OFF
    );
}

TEST(FanControlV2Test, OffToLowAtLowOn)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    EXPECT_EQ(
        decideFanState(FanState::OFF, 94, thresholds),
        FanState::LOW
    );
}

TEST(FanControlV2Test, OffToHighAtHighOn)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    EXPECT_EQ(
        decideFanState(FanState::OFF, 104, thresholds),
        FanState::HIGH
    );
}

TEST(FanControlV2Test, HighToLowAtHighOff)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    EXPECT_EQ(
        decideFanState(FanState::HIGH, 99, thresholds),
        FanState::LOW
    );
}

TEST(FanControlV2Test, LowToOffAtOff)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    EXPECT_EQ(
        decideFanState(FanState::LOW, 89, thresholds),
        FanState::OFF
    );
}

TEST(FanControlV2Test, ValidationSequenceMatchesSc05)
{
    const FanControlThresholds thresholds =
        thresholdsForVersion("fan_control_v2");

    const std::vector<int> temps = {
        93,
        94,
        104,
        99,
        89,
    };

    const std::vector<FanState> expected = {
        FanState::OFF,
        FanState::LOW,
        FanState::HIGH,
        FanState::LOW,
        FanState::OFF,
    };

    FanState state = FanState::OFF;

    for (std::size_t i = 0; i < temps.size(); ++i) {
        state = decideFanState(
            state,
            temps[i],
            thresholds
        );

        EXPECT_EQ(state, expected[i]);
    }
}
