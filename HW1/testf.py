f= open("HW1test.txt")
data = ""
for line in f.readlines():
  data += line
  print(data)