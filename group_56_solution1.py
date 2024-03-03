# Group Number: Group 56
# STUDENT NAME: Nithya Romeshika Yamasinghe 
# STUDENT NUMBER: S370170
# STUDENT NAME: Ruhani Kakkar 
# STUDENT NUMBER: S371452
# STUDENT NAME: Laba Limbu 
# STUDENT NUMBER: S370270
# STUDENT NAME: Purni Maya Rana 
# STUDENT NUMBER: S371011

import turtle
import time
import math

class Clock:
    """
    A simple analog clock displayed using Turtle graphics.

    This class creates an analog clock with hour, minute, and second hands.
    The clock face includes hour markers, and the current time is displayed below the clock.

    Attributes:
        window (turtle.Screen): The Turtle graphics window for the clock.
        pen (turtle.Turtle): The drawing pen used to draw the clock components.
    """
    def __init__(self):
        """
        Initializes the Clock object and sets up the turtle graphics window.
        """
        self.window = turtle.Screen()  # Create a turtle graphics window.
        self.window.bgcolor("white")  # Set the background color to white.
        self.window.setup(width=600, height=600)  # Set the window dimensions.
        self.window.title("CDU Clock")  # Set the window title.
        self.window.tracer(0)  # Disable automatic screen updates.

        self.pen = turtle.Turtle()  # Create a turtle graphics pen.
        self.pen.hideturtle()  # Hide the pen cursor.
        self.pen.speed(0)  # Set the drawing speed to maximum.
        self.pen.pensize(3)  # Set the pen thickness.

    def draw_center_point(self):
        """
        Draws the center point of the clock.
        """
        self.pen.up()  # Lift the pen up.
        self.pen.goto(0, 0)  # Move the pen to the center.
        self.pen.color("black")  # Set the pen color to black.
        self.pen.dot(5)  # Draw a small center point.

    def draw_clock_face(self):
        """
        Draws the clock face with hour markers.
        """
        self.pen.up()  # Lift the pen up.
        self.pen.goto(0, 150)  # Move the pen to the top center of the clock.
        self.pen.setheading(180)  # Set the pen's heading to face left.
        self.pen.color("black")  # Set the pen color to black.
        self.pen.pendown()  # Lower the pen.

        # Draw the outer circle of the clock.
        self.pen.circle(150)

        for i in range(1, 13):
            # Set the color of the hour markers (red for every 3rd hour, blue otherwise).
            self.pen.color("red" if i % 3 == 0 else "blue")

            # Calculate the position of the hour marker.
            angle = math.radians(360 / 12 * i)
            x = 120 * math.sin(angle)
            y = 120 * math.cos(angle)

            # Draw the hour marker as a filled circle.
            self.pen.up()
            self.pen.goto(x, y + 15)
            self.pen.pendown()
            self.pen.begin_fill()
            self.pen.circle(7)
            self.pen.end_fill()

            # Move to a position below the marker and write the hour value.
            self.pen.penup()
            self.pen.goto(x + 1, y - 26)
            self.pen.pendown()
            self.pen.color("black")
            self.pen.write(i, align="center", font=("Arial", 10, "normal"))
        else:
            # Draw the "CDU" label at the bottom of the clock.
            self.pen.up()
            self.pen.goto(x + 1, y - 60)
            self.pen.pendown()
            self.pen.color("red")
            self.pen.write("CDU", align="center", font=("Arial", 14, "bold"))

    def draw_clock_hands(self, hr, mn, sec):
        """
        Draws the clock hands for hours, minutes, and seconds.
        :param hr: Current hour
        :param mn: Current minute
        :param sec: Current second
        """
        hands = [("red", 70, 12), ("black", 100, 60), ("green", 80, 60)]
        time_set = (hr, mn, sec)

        for hand in hands:
            time_part = time_set[hands.index(hand)]
            angle = (time_part / hand[2]) * 360
            self.pen.penup()
            self.pen.goto(0, 0)
            self.pen.color(hand[0])
            self.pen.setheading(90)
            self.pen.right(angle)
            self.pen.pendown()
            self.pen.forward(hand[1])

    def show_current_time(self, hr, mn, sec):
        """
        Displays the current time below the clock face.
        :param hr: Current hour
        :param mn: Current minute
        :param sec: Current second
        """
        self.pen.penup()
        self.pen.goto(0, -250)
        self.pen.pendown()
        self.pen.color("black")
        self.pen.write(f"{hr:02d}:{mn:02d}:{sec:02d}", align="center", font=("Arial", 14, "normal"))

    def update(self):
        """
        Continuously updates the clock display with the current time.
        """
        while True:
            hr = int(time.strftime("%I"))  # Get the current hour (12-hour format).
            mn = int(time.strftime("%M"))  # Get the current minute.
            sec = int(time.strftime("%S"))  # Get the current second.

            self.pen.clear()  # Clear the previous drawing.
            self.draw_center_point()  # Draw the center point.
            self.draw_clock_face()  # Draw the clock face.
            self.draw_clock_hands(hr, mn, sec)  # Draw the clock hands.
            self.show_current_time(hr, mn, sec)  # Display the current time.
            self.window.update()  # Update the graphics window.
            time.sleep(1)  # Pause for 1 second.

if __name__ == "__main__":
    clock = Clock()
    clock.update()  # Start updating the clock display.
    clock.window.mainloop()  # Start the graphics window main loop.
