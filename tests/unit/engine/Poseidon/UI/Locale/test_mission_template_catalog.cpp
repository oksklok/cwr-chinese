#include <Poseidon/Game/Mission/MissionTemplateCatalog.hpp>
#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>
#include <Poseidon/UI/Locale/WorldLocalization.hpp>
#include <Poseidon/Core/ModSystem.hpp>
#include <chrono>
#include <fstream>
#include "../../Support/test_fixtures.hpp"

#include <catch2/catch_test_macros.hpp>

using namespace Poseidon;

TEST_CASE("wizard generation resolves active mod and language-specific banks", "[ui][wizard][localization]")
{
    const auto unique = std::to_string(std::chrono::steady_clock::now().time_since_epoch().count());
    const auto root = std::filesystem::temp_directory_path() / ("cwrc-wizard-bank-" + unique);
    std::filesystem::create_directories(root / "Templates");
    std::ofstream(root / "Templates" / "Test.Eden.pbo").put('x');
    std::ofstream(root / "Templates" / "Test.Eden.cz.pbo").put('x');
    const RString oldMods = ModSystem::GetModList();
    const RString oldLanguage = GLanguage;
    ModSystem::SetModPath(root.string().c_str());
    GLanguage = "English";
    auto resolved = ResolveMissionTemplateBankPath("Templates/Test.Eden");
    CHECK(std::filesystem::path((const char*)resolved).lexically_normal() == root / "Templates" / "Test.Eden");
    GLanguage = "Czech";
    resolved = ResolveMissionTemplateBankPath("Templates/Test.Eden");
    CHECK(std::filesystem::path((const char*)resolved).lexically_normal() == root / "Templates" / "Test.Eden.cz");
    CHECK(ResolveMissionTemplateBankPath("Templates/User.Eden") == RString("Templates/User.Eden"));
    ModSystem::SetModPath("");
    CHECK(ResolveMissionTemplateBankPath("Templates/Test.Eden") == RString("Templates/Test.Eden"));
    ModSystem::SetModPath(oldMods);
    GLanguage = oldLanguage;
    std::error_code ec;
    std::filesystem::remove_all(root, ec);
}

TEST_CASE("wizard template selector uses template identity, not localized briefing name", "[ui][wizard][localization]")
{
    ClearStringtable();
    MissionTemplateEntry entry;
    entry.name = "1-10_T_TeamFlagFight";
    entry.basePath = "Templates\\1-10_T_TeamFlagFight.Intro";
    entry.bank = true;

    CHECK(GetMissionTemplateSelectorText(entry) == RString("1-10_T_TeamFlagFight"));
}

TEST_CASE("wizard selector metadata changes display only and retains stock fallback", "[ui][wizard][localization]")
{
    ClearStringtable();
    GLanguage = "English";
    LoadStringtable("global", TestFixtures::GetTestFixturePath("residual_ui.utf8.csv"), 0, true);
    MissionTemplateEntry entry{"1-10_T_TeamFlagFight", "Templates\\1-10_T_TeamFlagFight.Intro", true};
    CHECK(GetMissionTemplateSelectorText(entry) == RString("团队夺旗战"));
    CHECK(entry.name == RString("1-10_T_TeamFlagFight"));
    CHECK(entry.basePath == RString("Templates\\1-10_T_TeamFlagFight.Intro"));
    CHECK(LocalizeWorldDisplayName("eDeN", "Everon") == RString("艾弗隆（Everon）"));
    CHECK(LocalizeWorldDisplayName("UserWorld", "My Island") == RString("My Island"));
    REQUIRE(SetLanguage("French"));
    CHECK(GetMissionTemplateSelectorText(entry) == entry.name);
    CHECK(LocalizeWorldDisplayName("Eden", "Everon") == RString("Everon"));
    entry.name = "1-10_T_TEAMFLAGFIGHT";
    CHECK(GetMissionTemplateSelectorText(entry) == entry.name);
    entry.name = "UnrelatedUserTemplate";
    CHECK(GetMissionTemplateSelectorText(entry) == entry.name);
    ClearStringtable();
    GLanguage = "English";
    CHECK(LocalizeWorldDisplayName("Eden", "Everon") == RString("Everon"));
}
