#pragma once

#include <Poseidon/IO/ParamFile/ParamFile.hpp>
#include <Poseidon/UI/Locale/Stringtable/CodepageTranscode.hpp>
#include <Poseidon/UI/Locale/Stringtable/Stringtable.hpp>

namespace Poseidon
{
// Resolve explicit presentation metadata only; canonical names stay untouched.
inline RString LocalizeIdentityDisplayName(RString canonicalName, RString key)
{
    RString value;
    if (key.GetLength() > 0 && TryLocalizeString(key, value) && value.GetLength() > 0)
        return DecodeLegacyTextToRString(value, GLanguage);
    return canonicalName;
}
} // namespace Poseidon
