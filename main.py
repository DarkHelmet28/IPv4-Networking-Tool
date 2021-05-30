import formattedResult as fr

def menu():
    print("Please choose the functionality you prefer:")
    print("\t1) Get IPv4 Properties")
    print("\t2) Divide into subnets")

if __name__ == '__main__':
    menu()
    choice = int(input("> "))
    if choice == 1:
        address = input("\nInsert IPv4 Address (CIDR Notation):\t")
        print(f'\n\n{fr.getIPv4Properties(address)}')
    elif choice == 2:
        address = input("\nInsert IPv4 Address (CIDR Notation):\t\t\t")
        desiredNetworks = int(input("Insert the desired number of networks:\t"))
        print(f'\n\n{fr.getIPv4Subnets(address, desiredNetworks)}')
    else:
        print("Pleace select a valid choice.")