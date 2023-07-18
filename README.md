Game README
Mortal Gold - Multiplayer Fighting Game
Mortal Gold
Game still under construction.
Welcome to Mortal Gold, a thrilling multiplayer fighting game where players can battle against each other in intense one-on-one combat using iconic characters such as Putin, Musk, and Trump. Challenge your friends or random opponents and prove your fighting skills in this action-packed game.

How to Play
Requirements
Python 3.x
Pygame
Django
Channels
Channels-Redis
Django rest framework
Docker
Installation
Clone the repository to your local machine.

Install the required dependencies by running the following command:

Copy code
pip install -r requirements.txt
Running the Game
Start the Django development server:

Copy code
python manage.py runserver
The game server should now be running on http://localhost:8000/.

Open a web browser and navigate to the game client:

http://localhost:8000/
Create an account or log in to your existing account to access the game.

Choose a character (Putin, Musk, or Trump) and start a new match or join an existing one.

Enjoy the thrilling multiplayer fighting experience! Use the arrow keys to move your character and press "Space" to perform a special action.

Gameplay Instructions
The goal of the game is to reduce your opponent's health to zero while preserving your health.

Each character has unique abilities and animations. Master your character's moves to gain an advantage over your opponents.

Monitor your health bar and make strategic decisions to maximize your chances of winning.

Be aware of your opponent's actions and movements to dodge attacks and retaliate effectively.

How the Game Works
Game Server
The game server is built using Django and Django Channels. It handles the creation of matches, player connections, and game events. The game data is transmitted over WebSockets in JSON format.

The main server components are:

consumers.py: This file contains the Django Channels WebSocket consumer class responsible for handling player connections, disconnections, and game events. It also updates player data and sends it to the connected clients.

views.py: This file contains the Django views for creating and listing available matches. It ensures that players cannot join their own created room.

Game Client
The game client is implemented using Pygame and WebSockets. Players interact with the game by controlling their characters on the screen.

The main client components are:

gameclient.py: This file contains the GameClient class, which initializes the game window and character data. It handles user input, updates the game screen, and communicates with the server using WebSockets to send and receive game data.

character.py: This file defines the Character class, which represents a player's character in the game. It handles character movement, animations, and health management.

background.py: This file defines the AnimatedBackground class, which handles the background animation in the game.

character_selection.py: This file contains the character selection screen logic.

login.py: This file contains the login screen logic.

License
This game is licensed under the MIT License. Feel free to use, modify, and distribute the code as you see fit.

Credits
The game assets, including character sprites, background images, and sound effects, are used for demonstration purposes only and belong to their respective creators.

Contact
For any inquiries or support, please contact the developer

Thank you for choosing Mortal Gold! Have fun battling your opponents and becoming the ultimate champion!
