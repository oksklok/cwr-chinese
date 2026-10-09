// Runtime language switching tests.
// Covers StringTable::SetLanguage, RelocalizeRegistered, callback registry.
#include <catch2/catch_test_macros.hpp>
#include <Poseidon/Core/ModSystem.hpp>
#include <Poseidon/Foundation/Framework/DebugLog.hpp>
#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>
#include <Poseidon/UI/Locale/LanguageRegistry.hpp>
#include <Poseidon/IO/ParamFile/ParamFile.hpp>
#include <Poseidon/IO/Streams/QBStream.hpp>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <chrono>
#include <sys/types.h>
#include <string>
#include <utility>
#include <Poseidon/Foundation/Strings/RString.hpp>
#ifdef _WIN32
#include <direct.h>
#include <Windows.h>
#else
#include <unistd.h>
#include <limits.h>
#if __APPLE__
#include <mach-o/dyld.h>
#endif

using Poseidon::LanguageChangedCallback;
using namespace Poseidon;

using Poseidon::GetLanguage;
using Poseidon::LocalizeString;
using Poseidon::RegisterLanguageChangedCallback;
using Poseidon::UnregisterLanguageChangedCallback;
#ifndef MAX_PATH
#define MAX_PATH PATH_MAX
#endif
#endif

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wexit-time-destructors"
static RString GetExeDir()
{
    static RString exeDir;
#pragma clang diagnostic pop

    if (exeDir.GetLength() == 0)
    {
        char p[MAX_PATH];
#ifdef _WIN32
        GetModuleFileNameA(nullptr, p, MAX_PATH);
        char* slash = strrchr(p, '\\');
#else
#if __APPLE__
        uint32_t n = sizeof(p) - 1;
        _NSGetExecutablePath(p, &n);
#else
        ssize_t n = readlink("/proc/self/exe", p, sizeof(p) - 1);
#endif
        if (n > 0)
            p[n] = '\0';
        else
            p[0] = '\0';
        char* slash = strrchr(p, '/');
#endif
        if (slash)
        {
            *slash = '\0';
        }
        exeDir = p;
    }
    return exeDir;
}

static std::string FixturePath(const char* name)
{
    std::string s = GetExeDir().Data();
#ifdef _WIN32
    s += "\\fixtures\\";
#else
    s += "/fixtures/";
#endif
    s += name;
    return s;
}

// RAII guard so a failed REQUIRE doesn't leave dangling stack-captured
// callbacks in the static registry (next test would SEGV when calling them).
struct LangCbGuard
{
    int token;
    explicit LangCbGuard(Poseidon::LanguageChangedCallback cb)
        : token(Poseidon::RegisterLanguageChangedCallback(std::move(cb)))
    {
    }
    ~LangCbGuard() { Poseidon::UnregisterLanguageChangedCallback(token); }
    LangCbGuard(const LangCbGuard&) = delete;
    LangCbGuard& operator=(const LangCbGuard&) = delete;
};

// Poseidon::SetLanguage — tables reload so by-name lookups follow the new column

TEST_CASE("Poseidon::SetLanguage switches by-name lookup to new column", "[stringtable][switch]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    REQUIRE(std::string(Poseidon::LocalizeString("STR_GREETING").Data()) == "Hello");

    REQUIRE(Poseidon::SetLanguage("French"));
    REQUIRE(std::string(Poseidon::LocalizeString("STR_GREETING").Data()) == "Bonjour");

    REQUIRE(Poseidon::SetLanguage("German"));
    // "Grüß Gott" — ü=C3 BC, ß=C3 9F after CP1252 transcode
    REQUIRE(std::string(Poseidon::LocalizeString("STR_GREETING").Data()) == "Gr\xC3\xBC\xC3\x9F Gott");

    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(std::string(Poseidon::LocalizeString("STR_GREETING").Data()) == "Hello");
}

TEST_CASE("Mission picker reads an unmounted bank's local UTF8 table", "[stringtable][cwrc-language]")
{
    const auto stem = std::filesystem::temp_directory_path() /
                      ("cwrc_picker_" + std::to_string(std::chrono::steady_clock::now().time_since_epoch().count()));
    const auto path = stem.string() + ".pbo";
    const std::string legacy = "LANGUAGE,English\nSTR_BANK_ONLY,Wrong legacy table\n";
    const std::string utf8 = "LANGUAGE,English,ChineseSimplified,ChineseTraditional\n"
                             "STR_BANK_ONLY,Hello,简体任务,繁體任務\n";
    {
        std::ofstream output(path, std::ios::binary);
        for (const auto& member : {std::make_pair("stringtable.csv", legacy),
                                   std::make_pair("stringtable.utf8.csv", utf8)})
        {
            output.write(member.first, std::strlen(member.first) + 1);
            const uint32_t fields[] = {0, 0, 0, 0, static_cast<uint32_t>(member.second.size())};
            output.write(reinterpret_cast<const char*>(fields), sizeof(fields));
        }
        const char end[21] = {};
        output.write(end, sizeof(end));
        output << legacy << utf8;
    }
    const RString savedLanguage = GLanguage;
    {
        Poseidon::QFBank bank;
        bank.open(stem.string().c_str());
        for (const auto& item : {std::make_pair("English", "Hello"),
                                std::make_pair("ChineseSimplified", "简体任务"),
                                std::make_pair("ChineseTraditional", "繁體任務"),
                                std::make_pair("French", "Hello")})
        {
            GLanguage = item.first;
            CHECK(Poseidon::LookupStringtableCsv("stringtable.csv", "STR_BANK_ONLY", &bank) == RString(item.second));
        }
        CHECK(Poseidon::LookupStringtableCsv("stringtable.csv", "STR_MISSING", &bank).GetLength() == 0);
        CHECK(Poseidon::LookupStringtableCsv("missing.csv", "STR_BANK_ONLY", &bank).GetLength() == 0);
        CHECK(std::string(Poseidon::LocalizeStringWithFallback("STR_BANK_ONLY", "Unchanged global")) == "Unchanged global");
    }
    GLanguage = savedLanguage;
    std::filesystem::remove(path);
}

TEST_CASE("Chinese column switches independently with stock English fallback", "[stringtable][switch][cwrc-language]")
{
    struct RegistryGuard { ~RegistryGuard() { CfgLib::LanguageRegistry::Instance().ResetToDefaults(); } } guard;
    const char* config = "class CfgLanguages { languages[]={\"English\",\"French\",\"ChineseSimplified\",\"ChineseTraditional\"}; "
                         "class ChineseSimplified { codepage=\"UTF8\"; voice=0; fallbackLanguage=\"English\"; }; "
                         "class ChineseTraditional { codepage=\"UTF8\"; voice=0; fallbackLanguage=\"English\"; }; };";
    ParamFile file;
    QIStream input(config, strlen(config));
    file.Parse(input);
    CfgLib::LanguageRegistry::Instance().LoadFromConfig(*file.FindEntry("CfgLanguages"));
    Poseidon::ClearStringtable();
    GLanguage = "English";
    const auto path = FixturePath("chinese_language.utf8.csv");
    Poseidon::LoadStringtable("global", path.c_str(), 0, true);
    int hello = Poseidon::RegisterString("STR_HELLO");
    REQUIRE(Poseidon::SetLanguage("ChineseSimplified"));
    CHECK(std::string(Poseidon::LocalizeString(hello).Data()) == "你好");
    CHECK(std::string(Poseidon::LocalizeString("STR_EMPTY").Data()) == "Fallback");
    CHECK(std::string(Poseidon::LookupStringtableCsv(path.c_str(), "STR_EMPTY").Data()) == "Fallback");
    REQUIRE(Poseidon::SetLanguage("ChineseTraditional"));
    CHECK(std::string(Poseidon::LocalizeString(hello).Data()) == "您好");
    CHECK(std::string(Poseidon::LookupStringtableCsv(path.c_str(), "STR_HELLO").Data()) == "您好");
    CHECK(std::string(Poseidon::LocalizeString("STR_EMPTY").Data()) == "Fallback");
    REQUIRE(Poseidon::SetLanguage("ChineseSimplified"));
    CHECK(std::string(Poseidon::LocalizeString(hello).Data()) == "你好");
    REQUIRE(Poseidon::SetLanguage("French"));
    CHECK(std::string(Poseidon::LocalizeString(hello).Data()) == "Bonjour");
    REQUIRE(Poseidon::SetLanguage("English"));
    CHECK(std::string(Poseidon::LocalizeString(hello).Data()) == "Hello");
    CHECK(Poseidon::LocalizeStringWithFallback("STR_MISSING", "Exact fallback") == std::string_view("Exact fallback"));
    Poseidon::ClearStringtable();
}

TEST_CASE("Missing language column uses configured fallback and its encoding",
          "[stringtable][switch][encoding][cwrc-language][missing-column]")
{
    namespace fs = std::filesystem;
    struct StateGuard
    {
        ~StateGuard()
        {
            Poseidon::ClearStringtable();
            GLanguage = "English";
            CfgLib::LanguageRegistry::Instance().ResetToDefaults();
        }
    } stateGuard;

    std::string fallback = "English";
    std::string fallbackColumn = "English";
    std::string value = "English \xA9";
    std::string expected = "English \xC2\xA9";
    const char* extension = ".csv";
    SECTION("French-first legacy addon falls back to English") {}
    SECTION("French-first UTF-8 addon falls back to English")
    {
        extension = ".utf8.csv";
        value = expected;
    }
    SECTION("Fallback column supplies its own legacy codepage")
    {
        fallback = fallbackColumn = "Czech";
        value = "\xE8"; // CP1250 č, not CP1252 è.
        expected = "\xC4\x8D";
    }
    SECTION("Absent configured fallback retains first-column behavior")
    {
        fallback = "German";
        expected = "Bonjour";
    }
    SECTION("Unconfigured fallback retains first-column behavior")
    {
        fallback.clear();
        expected = "Bonjour";
    }

    const std::string config = "class CfgLanguages { languages[]={\"English\",\"French\",\"Czech\",\"ChineseSimplified\"}; "
        "class ChineseSimplified { codepage=\"UTF8\"; voice=0; fallbackLanguage=\"" + fallback + "\"; }; };";
    ParamFile file;
    QIStream input(config.data(), config.size());
    file.Parse(input);
    CfgLib::LanguageRegistry::Instance().LoadFromConfig(*file.FindEntry("CfgLanguages"));

    const fs::path path = fs::temp_directory_path() / (std::string("cwrc_missing_language_column") + extension);
    struct FixtureGuard
    {
        fs::path path;
        ~FixtureGuard() { std::error_code error; fs::remove(path, error); }
    } fixtureGuard{path};
    {
        std::ofstream out(path, std::ios::binary);
        REQUIRE(out.is_open());
        out << "LANGUAGE,French," << fallbackColumn << "\nSTR_FALLBACK_PROBE,Bonjour," << value << "\n";
        out.close();
        REQUIRE(out.good());
    }

    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", path.string().c_str(), 0, true);
    REQUIRE(Poseidon::SetLanguage("ChineseSimplified"));
    CHECK(std::string(Poseidon::LocalizeString("STR_FALLBACK_PROBE").Data()) == expected);
    REQUIRE(Poseidon::SetLanguage("French"));
    CHECK(std::string(Poseidon::LocalizeString("STR_FALLBACK_PROBE").Data()) == "Bonjour");
    if (fallbackColumn == "English")
    {
        REQUIRE(Poseidon::SetLanguage("English"));
        CHECK(std::string(Poseidon::LocalizeString("STR_FALLBACK_PROBE").Data()) == "English \xC2\xA9");
    }
}

TEST_CASE("Poseidon::SetLanguage to same language is a no-op but returns true", "[stringtable][switch]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(std::string(Poseidon::LocalizeString("STR_GREETING").Data()) == "Hello");
}

TEST_CASE("Poseidon::SetLanguage empty string fails and keeps current language", "[stringtable][switch]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    REQUIRE_FALSE(Poseidon::SetLanguage(""));
    REQUIRE(std::string(Poseidon::LocalizeString("STR_GREETING").Data()) == "Hello");
}

// Poseidon::SetLanguage — registered ID snapshots refresh via RelocalizeRegistered

TEST_CASE("Registered string id reflects new language after Poseidon::SetLanguage", "[stringtable][switch][register]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    int id = Poseidon::RegisterString("STR_GREETING");
    REQUIRE(id >= 0);
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "Hello");

    REQUIRE(Poseidon::SetLanguage("French"));
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "Bonjour");

    REQUIRE(Poseidon::SetLanguage("Spanish"));
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "Hola");
}

TEST_CASE("Multiple registered ids refresh independently", "[stringtable][switch][register]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    int greet = Poseidon::RegisterString("STR_GREETING");
    int ascii = Poseidon::RegisterString("STR_ASCII");
    REQUIRE(std::string(Poseidon::LocalizeString(greet).Data()) == "Hello");
    REQUIRE(std::string(Poseidon::LocalizeString(ascii).Data()) == "plain");

    REQUIRE(Poseidon::SetLanguage("French"));
    REQUIRE(std::string(Poseidon::LocalizeString(greet).Data()) == "Bonjour");
    REQUIRE(std::string(Poseidon::LocalizeString(ascii).Data()) == "plain"); // ASCII is same in all columns
}

// Callback registry

TEST_CASE("Language-changed callback fires on Poseidon::SetLanguage", "[stringtable][switch][callback]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    int fired = 0;
    {
        LangCbGuard g([&fired]() { fired++; });

        REQUIRE(Poseidon::SetLanguage("French"));
        REQUIRE(fired == 1);

        REQUIRE(Poseidon::SetLanguage("German"));
        REQUIRE(fired == 2);
    } // guard unregisters here

    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(fired == 2); // unregistered — no further fires
}

TEST_CASE("Same-language Poseidon::SetLanguage does not fire callbacks", "[stringtable][switch][callback]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    int fired = 0;
    LangCbGuard g([&fired]() { fired++; });

    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(fired == 0);
}

TEST_CASE("Multiple callbacks fire in registration order", "[stringtable][switch][callback]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    std::string order;
    LangCbGuard g1([&order]() { order += "A"; });
    {
        LangCbGuard g2([&order]() { order += "B"; });
        LangCbGuard g3([&order]() { order += "C"; });

        REQUIRE(Poseidon::SetLanguage("French"));
        REQUIRE(order == "ABC");
    } // g2, g3 unregister here; g1 remains

    order.clear();
    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(order == "A");
}

TEST_CASE("Callback observes refreshed values via Poseidon::LocalizeString", "[stringtable][switch][callback]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);

    int id = Poseidon::RegisterString("STR_GREETING");
    std::string observed;
    LangCbGuard g([&observed, id]() { observed = std::string(Poseidon::LocalizeString(id).Data()); });

    REQUIRE(Poseidon::SetLanguage("French"));
    REQUIRE(observed == "Bonjour");

    REQUIRE(Poseidon::SetLanguage("Spanish"));
    REQUIRE(observed == "Hola");
}

// Tracked-files list is deduped across repeated loads

TEST_CASE("Repeated Poseidon::LoadStringtable on same file does not duplicate replays", "[stringtable][switch][loaded]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    // Load same file twice — should not result in duplicate work on Poseidon::SetLanguage.
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, true);
    Poseidon::LoadStringtable("global", FixturePath("stringtable_cp1252.csv").c_str(), 0, false);

    int id = Poseidon::RegisterString("STR_GREETING");
    REQUIRE(Poseidon::SetLanguage("French"));
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "Bonjour");
    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "Hello");
}

TEST_CASE("Poseidon::SetLanguage reloads mixed legacy and UTF-8 shards", "[stringtable][switch][loaded][shards]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", FixturePath("stringtable_shards.csv").c_str(), 0, true);

    int id = Poseidon::RegisterString("STR_OVERRIDE_CHAIN");
    REQUIRE(id >= 0);
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "final-thirty");

    REQUIRE(Poseidon::SetLanguage("Czech"));
    REQUIRE(std::string(Poseidon::LocalizeString("STR_BASE_ONLY").Data()) == "Základ");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_LEGACY_ONLY").Data()) == "Žába");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_PAIR_SOURCE").Data()) == "utf8 pár");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_UTF8_ONLY").Data()) == "Příliš");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_FINAL_ONLY").Data()) == "Třicet");
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "třicet");

    REQUIRE(Poseidon::SetLanguage("Russian"));
    REQUIRE(std::string(Poseidon::LocalizeString("STR_BASE_ONLY").Data()) == "База");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_LEGACY_ONLY").Data()) == "Щит");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_PAIR_SOURCE").Data()) == "utf8 пара");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_UTF8_ONLY").Data()) == "современный");
    REQUIRE(std::string(Poseidon::LocalizeString("STR_FINAL_ONLY").Data()) == "Финал");
    REQUIRE(std::string(Poseidon::LocalizeString(id).Data()) == "тридцать");
}

TEST_CASE("Campaign text resolves enabled mod overrides without redirecting assets", "[stringtable][campaign][mods]")
{
    namespace fs = std::filesystem;
    const auto previousMods = Poseidon::ModSystem::GetModList();
    const auto previousLanguage = GLanguage;
    const auto root = fs::temp_directory_path() /
        ("cwrc-campaign-" + std::to_string(std::chrono::steady_clock::now().time_since_epoch().count()));
    struct Cleanup {
        fs::path root;
        RString mods, language;
        ~Cleanup() { Poseidon::ClearStringtable(); Poseidon::ModSystem::SetModPath(mods); GLanguage = language; fs::remove_all(root); }
    } cleanup{root, previousMods, previousLanguage};
    const auto folder = root / "localization/Campaigns/1985/missions/demo.eden";
    fs::create_directories(folder);
    std::ofstream(folder / "stringtable.utf8.csv") <<
        "LANGUAGE,English,French,ChineseSimplified,ChineseTraditional\n"
        "STR_CAMPAIGN_TEST,Hello,Bonjour,SC,TC\n";
    std::ofstream(root / "localization/Campaigns/1985/description.ext") << "class Campaign {};";
    std::ofstream(folder / "mission.sqm") << "class Mission {};";
    std::ofstream(folder / "init.sqs") << "must not override";
    std::ofstream(folder / "briefing.ChineseSimplified.utf8.html") << "SC briefing";
    std::ofstream(folder / "briefing.ChineseTraditional.utf8.html") << "TC briefing";
    std::ofstream(folder / "briefing.utf8.html") << "must not override stock languages";
    Poseidon::ModSystem::SetModPath(root.string().c_str());
    const char* path = "Campaigns/1985/missions/demo.eden/stringtable.csv";
    for (const auto* language : {"ChineseSimplified", "ChineseTraditional"})
    {
        const auto name = std::string("briefing.") + language + ".utf8.html";
        REQUIRE(fs::equivalent(Poseidon::ResolveCampaignTextFile(
            (std::string("Campaigns/1985/missions/demo.eden/") + name).c_str()).Data(), folder / name));
    }
    REQUIRE(std::string(Poseidon::ResolveCampaignTextFile("Campaigns/1985/missions/demo.eden/briefing.utf8.html").Data()) ==
            "Campaigns/1985/missions/demo.eden/briefing.utf8.html");
    REQUIRE(fs::equivalent(Poseidon::ResolveCampaignTextFile(path).Data(), folder / "stringtable.utf8.csv"));
    REQUIRE(fs::equivalent(Poseidon::ResolveCampaignTextFile("Campaigns/1985/description.ext").Data(),
                          root / "localization/Campaigns/1985/description.ext"));
    REQUIRE(fs::equivalent(Poseidon::ResolveCampaignTextFile("Campaigns/1985/missions/demo.eden/mission.sqm").Data(),
                          folder / "mission.sqm"));
    REQUIRE(std::string(Poseidon::ResolveCampaignTextFile("Campaigns/1985/missions/demo.eden/init.sqs").Data()) ==
            "Campaigns/1985/missions/demo.eden/init.sqs");
    REQUIRE(std::string(Poseidon::ResolveCampaignTextFile("Campaigns/1985/missions/missing.eden/mission.sqm").Data()) ==
            "Campaigns/1985/missions/missing.eden/mission.sqm");
    REQUIRE(std::string(Poseidon::ResolveCampaignTextFile("Campaigns/resistance/stringtable.csv").Data()) ==
            "Campaigns/resistance/stringtable.csv");
    Poseidon::ClearStringtable();
    GLanguage = "ChineseSimplified";
    Poseidon::LoadStringtable("mission", path);
    REQUIRE(std::string(Poseidon::LocalizeString("STR_CAMPAIGN_TEST").Data()) == "SC");
    for (const auto& pair : {std::pair{"ChineseTraditional", "TC"}, {"English", "Hello"}, {"French", "Bonjour"}})
    {
        REQUIRE(Poseidon::SetLanguage(pair.first));
        REQUIRE(std::string(Poseidon::LocalizeString("STR_CAMPAIGN_TEST").Data()) == pair.second);
        REQUIRE(std::string(Poseidon::LookupStringtableCsv(path, "STR_CAMPAIGN_TEST").Data()) == pair.second);
    }
    Poseidon::ModSystem::SetModPath("");
    REQUIRE(std::string(Poseidon::ResolveCampaignTextFile(path).Data()) == path);
}
