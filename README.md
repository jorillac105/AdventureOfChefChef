# README #
Studios: LookingForOneMorePerson
(Quan Bui, Vladimir Postnikov, Julian Orillac, Nate Smith)

To run the game, type: python3 game.py

~~ CONTROLS ~~

  Arrow keys -> Movement
  Space Bar  -> Attack (hold down to continuously attack)
  'Enter'    -> Use (cabinet, door)
  'Z'        -> Drop bomb
  'X'        -> Detonate bomb
  'P'        -> Opens pause menu.
  'M'        -> Quit to menu
  'Q'        -> Quit game
   'W/A/S/D' -> Control the knife ranged weaponry after you pick up knives at the start of level 4 (diagonal throwing is possible with key combos)


!!! IMPORTANT !!!
Debug commands:

  '2' - transports you to level 2.
  '3' - transports you to level 3.
  '4' - transports you to level 4.
  'H' - adds 8 health.
  'L' - adds a randomly placed rat (try holding it down if you want a challenge).
  'C' - toggles a carrot item which gives "carrot vision" ie greater visibility in the levels after level 1
  'K' - toggles key object which is required to exit level 1.
  'E' - causes an "explosion" of particles centered on the chef.
  'Y' - on level 3 this kills the boss instantly
  'B' - after level 1, adds a bomb


-- Win conditions --

Level 1:
  Kill all rats
  Find key
  Go down stairs (press enter)
  (OPTIONAL)
  Find the carrot (Will help in level 2)

Level 2:
  Find trap door (press enter)
  (OPTIONAL)
  Try to find the hidden weapon upgrade!

Level 3:
  Kill the boss, reveal the ladder, escape to level 4!

Level 4:
  Close all of the sewer pipes to win!
  (Protip: Knives are god-mode right now just for this version!)

Level 6 / PvP:
  Can't win, you just kill the enemy player repeatedly


Level Transitions:
-Indication that the exit is open on level 2
  -Messages that trigger once exit condition is met that tells you what to do for each level?

Sound:
-sound on opening containers
-sound on shutting pipes

Misc:
-finalize readme

Quan's list of things to fix:
-music on title screen
-for title screen, have "press any key" blink
-for title screen, maybe slow moving fog
-sound effects for hitting "next" during the story cutscenes
-music during story cutscenes
-change score font and place it somewhere else (maybe bottom left) so not in the way
-center the pop-up messages
-boss dying animation (quan)
-boss hurt animation (quan)
-less pizza drop or have knives use the pizza meter
-add "p" to pause to controls graphic (quan)
-win game sound
-lose game sound
-level 3: different music that is spookier
-level 3: add fog or something to be spookier?
-level 4: rat sometimes spawns along outer left wall and is unreachable
-level 4: no tiles on bottom row of map?
-add in credits image!

Achievements of week 13:
Vladimir:
-boss shoots missiles that follow ya and blow up if they hit eachother
-implemented boss animations and pathing
-expanded projectile class for fancier missle operators to be used later for the boss

Nate:
- Fixed some initial camera stuttering
- Added "bumping" for both chef and rats
  - Chef and rats will now be bumped when hit
- Put hit sound on all hits for enemy and chef

Julian:
- created lighting effects:
  - for darkness, ratBoss, bombs
- added mouse usability to most ui screens
- fixed issue where instruction screens would take too long to load

Quan:
- Redesigned item information pop-up messages
- Redesigned purple mini boss attack graphics
- Designed final boss fire projectile

Achievements of week 12:

Vladimir:
- Created a player vs player knife dodging fiesta game that's vastly unfinished.
- aka changing a bunch of things in a bunch of files to support 2 chefs at the same time
- created the room layout for pvp
- high level executive marketing decisions

Julian:
- bug fixes
- Changed way high scoring works so that it creates a new file on initial play.
- Added in stupid version of boss into lvl 5

Nate:
- Lots of bug fixes
- Changed the first boss' orange melee attack, should always hit if within certain range
- Made it so that you cannot spam bombs
- Because you cannot spam bombs, increased bomb damage from 2 to 10 on boss
- Can now melee attack the boss
- Initial implementation of level 5
- Heavily altered level 5 layout
- Added in item instructions on first pickup

Quan:
- Designed final boss: four directional movement, two attacks, two forms, transformation sequence
- Designed level 5 tiles and map layout
- Added new controls to controls screen graphic


Achievements of week 11:

Nate:
- Completely redid rat AI
- Designed and implemented intelligent pathfinding for enemies
 - Each map is now a graph of tiles and their connections
 - Enemies will now pathfind toward the character and move around obstacles, finding the optimal path
 - Credits for the sample A* algorithm (contained in navGraph.navigate()) at bottom of README
- Added rewards for beating the boss in level 3
- Removed unlimited bombs, now you need to pick them up yourself
- Added bomb placement animations

Quan:
- Designed assets for new range attack
 - Chef spinning, multiple knives, knife set pickup item
- Changed final boss, developed character design
- Cleaned up some assets to improve animation flow
- Designed options menu for controlling volume and brightness
 - Uses a dot system to show volume and brightness levels

Julian:
------wrote by Vlad, I know he did a bunch but idk exactly what :^) ------
- Helped Nate with some aspects of rat AI
- Brightness and sound now works ayyyy
- Cleaned up some code
- def other stuff too

Vladimir:
- Implemented the most broken weapon known to mankind: the knife attack - and all of the related complexities
- You thought bombs were OP Tristan? This is basically god mode (until I limit the rate of fire next week,
  - I wanted you to have some fun after the hard boss from last week)
- Other than that, just cleaned up some of the code and updated the variables attached with the chef
  - to make things easier for us going fowards (i.e. making more weaponry)

Achievements of week 10:
Quan:
- Designed rat boss for new level 3
- Animated rat boss: left, right, idle, three different attacks, hurt, death
- Designed level 3 map

Vladimir:
- Boss animation inserted
- Added projectile class because we're def gona need it later
- Added chef health
- Fine tuned the collision boxes for the boss's projectiles
- Changes to camera so it pans over the boss as he dies

Jullian:
-Made bossrat.py
-Added a ladder that appears upon the boss's death
-Fixed rat spawn points in level 3
-Made the boss fight room close once the player enters so they can't escape
-Boss music plays upon entering boss room
-Implemented other songs/sounds too

Nate:
-Implemented boss' melee combat attacks
-Added randomized ranged and melee attacks at certain time intervals for the boss
-Added explosions for the boss' projectiles

Achievements of week 9:

Nate:
-Rebalanced drops
-Added health caps and max number of bomb
-Player now stays facing in the direction they last moved in
-Implemented idle animations for new directions

Julian:
-Implemented Chunks and sound effects
-as well as songs
-Implemented new menu screen
-Implemented pause menu screen on all levels
-Implemented new rats in lvl 3

Vladimir:
-changed the timing on the energy regeneration
-compressed/organized/found all of our sound files


Achievements of week 8:

Vladimir Postnikov:
- Put everything related to the bombs (animation and pickup conditions, etc)
together so they work as intended
-Organized the textures that the chef has so it's not a clusterfuck
-Set up level 3 so it's loaded properly
-Moved the weapons to the proper spawn points during the various levels so it makes sense
progression wise
-Added fade to black screen once level 3 is complete

Nate Smith:
-Added renderArray, which orders objects to be rendered objects in order of their y position. Now rats will not render under cabinets etc.
-Added in debug commands
-Fixed boundary bug
-Added resetChef(), which resets chef's variables during new game.
-Added emitter framework to game. enemies will emit particles when dying.
-Added random drops for cabinets, changed droprate for cabinets and rats.
-Added more intelligent rat AI. Will update rat direction more frequently. (WIP)

Quan Bui:
-Designed level 3 tiles and map
-Added bomb graphics (floating item and explosion)
-Fixed cutscene graphic between Level 1 and 2 so that it's no longer "to be cont..."
-Animated chef for bomb attack
-Added necessary UI messages for items and other interactive game elements
-Added story/instruction graphics for each level, a controls screen, and "to be
continued" screen

Achievements of week 7:

Nate Smith:
-Helped making particle emitters.
-Fixed minor bug with menu cursor animation.
-Added trap door win condition
-Added energy depleted message
-Added debug commands
(spent most of time this week trying to get Sublime text to work; expect much more coding next week)

Julian Orillac:
-Fixed huge bug where the game was rendering far more times than it needed to be, made game significantly faster.
-Helped making particle emitters.
-implemented level 2.
-Added second attack.
-Made the chef be an object passed between classes.

Vladimir Postnikov:
-Added in the "carrot", which will greatly improve vision in level 2.
-Made reduced vision for level 2.
-Changed the scoring system to promote speed running and efficient pathing/killing
-Fixed collision glitch that plauged level 2
-Updated UI To reflect items

Quan Bui:

- Level 2 map tiles, key, and data
   - The pushable box (19, 20, 21, or 22) belongs on the tile coded "1",
     which is the exit.
- Level 2 pantry opening animation
- New pop-up messages
   - This includes all necessary carrot-related messages, if ready to implement.- Item graphics that can show up in your inventory next to the key
   - Shows ladles or cheese graters, depending on which item is equipped
- Cheese grater attack sprite
   - Have this be the attack sprite after the player finds the graters
- New chef idle animation with stroke around it for the menu screen for better
visibility.


Achievements of week 6:

Nate Smith:
-Freed surfaces and destroyed textures after we are done with them.
-Added energy regeneration.
-Added ability to pick up items.
-Added random spawn locations for enemies.
-Consolidated rendering into the camera class.

Julian Orillac:
-Made cabinets interactible
-Added in story slides and loading screen

Vladimir Postnikov:
-Sped up collision detection.
-Fixed rat movement.
-Added heart and pizza drops.
-Added in energy.

Quan Bui:
New graphic assets:
- Cutscene graphics to improve storytelling and instructional flow. The game
  now starts with an introduction of the setting, moves to an instructions and
  controls screen, and then after gameplay shows either the "you lose" screen,
  or a "to be continued..." (alluding to Level 2) and then the "you won" screen.
- Frames for pantry-opening animation. Pantries act as unlockable "chests"
  containing various items.
- Various pick-up items: carrot (for vision in dark areas), key (for
  opening doors), tomato (shaped like a heart, to add health).
- Pop-up messages to alert user ("The basement door is locked", "You found
  a carrot!", "Press enter to open").
- Pizza slices which act as a health bar for the chef.

CREDITS:
A* pathing algorithm based off of "Introduction to A" by RedBlobGames
http://www.redblobgames.com/pathfinding/a-star/introduction.html



 ------ OUTDATED -------

game.py -- holds the essential game loop (main function)
driver.py -- holds the code for setup, load, run, and cleanup
MCClass.py -- is the main character class which in this case is the Chef.
rats.py -- is the 'enemy' class
basicState.py -- an abstract "state" class
highScoreScreen.py -- a leaderboard "state" class, contains highschore screen
levelZero.py -- the initial debug level class, contains 5 rats and 1 chef
menuScreen.py -- the menu screen class, can go to game, leaderboard or quit
gameOver.py -- the game over screen triggered when your HP is reduced to 0
, either goes to highscore screen or quits
winScreen.py -- the screen you get when you win the game
 (currently triggered by going in top left corner), goes to highscore screen
  or quits

This is going to be a good game!

Information about Sprites:
 - Chef 2.0
    - chef_*_new.png is the convention for the chef redesign
    - up/down/left/right/idle: 4 frames long, each sprite is 48px x 80px
    - hurt: 6 frames long, each sprite is 48px x 80px
    - attack: 4 frames long, each sprite is 67px x 80px
