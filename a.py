a = {}
b = "aaa"
if b in a.keys():
    print("in")
else:
    print("not in")
a[b] = 0
if b in a.keys():
    print("in")
else:
    print("not in")

x = "a"
print(type(x))
