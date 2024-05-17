import click
import tkinter as tk
import grid
import utility_funcs
import models

def confirm_grid(n, m):
    root = tk.Tk()
    root.title("Confirm Grid")

    # Create a 2D list to store the values of each cell
    grid_values = [[0] * m for _ in range(n)]

    def toggle_cell(row, col):
        if grid_values[row][col] == 0:
            grid_values[row][col] = 1
            buttons[row][col].config(bg='black')
        else:
            grid_values[row][col] = 0
            buttons[row][col].config(bg='white')

    def confirm():
        # Close the window and return the whether yes or not the layout is tilable
        root.destroy()
        click.echo("Grid confirmed!")
        grd= grid.Grid(n, m, grid_values)
        if(utility_funcs.is_tilable(grd)):
            click.echo("Yes, the layout is tilable!")
        else:
            click.echo("No, the layout isn't tilable.")

    # Create buttons for each cell in the grid
    buttons = []
    for i in range(n):
        row_buttons = []
        for j in range(m):
            button = tk.Button(root, text='', bg='white', width=2,
                               command=lambda row=i, col=j: toggle_cell(row, col))
            button.grid(row=i, column=j)
            row_buttons.append(button)
        buttons.append(row_buttons)

    # Confirm button
    confirm_button = tk.Button(root, text="Confirm", command=confirm)
    confirm_button.grid(row=n, columnspan=m)

    root.mainloop()

def compute_wall(n,m,p):
    res= utility_funcs.wallObstaclesTilability_likelihood(n,m,p)
    click.echo(f"An approximation of the probability of tilability is: {res*100}%")

def compute_cell(n,m,p):
    res= utility_funcs.cellObstaclesTilability_likelihood(n,m,p)
    click.echo(f"An approximation of the probability of tilability is: {res*100}%")

def predict_wall(n,m,p,model):
    res = model.predict(n,m,p)
    click.echo(f"A prediction of the probability of tilability is: {res*100}%")

def predict_cell(n,m,p,model):
    res = model.predict(n, m, p)
    click.echo(f"A prediction of the probability of tilability is: {res * 100}%")
@click.command()
def main():
    click.echo("Welcome to the CLI tool!")
    #initialize the machine learning models
    wall_model= models.Model('../inputs/tilability_data_500_wall.csv')
    cell_model= models.Model('../inputs/tilability_data_500_cell.csv')
    while True:
        command = input("Enter command ('help' for more information): ")
        if command.startswith("istilabel "):
            args = command.split()[1:]
            if len(args) != 2:
                click.echo("Invalid command. Please enter in the format 'istilabel n m'.")
                continue
            try:
                n, m = map(int, args)
                confirm_grid(n, m)
            except ValueError:
                click.echo("Invalid command. Please enter integers for n and m.")



        elif command.startswith("compute "):
            args = command.split()[1:]
            if len(args) != 4:
                click.echo("Invalid command. Please enter in the format 'compute n m p c'.")
                continue
            try:
                n, m = map(int, args[:2])
                p = float(args[2])
                c = str(args[3])
                if(c=="w"):
                    compute_wall(n,m,p)
                else:
                    compute_cell(n,m,p)
            except ValueError:
                click.echo("Invalid command. Please enter integers for n and m, a float for p, and a char for c")



        elif command.startswith("predict "):
            args = command.split()[1:]
            if len(args) != 4:
                click.echo("Invalid command. Please enter in the format 'predict n m p c'.")
                continue
            try:
                n, m = map(int, args[:2])
                p = float(args[2])
                c = str(args[3])
                if (c == "w"):
                    predict_wall(n, m, p, wall_model)
                else:
                    predict_cell(n, m, p, cell_model)

            except ValueError:
                click.echo("Invalid command. Please enter integers for n and m, a float for p, and a char for c")
        elif command.startswith("help"):
            click.echo("")
            click.echo("This CLI offers you 3 types of commands: ")
            click.echo("1. istilabel n m : where n and m are integers. With this command a GUI pops, and you can input "
                       "your layout. The program then outputs for you whether the given layout is tilable or not.")
            click.echo("")
            click.echo("2. compute n m p c : where n and m are integers, p a float between 0 and 1, and c a char where "
                       "'w' indicates obstacles of type wall.\n  The program will then estimate, using the algorithm, what "
                       "is the probability of tilability of a n*m room with a probability p to have a wall for each "
                       "row/column if c='w',\n  and otherwise to have an obstacle in each cell")
            click.echo("")
            click.echo("3. predict n m p c : where n and m are integers, p a float between 0 and 1, and c a char where "
                       "'w' indicates obstacles of type wall.\n  The program will then predict, using a machine learning "
                       "model, what is the probability of tilability of a n*m room with a probability p to have a wall for each "
                       "row/column if c='w',\n  and otherwise to have an obstacle in each cell. It should be noted that for the "
                       "first call to the predict command the execution takes significantly more time as the model is trained.")
            click.echo("")
        elif command == "exit":
            click.echo("Exiting the program. Thanks!")
            break
        else:
            click.echo("Invalid command. Please enter a command starting with 'istilabel', 'compute' or 'predict'.\n"
                       "Enter 'exit' to quit")

if __name__ == '__main__':
    main()