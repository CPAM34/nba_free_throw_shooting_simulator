try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

import six
from pyfiglet import figlet_format


def log(string, color, font="slant", figlet=False):
    """
    Outputs a string in the specified color

    :param string: The string you are looking to output
    :param color: The color in which you'd like the string to be outputted
    :param font: The font in which you'd like the string to be outputted if figlet is true. Defaults to "slant"
    :param figlet: If set to true, creates ASCII art
    """
    if colored:
        if not figlet:
            # Print bog standard colored text
            six.print_(colored(string, color))
        else:
            # Print ASCII art
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        # Print uncolored, plain string
        six.print_(string)
