import os

class CancelledError(Exception): pass

def main():
    print("\nStrážce seznamu\n")
    while True:
        try:
            enum_file = list(enumerate(list_dir(),start=1))
            if len(list_dir()) > 0:
                if len(list_dir()) < 10:
                    for n, f in enum_file:
                        print(f"{n:1}", f)
                elif 10 <= len(list_dir()) < 100:
                    for n, f in enum_file:
                        print(f"{n:2}", f)
                elif len(list_dir()) >= 100:
                    for n, f in enum_file:
                        print(f"{n:3}", f)
                cislo_seznamu = get_integer("Zadejte číslo seznamu nebo 0 pro nový", "číslo")
                if cislo_seznamu == 0:
                    new_file = get_string("Zadejte název nového seznamu", "string")
                    if new_file and not new_file.endswith(".lst"):
                        new_file += ".lst"
                else:
                    nazev_seznamu = enum_file[cislo_seznamu]
                    process_list(nazev_seznamu)
            else:
                new_file = get_string("Zadejte název nového seznamu", "string")
                if new_file and not new_file.endswith(".lst"):
                    new_file += ".lst"
                    process_list(nazev_seznamu=new_file)
        except CancelledError:
            print("Zrušeno")

def list_dir():
    file_lst = []
    for file in os.listdir("."):
        if file.endswith(".lst"):
            file_lst.append(file)
        else:
            continue
    return sorted(file_lst, key=str.lower)

def process_list(nazev_seznamu):
    fh = None
    seznam_filmu=[]
    try:
        print(nazev_seznamu)
        #fh = open(nazev_seznamu[1], "w", encoding="UTF-8")
        #fh.close()
        fh = open(nazev_seznamu[1], "r+", encoding="UTF-8")
        seznam_filmu = fh.readlines()
        if len(seznam_filmu) < 1:
            print("Seznam je prázdný")
            nazev_filmu = get_string("Zadejte název filmu", "název")
            seznam_filmu.append(nazev_filmu)
        else:
            enum_list = list(enumerate(seznam_filmu, start=1))
            if len(seznam_filmu) > 0:
                if len(seznam_filmu) < 10:
                    for c, m in enum_list:
                        print(f"{c:1}", m)
                elif 10 <= len(seznam_filmu) < 100:
                    for c, m in enum_list:
                        print(f"{c:2}", m)
                elif len(seznam_filmu) >= 100:
                    for c, m in enum_list:
                        print(f"{c:3}", m)
    except EnvironmentError as err:
        print("ERROR", err)
    else:
        print("Uložen seznam", nazev_seznamu)
    finally:
        if fh is not None:
            fh.close()


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                                     name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{name} musí mít nejméně "
                        "{minimum_length} a nejvíce "
                        "{maximum_length} znaků".format(
                        **locals()))
            return line
        except ValueError as err:
            print("CHYBA", err)

def get_integer(message, name="integer", default=None, minimum=0,
                maximum=100, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} musí být mezi {minimum} "
                        "a {maximum} včetně {0}".format(
                        " (nebo 0)" if allow_zero else "", **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))

main()