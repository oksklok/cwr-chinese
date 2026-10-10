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

TEST_CASE("Failed MODS activation preserves the selection across restart", "[mods][selection][regression]")
{
    const auto root = MakeTempDir();
    const auto cfg = (root / "mods.cfg").string();
    const std::vector<std::string> previous = {"@user-mod", "@cwr-chinese"};
    REQUIRE(SaveModSelection(cfg, previous));
    bool attempted = false;
    CHECK_FALSE(ActivateModSelection(cfg, "@broken;@cwr-chinese", [&] {
        attempted = true;
        CHECK(LoadModSelection(cfg) == previous); // no speculative save during remount
        return false; // remount has recovered the previous active set
    }));
    REQUIRE(attempted);
    CHECK(LoadModSelection(cfg) == previous); // startup reads mods.cfg again

    CHECK(ActivateModSelection(cfg, "@another;@cwr-chinese", [&] {
        CHECK(LoadModSelection(cfg) == previous);
        return true;
    }));
    CHECK(LoadModSelection(cfg) == std::vector<std::string>{"@another", "@cwr-chinese"});
    CHECK(ActivateModSelection(cfg, "", [] { return true; }));
    CHECK(LoadModSelection(cfg).empty()); // explicitly disabling all mods persists too

    std::filesystem::remove(cfg);
    CHECK_FALSE(ActivateModSelection(cfg, "@broken", [] { return false; }));
    CHECK_FALSE(std::filesystem::exists(cfg)); // failed first apply creates no startup selection
    std::error_code ec;
    std::filesystem::remove_all(root, ec);
}
