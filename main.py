name = input("your name:").strip()
age = input("age:")
if age.isdigit():
    age=int(age)
else:
    print("error")
    exit()
hobbie = input("hobbie:")
job = input("job:")

msg=f"{name},{age},{hobbie},{job}"

print(msg)