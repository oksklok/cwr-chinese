#include <catch2/catch_test_macros.hpp>
#include <Poseidon/UI/Controls/HtmlTextWrap.hpp>
#include <vector>
#include <Poseidon/Foundation/Strings/RString.hpp>

using namespace Poseidon;

TEST_CASE("HtmlTextWrap: UTF-8 breakpoints stay on whole Cyrillic characters", "[ui][html][wrap]")
{
    const RString text = "яяя яяя";
    const auto breaks = HtmlTextWrap::ComputeWrapBreaks(
        text, 3.5f, [](RString ch) { return HtmlTextWrap::IsWrapWhitespace(ch, ch.GetLength()) ? 0.5f : 1.0f; });

    REQUIRE(breaks.size() == 1);
    CHECK(breaks[0] == 7);
    CHECK(text.Substring(0, breaks[0]) == RString("яяя "));
    CHECK(text.Substring(breaks[0], text.GetLength()) == RString("яяя"));
}

TEST_CASE("HtmlTextWrap: UTF-8 helper reports Russian letters as two-byte spans", "[ui][html][wrap]")
{
    const char* text = "я";
    REQUIRE(HtmlTextWrap::Utf8CharBytes(text, 2) == 2);
    REQUIRE(HtmlTextWrap::Utf8CharBytes(text, 1) == 1);
}

TEST_CASE("HtmlTextWrap: Chinese punctuation and Latin tokens stay together", "[ui][html][wrap][zhcn]")
{
    auto measure = [](RString) { return 1.0f; };
    SECTION("A comma moves with the preceding character")
    {
        const RString text = "子弹贴着脑袋飞过，我发誓";
        const auto breaks = HtmlTextWrap::ComputeWrapBreaks(text, 8.0f, measure, true);
        REQUIRE(!breaks.empty());
        CHECK(text.Substring(0, breaks[0]) == RString("子弹贴着脑袋飞"));
        CHECK(text.Substring(breaks[0], text.GetLength()) == RString("过，我发誓"));
    }
    SECTION("An island name and its parentheses are not split")
    {
        const RString text = "解放艾弗隆（Everon）的第一步";
        const auto breaks = HtmlTextWrap::ComputeWrapBreaks(text, 11.0f, measure, true);
        REQUIRE(!breaks.empty());
        CHECK(text.Substring(breaks[0], breaks[0] + 12) == RString("（Everon）"));
    }
    SECTION("A comma in the next HTML field reserves room beside its link")
    {
        const RString text = "我记了些笔记";
        const auto breaks = HtmlTextWrap::ComputeWrapBreaks(text, 6.0f, measure, true, 1.0f);
        REQUIRE(breaks.size() == 1);
        CHECK(text.Substring(breaks[0], text.GetLength()) == RString("记"));
    }
    SECTION("Stock wrapping remains unchanged when Chinese rules are disabled")
    {
        const RString text = "子弹贴着脑袋飞过，我发誓";
        const auto breaks = HtmlTextWrap::ComputeWrapBreaks(text, 8.0f, measure);
        REQUIRE(!breaks.empty());
        CHECK(text.Substring(breaks[0], breaks[0] + 3) == RString("，"));
    }
}
