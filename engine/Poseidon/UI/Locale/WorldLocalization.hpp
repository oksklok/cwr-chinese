#pragma once

#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>
#include <Poseidon/UI/Locale/Stringtable/CodepageTranscode.hpp>
#include <cctype>
#include <string>

namespace Poseidon
{
// Optional display metadata only: never rename a world or mutate its config.
inline RString LocalizeWorldDisplayName(RString world, RString stockDisplay)
{
    std::string key = "STR_CWRC_WORLD_";
    for (unsigned char c : std::string((const char*)world))
        key += static_cast<char>(std::toupper(c));
    RString value;
    if (TryLocalizeString(key.c_str(), value) && value.GetLength() > 0)
        return DecodeLegacyTextToRString(value, GLanguage);
    return stockDisplay;
}
} // namespace Poseidon
