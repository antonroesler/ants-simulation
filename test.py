import util
from main import Ant, Simulator

s = Simulator()
s.data.append(0, 0, "H", 0)
s.data.append(9, 7, "F", 0)
s.data.append(1, 1, "F", 0)
s.data.append(3, 1, "F", 0)
s.data.append(1.5, 1, "F", 0)
s.data.append(0, 0, "food", 0)
s.data.append(1, 1.2, "food", 0)
s.data.append(1, 1, "food", 0)
s.data.append(1, 1, "home", 0)
s.data.append(1.5, 1, "home", 0)
s.create_new_ant(n=3)


ant = Ant()
ant.forward()
ant.forward()
ant.forward()






print(s.data.df.head())
mask = util.close(s.data.df, ant.getx(), ant.gety())
print(s.data.df[mask].head())
vls = s.data.df[mask].type.value_counts()
print("----")
print(vls.get("X"))

df = s.data.df[mask]
row = df[df["type"]=="H"].iloc[0]
print(row["x"])
print(row["y"])
