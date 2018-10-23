#This is the sample solution for comp1405/1005 w2018
#author: Andrew Runka

#some constants for simplicity (not a required design)
item1="Chocolate-dipped Maple Puff"
item2="Strawberry Twizzler"
item3="Vanilla Chai Strudel"
item4="Honey-drizzled Lemon Dutchie"
price1 = 3.50
price2 = 2.25
price3 = 4.05
price4 = 1.99

#quantity variables for each type
q1=0
q2=0
q3=0
q4=0

#ask the users name
name = input("Please enter your name to begin: ")

selection =""
while(selection == "" or selection !="5"): #loop for unlimited doughnuts
	#create a menu for doughnut selection
	print("\nPlease select your doughnut from the following menu: ")
	print("1. Chocolate-dipped Maple Puff ($3.50 each)")
	print("2. Strawberry Twizzler ($2.25 each)")
	print("3. Vanilla Chai Strudel ($4.05 each)")
	print("4. Honey-drizzled Lemon Dutchie ($1.99)")
	print("5. No more doughnuts")
	selection = input("> ")

	if(selection=="1"):
		#ask for quantity
		q1 = int(input("How many "+item1+"s would you like to purchase? "))
	elif selection =="2":
		q2 = int(input("How many "+item2+"s would you like to purchase? "))
	elif selection =="3":
		q3 = int(input("How many "+item3+"s would you like to purchase? "))
	elif selection =="4":
		q4 = int(input("How many "+item4+"s would you like to purchase? "))
	elif selection =="5":
		pass #do nothing (loop condition triggers on selection, students may omit this case if their design permits)
	else:
		print("Sorry, that's not a valid selection...")
		item = ""

currency=""
while(currency==""):
	#ask for currency (CAD, USD, EUR) (menu#2)
	print("\nWhat currency will you be paying with?")
	print("1.CAD")
	print("2.EUR")
	print("3.USD")
	selection = input("> ")

	if(selection=="1"):
		currency="CAD"
		exchange = 1
	elif selection=="2":
		currency = "EUR"
		exchange = 0.66
	elif selection=="3":
		currency = "USD"
		exchange = 0.77
	else:
		print("Sorry, that's not a valid selection.")
		currency = "" #


#report cost
cost = ((q1*price1)+(q2*price2)+(q3*price3)+(q4*price4)) * exchange
print(f"\n\n{name}, here is your receipt:")
print("----------------------------------------")
if q1>0:
	print(f"{q1} {item1}s")
if q2>0:
	print(f"{q2} {item2}s")
if q3>0:
	print(f"{q3} {item3}s")
if q4>0:
	print(f"{q4} {item4}s")
print("----------------------------------------")
print(f"Total cost: {cost:.2f} ({currency})")
print("\nThank you, have a nice day!")

