Project Name: design a Chinese Tuanshan
Function: An interactive application that can dynamically change the basemap, the stamp, and generate a poem to be displayed on the basemap.

Technology Stack:

The main technologies used in the project HTML, Python, Markov Chain Algorithm, and more.

Installation and usage guide:
windows mac OS
python 3.10
Flask==2.0.1
flask-cors==3.0.10
The required library requirements.txt can be installed with the following command: pip install -r requirements.txt

To use flask, you need to run flask before using it. You can activate flask by typing the command python main.py in the terminal to realize the link between the front and back ends. Users enter keywords in the front-end interface, and the back-end will run and return the poems generated to the front-end.

File structure:
index.html: front-end interface code.
main.py: back-end logic, including Markov chain implementation.
assets: the folder where all the basemaps are stored.
fonts: Contains all the changeable fonts in .ttf files.
poem_7.txt: The file that holds the dataset.
