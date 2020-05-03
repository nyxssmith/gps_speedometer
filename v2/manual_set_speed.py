import SetDegree

pin = 17
setdegree = SetDegree.SetDegree(pin)

setdegree.to(1)

while 1:
    a = input("enter a degree")
    setdegree.to(a)