import csv
minimize = "minimize +"
subjectToProtein = "subject to +"
subjectToCarbs = "+"
subjectToFats = "+"
subjectToCholesterol = "+"
subjectToSodium = "+"
subjectToPotassium = "+"
a = 2.752626
b = 2.528063
test = 41
zero = ""
optimalSubValues = [105,531,578,672,848,857,938,1260,1326,1422,1627,1742,2274,2324,2360,2587,2779,2872,2951,2980,3249,3354,3533,3675,3683,3706,3867,4100,4212,4487,4564,4609,4665,4720,4973,5072,5352,5394,5583,5619,5705,5782,5968,6046,6176,6261,6357,6420,6498,6356,6853,6854,6880,7080,7099,7399,7541,7625,7873,8005,8086,8151,8269,8309,8406,8684,8716,8807,9015,9070,9269,9345,9400,9469,9606,9686,9960,9992,10082,10195,10197,10373,10422,10572,10580,10798,10807,10941,10974,11225,11438,11496,11577,11788,11974,12054,12063,12084,12091,12102,12104,12111,12119]
with open('table.csv', 'rb') as csvfile:
	x = 0
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		#print row[4]
		if x in optimalSubValues and float(row[10]) != 0:
			#print x
			# Minimizing the price
			minimize += str(int(1000*float(row[10]))) + " x" + str(x) + " + "
			# Maximizing protein
			subjectToProtein += str(int(1000*float(row[4]))) + " x" + str(x) + " + "
			# Maximizing carbs
			subjectToCarbs += str(int(1000*float(row[5]))) + " x" + str(x) + " + "
			# Maximizing fats
			subjectToFats += str(int(1000*float(row[6]))) + " x" + str(x) + " + "
			# Controlling Cholesterol
			subjectToCholesterol += str(int(1000*float(row[7]))) + " x" + str(x) + " + "
			# Controlling Sodium
			subjectToSodium += str(int(1000*float(row[8]))) + " x" + str(x) + " + "
			# Controlling Potassium
			subjectToPotassium += str(int(1000*float(row[9]))) + " x" + str(x) + " + "
			#print "x" + str(x) + " >= 0"
			if x  == 1627 or x==3706 or x==7080 or x==8684:
				#ID, brand, name, price, prot, carb, fat, chol, sod, pota, PPG, foodTypeUpper, foodTypeLower
				print str(x) + " " + row[0] + " name: " +  str(row[2]) + " price: "  +  str(float(row[3])) + " prot: " +  str(float(row[4])) + " carbs: " +   str(float(row[5])) + " fat: " +  str(float(row[6])) +  " chol: " +  str(float(row[7])) +  " sod: " +  str(float(row[8])) + " potassium: " +  str(float(row[9])) + " ppg: " +  str(a*float(row[10]))
				print "\n"
			#if x  == 155:
				#print row[0] + " price: " +  str(b*float(row[10])) + " prot: " +  str(b*float(row[4])) + " carbs: " +   str(b*float(row[5])) + " fat: " +  str(b*float(row[6]))
		x+=1

#Numbers based on active male 170lbs
print "enter test" + str(test) + "\n"
print minimize[:-3]
print subjectToProtein[:-3] + " >= 108000"
print subjectToProtein[11:-3] + " <= 139400"
print subjectToCarbs[:-3] + " >= 391000"
print subjectToCarbs[:-3] + " <= 765000"
#Approximations
print subjectToFats[:-3] + " >= 66000"
print subjectToFats[:-3] + " <= 100000"
print subjectToCholesterol[:-3] + " <= 300"
print subjectToSodium[:-3] + " <= 2000"
print subjectToPotassium[:-3] + " <= 4700"
print "end"
print "\n"
print "optimize"
print "\n"
print "display solution variables -"
print "\n"


