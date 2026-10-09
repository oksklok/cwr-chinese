#include <Poseidon/Game/Mission/MissionTemplateCatalog.hpp>

#include <Poseidon/Core/ModSystem.hpp>
#include <Poseidon/Foundation/platform.hpp>
#include <Poseidon/IO/Filesystem/DirScanner.hpp>
#include <Poseidon/UI/Locale/MissionHtmlLocalization.hpp>
#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>
#include <Poseidon/UI/Locale/Languages.hpp>
#include <Poseidon/IO/Filesystem/FileOps.hpp>

#include <cctype>
#include <set>
#include <string.h>
#include <string>

namespace Poseidon
{

namespace
{

bool EndsWithIgnoreCase(const char* value, const char* suffix)
{
    const size_t valueLen = strlen(value);
    const size_t suffixLen = strlen(suffix);
    return valueLen >= suffixLen && stricmp(value + valueLen - suffixLen, suffix) == 0;
}

RString StripSuffix(RString value, const char* suffix)
{
    return value.Substring(0, value.GetLength() - (int)strlen(suffix));
}

void AddTemplate(AutoArray<MissionTemplateEntry>& templates, RString name, RString basePath, bool bank)
{
    MissionTemplateEntry& entry = templates.Append();
    entry.name = name;
    entry.basePath = basePath;
    entry.bank = bank;
}

void ScanTemplateEntries(AutoArray<MissionTemplateEntry>& templates, std::set<std::string>& seen, RString root,
                         RString world, bool multiplayer, bool bank)
{
    char suffix[256];
    snprintf(suffix, sizeof(suffix), bank ? ".%s.pbo" : ".%s", (const char*)world);

    DirScanner scanner;
    if (!scanner.First(root, nullptr))
        return;

    do
    {
        if (scanner.IsDirectory() == bank)
            continue;

        const RString filename = scanner.GetName();
        if (!EndsWithIgnoreCase(filename, suffix))
            continue;

        const RString templ = StripSuffix(filename, suffix);
        std::string key((const char*)templ);
        for (char& c : key)
            c = static_cast<char>(tolower(static_cast<unsigned char>(c)));
        if (!seen.insert(key).second)
            continue; // a mod (scanned first) or an earlier same-name entry already claimed this template
        AddTemplate(templates, templ, GetMissionTemplateBasePath(multiplayer, templ, world), bank);
    } while (scanner.Next());
}

} // namespace

RString GetMissionTemplateRoot(bool multiplayer)
{
    return multiplayer ? RString("Templates") : RString("SPTemplates");
}

RString GetMissionTemplateBasePath(bool multiplayer, RString templ, RString world)
{
    return GetMissionTemplateRoot(multiplayer) + RString("\\") + templ + RString(".") + world;
}

RString ResolveMissionTemplateDisplayName(RString missionDirectory, RString fallback)
{
    RString displayName = LoadLocalizedMissionBriefingName(missionDirectory, fallback);
    return displayName.GetLength() > 0 ? displayName : fallback;
}

RString GetMissionTemplateSelectorText(const MissionTemplateEntry& templ)
{
    // Optional display-only metadata; keep the template identity in list data.
    std::string key = "STR_CWRC_WIZARD_";
    for (unsigned char c : std::string((const char*)templ.name))
        key += c == '-' ? '_' : static_cast<char>(std::toupper(c));
    RString value;
    if (TryLocalizeString(key.c_str(), value) && value.GetLength() > 0)
        return stricmp(value, templ.name) == 0 ? templ.name : value;
    return templ.name;
}

RString ResolveMissionTemplateBankPath(RString relativePath)
{
    // Generation must extract the same mod bank that the preview loads.
    struct Context { RString relative; RString result; } ctx{relativePath, relativePath};
    ModSystem::EnumDirectories([](RStringB dir, void* context) -> bool
    {
        if (dir.GetLength() == 0)
            return false;
        auto* c = static_cast<Context*>(context);
        const char separator[] = {PATH_SEP, '\0'};
        const RString path = dir + RString(separator) + c->relative;
        if (const char* suffix = GetLanguagePboSuffix(GLanguage))
        {
            const RString localized = path + RString(".") + RString(suffix);
            if (FilePathExists(localized + RString(".pbo")))
            {
                c->result = localized;
                return true;
            }
        }
        if (!FilePathExists(path + RString(".pbo")))
            return false;
        c->result = path;
        return true;
    }, &ctx);
    return ctx.result;
}

void ListMissionTemplates(AutoArray<MissionTemplateEntry>& templates, bool multiplayer, RString world)
{
    templates.Clear();

    const RString subRoot = GetMissionTemplateRoot(multiplayer);

    std::set<std::string> seen;
    struct Ctx
    {
        AutoArray<MissionTemplateEntry>* templates;
        std::set<std::string>* seen;
        RString world;
        bool multiplayer;
        RString subRoot;
    } ctx{&templates, &seen, world, multiplayer, subRoot};

    // Every active mod's Templates/SPTemplates (packed only) plus the base, additively and deduped
    // case-folded (mods first). basePath stays relative; the load side resolves it via the mod dir.
    ModSystem::EnumDirectories(
        [](RStringB dir, void* context) -> bool
        {
            auto* c = static_cast<Ctx*>(context);
            if (dir.GetLength() == 0)
            {
                ScanTemplateEntries(*c->templates, *c->seen, c->subRoot, c->world, c->multiplayer, false);
                ScanTemplateEntries(*c->templates, *c->seen, c->subRoot, c->world, c->multiplayer, true);
            }
            else
            {
                const char sep[2] = {PATH_SEP, '\0'};
                const RString modRoot = RString((const char*)dir) + RString(sep) + c->subRoot;
                ScanTemplateEntries(*c->templates, *c->seen, modRoot, c->world, c->multiplayer, true);
            }
            return false;
        },
        &ctx);
}

} // namespace Poseidon
