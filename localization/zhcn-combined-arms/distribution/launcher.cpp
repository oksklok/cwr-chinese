// SPDX-License-Identifier: GPL-3.0-or-later
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <string>

int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR arguments, int)
{
    wchar_t path[32768];
    const DWORD length = GetModuleFileNameW(nullptr, path, ARRAYSIZE(path));
    if (!length || length == ARRAYSIZE(path)) return 1;
    const std::wstring location(path, length);
    const auto directory = location.substr(0, location.find_last_of(L"\\/"));
    const auto client = directory + L"\\@cwr-chinese\\client\\PoseidonGame.exe";
    auto command = L"\"" + client + L"\" --add-mod @cwr-chinese --voice English " + arguments;
    STARTUPINFOW startup{};
    startup.cb = sizeof(startup);
    PROCESS_INFORMATION process{};
    if (!CreateProcessW(client.c_str(), command.data(), nullptr, nullptr, FALSE, 0,
                        nullptr, directory.c_str(), &startup, &process))
    {
        const DWORD error = GetLastError();
        wchar_t detail[1024]{};
        FormatMessageW(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
                       nullptr, error, 0, detail, ARRAYSIZE(detail), nullptr);
        const auto message = L"Cannot start @cwr-chinese\\client\\PoseidonGame.exe.\n"
            L"Extract the complete ZIP beside the original PoseidonGame.exe.\n\n" + std::wstring(detail);
        MessageBoxW(nullptr, message.c_str(), L"cwr-chinese", MB_OK | MB_ICONERROR);
        return 1;
    }
    CloseHandle(process.hThread);
    CloseHandle(process.hProcess);
    return 0;
}
