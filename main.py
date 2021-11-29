import os

class CancelledError(Exception): pass

def main():
    print("\nStrážce seznamu\n")
    while True:
        try:
            c_dir = []
            enum_file = list(enumerate(list_dir(), start=1))
            for c in range(1,len(list_dir())+1):
                c_dir.append(c)
            file_dict = dict(zip(c_dir, list_dir()))
            if len(list_dir()) > 0:
                column_format(list_dir(), enum_file)
                cislo_seznamu = get_integer("Zadejte číslo seznamu nebo 0 pro nový", "číslo")
                if cislo_seznamu == 0:
                    new_file = get_string("Zadejte název nového seznamu", "string")
                    if new_file and not new_file.endswith(".lst"):
                        new_file += ".lst"
                        nf = None
                        try:
                            nf = open(new_file, "w", encoding="utf8")
#                            nf.close()
                            process_list(new_file)
                        except EnvironmentError as err:
                            print("ERROR", err)
#                        else:
#                            print(f"Uložen nový seznam {new_file}") # neprintuje
                        finally:
                            if nf is not None:
                                print(f"Uložen nový seznam {new_file}")  # neprintuje
                                nf.close()
                else:
                    nazev_seznamu = file_dict.get(cislo_seznamu)
                    process_list(nazev_seznamu)
            else:
                print("Žádný seznam k dispozici")
                new_file = get_string("Zadejte název nového seznamu", "string")
                if new_file and not new_file.endswith(".lst"):
                    new_file += ".lst"
                    process_list(nazev_seznamu=new_file)
        except CancelledError:
            print("Zrušeno")
            break
        except Exception:
            print("Program ukončen")
            break

def list_dir():
    file_lst = []
    for file in os.listdir("."):
        if file.endswith(".lst"):
            file_lst.append(file)
        else:
            continue
    return sorted(file_lst, key=str.lower)

def process_list(nazev_seznamu):
    saved = True
    fh = None
    seznam_filmu=[]
    try:
        print(nazev_seznamu)
        fh = open(nazev_seznamu, encoding="UTF-8")
        while True:
            if saved:
                seznam_filmu=[]
                fh = open(nazev_seznamu, encoding="UTF-8")
                for line in fh:
                    seznam_filmu.append(line.strip("\n"))
            if len(seznam_filmu) < 1:
                print("Seznam je prázdný")
                empty_list = get_string("[P]řidat [K]onec", "volba", default="p")
                if empty_list.lower() == "p":
                    seznam_filmu = []   #vytvořen nový prázdný seznam
                    nazev_filmu = get_string("Zadejte název filmu", "název")
                    seznam_filmu.append(nazev_filmu)
                    seznam_filmu = list(dict.fromkeys(seznam_filmu))
                    enum_list = list(enumerate(seznam_filmu, start=1))
                    column_format(seznam_filmu, enum_list)
                    saved = False
                elif empty_list.lower() == "k":
                    raise CancelledError
                else:
                    print("Volba musí být [PpKk]")
                    saved = False
            else:
                enum_list = list(enumerate(seznam_filmu, start=1))
                column_format(seznam_filmu, enum_list)
                if saved:
                    full_list = get_string("[P]řidat [V]ymazat [K]onec", "volba", default="p")
                    if full_list.lower() == "p":
                        nazev_filmu = get_string("Zadejte název filmu", "název")
                        seznam_filmu.append(nazev_filmu)
                        seznam_filmu = list(dict.fromkeys(seznam_filmu))
                        enum_list = list(enumerate(seznam_filmu, start=1))
                        column_format(seznam_filmu, enum_list)
                        saved=False
                    elif full_list.lower() == "v":
                        c_list=[]
                        for c in range(1, len(seznam_filmu) + 1):
                            c_list.append(c)
                        list_dict = dict(zip(c_list, seznam_filmu))
                        cislo_filmu = get_integer("Zadejte číslo filmu", "číslo")
                        list_item = list_dict.get(cislo_filmu)
                        seznam_filmu.remove(list_item)
                        enum_list = list(enumerate(seznam_filmu, start=1))
                        seznam_filmu = list(dict.fromkeys(seznam_filmu))
                        column_format(seznam_filmu,enum_list)
                        saved=False
                    elif full_list.lower() == "k":
                        raise Exception
                    else:
                        print("Volba musí být [PpVvKk]")
                        saved = True
                        continue
                if not saved:
                    full_list = get_string("[P]řidat [V]ymazat [U]ložit [K]onec", "volba", default="p")
                    if full_list.lower() == "p":
                        nazev_filmu = get_string("Zadejte název filmu", "název")
                        seznam_filmu.append(nazev_filmu)
                        saved = False
                    elif full_list.lower() == "v":
                        c_list = []
                        for c in range(1, len(seznam_filmu) + 1):
                            c_list.append(c)
                        list_dict = dict(zip(c_list, seznam_filmu))
                        cislo_filmu = get_integer("Zadejte číslo seznamu", "číslo")
                        list_item = list_dict.get(cislo_filmu)
                        seznam_filmu.remove(list_item)
                        enum_list = list(enumerate(seznam_filmu, start=1))
#                        column_format(seznam_filmu, enum_list)
                        saved = False
                    elif full_list.lower() == "u":
                        fh = open(nazev_seznamu, "w", encoding="UTF-8")
                        for items in seznam_filmu:
                            fh.writelines(items+"\n")
                        fh.close()
                        print("seznam filmů uložen")
                        fh = open(nazev_seznamu, encoding="UTF-8")
                        saved = True
                    elif full_list.lower() == "k":
                        raise CancelledError
                    else:
                        print("Volba musí být [PpVvUuKk]")
                        saved = False
                        continue
    except EnvironmentError as err:
        print("ERROR", err)
    except CancelledError:
        raise
    else:
        print("Uložen seznam", nazev_seznamu)
    finally:
        if fh is not None:
            fh.close()

def column_format(list_item, enum_item):
    if len(list_item) < 10:
        for n, f in enum_item:
            print(f"{n:1}", f)
    elif 10 <= len(list_item) < 100:
        for n, f in enum_item:
            print(f"{n:2}", f)
    elif len(list_item) >= 100:
        for n, f in enum_item:
            print(f"{n:3}", f)

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