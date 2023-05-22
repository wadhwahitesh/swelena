# Swelena
Elevation based navigation system is a web application for displaying the optimal route by considering the elevation of terrain of the map. The user can maximize or minimize his elevation variation in the UI. The purpose of this application is to give the user control towards their workouts like cycling or running. 

# Steps to run the Swelena application

- Run ```./init.sh``` . This starts up the flask server and install the necessory libraries.
- Open `http://127.0.0.1:5000/view` on any browser to view SweleNa's GUI.

- The user should now select the start and end points on the map presented on the screen
- The user should select if they want to maximize or minimize the elevation using the buttons available.
- The user now inputs the percentage increase in the total distance that they are willing to travel.
- The user can click on `FIND PATH` button to see the optimal path on the map considering elevation in RED. The application also shows the shortest path without considering the elevation in GREEN.
- The user can click on the `RESET` button to reset the app to the initial default view.

- To run the tests run `python src/test/test.py` from the home directory

# Look out for the following

- If you want to play with the location, you can change the range inside `View/templates/main_GUI.html`
- In case startup is taking too much time, this might mean that a new graph.p (containing all neighboring node information for an area) file is getting downloaded which may take up to 5 minutes. Be patient, it will continue to work as expected. 
- To get your own API keys, visit `https://developers.google.com/maps/documentation/javascript/get-api-key`
- If distance between start and end is too large, you will get an exception.
- If percentage `<= 100` you will be thrown an exception.

# Design Pattern 
- We use the Model View Controller Design patterm where we have 
    - Model - The map of Amherst treated as a Graph. 
    - View - Our interactive GUI.
    - Controller - Server and other algorithms used to manipulate the Model.

# User Interface features
- Components of the User Interface include
    - The map of Amherst rendered using Google Maps
    - Current coordinates available on hover
    - Interactive on-click pins placed on the map indicating start and end point
    - Buttons for Maximize and Minimize elevation
    - Text Box to get the percentage of the shortest path we need in our new optimally elevated route
    - Start location, End location visible after we click our start and destination
    - RESET Button
    - FIND PATH button
    - Comprehensive display of shortest route vs algorithm's route colored in Red and Green.
    - Stylish clear UI display in terrain mode