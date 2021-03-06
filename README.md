# fortinosAPI
Application that allows for product data to be pulled from the Fortinos website for analysis. Currently stored on a MySQL server and being used with IBM CPLEX to optimize the lowest cost diet while maintaining specific nutritional requirements.

Here's an example of the data acquired:
![Alt text](./fortinosScraper/tomatoExampleSQL.png?raw=true "Example Showing The Cheapest 20 Tomatos by Price/G")

## Update1:

Below is the output of the CPLEX optimization model, currently minimizing price with constraints on carbohydrates, protein, fat, potassium, sodium, and cholesterol. All solution variables are multiples of 100g, and the objective value is 1000 times more than its dollar amount (this was done in order to make it easier to have decimal values in CPLEX).
![Alt text](./fortinosScraper/optimized.png?raw=true "Example showing the optimization/G")
With the above in mind, the values in the image are as follows:

* Objective: $0.27
* Yellow Split Peas: 92.97g
* Gingerbread, Apple: 471.28g
* Swiss Cheese: 226.25g
  
  
  
These values are per day, meaning you could survive spending $1.89 a week. Next steps are to include sugar, fiber, and other nutrional constraints with the goal of making the optimal solution more reasonable in terms of an everyday diet.


## Update2:

Was given the opportunity to present my findings a few weeks back. The PDF is labelled "Practical Applications Of Linear Optimization" and can be found in the source folder. Also uploaded a spreadsheet with all the collected data (it's not perfect, but it does its job for now).
