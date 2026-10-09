#include <catch2/catch_test_macros.hpp>

#include <Poseidon/Core/ModSelection.hpp>

#include <filesystem>
#include <fstream>
#include <random>
#include <string>
#include <vector>
#include <system_error>

using namespace Poseidon;

namespace
{
std::filesystem::path MakeTempDir()
{
    std::random_device rd;
    auto dir = std::filesystem::temp_directory_path() /
               ("cwr_modselection_" + std::to_string(rd()) + "_" + std::to_string(rd()));
    std::error_code ec;
    std::filesystem::create_directories(dir, ec);
    return dir;
}
} // namespace

TEST_CASE("ModSelection round-trips active mods", "[mods][selection]")
{
    const auto root = MakeTempDir();
    const std::string cfg = (root / "sub" / "mods.cfg").string(); // parent dir created on save

    const std::vector<std::string> mods = {"@ecp", "@csla", "@ffur1985"};
    REQUIRE(SaveModSelection(cfg, mods));
    CHECK(LoadModSelection(cfg) == mods);

    std::error_code ec;
    std::filesystem::remove_all(root, ec);
}

TEST_CASE("LoadModSelection ignores comments and blank lines", "[mods][selection]")
{
    const auto root = MakeTempDir();
    const auto cfg = root / "mods.cfg";
    {
        std::ofstream out(cfg, std::ios::binary);
        out << "// header comment\n\n  @ecp  \n# another comment\n@csla\n\n";
    }

    const std::vector<std::string> expected = {"@ecp", "@csla"};
    CHECK(LoadModSelection(cfg.string()) == expected);

    std::error_code ec;
    std::filesystem::remove_all(root, ec);
}

TEST_CASE("LoadModSelection returns empty for a missing file", "[mods][selection]")
{
    CHECK(LoadModSelection("/no/such/path/mods.cfg").empty());
}

TEST_CASE("MODS UI keeps the parsed mount set alive during selection persistence", "[mods][selection][regression]")
{
    // All() returns a reference. Iterating All() on a temporary ActiveMods
    // used a destroyed container and silently saved an empty mods.cfg.
    const auto source = std::filesystem::path(TESTS_ROOT_DIR).parent_path() /
                        "engine/Poseidon/UI/OptionsUIApp.cpp";
    std::ifstream input(source);
    REQUIRE(input.is_open());
    const std::string text((std::istreambuf_iterator<char>(input)), {});
    CHECK(text.find("ActiveModsFromMountPath((const char*)modPath).All()") == std::string::npos);
    CHECK(text.find("ActiveModsFromMountPath((const char*)ModSystem::GetModList()).All()") == std::string::npos);
}
