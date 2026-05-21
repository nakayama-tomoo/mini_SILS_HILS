#include <gtest/gtest.h>

#include "fan_control.hpp"

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
