import os

cmd = "git add photos/fish-"

for i in range(59000, 69000):
    os.system(cmd+str(i)+".jpg")