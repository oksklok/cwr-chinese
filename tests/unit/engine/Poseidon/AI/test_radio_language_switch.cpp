#include <Poseidon/Foundation/PoseidonPCH.hpp>
#include <catch2/catch_test_macros.hpp>

#include <Poseidon/UI/Locale/Sentences.hpp>
#include <Poseidon/UI/Locale/StringtableExt.hpp>

#include <cmath>
#include <filesystem>
#include <string>
#include <utility>
#include <vector>

using namespace Poseidon;

TEST_CASE("Generated radio words follow live language changes without changing speech tokens",
          "[ai][radio][localization][switch]")
{
    struct Word
    {
        int* id;
        const char* key;
        const char* speech;
    };
    const Word clocks[] = {
        {&IDS_WORD_AT12, "STR_WORD_AT12", "at12"},
        {&IDS_WORD_AT1, "STR_WORD_AT1", "at1"},
        {&IDS_WORD_AT2, "STR_WORD_AT2", "at2"},
        {&IDS_WORD_AT3, "STR_WORD_AT3", "at3"},
        {&IDS_WORD_AT4, "STR_WORD_AT4", "at4"},
        {&IDS_WORD_AT5, "STR_WORD_AT5", "at5"},
        {&IDS_WORD_AT6, "STR_WORD_AT6", "at6"},
        {&IDS_WORD_AT7, "STR_WORD_AT7", "at7"},
        {&IDS_WORD_AT8, "STR_WORD_AT8", "at8"},
        {&IDS_WORD_AT9, "STR_WORD_AT9", "at9"},
        {&IDS_WORD_AT10, "STR_WORD_AT10", "at10"},
        {&IDS_WORD_AT11, "STR_WORD_AT11", "at11"},
    };
    const Word distances[] = {
        {&IDS_WORD_DIST50, "STR_WORD_DIST50", "dist50"},
        {&IDS_WORD_DIST100, "STR_WORD_DIST100", "dist100"},
        {&IDS_WORD_DIST200, "STR_WORD_DIST200", "dist200"},
        {&IDS_WORD_DIST500, "STR_WORD_DIST500", "dist500"},
        {&IDS_WORD_DIST1000, "STR_WORD_DIST1000", "dist1000"},
        {&IDS_WORD_DIST2000, "STR_WORD_DIST2000", "dist2000"},
        {&IDS_WORD_DISTFAR, "STR_WORD_DISTFAR", "far"},
    };
    struct RestoreIds
    {
        RString language = GLanguage;
        std::vector<std::pair<int*, int>> ids;
        ~RestoreIds()
        {
            ClearStringtable();
            GLanguage = language;
            for (const auto& [id, original] : ids)
                *id = original;
        }
    } restore;
    for (const auto& word : clocks)
        restore.ids.emplace_back(word.id, *word.id);
    for (const auto& word : distances)
        restore.ids.emplace_back(word.id, *word.id);

    ClearStringtable();
    GLanguage = "ChineseTraditional";
    const auto fixture = (std::filesystem::path(TESTS_ROOT_DIR) / "fixtures" / "stringtable" /
                          "radio_words.utf8.csv").string();
    LoadStringtable("global", fixture.c_str(), 0, true);
    for (const auto& word : clocks)
    {
        *word.id = RegisterString(word.key);
        REQUIRE(*word.id >= 0);
    }
    for (const auto& word : distances)
    {
        *word.id = RegisterString(word.key);
        REQUIRE(*word.id >= 0);
    }

    const int distanceBins[] = {0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                               5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6};
    struct Language
    {
        const char* name;
        const char* noon;
    };
    const Language languages[] = {
        {"ChineseTraditional", "12點鐘方向"},
        {"ChineseSimplified", "12点钟方向"},
        {"English", "12 o'clock"},
        {"French", "a midi"},
        {"ChineseTraditional", "12點鐘方向"},
        {"ChineseSimplified", "12点钟方向"},
    };
    for (const auto& language : languages)
    {
        CAPTURE(language.name);
        REQUIRE(SetLanguage(language.name));
        REQUIRE(std::string(LocalizeString(IDS_WORD_AT12).Data()) == language.noon);
        for (int clock = 0; clock <= 12; ++clock)
        {
            CAPTURE(clock);
            const float angle = clock * (H_PI / 6);
            SentenceParams params;
            params.AddAzimutRelDir(Vector3(std::sin(angle), 0, std::cos(angle)));
            const auto& word = clocks[clock % 12];
            REQUIRE(params.Size() == 1);
            CHECK(params[0].type == SPTWordText);
            CHECK(std::string(params[0].text.Data()) == word.speech);
            CHECK(std::string(params[0].text2.Data()) == LocalizeString(*word.id).Data());
        }
        for (int bin = -1; bin <= 27; ++bin)
        {
            CAPTURE(bin);
            SentenceParams params;
            params.AddDistance(bin * 100.0f);
            const auto& word = distances[distanceBins[bin < 0 ? 0 : bin > 26 ? 26 : bin]];
            REQUIRE(params.Size() == 1);
            CHECK(params[0].type == SPTWordText);
            CHECK(std::string(params[0].text.Data()) == word.speech);
            CHECK(std::string(params[0].text2.Data()) == LocalizeString(*word.id).Data());
        }
    }
}
