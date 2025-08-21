def add(firstName: str, lastName):
    firstName.capitalize()
    return firstName + " " + lastName

fName = "bill"
lName = "Gates" 

name = add(fName, lName)
print(name)