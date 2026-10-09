class CfgLanguages
{
    languages[] = {"English", "Czech", "Tundra", "ChineseSimplified", "ChineseTraditional"};
    class ChineseSimplified
    {
        autonym = "简体中文";
        code = "ZH-CN";
        codepage = "UTF8";
        voice = 0;
        fallbackLanguage = "English";
    };
    class ChineseTraditional
    {
        autonym = "繁體中文";
        code = "zh-TW";
        codepage = "UTF8";
        voice = 0;
        fallbackLanguage = "English";
        fontDirectory = "Fonts/ChineseTraditional";
    };
};
