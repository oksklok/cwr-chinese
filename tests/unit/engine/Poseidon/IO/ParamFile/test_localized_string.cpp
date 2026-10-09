#include <catch2/catch_test_macros.hpp>
#include "../Support/test_fixtures.hpp"

#include <Poseidon/IO/ParamFile/InitLibraryElement.hpp>
#include <Poseidon/IO/ParamFile/LocalizedString.hpp>
#include <Poseidon/IO/ParamFile/ParamFile.hpp>
#include <Poseidon/IO/Streams/QStream.hpp>
#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>
#include <Poseidon/UI/Locale/IdentityLocalization.hpp>
#include <Poseidon/AI/AI.hpp>
#include <Poseidon/Core/SaveVersion.hpp>
#include <Poseidon/IO/Serialization/ParamArchive.hpp>

#include <cstring>
#include <string>
#include <filesystem>

// Isolation tests for LocalizedString — the engine primitive that resolves a
// localized config value on demand and re-resolves it when the active language
// changes, instead of snapshotting it once at load time (the bug behind GitLab
// #25). These tests exercise the type directly against a two-language
// (English/Czech) stringtable, with no weapon/UI involvement; the end-to-end
// weapon-HUD regression lives in
// tests/unit/.../World/Entities/Weapons/test_weapon_displayname_lang_switch.cpp.

using namespace Poseidon;
using namespace TestFixtures;

namespace
{
// Two-language stringtable: STR_DN_BURST = "Burst"/"Davka" (ASCII Czech so the
// assertions are exact-match and independent of codepage transcoding).
void LoadLocaleFixture()
{
    Poseidon::InitParamFileStringtable(); // wire $STR_ -> stringtable for ParamFile reads
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", GetTestFixturePath("weapon_modes_lang.csv"), 0, true);
    REQUIRE(std::string(Poseidon::LocalizeString("STR_DN_BURST").Data()) == "Burst");
}

ParamFile ParseConfig(const char* text)
{
    ParamFile pf;
    QIStream in(text, static_cast<int>(strlen(text)));
    pf.Parse(in);
    return pf;
}

RString ReadIdentityDisplayName(const ParamEntry& identity)
{
    AIUnitInfo info{};
    info.LoadIdentityName(identity);
    return info.GetDisplayName();
}
} // namespace

TEST_CASE("Identity localization requires explicit metadata and an available key", "[generated-names][localized]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    ParamFile optedIn = ParseConfig("class T { name = \"David Armstrong\"; nameKey = \"STR_TEST_IDENTITY\"; };\n");
    ParamFile arbitrary = ParseConfig("class T { name = \"David Armstrong\"; };\n");
    ParamFile missing = ParseConfig("class T { name = \"My Player\"; nameKey = \"STR_NOT_INSTALLED\"; };\n");
    REQUIRE(std::string(ReadIdentityDisplayName(optedIn >> "T").Data()) == "David Armstrong");
    Poseidon::LoadStringtable("global", GetTestFixturePath("generated_names.utf8.csv"), 0, true);
    REQUIRE(ReadIdentityDisplayName(optedIn >> "T") == LocalizeString("STR_TEST_IDENTITY"));
    REQUIRE(std::string(ReadIdentityDisplayName(arbitrary >> "T").Data()) == "David Armstrong");
    REQUIRE(std::string(ReadIdentityDisplayName(missing >> "T").Data()) == "My Player");
    // Localized display text never overwrites the config name or identity class.
    REQUIRE(std::string(RString(optedIn >> "T" >> "name").Data()) == "David Armstrong");
    Poseidon::ClearStringtable();
    REQUIRE(std::string(ReadIdentityDisplayName(optedIn >> "T").Data()) == "David Armstrong");
}

TEST_CASE("Generated-name metadata follows language columns, not the English language flag",
          "[generated-names][localized][switch]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", GetTestFixturePath("generated_names.utf8.csv"), 0, true);
    ParamFile identity = ParseConfig("class T { name = \"David Armstrong\"; nameKey = \"STR_TEST_IDENTITY\"; };\n");
    REQUIRE(std::string(ReadIdentityDisplayName(identity >> "T").Data()) == "戴维·阿姆斯特朗");
    REQUIRE(Poseidon::SetLanguage("French"));
    REQUIRE(std::string(ReadIdentityDisplayName(identity >> "T").Data()) == "David Armstrong");
    RString category;
    REQUIRE(TryLocalizeString("STR_SINGLE_CATEGORY_RESISTANCE", category));
    REQUIRE(std::string(category.Data()) == "Resistance");
    REQUIRE(Poseidon::SetLanguage("ChineseTraditional"));
    REQUIRE(std::string(ReadIdentityDisplayName(identity >> "T").Data()) == "戴維·阿姆斯壯");
    REQUIRE(Poseidon::SetLanguage("ChineseSimplified"));
    REQUIRE(std::string(ReadIdentityDisplayName(identity >> "T").Data()) == "戴维·阿姆斯特朗");
    Poseidon::ClearStringtable();
    GLanguage = "English";
}

TEST_CASE("Identity display localization leaves the script/network name and context canonical",
          "[generated-names][localized][canonical]")
{
    ClearStringtable();
    GLanguage = "English";
    LoadStringtable("global", GetTestFixturePath("generated_names.utf8.csv"), 0, true);
    ParamFile identity = ParseConfig("class T { name = \"David Armstrong\"; nameKey = \"STR_TEST_IDENTITY\"; };\n");
    AIUnitInfo info{};
    info._identityContext = "KeepContext";
    info.LoadIdentityName(identity >> "T");
    REQUIRE(std::string(info._name.Data()) == "David Armstrong");
    REQUIRE(std::string(info._identityContext.Data()) == "KeepContext");
    REQUIRE(info.GetDisplayName() == LocalizeString("STR_TEST_IDENTITY"));
    REQUIRE(SetLanguage("French"));
    REQUIRE(info.GetDisplayName() == info._name);
    REQUIRE(std::string(info._name.Data()) == "David Armstrong");
    ParamFile arbitrary = ParseConfig("class T { name = \"David Armstrong\"; };\n");
    info.LoadIdentityName(arbitrary >> "T");
    REQUIRE(info._displayNameKey.GetLength() == 0);
    REQUIRE(SetLanguage("English"));
    REQUIRE(info.GetDisplayName() == info._name);
    ClearStringtable();
}

TEST_CASE("Identity archive preserves canonical name and optional display metadata",
          "[generated-names][save][load]")
{
    ClearStringtable();
    GLanguage = "English";
    LoadStringtable("global", GetTestFixturePath("generated_names.utf8.csv"), 0, true);
    ParamFile identity = ParseConfig("class T { name = \"David Armstrong\"; nameKey = \"STR_TEST_IDENTITY\"; };\n");
    AIUnitInfo info{};
    info.LoadIdentityName(identity >> "T");
    ParamArchiveSave save(WorldSerializeVersion);
    REQUIRE(info.Serialize(save) == LSOK);
    REQUIRE(std::string(RString(*save.GetParamFile() >> "name").Data()) == "David Armstrong");
    bool legacy = false;
    SECTION("new save preserves the presentation key") {}
    SECTION("legacy save has no presentation metadata")
    {
        save.GetParamFile()->Delete("displayNameKey");
        legacy = true;
    }
    const auto path = std::filesystem::temp_directory_path() / "cwrc-identity-roundtrip.bin";
    REQUIRE(save.SaveBin(path.string().c_str()));
    AIUnitInfo restored{};
    restored._displayNameKey = "MustNotSurviveLegacyLoad";
    ParamArchiveLoad load;
    REQUIRE(load.LoadBin(path.string().c_str()));
    load.FirstPass();
    REQUIRE(restored.Serialize(load) == LSOK);
    load.SecondPass();
    REQUIRE(restored.Serialize(load) == LSOK);
    REQUIRE(std::string(restored._name.Data()) == "David Armstrong");
    REQUIRE(restored.GetDisplayName() == (legacy ? restored._name : LocalizeString("STR_TEST_IDENTITY")));
    REQUIRE(restored._displayNameKey.GetLength() == (legacy ? 0 : info._displayNameKey.GetLength()));
    REQUIRE(std::filesystem::remove(path));
    ClearStringtable();
}

TEST_CASE("Optional localization lookup finds global/campaign entries and clears a missing result",
          "[generated-names][stringtable]")
{
    Poseidon::ClearStringtable();
    GLanguage = "English";
    Poseidon::LoadStringtable("global", GetTestFixturePath("generated_names.utf8.csv"), 0, true);
    RString value;
    REQUIRE(TryLocalizeString("STR_TEST_IDENTITY", value));
    REQUIRE(value == LocalizeString("STR_TEST_IDENTITY"));
    REQUIRE_FALSE(TryLocalizeString("STR_NOT_INSTALLED", value));
    REQUIRE(value.GetLength() == 0);
    Poseidon::LoadStringtable("campaign", GetTestFixturePath("weapon_modes_lang.csv"), 0, true);
    REQUIRE(TryLocalizeString("STR_DN_BURST", value));
    REQUIRE(std::string(value.Data()) == "Burst");
    Poseidon::ClearStringtable();
}

TEST_CASE("LocalizedString re-resolves a $STR value after a language switch", "[paramfile][localized][switch]")
{
    LoadLocaleFixture();

    ParamFile pf = ParseConfig("class T { loc = \"$STR_DN_BURST\"; };\n");

    LocalizedString loc;
    loc.Bind(pf >> "T" >> "loc");
    REQUIRE(loc.IsBound());

    // Resolves against the current language on demand.
    REQUIRE(std::string(loc.CStr()) == "Burst");

    REQUIRE(Poseidon::SetLanguage("Czech"));
    REQUIRE(std::string(loc.CStr()) == "Davka");

    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(std::string(loc.CStr()) == "Burst");

    // operator RStringB() resolves the same way.
    REQUIRE(Poseidon::SetLanguage("Czech"));
    const RStringB asRString = loc;
    REQUIRE(std::string(asRString.Data()) == "Davka");
}

TEST_CASE("LocalizedString returns a stable value across repeated reads and same-language no-ops",
          "[paramfile][localized]")
{
    LoadLocaleFixture();

    ParamFile pf = ParseConfig("class T { loc = \"$STR_DN_BURST\"; };\n");

    LocalizedString loc;
    loc.Bind(pf >> "T" >> "loc");

    REQUIRE(std::string(loc.CStr()) == "Burst");
    REQUIRE(std::string(loc.CStr()) == "Burst"); // cached read, same value

    // SetLanguage to the current language is a no-op and must not disturb the value.
    REQUIRE(Poseidon::SetLanguage("English"));
    REQUIRE(std::string(loc.CStr()) == "Burst");
}

TEST_CASE("LocalizedString leaves a non-$STR literal untouched across language switches", "[paramfile][localized]")
{
    LoadLocaleFixture();

    ParamFile pf = ParseConfig("class T { lit = \"PlainLiteral\"; };\n");

    LocalizedString lit;
    lit.Bind(pf >> "T" >> "lit");

    REQUIRE(std::string(lit.CStr()) == "PlainLiteral");
    REQUIRE(Poseidon::SetLanguage("Czech"));
    REQUIRE(std::string(lit.CStr()) == "PlainLiteral");
}

TEST_CASE("LocalizedString decodes legacy Central European config literals", "[paramfile][localized][encoding]")
{
    LoadLocaleFixture();

    ParamFile pf = ParseConfig("class T { name = \"\xC8"
                               "MOD\"; title = \"P\xF8"
                               "iklad \xE8"
                               "as\"; utf8 = \"\xC4\x8C"
                               "MOD\"; };\n");

    LocalizedString name;
    name.Bind(pf >> "T" >> "name");
    REQUIRE(std::string(name.CStr()) == "\xC4\x8C"
                                        "MOD");

    LocalizedString title;
    title.Bind(pf >> "T" >> "title");
    REQUIRE(std::string(title.CStr()) == "P\xC5\x99"
                                         "iklad \xC4\x8D"
                                         "as");

    LocalizedString utf8;
    utf8.Bind(pf >> "T" >> "utf8");
    REQUIRE(std::string(utf8.CStr()) == "\xC4\x8C"
                                        "MOD");

    REQUIRE(std::string((pf >> "T" >> "name").GetValue().Data()) == "\xC8"
                                                                    "MOD");
}

TEST_CASE("LocalizedString is empty when unbound or cleared, and follows a rebind", "[paramfile][localized]")
{
    LoadLocaleFixture();

    ParamFile pf = ParseConfig("class T { loc = \"$STR_DN_BURST\"; lit = \"PlainLiteral\"; };\n");

    SECTION("default-constructed is unbound and empty")
    {
        LocalizedString ls;
        REQUIRE_FALSE(ls.IsBound());
        REQUIRE(std::string(ls.CStr()).empty());
    }

    SECTION("Clear() unbinds and empties")
    {
        LocalizedString ls;
        ls.Bind(pf >> "T" >> "loc");
        REQUIRE(std::string(ls.CStr()) == "Burst");
        ls.Clear();
        REQUIRE_FALSE(ls.IsBound());
        REQUIRE(std::string(ls.CStr()).empty());
    }

    SECTION("rebinding switches the resolved source")
    {
        LocalizedString ls;
        ls.Bind(pf >> "T" >> "loc");
        REQUIRE(std::string(ls.CStr()) == "Burst");
        ls.Bind(pf >> "T" >> "lit");
        REQUIRE(std::string(ls.CStr()) == "PlainLiteral");
    }
}
