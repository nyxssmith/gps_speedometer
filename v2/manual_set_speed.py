import SetDegree

pin = 17
setdegree = SetDegree.SetDegree(pin)

setdegree.to(1)

while 1:
    a = input("enter a degree")
    print(a,type(a))
    a = float(a)
    print(a,type(a))

    setdegree.to(a)