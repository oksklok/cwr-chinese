// Display-only stock configuration overrides; no commercial payloads.
class CfgPatches
{
    class CWRC_UI
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 3.05;
        requiredAddons[] = {"G36a", "BIS_Resistance"};
    };
};
class CfgWeapons
{
    // ParamClass::Update replaces inheritance; retain the exact stock chain.
    class Default {};
    class MGun: Default {};
    class Riffle: MGun {};
    class G36aBase: Riffle
    {
        class FullAuto { displayName = "$STR_CWRC_G36_AUTO"; };
    };
};
class CfgSFX
{
    class FunMusicSfx { name = "$STR_CWRC_SFX_MUSIC"; };
};
class CfgMusic
{
    class RTrack1a { name = "$STR_CWRC_RTRACK1A"; };
    class RTrack1b { name = "$STR_CWRC_RTRACK1B"; };
    class RTrack2 { name = "$STR_CWRC_RTRACK2"; };
    class RTrack3 { name = "$STR_CWRC_RTRACK3"; };
    class RTrack4 { name = "$STR_CWRC_RTRACK4"; };
    class RTrack5 { name = "$STR_CWRC_RTRACK5"; };
    class RTrack6 { name = "$STR_CWRC_RTRACK6"; };
    class RTrack7 { name = "$STR_CWRC_RTRACK7"; };
    class RTrack8 { name = "$STR_CWRC_RTRACK8"; };
    class RTrack9 { name = "$STR_CWRC_RTRACK9"; };
    class RTrack10 { name = "$STR_CWRC_RTRACK10"; };
};
