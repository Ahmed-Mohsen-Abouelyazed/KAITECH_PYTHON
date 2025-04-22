#################################################################
######### KAITECH INTERNSHIP: PROGRAMMING FOR ENGINEERS #########
################ Task 2 - Linear Equation Solver ################
#################  By: Ahmed Mohsen Abouelyazed #################
#################################################################

# This Python script solves a 3x3 system of linear equations using Cramer's Rule ✅
# The equations are in the form:
#     a1x + b1y + c1z = d1
#     a2x + b2y + c2z = d2
#     a3x + b3y + c3z = d3

# ----------------------------- #
# Class to handle 3x3 matrices #
# ----------------------------- #
class Matrix:
    def __init__(self, data):
        # Initialize the matrix with a 2D list (3x3)
        self.data = data

    def determinant(self):
        # Calculates the determinant of a 3x3 matrix using the rule of Sarrus
        a, b, c = self.data  # Unpack matrix rows for clarity

        # Apply the 3x3 determinant formula:
        # D = a(ei − fh) − b(di − fg) + c(dh − eg)
        return (
                a[0] * (b[1] * c[2] - c[1] * b[2]) -
                a[1] * (b[0] * c[2] - b[2] * c[0]) +
                a[2] * (b[0] * c[1] - b[1] * c[0])
        )


# ---------------------------------------- #
# Class to represent and solve the system  #
# ---------------------------------------- #
class LinearEquation:
    def __init__(self, coeff):
        # coeff is a 2D list representing the augmented matrix [A|b]
        # Each row is: [a, b, c, d] → coefficients and constant term
        self.coeff = coeff

    def solve(self):
        # Step 1: Create matrices needed for Cramer's Rule

        # Coefficient matrix A (from the first 3 columns)
        d = Matrix([
            [self.coeff[0][0], self.coeff[0][1], self.coeff[0][2]],
            [self.coeff[1][0], self.coeff[1][1], self.coeff[1][2]],
            [self.coeff[2][0], self.coeff[2][1], self.coeff[2][2]]
        ])

        # Matrix D1: Replace 1st column of A with constants (column 4)
        d1 = Matrix([
            [self.coeff[0][3], self.coeff[0][1], self.coeff[0][2]],
            [self.coeff[1][3], self.coeff[1][1], self.coeff[1][2]],
            [self.coeff[2][3], self.coeff[2][1], self.coeff[2][2]]
        ])

        # Matrix D2: Replace 2nd column of A with constants
        d2 = Matrix([
            [self.coeff[0][0], self.coeff[0][3], self.coeff[0][2]],
            [self.coeff[1][0], self.coeff[1][3], self.coeff[1][2]],
            [self.coeff[2][0], self.coeff[2][3], self.coeff[2][2]]
        ])

        # Matrix D3: Replace 3rd column of A with constants
        d3 = Matrix([
            [self.coeff[0][0], self.coeff[0][1], self.coeff[0][3]],
            [self.coeff[1][0], self.coeff[1][1], self.coeff[1][3]],
            [self.coeff[2][0], self.coeff[2][1], self.coeff[2][3]]
        ])

        # Step 2: Calculate all required determinants
        D = d.determinant()  # Determinant of A
        D1 = d1.determinant()  # Determinant of A with 1st column replaced
        D2 = d2.determinant()  # Determinant of A with 2nd column replaced
        D3 = d3.determinant()  # Determinant of A with 3rd column replaced

        # Step 3: Apply Cramer’s Rule:
        # If D ≠ 0 → unique solution exists:
        if D != 0:
            x = D1 / D
            y = D2 / D
            z = D3 / D
            return x, y, z  # Return unique solution as a tuple
        else:
            # If all numerators also zero → infinite solutions
            if D1 == 0 and D2 == 0 and D3 == 0:
                return "Infinite solutions"
            else:
                # If D == 0 but any numerator ≠ 0 → no solution
                return "No solutions"


# -------------------------- #
#   Example usage of solver  #
# -------------------------- #

# Define the augmented matrix: [a, b, c, d]
# This represents the equations:
# 2x + 3y + 1z = 1
# 4x + 1y + 2z = 2
# 3x + 2y + 3z = 3
coefficients = [
    [2, 3, 1, 1],
    [4, 1, 2, 2],
    [3, 2, 3, 3]
]

# Create an object of LinearEquation with the matrix
equation = LinearEquation(coefficients)

# Solve the system using Cramer's Rule
solution = equation.solve()

# Print the solution in a readable format
print("Solution: x =", solution[0], ", y =", solution[1], ", z =", solution[2])
