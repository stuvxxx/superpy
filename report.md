# superpy

Im not sure if there is something noteworthy here because the program mostly consists of simple logic. But Ill try: 

1: I think I had an unconventional way of using argparse, I did it so I was able to have more control of the style and the way errors are shown to the user. 
To be able to have this control or 'to solve the problem' I hardcoded the values in an list to compare them later on with the user input. 

2: I wanted the program to recognize if a new adding of a product can be stacked or not. To solve this problem every input compares its values in the bought.csv field if the right values are the same the products are stacked! 

3: A prompt after the report with a simple yes or no (y or n) question to ask wheter the user wants to save his report or not! 

4: When selling a product Superpy automaticly finds the right order of selling. The problem it solves is that when you have 10 product with the same name but different exp-dates. Superpy always sells the exp-dates which are the closest first. If those are the same and but the buyprice differs, Superpy sells the ones with the lowest buyprice first. 

5: An easy way to sort the inventory! For example sorting on exp-date can quickly show which products are the first to expire!  

6: I really wanted to stick with only the sold and bought csv's. Working with only those two sources made it easy to work/code with. 
