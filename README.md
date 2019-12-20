# Project Wintermute - prototype

## 12/20/19

Wintermute is a learning Agent whose goal is to successfully play Final Fantasy. Final Fantasy is the progenitor of the role playing game.
No remotely-publicized attention has been given to the challenge of creating a learning agent to play RPGs. This is a shame, because
RPGs contain both the thought processes required for true intelligence: Long term planning and execution and the ability to derive a goal
through generalized analysis of available information.

This is the first prototype of Wintermute, the system which will actually be playing the game. Wintermute prototype will start with the Temple of Fiends
(the first dungeon of the game as well as the initial reward point) in sight. It will then use Dynamic programming policy improvement to make its way to the Reward
When it is attacked, it will need to know that it is under attack. If it comes under attack, it will run. Handling a combat strategy will be next step after
Cowardly approach is working.

At time of posting, contains the emulation layer, which runs in python 2.7 and consists of the Nintaco API, a file named actuation which connects to the API, gets the pixels at an externally
determined interval and encodes these pictures to a kafka topic, `emulator_to_environment`.

On other side of topic is a python 3 consumer. This consumer takes the raw data and formats it in a 15 x 13 matrix of 16 x 16 pixel grid squares.

Next step is to flesh out agent/environment interactions. Worth noting that there are all sorts of hacky bullshit methods to get to the Temple, but none will matter
without the ability to recognize that the character is in a fight. Requires a simple perception function, but have not contemplated the details of that.

I also need to actually code the gridworld playing agent. I think this will probably mean re-examining each of its rules and determining what that action flow should be
