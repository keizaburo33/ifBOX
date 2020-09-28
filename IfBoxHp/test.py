from datetime import datetime,date,timedelta
# c="2010-08-07 19:20"
# x=datetime.strptime(c,)

x=datetime(2012, 1, 1, 20, 14, 39)
y=datetime(2012, 1, 1, 23, 29, 39)
s=y-x
p=timedelta(0,3600)
print(p)
print(x+s)
print(s>p)
print(x.hour)
print(x.minute)
print(type(x.date()))

print(datetime.now()>p+x)
x=datetime.now()
y=x.date()
p=datetime(x.year,x.month,x.day)
print(p)
