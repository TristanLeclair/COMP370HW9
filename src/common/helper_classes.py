from enum import Enum


class Headers(Enum):
    """
    Enum class for the headers in the data file.
    """

    title = "title"
    writer = "writer"
    pony = "pony"
    dialog = "dialog"


class Pony(Enum):
    """
    Enum class for the ponies.
    """

    twilight = "twilight sparkle"
    applejack = "applejack"
    rarity = "rarity"
    pinkie = "pinkie pie"
    rainbow = "rainbow dash"
    fluttershy = "fluttershy"
