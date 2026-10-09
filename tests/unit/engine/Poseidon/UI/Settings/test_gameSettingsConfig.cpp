#include <catch2/catch_test_macros.hpp>

#include <Poseidon/Foundation/Common/GamePaths.hpp>
#include <Poseidon/UI/Settings/GameSettingsConfig.hpp>
#include <Poseidon/IO/Filesystem/Utf8Paths.hpp>
#include <Poseidon/UI/Locale/LanguageRegistry.hpp>
#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>
#include <Poseidon/IO/ParamFile/ParamFile.hpp>
#include <Poseidon/IO/Streams/QBStream.hpp>

#include <filesystem>
#include <fstream>
#include <random>
#include <string>
#include <optional>
#include <cstring>

using Poseidon::ResolveEffectiveViewDistance;

using Poseidon::GameSettingsConfig;

namespace
{
std::string TmpPath(const char* leaf)
{
    static std::random_device rd;
    static std::mt19937 rng(rd());
    std::uniform_int_distribution<unsigned> dist;
    auto root = std::filesystem::temp_directory_path() / ("gamesettings_test_" + std::to_string(dist(rng)));
    std::filesystem::create_directories(root);
    return (root / leaf).string();
}

struct FakeEnvironment : GameSettingsConfig::Environment
{
    std::string language;
    std::string DetectSystemLanguage() const override { return language; }
};
} // namespace

TEST_CASE("GameSettingsConfig: defaults follow detected language", "[Settings][GameSettings]")
{
    FakeEnvironment env;
    env.language = "Czech";
    GameSettingsConfig cfg;
    cfg.LoadDefaults(env);

    CHECK(cfg.textLanguage == "Czech");
    CHECK(cfg.voiceLanguage == "Czech");
    CHECK(cfg.activeProfile.empty());
    CHECK(cfg.blood == true);
    CHECK(cfg.preferredViewDistance == 900.0f);
    CHECK(cfg.respectMissionViewDistance == true);
}

TEST_CASE("GameSettingsConfig: configured Chinese text persists independently of English voices", "[Settings][GameSettings][cwrc-language]")
{
    const char* config = "class CfgLanguages { languages[]={\"English\",\"ChineseSimplified\",\"ChineseTraditional\"}; "
                         "class ChineseSimplified { code=\"ZH-CN\"; autonym=\"简体中文\"; codepage=\"UTF8\"; voice=0; }; "
                         "class ChineseTraditional { code=\"zh-TW\"; autonym=\"繁體中文\"; codepage=\"UTF8\"; voice=0; }; };";
    ParamFile file;
    QIStream input(config, strlen(config));
    file.Parse(input);
    struct Guard { ~Guard() { CfgLib::LanguageRegistry::Instance().ResetToDefaults(); } } guard;
    CfgLib::LanguageRegistry::Instance().LoadFromConfig(*file.FindEntry("CfgLanguages"));
    for (const char* language : {"ChineseSimplified", "ChineseTraditional"})
    {
        GameSettingsConfig source;
        source.textLanguage = language;
        source.voiceLanguage = "English";
        const auto path = TmpPath("chinese.cfg");
        REQUIRE(source.Save(path));
        GameSettingsConfig restored;
        REQUIRE(restored.Load(path));
        FakeEnvironment environment;
        environment.language = "English";
        CHECK_FALSE(restored.Normalize(environment));
        CHECK(restored.textLanguage == language);
        CHECK(restored.voiceLanguage == "English");
        std::filesystem::remove_all(std::filesystem::path(path).parent_path());
    }
}

TEST_CASE("Chinese mod language is independent of stock settings and remembers stock-language choices",
          "[Settings][GameSettings][cwrc-language]")
{
    const auto dir = Poseidon::Foundation::GamePaths::Instance().UserDir();
    const auto stockPath = dir + "game.cfg";
    const auto modPath = dir + "cwr-chinese-language.cfg";
    struct Guard
    {
        std::string stock, mod;
        ~Guard()
        {
            CfgLib::LanguageRegistry::Instance().ResetToDefaults();
            Poseidon::SetLanguage("English");
            std::filesystem::remove(stock);
            std::filesystem::remove(mod);
        }
    } guard{stockPath, modPath};
    const char* config = "class CfgLanguages { languages[]={\"English\",\"French\","
                         "\"ChineseSimplified\",\"ChineseTraditional\"}; };";
    ParamFile file;
    QIStream input(config, strlen(config));
    file.Parse(input);
    REQUIRE(file.FindEntry("CfgLanguages"));

    for (const char* previous : {"English", "French", "ChineseSimplified", "ChineseTraditional"})
    {
        INFO("Previous shared preference: " << previous);
        CfgLib::LanguageRegistry::Instance().LoadFromConfig(*file.FindEntry("CfgLanguages"));
        std::filesystem::remove(modPath);
        GameSettingsConfig stock;
        stock.textLanguage = previous;
        stock.voiceLanguage = "French";
        stock.activeProfile = "ExistingPlayer";
        REQUIRE(stock.Save(stockPath));

        Poseidon::LoadGameSettings();
        const std::string expected = std::string(previous) == "ChineseTraditional"
                                       ? "ChineseTraditional" : "ChineseSimplified";
        CHECK(std::string((const char*)GLanguage) == expected);
        GameSettingsConfig savedMod;
        REQUIRE(savedMod.Load(modPath));
        CHECK(savedMod.textLanguage == expected);

        for (const char* chosen : {"ChineseTraditional", "English", "French"})
        {
            Poseidon::SetLanguage(chosen);
            Poseidon::SetSelectedVoiceLanguage("English");
            Poseidon::SaveGameSettings();
            Poseidon::SaveActiveProfile("ExistingPlayer");
            Poseidon::SetLanguage("ChineseSimplified");
            Poseidon::LoadGameSettings();
            CHECK(std::string((const char*)GLanguage) == chosen);
            REQUIRE(stock.Load(stockPath));
            CHECK(stock.textLanguage == previous);
            CHECK(stock.voiceLanguage == "French");
            CHECK(stock.activeProfile == "ExistingPlayer");
        }

        // Without the mod's registered languages, its preference must be ignored.
        CfgLib::LanguageRegistry::Instance().ResetToDefaults();
        if (std::string(previous) == "English" || std::string(previous) == "French")
        {
            Poseidon::LoadGameSettings();
            CHECK(std::string((const char*)GLanguage) == previous);
        }
    }
}

TEST_CASE("GameSettingsConfig: defaults normalize unsupported detected language", "[Settings][GameSettings]")
{
    FakeEnvironment env;
    env.language = "Korean";
    GameSettingsConfig cfg;
    cfg.LoadDefaults(env);

    CHECK(cfg.textLanguage == "English");
    CHECK(cfg.voiceLanguage == "English");
    CHECK(cfg.blood == true);
}

TEST_CASE("GameSettingsConfig: first run creates file from detected language", "[Settings][GameSettings]")
{
    const std::string path = TmpPath("first-run.cfg");
    std::filesystem::remove(path);

    FakeEnvironment env;
    env.language = "Polish";

    GameSettingsConfig cfg;
    bool created = false;
    REQUIRE(EnsureGameSettingsFile(cfg, path, env, &created));

    CHECK(created);
    CHECK(cfg.textLanguage == "Polish");
    CHECK(cfg.voiceLanguage == "Polish");
    CHECK(cfg.blood == true);

    GameSettingsConfig roundTrip;
    REQUIRE(roundTrip.Load(path));
    CHECK(roundTrip.textLanguage == "Polish");
    CHECK(roundTrip.voiceLanguage == "Polish");
    CHECK(roundTrip.blood == true);
}

TEST_CASE("GameSettingsConfig: normalize fixes unsupported languages", "[Settings][GameSettings]")
{
    FakeEnvironment env;
    env.language = "French";
    GameSettingsConfig cfg;
    cfg.textLanguage = "Esperanto";
    cfg.voiceLanguage = "Klingon";
    cfg.blood = false;

    CHECK(cfg.Normalize(env));
    CHECK(cfg.textLanguage == "French");
    CHECK(cfg.voiceLanguage == "French");
    CHECK(cfg.blood == false);
}

TEST_CASE("GameSettingsConfig: normalize clamps preferred view distance", "[Settings][GameSettings]")
{
    FakeEnvironment env;
    env.language = "English";
    GameSettingsConfig cfg;
    cfg.preferredViewDistance = 50.0f;

    CHECK(cfg.Normalize(env));
    CHECK(cfg.preferredViewDistance == GameSettingsConfig::kMinViewDistance);

    cfg.preferredViewDistance = 6000.0f;
    CHECK(cfg.Normalize(env));
    CHECK(cfg.preferredViewDistance == GameSettingsConfig::kMaxViewDistance);
}

TEST_CASE("GameSettingsConfig: save and load round-trip every field", "[Settings][GameSettings]")
{
    const std::string path = TmpPath("roundtrip.cfg");
    std::filesystem::remove(path);

    GameSettingsConfig src;
    src.textLanguage = "German";
    src.voiceLanguage = "Russian";
    src.activeProfile = "Veteran";
    src.blood = false;
    src.preferredViewDistance = 1700.0f;
    src.respectMissionViewDistance = false;
    REQUIRE(src.Save(path));

    GameSettingsConfig dst;
    REQUIRE(dst.Load(path));
    CHECK(dst.textLanguage == src.textLanguage);
    CHECK(dst.voiceLanguage == src.voiceLanguage);
    CHECK(dst.activeProfile == src.activeProfile);
    CHECK(dst.blood == src.blood);
    CHECK(dst.preferredViewDistance == src.preferredViewDistance);
    CHECK(dst.respectMissionViewDistance == src.respectMissionViewDistance);
}

TEST_CASE("GameSettingsConfig: saves under a UTF-8 user directory", "[Settings][GameSettings][utf8]")
{
    const std::string root = Poseidon::FilesystemPathToUtf8(std::filesystem::temp_directory_path()) +
                             "/gamesettings_\xE6\xB5\x8B\xE8\xAF\x95";
    const std::string path = root + "/game.cfg";

    GameSettingsConfig src;
    src.textLanguage = "Chinese";
    REQUIRE(src.Save(path));

    GameSettingsConfig dst;
    REQUIRE(dst.Load(path));
    CHECK(dst.textLanguage == "Chinese");

    std::filesystem::remove_all(Poseidon::FilesystemPathFromUtf8(root));
}

TEST_CASE("GameSettingsConfig: missing file leaves instance untouched", "[Settings][GameSettings]")
{
    const std::string path = TmpPath("missing.cfg");
    std::filesystem::remove(path);

    GameSettingsConfig cfg;
    cfg.textLanguage = "Polish";
    cfg.activeProfile = "Original";
    CHECK_FALSE(cfg.Load(path));
    CHECK(cfg.textLanguage == "Polish");
    CHECK(cfg.activeProfile == "Original");
}

TEST_CASE("GameSettingsConfig: migrates the legacy active profile", "[Settings][GameSettings]")
{
    const std::string& userDir = Poseidon::Foundation::GamePaths::Instance().UserDir();
    const std::string gamePath = userDir + "game.cfg";
    const std::string prefsPath = userDir + "prefs.cfg";
    std::filesystem::remove(gamePath);
    std::filesystem::remove(prefsPath);

    {
        std::ofstream prefs(prefsPath);
        REQUIRE(prefs.is_open());
        prefs << "PlayerName=Veteran\n";
    }

    CHECK(Poseidon::LoadActiveProfile() == "Veteran");

    GameSettingsConfig migrated;
    REQUIRE(migrated.Load(gamePath));
    CHECK(migrated.activeProfile == "Veteran");

    migrated.activeProfile = "Current";
    REQUIRE(migrated.Save(gamePath));
    CHECK(Poseidon::LoadActiveProfile() == "Current");

    std::filesystem::remove(gamePath);
    std::filesystem::remove(prefsPath);
}

TEST_CASE("GameSettingsConfig: effective view distance respects mission policy", "[Settings][GameSettings]")
{
    CHECK(ResolveEffectiveViewDistance(1500.0f, false, 600.0f) == 1500.0f);
    CHECK(ResolveEffectiveViewDistance(1500.0f, true, 600.0f) == 600.0f);
    CHECK(ResolveEffectiveViewDistance(900.0f, true, std::nullopt) == 900.0f);
}
