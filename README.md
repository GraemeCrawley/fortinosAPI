Initial Commit
# fortinosAPI
Application that allows for product data to be pulled from the Fortinos website for analysis. Currently stored on a MySQL server and being used with IBM CPLEX to optimize the lowest cost diet while maintaining specific nutritional requirements.

Here's an example of the data acquired:
![Alt text](./fortinosScraper/tomatoExampleSQL.png?raw=true "Example Showing The Cheapest 20 Tomatos by Price/G")

Below is the output of the CPLEX optimization model, currently minimizing price with constraints on carbohydrates, protein, fat, potassium, sodium, and cholesterol. All solution variables are multiples of 100g, and the objective value is 1000 times less than its dollar amount (this was done in order to make it easier to have decimal values).
![Alt text](./fortinosScraper/optimized.png?raw=true "Example showing the optimization/G")
