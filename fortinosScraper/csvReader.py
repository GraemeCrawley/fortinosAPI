import csv
import re
minimize = "Minimize \n Obj: "
subjectToProtein = ""
subjectToCarbs = ""
subjectToFats = ""
subjectToCholesterol = ""
subjectToSodium = ""
subjectToPotassium = ""
a = 2.752626
b = 2.528063
test = 41
zero = ""
#optimalSubValues = [105,531,578,672,848,857,938,1260,1326,1422,1627,1742,2274,2324,2360,2587,2779,2872,2951,2980,3249,3354,3533,3675,3683,3706,3867,4100,4212,4487,4564,4609,4665,4720,4973,5072,5352,5394,5583,5619,5705,5782,5968,6046,6176,6261,6357,6420,6498,6356,6853,6854,6880,7080,7099,7399,7541,7625,7873,8005,8086,8151,8269,8309,8406,8684,8716,8807,9015,9070,9269,9345,9400,9469,9606,9686,9960,9992,10082,10195,10197,10373,10422,10572,10580,10798,10807,10941,10974,11225,11438,11496,11577,11788,11974,12054,12063,12084,12091,12102,12104,12111,12119]
with open('table.csv', 'rb') as csvfile:
	x = 0
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		if x < 10:
			#print row[4]
			result = (''.join(i for i in row[2] if not i.isdigit())).lower()
			result = re.sub('[^0-9a-zA-Z]+', '', result)
			if float(row[10]) != 0 and not (float(row[4]) == 0 and float(row[5]) == 0 and float(row[6]) == 0):
				#print x
				# Minimizing the price
				minimize += str(int(1000*float(row[10]))) + " " + result + " + "	
				# Maximizing protein
				subjectToProtein += str(int(1000*float(row[4]))) + " " + result + " + "
				# Maximizing carbs
				subjectToCarbs += str(int(1000*float(row[5]))) + " " + result + " + "
			if float(row[6]) != 0:
				# Maximizing fats
				subjectToFats += str(int(1000*float(row[6]))) + " " + result + " + "
			if float(row[7]) != 0:
				# Controlling Cholesterol
				subjectToCholesterol += str(int(1000*float(row[7]))) + " " + result + " + "
			if float(row[8]) != 0:
				# Controlling Sodium
				subjectToSodium += str(int(1000*float(row[8]))) + " " + result + " + "
			if float(row[9]) != 0:
				# Controlling Potassium
				subjectToPotassium += str(int(1000*float(row[9]))) + " " + result + " + "
			#if x  == 279 or x==1146 or x==3328 or x==8773:
				#ID, brand, name, price, prot, carb, fat, chol, sod, pota, PPG, foodTypeUpper, foodTypeLower
				#print str(x) + " " + row[0] + " name: " +  str(row[2]) + " price: "  +  str(float(row[3])) + " prot: " +  str(float(row[4])) + " carbs: " +   str(float(row[5])) + " fat: " +  str(float(row[6])) +  " chol: " +  str(float(row[7])) +  " sod: " +  str(float(row[8])) + " potassium: " +  str(float(row[9])) + " ppg: " +  str(a*float(row[10]))
				#print "\n\n"
			#if x  == 155:
				#print row[0] + " price: " +  str(b*float(row[10])) + " prot: " +  str(b*float(row[4])) + " carbs: " +   str(b*float(row[5])) + " fat: " +  str(b*float(row[6]))
			x+=1

#Numbers based on active male 170lbs
#print "enter test" + str(test) + "\n"
print minimize[:-3]
print "Subject To \nC1: " + subjectToProtein[:-3] + " >= 108000\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C2: " + subjectToProtein[:-3] + " <= 139400\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C3: " + subjectToCarbs[:-3] + " >= 391000\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C4: " + subjectToCarbs[:-3] + " <= 765000\n"
print "\n\n"
print "\n\n"
print "\n\n"
#Approximations
print "C5: " + subjectToFats[:-3] + " >= 66000\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C6: " + subjectToFats[:-3] + " <= 100000\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C7: " + subjectToCholesterol[:-3] + " <= 300\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C8: " + subjectToSodium[:-3] + " <= 2000\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "C9: " + subjectToPotassium[:-3] + " <= 4700\n"
print "\n\n"
print "\n\n"
print "\n\n"
print "End"

