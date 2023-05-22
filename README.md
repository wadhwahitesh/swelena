# ELENA
Elevation based navigation system is a web application for displaying the optimal route between a start location and an end location, considering the elevation of terrain. The user can maximize or minimize his elevation variation in the UI. The purpose of this application is to give the user control towards his/her workouts like cycling or running. 

# Steps to run the elevation based navigation application

- Run ```./init.sh``` from the root folder of the project. This starts up the flask server and installs the necessory libraries.
- Open `http://127.0.0.1:5000/view` on any browser to view SWEleNA's GUI.

- The user should now select the start and end points on the map presented on the screen.
- The user should select if they want to maximize or minimize the elevation using the buttons available.
- The user now inputs the percentage increase (with respect to the shortest path) in the total distance that they are willing to travel for their workout.
- The user can click on `FIND PATH` button to see the optimal path (in RED) on the map considering elevation. The application also shows the shortest path (in GREEN) without considering the elevation.
- The user can click on the `RESET` button to reset the app to the initial default view.

- To run the tests run `python src/test/test.py` from the home directory.


# Design Pattern 
- We have used the Model-View-Controller Design pattern where we have 
    - Model - The map of Amherst treated as a Graph. 
    - View - Our interactive GUI.
    - Controller - Server and other algorithms used to manipulate the Model.

# User Interface features
- Components of the User Interface include
    - The map of Amherst rendered using mapbox api key
    - Current coordinates available on hover
    - Interactive on-click pins placed on the map indicating start and end location
    - Buttons for choosing Maximize and Minimize elevation
    - Textbox to input the percentage of the shortest path we are willing to travel extra for the elevation constraint
    - Start location, End location visible after we select them on the map
    - RESET Button
    - FIND PATH button
    - Comprehensive display of shortest route vs algorithm's route colored in Green and Red respectively.
    - Stylish clear UI display in terrain mode