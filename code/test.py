import graph
import grid
import utility_funcs

relative_path_input = "../inputs/test1.in" #Choose with test to run
relatice_path_output = "../inputs/test1.out"
if __name__ == "__main__":
    # Open the file for reading
    with open(relative_path_input, 'r') as file:
        lines = file.readlines()
        # Parse the number of tests
        num_instances = int(lines[0])

        all_instances = []
        grids =[]
        i = 1

        for _ in range(num_instances):
            # Extract the dimensions of the layout
            n, m = map(int, lines[i].split())
            i += 1

            layout = []
            arr = []

            for _ in range(m):
                row = list(lines[i].strip())
                layout.append(row)
                arr.append([0 if entry=='.' else 1 for entry in row])
                i += 1

            all_instances.append((m, n, layout))
            grids.append(grid.Grid(m, n, arr))

    # Print the dimensions and layout of each instance
    for idx, (n, m, layout) in enumerate(all_instances, start=1):
        print(f"Instance {idx}:")
        print("n:", n)
        print("m:", m)
        print("layout:")
        for row in layout:
            print(row)
        print()

    print('***************************************************')
    output=[]
    for grd in grids:
        if(utility_funcs.is_tilable(grd)):
            output.append("yes")
        else:
            output.append("no")

    with open(relatice_path_output,'r') as file:
        lines = file.readlines()
        expected=[]
        for l in lines:
            expected.append(l.strip())

    if(expected==output):
        print("Test Successful")
    else:
        print("Test Unsuccessful")


    print('*************************')
    utility_funcs.randomWalls_grid(10,8,0.2).print_grid()
    print()
    utility_funcs.randomObstacles_grid(10, 8, 0.2).print_grid()
    print()
    print('*************************')
