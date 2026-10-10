#include <Poseidon/UI/Options/OptionsScrollList.hpp>
#include <Poseidon/Foundation/Strings/Mbcs.hpp>
#include <Poseidon/UI/Options/OptionsShell.hpp>
#include <Poseidon/UI/OptionsUI.hpp>
#include <Poseidon/UI/Controls/UIControlsBase.hpp>
#include <Poseidon/UI/OptionsUICommon.hpp>
#include <Poseidon/UI/UITestEngine.hpp>
#include <Poseidon/IO/ParamFile/ParamFile.hpp>
#include <SDL3/SDL_keycode.h>
#include <catch2/catch_test_macros.hpp>

#include <chrono>
#include <cstdio>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <system_error>

using namespace Poseidon;
namespace fs = std::filesystem;

namespace
{
struct TempOptionsDir
{
    fs::path root;

    TempOptionsDir()
    {
        const auto nonce = std::chrono::steady_clock::now().time_since_epoch().count();
        root = fs::temp_directory_path() / ("poseidon_options_" + std::to_string(nonce));
        fs::create_directories(root);
    }

    ~TempOptionsDir()
    {
        std::error_code ec;
        fs::permissions(root, fs::perms::owner_all, fs::perm_options::add, ec);
        fs::remove_all(root, ec);
    }
};
} // namespace

namespace
{
class SlotHitControl : public Control
{
public:
    SlotHitControl(ControlsContainer* parent, int idc) : Control(parent, CT_STATIC, idc, 0, 0, 0, 1, 1) {}
    void OnDraw(float) override {}
};

class SlotNotebook : public ControlObjectContainer
{
public:
    SlotNotebook(ControlsContainer* parent, const ParamEntry& cls) : ControlObjectContainer(parent, 105, cls)
    {
        for (int digit : {3, 7})
        {
            ControlInObject item{};
            item._control = new SlotHitControl(parent, 580 + digit);
            _controls.Add(item);
        }
    }
};

class SlotDisplay : public Display
{
public:
    SlotDisplay() : Display(nullptr) {}
    void Attach(ControlObject* notebook) { _objects.Add(notebook); }
};

struct SlotProvider : OptionsScrollList::Provider
{
    int actions = 0;
    int RowCount() const override { return 10; }
    const char* RowLabel(int) const override { return ""; }
    OptionsScrollList::RowDef RowFor(int) const override { return {-1, nullptr, 0}; }
    int RowValue(int) const override { return 0; }
    void SetRowValue(int, int) override {}
    OptionsScrollList::Kind RowKind(int row) const override
    { return row == 9 ? OptionsScrollList::KindAction : OptionsScrollList::KindBinding; }
    void OnRowAction(int row, Display&) override { if (row == 9) ++actions; }
};
}

TEST_CASE("scrolling a binding slot to an action restores the full click width", "[optionsUI][UI][regression]")
{
    const char* resource = R"cfg(class Notebook {
        model=""; position[]={0,0,1}; positionBack[]={0,0,1};
        direction[]={0,0,1}; up[]={0,1,0}; scale=1;
        inBack=0; enableZoom=0; zoomDuration=0;
    };)cfg";
    ParamFile config;
    QIStream in(resource, static_cast<int>(strlen(resource)));
    config.Parse(in);
    SlotDisplay display;
    auto* notebook = new SlotNotebook(&display, config >> "Notebook");
    display.Attach(notebook);
    SlotProvider provider;
    OptionsScrollList list(display, provider);
    list.FocusInitial();
    float x, y, w, h;
    REQUIRE(notebook->GetSubControlPos(583, x, y, w, h));
    CHECK(w == 0.615f);
    CHECK(notebook->GetCtrl(587)->IsVisible());
    list.OnKeyDown(SDLK_PAGEDOWN);
    REQUIRE(list.ScrollOffset() == 1);
    REQUIRE(notebook->GetSubControlPos(583, x, y, w, h));
    CHECK(x == 0.02f);
    CHECK(w == 0.96f);
    CHECK_FALSE(notebook->GetCtrl(587)->IsVisible());
    CHECK(list.OnButtonClicked(583));
    CHECK(provider.actions == 1);
    list.OnKeyDown(SDLK_PAGEUP);
    REQUIRE(notebook->GetSubControlPos(583, x, y, w, h));
    CHECK(w == 0.615f);
    CHECK(notebook->GetCtrl(587)->IsVisible());
}

TEST_CASE("optionsUI compiles", "[optionsUI][tier3]")
{
    REQUIRE(sizeof(AbstractOptionsUI) > 0);
}

class TestableOptionsShell : public OptionsShell
{
  public:
    TestableOptionsShell(bool enableSimulation, bool credits) : OptionsShell(nullptr, enableSimulation, credits) {}
};

class TestableOptionsPage : public OptionsPage
{
  public:
    using OptionsPage::ContainsCycleIdc;

    const char* TitleText() const override { return ""; }
    int DefaultFocusIdc() const override { return -1; }
    const char* ResourceClassName() const override { return ""; }
};

class TestSemanticControl : public IControl
{
  public:
    TestSemanticControl() : IControl(nullptr, 42) {}

    int GetType() override { return 0; }
    int GetStyle() override { return 0; }
    bool IsInside(float, float) override { return false; }
    void Move(float, float) override {}
    void OnDraw(float) override {}
};

class TestHtmlContainer : public CHTMLContainer
{
  public:
    void SelectSection(const char* name) { _currentSection = FindSection(name); }

    float GetPageWidth() const override { return 1000; }
    float GetPageHeight() const override { return 1000; }
    float GetTextWidth(float, Font*, const char* text) const override { return std::strlen(text); }
};

TEST_CASE("OptionsShell propagates the simulation flag to the display base", "[optionsUI][UI]")
{
    TestableOptionsShell pausedShell(false, false);
    CHECK(pausedShell.EnableSimulation() == false);
    CHECK(pausedShell.SimulationEnabled() == false);

    TestableOptionsShell runningShell(true, false);
    CHECK(runningShell.EnableSimulation() == true);
    CHECK(runningShell.SimulationEnabled() == true);
}

TEST_CASE("OptionsScrollList maps every slot-local control IDC back to its slot", "[optionsUI][UI]")
{
    for (int digit = 0; digit <= 9; ++digit)
        CHECK(OptionsScrollList::SlotForControlIdc(540 + digit) == 4);

    CHECK(OptionsScrollList::SlotForControlIdc(499) == -1);
    CHECK(OptionsScrollList::SlotForControlIdc(590) == -1);
    CHECK(OptionsScrollList::SlotForControlIdc(700) == -1);
}

TEST_CASE("OptionsScrollList row policy keeps disabled rows focusable but inert", "[optionsUI][UI]")
{
    CHECK(OptionsScrollList::CanRowReceiveFocus(OptionsScrollList::KindHeader) == false);
    CHECK(OptionsScrollList::CanRowReceiveFocus(OptionsScrollList::KindAction) == true);
    CHECK(OptionsScrollList::CanRowReceiveFocus(OptionsScrollList::KindSlider) == true);

    CHECK(OptionsScrollList::CanRowAdjustValue(OptionsScrollList::KindStepper, false) == true);
    CHECK(OptionsScrollList::CanRowAdjustValue(OptionsScrollList::KindBoolean, false) == true);
    CHECK(OptionsScrollList::CanRowAdjustValue(OptionsScrollList::KindSlider, false) == true);
    CHECK(OptionsScrollList::CanRowAdjustValue(OptionsScrollList::KindAction, false) == false);
    CHECK(OptionsScrollList::CanRowAdjustValue(OptionsScrollList::KindBinding, false) == false);
    CHECK(OptionsScrollList::CanRowAdjustValue(OptionsScrollList::KindStepper, true) == false);

    CHECK(OptionsScrollList::CanRowInvokeAction(OptionsScrollList::KindAction, false) == true);
    CHECK(OptionsScrollList::CanRowInvokeAction(OptionsScrollList::KindAction, true) == false);
    CHECK(OptionsScrollList::CanRowOpenBinding(OptionsScrollList::KindBinding, false) == true);
    CHECK(OptionsScrollList::CanRowOpenBinding(OptionsScrollList::KindBinding, true) == false);
}

TEST_CASE("UITestEngine returns semantic text when controls render a clipped marquee", "[optionsUI][UI]")
{
    TestSemanticControl ctrl;

    UITestEngine::SetSemanticControlText(&ctrl, "Particles & Volumetrics");
    CHECK(UITestEngine::GetControlText(&ctrl) == "Particles & Volumetrics");

    UITestEngine::ClearSemanticControlText(&ctrl);
    CHECK(UITestEngine::GetControlText(&ctrl).empty());
}

TEST_CASE("UITestEngine returns text from the current HTML section", "[ui][html]")
{
    TestHtmlContainer html;
    html.LoadBuffer("inline.html", R"html(<html><body>
        <h1><a name="End1"></a>Mission complete</h1>
        <p>Selected result</p>
        <hr>
        <h1><a name="End2"></a>Hidden alternate result</h1>
    </body></html>)html");

    REQUIRE(html.NSections() == 2);
    html.SelectSection("End1");
    CHECK(UITestEngine::GetHtmlText(html) == "Mission complete Selected result");
    html.SelectSection("End2");
    CHECK(UITestEngine::GetHtmlText(html) == "Hidden alternate result");
    html.SelectSection("Missing");
    CHECK(UITestEngine::GetHtmlText(html).empty());
}


TEST_CASE("OptionsPage cycle membership helper only accepts listed IDCs", "[optionsUI][UI]")
{
    const int cycle[] = {1101, 1104, 1107};
    TestableOptionsPage page;

    CHECK(page.ContainsCycleIdc(1101, cycle, 3));
    CHECK(page.ContainsCycleIdc(1107, cycle, 3));
    CHECK_FALSE(page.ContainsCycleIdc(1105, cycle, 3));
    CHECK_FALSE(page.ContainsCycleIdc(-1, cycle, 3));
    CHECK_FALSE(page.ContainsCycleIdc(1101, nullptr, 3));
}

TEST_CASE("Continue save selection creates a readable copy", "[optionsUI][savegame]")
{
    TempOptionsDir dir;
    const fs::path save = dir.root / "save.fps";
    const fs::path continueSave = dir.root / "continue.fps";
    std::ofstream(save, std::ios::binary) << "saved-world";

    const std::string saveDir = dir.root.string() + "/";
    EnsureContinueSave(saveDir.c_str());

    std::ifstream input(continueSave, std::ios::binary);
    std::string payload;
    input >> payload;
    CHECK(payload == "saved-world");
}

TEST_CASE("User missions use profile save directories", "[optionsUI][savegame]")
{
    const bool userMission = IsUserMission();
    const RString baseDirectory = GetBaseDirectory();
    const RString baseSubdirectory = GetBaseSubdirectory();
    const RString filenameReal = Glob.header.filenameReal;
    const std::string worldName = Glob.header.worldname;

    SetBaseDirectory(true, GetUserMissionsBase());
    SetBaseSubdirectory("missions/");
    Glob.header.filenameReal = "";

    CHECK(GetSaveDirectory() == GetTmpSaveDirectory());

    Glob.header.filenameReal = "editor_test";
    std::snprintf(Glob.header.worldname, sizeof(Glob.header.worldname), "%s", "demo");
    const RString namedSaveDirectory = GetUserDirectory() + RString("UserSaved/missions/editor_test.demo/");
    CHECK(GetSaveDirectory() == namedSaveDirectory);

#ifndef _WIN32
    Glob.header.filenameReal = "legacy_test";
    const RString legacySaveDirectory = GetUserDirectory() + RString("Saved/") + GetBaseDirectory() +
                                        GetBaseSubdirectory() + RString("legacy_test.demo/");
    fs::create_directories(fs::path(static_cast<const char*>(legacySaveDirectory)));
    std::ofstream(fs::path(static_cast<const char*>(legacySaveDirectory)) / "save.fps", std::ios::binary)
        << "saved-world";

    const RString migratedSaveDirectory = GetSaveDirectory();
    std::ifstream migrated(fs::path(static_cast<const char*>(migratedSaveDirectory)) / "save.fps", std::ios::binary);
    std::string payload;
    migrated >> payload;
    CHECK(payload == "saved-world");
    CHECK(fs::exists(fs::path(static_cast<const char*>(legacySaveDirectory)) / "save.fps"));
#endif

    SetBaseDirectory(userMission, baseDirectory);
    SetBaseSubdirectory(baseSubdirectory);
    Glob.header.filenameReal = filenameReal;
    std::snprintf(Glob.header.worldname, sizeof(Glob.header.worldname), "%s", worldName.c_str());
}
