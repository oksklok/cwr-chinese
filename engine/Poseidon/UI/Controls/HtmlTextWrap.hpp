#pragma once

#include <algorithm>
#include <Poseidon/Foundation/Strings/RString.hpp>
#include <Poseidon/Foundation/Strings/Mbcs.hpp>

#include <vector>

#define HTML_WRAP_ISSPACE(c) ((c) >= 0 && (c) <= 32)


namespace Poseidon
{
namespace HtmlTextWrap
{

inline int Utf8CharBytes(const char* text, int remaining)
{
    if (!text || remaining <= 0)
        return 0;
    return std::min(Poseidon::Foundation::Utf8CodepointBytes(text), remaining);
}

inline bool IsWrapWhitespace(const char* text, int byteCount)
{
    return byteCount == 1 && HTML_WRAP_ISSPACE(static_cast<unsigned char>(text[0]));
}

inline uint32_t Codepoint(const char* text)
{
    uint32_t cp = 0;
    if (text && *text)
        DecodeUtf8Codepoint(text, &cp);
    return cp;
}

inline uint32_t PreviousCodepoint(const char* text, int offset)
{
    if (offset <= 0)
        return 0;
    int previous = offset - 1;
    while (previous > 0 && (static_cast<unsigned char>(text[previous]) & 0xC0) == 0x80)
        --previous;
    return Codepoint(text + previous);
}

inline bool IsClosingPunctuation(uint32_t cp)
{
    return cp == 0x3001 || cp == 0x3002 || cp == 0xFF0C || cp == 0xFF0E ||
           cp == 0xFF01 || cp == 0xFF1F || cp == 0xFF1A || cp == 0xFF1B ||
           cp == 0xFF09 || cp == 0x3009 || cp == 0x300B || cp == 0x300D ||
           cp == 0x300F || cp == 0x201D || cp == 0x2019 || cp == ',' ||
           cp == '.' || cp == '!' || cp == '?' || cp == ':' || cp == ';' || cp == ')';
}

inline bool IsOpeningPunctuation(uint32_t cp)
{
    return cp == 0xFF08 || cp == 0x3008 || cp == 0x300A || cp == 0x300C ||
           cp == 0x300E || cp == 0x201C || cp == 0x2018 || cp == '(';
}

// Chinese notebook prose has no inter-word spaces. Prefer legal character
// boundaries instead of splitting a Latin name or starting a row with a comma.
inline bool IsChineseWrapBoundary(uint32_t previous, uint32_t current)
{
    if (!previous || !current || IsOpeningPunctuation(previous) || IsClosingPunctuation(current))
        return false;
    const auto cjk = [](uint32_t cp) { return cp >= 0x2E80 && cp <= 0x9FFF; };
    return cjk(previous) || cjk(current) || IsClosingPunctuation(previous) || IsOpeningPunctuation(current);
}

template <class MeasureFn>
inline std::vector<int> ComputeWrapBreaks(RString text, float lineWidth, MeasureFn&& measure,
                                        bool chinese = false, float trailingWidth = 0)
{
    std::vector<int> breaks;
    float curW = 0;
    float wordW = 0;
    int wordI = -1;
    const int n = text.GetLength();

    for (int i = 0; i < n;)
    {
        const int j = i;
        const int charBytes = Utf8CharBytes(text + i, n - i);
        const RString ch = text.Substring(i, i + charBytes);
        if (chinese && i > 0)
        {
            if (IsChineseWrapBoundary(PreviousCodepoint(text, i), Codepoint(text + i)))
            {
                wordI = i;
                wordW = curW;
            }
        }
        if (IsWrapWhitespace(text + i, charBytes))
        {
            wordI = i + charBytes;
            wordW = curW;
        }

        const float cW = measure(ch);
        if (curW + cW + ((chinese && i + charBytes == n) ? trailingWidth : 0) > lineWidth)
        {
            if (wordW > 0)
            {
                breaks.push_back(wordI);
                i = wordI;
            }
            else
            {
                if (curW <= 0)
                {
                    curW += cW;
                    i += charBytes;
                    continue;
                }
                breaks.push_back(j);
                i = j;
            }
            curW = 0;
            wordW = 0;
            wordI = i;
        }
        else
        {
            curW += cW;
            i += charBytes;
        }
    }

    return breaks;
}

} // namespace HtmlTextWrap

}  // namespace Poseidon
