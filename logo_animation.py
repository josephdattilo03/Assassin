def get_title_animation():
    title = ["          _____                    _____                    _____                    _____                    _____                    _____                    _____                    _____          ",
    "         /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \         ",
    "        /::\    \                /::\    \                /::\    \                /::\    \                /::\    \                /::\    \                /::\    \                /::\____\        ",
    "       /::::\    \              /::::\    \              /::::\    \              /::::\    \              /::::\    \              /::::\    \               \:::\    \              /::::|   |        ",
    "      /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \               \:::\    \            /:::::|   |        ",
    "     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \               \:::\    \          /::::::|   |        ",
    "    /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \               \:::\    \        /:::/|::|   |        ",
    "   /::::\   \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \      /::::\   \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \              /::::\    \      /:::/ |::|   |        ",
    "  /::::::\   \:::\    \    ___\:::\   \:::\    \    ___\:::\   \:::\    \    /::::::\   \:::\    \    ___\:::\   \:::\    \    ___\:::\   \:::\    \    ____    /::::::\    \    /:::/  |::|   | _____  ",
    " /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \  /\   \:::\   \:::\    \  /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \  /\   \:::\   \:::\    \  /\   \  /:::/\:::\    \  /:::/   |::|   |/\    \ ",
    "/:::/  \:::\   \:::\____\/::\   \:::\   \:::\____\/::\   \:::\   \:::\____\/:::/  \:::\   \:::\____\/::\   \:::\   \:::\____\/::\   \:::\   \:::\____\/::\   \/:::/  \:::\____\/:: /    |::|   /::\____ ",
    "\::/    \:::\  /:::/    /\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\::/    \:::\  /:::/    /\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\:::\  /:::/    \::/    /\::/    /|::|  /:::/    /",
    " \/____/ \:::\/:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \/____/ \:::\/:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \:::\/:::/    / \/____/  \/____/ |::| /:::/    / ",
    "          \::::::/    /    \:::\   \:::\    \       \:::\   \:::\    \               \::::::/    /    \:::\   \:::\    \       \:::\   \:::\    \       \::::::/    /                   |::|/:::/    /  ",
    "           \::::/    /      \:::\   \:::\____\       \:::\   \:::\____\               \::::/    /      \:::\   \:::\____\       \:::\   \:::\____\       \::::/____/                    |::::::/    /   ",
    "           /:::/    /        \:::\  /:::/    /        \:::\  /:::/    /               /:::/    /        \:::\  /:::/    /        \:::\  /:::/    /        \:::\    \                    |:::::/    /    ",
    "          /:::/    /          \:::\/:::/    /          \:::\/:::/    /               /:::/    /          \:::\/:::/    /          \:::\/:::/    /          \:::\    \                   |::::/    /     ",
    "         /:::/    /            \::::::/    /            \::::::/    /               /:::/    /            \::::::/    /            \::::::/    /            \:::\    \                  /:::/    /      ",
    "        /:::/    /              \::::/    /              \::::/    /               /:::/    /              \::::/    /              \::::/    /              \:::\____\                /:::/    /       ",
    "        \::/    /                \::/    /                \::/    /                \::/    /                \::/    /                \::/    /                \::/    /                \::/    /        ",
    "         \/____/                  \/____/                  \/____/                  \/____/                  \/____/                  \/____/                  \/____/                  \/____/         "]
    style = []
    for i in range(0,len(title)):
        style.append("animation-delay: " + str(i*100) + "ms;")
    return title,style
