#ask user yes or no and return 1 for yes and 0 for no
def yes_or_no(message):
    input = raw_input(message+" [y/N]")
    if (str(input).lower() == "y") or (str(input).lower() == "yes"):
        return 1
    elif (str(input).lower() == "n") or (str(input).lower() == "no"):
        return 0
    else:
        return 0    