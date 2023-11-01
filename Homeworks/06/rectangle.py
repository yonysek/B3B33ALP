# projizdime pole odspodu a hledame zaporna cisla a pak pricitima kdyz nad nima je neco jako zaporne
import sys

f = open(sys.argv[1], "rt")

# f = open("B3B33ALP/Homeworks/06/matrix.txt", "rt")

# Read the contents of the file
contents = f.read()

# Split the contents into rows
rows = contents.strip().split("\n")

# Split each row into columns
matrix = [list(map(int, row.split())) for row in rows]


def matrix_to_histograms(matrix):
    histogram_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(len(matrix) - 1, -1, -1):
        for j in range(len(matrix[i])):
            if matrix[i][j] < 0:
                if i < len(matrix) - 1:
                    histogram_matrix[i][j] = histogram_matrix[i + 1][j] + 1
                else:
                    histogram_matrix[i][j] = 1
    return histogram_matrix


histogram_matrix = matrix_to_histograms(matrix)


def max_area_histogram(histogram):
    # This function calculates maximum
    # rectangular area under given
    # histogram with n bars

    # Create an empty stack. The stack
    # holds indexes of histogram[] list.
    # The bars stored in the stack are
    # always in increasing order of
    # their heights.
    stack = list()

    max_area = 0  # Initialize max area
    l_index = ""
    r_index = ""
    height = 0

    # Run through all bars of
    # given histogram
    index = 0
    while index < len(histogram):
        # If this bar is higher
        # than the bar on top
        # stack, push it to stack

        if (not stack) or (histogram[stack[-1]] <= histogram[index]):
            stack.append(index)
            index += 1

        # If this bar is lower than top of stack,
        # then calculate area of rectangle with
        # stack top as the smallest (or minimum
        # height) bar.'i' is 'right index' for
        # the top and element before top in stack
        # is 'left index'
        else:
            # pop the top
            top_of_stack = stack.pop()

            # Calculate the area with
            # histogram[top_of_stack] stack
            # as smallest bar
            area = histogram[top_of_stack] * (
                (index - stack[-1] - 1) if stack else index
            )

            # update max area, if needed
            # max_area = max(max_area, area)
            if area > max_area:
                max_area = area
                l_index = stack[-1] + 1 if stack else 0
                r_index = index - 1
                height = histogram[top_of_stack]

    # Now pop the remaining bars from
    # stack and calculate area with
    # every popped bar as the smallest bar
    while stack:
        # pop the top
        top_of_stack = stack.pop()

        # Calculate the area with
        # histogram[top_of_stack]
        # stack as smallest bar
        area = histogram[top_of_stack] * ((index - stack[-1] - 1) if stack else index)

        # update max area, if needed
        # max_area = max(max_area, area)
        if area > max_area:
            max_area = area
            l_index = stack[-1] + 1 if stack else 0
            r_index = index - 1
            height = histogram[top_of_stack]

    # Return maximum area under
    # the given histogram
    return max_area, l_index, r_index, height


max_area = 0
max_coords = []

for i in range(len(histogram_matrix)):
    row_max_area, l_index, r_index, height = max_area_histogram(histogram_matrix[i])
    # max_area = max(max_area, row_max_area)
    coords = [[i, l_index], [i + height - 1, r_index]]
    if row_max_area > max_area:
        max_area = row_max_area
        max_coords = coords


print(max_coords[0][0], max_coords[0][1])
print(max_coords[1][0], max_coords[1][1])
