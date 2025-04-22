#################################################################
######### KAITECH INTERNSHIP: PROGRAMMING FOR ENGINEERS #########
################ Task 3 - Mini Robotics Software ################
#################  By: Ahmed Mohsen Abouelyazed #################
#################################################################

import math  # Import the math library for mathematical functions

# Class representing a link of the robotic arm
class Link:
    def __init__(self, length, name):
        # Initialize the link with a given length and name
        if length <= 0:
            raise ValueError("Link length must be positive.")  # Ensure the link length is positive
        self.length = length  # Store the length of the link
        self.name = name  # Store the name of the link

# Class representing a joint of the robotic arm
class Joint:
    def __init__(self, angle=0, min_angle=-180, max_angle=180):
        # Initialize the joint with an angle and its limits
        self.angle = angle  # Store the current angle of the joint
        self.min_angle = min_angle  # Store the minimum angle limit
        self.max_angle = max_angle  # Store the maximum angle limit
        self.validate_angle()  # Validate the angle upon initialization

    def validate_angle(self):
        # Check if the current angle is within the defined limits
        if not (self.min_angle <= self.angle <= self.max_angle):
            raise ValueError(f"Joint angle must be between {self.min_angle} and {self.max_angle} degrees.")

    def angle_rad(self):
        # Convert the angle from degrees to radians for calculations
        return math.radians(self.angle)

# Class for handling Denavit-Hartenberg parameters
class DHParameter:
    @staticmethod
    def transformation_matrix(theta, d, a, alpha):
        # Calculate the transformation matrix based on DH parameters
        theta_rad = math.radians(theta)  # Convert theta to radians
        alpha_rad = math.radians(alpha)  # Convert alpha to radians
        return [
            [math.cos(theta_rad), -math.sin(theta_rad) * math.cos(alpha_rad), math.sin(theta_rad) * math.sin(alpha_rad), a * math.cos(theta_rad)],
            [math.sin(theta_rad), math.cos(theta_rad) * math.cos(alpha_rad), -math.cos(theta_rad) * math.sin(alpha_rad), a * math.sin(theta_rad)],
            [0, math.sin(alpha_rad), math.cos(alpha_rad), d],
            [0, 0, 0, 1]
        ]  # Return the 4x4 transformation matrix

# Class representing the robotic arm with two links and joints
class RobotArm:
    def __init__(self, link1, joint1, link2, joint2):
        # Initialize the robot arm with two links and their corresponding joints
        self.link1 = link1  # Store the first link
        self.joint1 = joint1  # Store the first joint
        self.link2 = link2  # Store the second link
        self.joint2 = joint2  # Store the second joint

    def forward_kinematics(self):
        # Calculate the position of the end effector based on joint angles and link lengths
        x1 = self.link1.length * math.cos(self.joint1.angle_rad())  # Calculate x position of the first joint
        y1 = self.link1.length * math.sin(self.joint1.angle_rad())  # Calculate y position of the first joint
        x2 = x1 + self.link2.length * math.cos(self.joint1.angle_rad() + self.joint2.angle_rad())  # Calculate x position of the end effector
        y2 = y1 + self.link2.length * math.sin(self.joint1.angle_rad() + self.joint2.angle_rad())  # Calculate y position of the end effector
        return {"elbow": (x1, y1), "end_effector": (x2, y2)}  # Return positions as a dictionary

    def inverse_kinematics(self, target_x, target_y):
        # Calculate the joint angles required to reach a target position (target_x, target_y)
        l1 = self.link1.length  # Length of the first link
        l2 = self.link2.length  # Length of the second link
        distance = math.sqrt(target_x**2 + target_y**2)  # Calculate the distance to the target point

        # Check if the target is reachable
        if distance > (l1 + l2) or distance < abs(l1 - l2):
            raise ValueError("Target is unreachable.")

        # Using the cosine law to find the angles
        angle2 = math.acos((target_x**2 + target_y**2 - l1**2 - l2**2) / (2 * l1 * l2))  # Calculate angle2
        angle1 = math.atan2(target_y, target_x) - math.atan2(l2 * math .sin(angle2), l1 + l2 * math.cos(angle2))  # Calculate angle1

        # Calculate alternative solution (elbow-down configuration)
        angle2_alt = -angle2  # Alternative angle2
        angle1_alt = math.atan2(target_y, target_x) - math.atan2(l2 * math.sin(angle2_alt), l1 + l2 * math.cos(angle2_alt))  # Alternative angle1

        # Return both solutions as degrees
        return [(math.degrees(angle1), math.degrees(angle2)), (math.degrees(angle1_alt), math.degrees(angle2_alt))]

    def jacobian(self):
        # Calculate the Jacobian matrix for the robot arm
        j11 = -self.link1.length * math.sin(self.joint1.angle_rad()) - self.link2.length * math.sin(self.joint1.angle_rad() + self.joint2.angle_rad())  # Partial derivative with respect to joint 1
        j12 = -self.link2.length * math.sin(self.joint1.angle_rad() + self.joint2.angle_rad())  # Partial derivative with respect to joint 2
        j21 = self.link1.length * math.cos(self.joint1.angle_rad()) + self.link2.length * math.cos(self.joint1.angle_rad() + self.joint2.angle_rad())  # Partial derivative with respect to joint 1
        j22 = self.link2.length * math.cos(self.joint1.angle_rad() + self.joint2.angle_rad())  # Partial derivative with respect to joint 2
        return [[j11, j12], [j21, j22]]  # Return the Jacobian matrix

    def workspace_analysis(self):
        # Analyze the workspace of the robot arm
        min_reach = abs(self.link1.length - self.link2.length)  # Minimum reach is the absolute difference of link lengths
        max_reach = self.link1.length + self.link2.length  # Maximum reach is the sum of link lengths
        return min_reach, max_reach  # Return minimum and maximum reach

    def detailed_workspace_analysis(self):
        # Provide detailed information about the workspace
        min_reach, max_reach = self.workspace_analysis()  # Get min and max reach
        return {
            "Minimum Reach": min_reach,  # Minimum reachable distance
            "Maximum Reach": max_reach,  # Maximum reachable distance
            "Reachable Area": f"From {min_reach} to {max_reach} units from the base."  # Description of the reachable area
        }

# Example usage of the RobotArm class
if __name__ == "__main__":
    link1 = Link(5, "Link 1")  # Create the first link with length 5
    joint1 = Joint(45)  # Create the first joint with an angle of 45 degrees
    link2 = Link(3, "Link 2")  # Create the second link with length 3
    joint2 = Joint(30)  # Create the second joint with an angle of 30 degrees

    robot_arm = RobotArm(link1, joint1, link2, joint2)  # Instantiate the robot arm with the links and joints

    # Forward Kinematics
    print("Forward Kinematics:", robot_arm.forward_kinematics())  # Print the positions of the elbow and end effector

    # Inverse Kinematics
    try:
        target_x, target_y = 6, 2  # Define a target position
        angles = robot_arm.inverse_kinematics(target_x, target_y)  # Calculate the required joint angles
        print("Inverse Kinematics Angles:", angles)  # Print the calculated angles
    except ValueError as e:
        print(e)  # Print error if the target is unreachable

    # Jacobian Matrix
    print("Jacobian Matrix:", robot_arm.jacobian())  # Print the Jacobian matrix

    # Workspace Analysis
    min_reach, max_reach = robot_arm.workspace_analysis()  # Analyze the workspace
    print("Workspace Reach: Min =", min_reach, "Max =", max_reach)  # Print the minimum and maximum reach

    # Detailed Workspace Analysis
    workspace_info = robot_arm.detailed_workspace_analysis()  # Get detailed workspace information
    print("Workspace Analysis:", workspace_info)  # Print the detailed workspace analysis