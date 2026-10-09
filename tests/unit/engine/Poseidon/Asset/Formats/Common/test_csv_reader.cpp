#include <catch2/catch_test_macros.hpp>
#include <Poseidon/Asset/Formats/Common/CsvReader.hpp>
#include <Poseidon/IO/Streams/QStream.hpp>

TEST_CASE("CsvReadAll reads all rows", "[csv]")
{
    const char* data = "1,2,3\n4,5,6\n";
    QIStream stream(data, static_cast<int>(strlen(data)));
    auto rows = Poseidon::Asset::Formats::CsvReadAll(stream);
    REQUIRE(rows.size() == 2);
    CHECK(rows[0][0] == "1");
    CHECK(rows[0][2] == "3");
    CHECK(rows[1][0] == "4");
    CHECK(rows[1][2] == "6");
}

TEST_CASE("CsvReadAll returns empty for empty input", "[csv]")
{
    const char* data = "";
    QIStream stream(data, 0);
    auto rows = Poseidon::Asset::Formats::CsvReadAll(stream);
    CHECK(rows.empty());
}

TEST_CASE("CsvReadAll includes header row", "[csv]")
{
    const char* data = "name,value\nfoo,42\n";
    QIStream stream(data, static_cast<int>(strlen(data)));
    auto rows = Poseidon::Asset::Formats::CsvReadAll(stream);
    REQUIRE(rows.size() == 2);
    CHECK(rows[0][0] == "name");
    CHECK(rows[1][0] == "foo");
}

TEST_CASE("CsvReadAll preserves quoted commas after separator spaces", "[csv]")
{
    const char* data =
        "STR_CRATE, \"Ammo Crates (West, AddOns)\", "
        "\"Caisses de munitions (Ouest, AddOns)\", "
        "\"Casse di munizioni (Occidente, AddOns)\"\r\n";
    QIStream stream(data, static_cast<int>(strlen(data)));
    auto rows = Poseidon::Asset::Formats::CsvReadAll(stream);
    REQUIRE(rows.size() == 1);
    REQUIRE(rows[0].size() == 4);
    CHECK(rows[0][0] == "STR_CRATE");
    CHECK(rows[0][1] == "Ammo Crates (West, AddOns)");
    CHECK(rows[0][2] == "Caisses de munitions (Ouest, AddOns)");
    CHECK(rows[0][3] == "Casse di munizioni (Occidente, AddOns)");
}
