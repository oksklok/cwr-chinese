// Extends stock GOG 3.05 language metadata; Chinese text never occupies English.
class CfgLanguages
{
    languages[] = {"English", "French", "Italian", "Spanish", "German", "Czech", "Polish", "Russian", "ChineseSimplified", "ChineseTraditional"};
    class ChineseSimplified
    {
        autonym = "简体中文";
        code = "ZH-CN";
        codepage = "UTF8";
        localeAliases[] = {"zh_CN", "zh_SG", "zh-Hans", "zh_Hans"};
        // Do not map the primary Win32 Chinese ID: it also covers Traditional.
        win32 = 0;
        voice = 0;
        voiceSuffix = "";
        fallbackLanguage = "English";
        fontDirectory = "Fonts/ChineseSimplified";
    };
    class ChineseTraditional
    {
        autonym = "繁體中文";
        code = "zh-TW";
        codepage = "UTF8";
        localeAliases[] = {"zh_TW", "zh-TW", "zh-Hant-TW", "zh_Hant_TW"};
        win32 = 0;
        voice = 0;
        voiceSuffix = "";
        fallbackLanguage = "English";
        fontDirectory = "Fonts/ChineseTraditional";
    };
};
