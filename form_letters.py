import pickle
#Initializing the list of receipients
rcpntList = {}

#menu display and input validation, returns an integer 1-7
def menu():
    validInput = False

    while not validInput:
        print("""Enter your choice:
1) Create letters from template
2) List recipients
3) Add recipient
4) Delete recipient
5) Import recipient list
6) Export recipient list
7) Quit""")
        choice = input()
        try:
            intChoice = int(choice)
            if(1<= intChoice <=7):
                validInput = True
            else:
                print("Number must be between 1 and 7\n")
        except:
            print("Please input an integer between 1 and 7\n")
    return intChoice

# "main()" function, infinitely calls menu() to recieve the user's option (or quit).
# calls appropriate function based on user's input from menu()
def main():
    while True:
        selection = menu()
        if (selection == 7):
            print("Goodbye!")
            break
        elif(selection == 1):
            create_letters()
        elif(selection == 2):
            list_recipients()
        elif(selection == 3):
            add_recipient()
        elif(selection == 4):
            delete_recipient()
        elif(selection == 5):
            import_rcpnt_list()
        elif(selection == 6):
            export_rcpnt_list()

#creating an input address method (multiline input)
def input_address():
    address = input("Address: \n")
    while (True):
        info = input()
        if(info == ""): break
        address = address + "\n" + info
    return address

def create_letters():
    fileName = input("Template filename:")
    try:
        template = open(fileName, "r")
        lines = template.readlines()
        for key in rcpntList:
            outfile = open("letter."+key+".txt", "w")
            for line in lines:
                outfile.write(rcpntList[key].substitute(line))
            outfile.close()
        template.close()
        print("Substitution completed")
    except:
        print("Could not open file for reading")


def list_recipients():
    print("Recipient list\n--------------")
    for key in rcpntList:
        print(key)
    print("--------------")

def add_recipient():
    SN = input("Short name: ")
    if(SN in rcpntList):
        print("Recipient exists")
    else:
        LN = input("Long name: ")
        ADD = input_address()
        rcpntList[SN] = Recipient(SN)
        rcpntList[SN].fullname = LN
        rcpntList[SN].address = ADD

def delete_recipient():
    info = input("Name (blank to cancel): ")
    rcpntList.pop(info, "")

def import_rcpnt_list():
    global rcpntList
    infile = open("recipients.bin", "rb")
    rcpntList = pickle.load(infile)
    infile.close()
    print("Recipients imported from recipients.bin")

def export_rcpnt_list():
    outfile = open("recipients.bin", "wb")
    pickle.dump(rcpntList, outfile)
    outfile.close()
    print("Recipients exported to recipients.bin")


class Recipient: #the recipient class

    def __init__(self, short):
        self.address = ""
        self.fullname = ""
        self.__shortname = short
    @property
    def shortname(self):
        return self.__shortname

    def substitute(self, text):
        subbedText = text.replace("{shortname}", self.shortname)
        subbedText = subbedText.replace("{fullname}", self.fullname)
        subbedText = subbedText.replace("{address}", self.address)
        return subbedText

main()
