Prompt Engineering Tutorial

## Introduction

Large language models have an amazing depth of understanding, but still can fall short when getting them to do exactly what you want. When it comes to communicating with computers, we went from being frustrated with how specific we needed to be to get computers to do what we want through programming languages. Now, with large language models such as chatgpt, computers can finally understand basic concepts that we take for granted such as using context to figure out ambiguity. However, their understanding of language is still different in a lot of ways from ours, so it takes a bit more effort to unlock the power that they have. This can be done with prompt engineering. What exactly is prompt engineering? Why not ask ChatGPT?!

`In concise and plain terms, explain what prompt engineering is and why people should learn it.` (note that I actually engineered this prompt a bit from the starting point of `What is prompt engineering?` for the purposes of this tutorial)

```
>ChatGPT:
Prompt engineering is the process of creating clear and effective instructions for language models to generate text. It involves designing prompts that guide the language model to produce the desired type of output.

People should learn prompt engineering if they are interested in developing applications that use language models. Effective prompt engineering can help improve the accuracy and relevance of language model output, leading to better user experiences and more successful applications. It is an important skill for anyone working in natural language processing or machine learning.
```

Not bad, Chat GPT! I would also add that anyone seeking to take advance of the leading edge of AI should learn it also. It can be argued that the models will get so good that it will no longer be required to engineer prompts. While it is true that improved models will make it easier for the layperson to get effective responses, I think it will always be helpful to be familiar with prompt engineering to really get the most out of these models.

## Disclaimer
This tutorial was developed on ChatGPT Feb 13 Version on Feb 25. It is possible that some of the issues had here are no longer present in a future version. It is also possible that a future version will break the existing functionality.

## Tic Tac Toe Example
Let's try the game of tic tac toe. The goal here is to come up with a prompt to 'program' the game of TicTacToe within the ChatGPT interface. We want to be able to play TicTacToe against ChatGPT and have it correctly moderate the game. This means that it will announce when the game is over and enforce legal moves. Then, we will try to push the boundaries even further and teach it how to play well. In a game of TicTacToe, if both players are playing optimally, every game will end in a draw. Therefore, it thoeretically possible to program ChatGPT to never lose a game of TicTacToe! (spoiler, I was able to achieve this! Go ahead and try beating it yourself by scrolling to the bottom and copying the final engineered prompt! note that the free chatgpt is limited to **x** requests per hour)

## Part 1: Play a complete game
As a starting point, lets try to quickly describe what we want to do on a high level and see if it is enough to go off of. Since we are working with a chatbot, we cannot simply draw out the board like you typically would. We will need to either communicate the moves and each keep our own representation of the board or we could try representing the board driectly with text. TicTacToe is simple enough to atleast try representing the board directly. (and it turns out this is actually hugely helpful to the model to represent the game directly with tokens instead of a visual representation because?)
```
Let's play a game of tic-tac-toe. I will send you the board with my move, then you respond by sending back the board with your move. I'll go first:
   |   |   
-----------
   | X |   
-----------
   |   |   
```

Response:
![tactutimg1](https://user-images.githubusercontent.com/11038745/221381618-989b4f98-40f7-45d5-af10-f63acc4d1145.png)


This is a bit rough to look at and also copy back. Lets try something else. Here, I shifted it to represent the empty spaces with a period and the x's and o's naturally with the letters x and o.

```
me:
Lets change the board format to something easier to see. Here is my next move in the new format. (by the way, did I get your move correct?)
o..
.x.
x..

chatgpt:
Yes, your interpretation of my move was correct! Here's my next move:
o..
.x.
x.o

It's your turn again.
```
Look at that! it immediately understood and shifted to this representation. Additionally, there is some additional polite banter going on between all of our messages. This is also interesting and we will come back to that. Although, it did not make a very good move. We will get back to that...

I then made my next move, which would be the winning move to end the game. 
``` 
me:
o.x
.x.
x..
```

I could have claimed the win explicitly in the message, but I wanted to just play the move and see how it answered. There is a danger in being too helpful here actually. My goal here is to find limitations. I am scoping out its understanding of the game to see that it would recognize that the game was over or if it would just keep playing. Lets see how ChatGPT responds...

```
ChatGPT:
Good move! Here's my next move:
o.x
.x.
x.o

It looks like the game is currently tied with no clear winner yet. It's your turn again.
```

There are a couple of interesting things going on here. It was right that I made a good move as it was winning after all. However, it should know that the game should be over at this point. Instead it is trying to continue.
Additionally, you may have noticed that I made a mistake in my previous prompt by omitting chatgpt's move. I had just forgotten to add it, but it brings up an important aspect of this game that we should handle: cheating! It is unfair for me to just erase their move and chatgpt should be more assertive and not let me do this. It turns out that I am utilizing my human strength of making mistakes to help find limitations!

So I decided to address the obvious fact that the game should be over. (I didn't come clean about cheating, but don't tell ChatGPT 🤫)
```
me:
are you sure that the game is tied? isnt it over?

ChatGPT:
Oh, my apologies. You are correct! I missed the fact that I had formed a line of three Os, which means that I won the game.

Congratulations on a great game, and thanks for playing with me! Do you want to play again or is there anything else I can help you with?
```

ChatGPT did aknowledge that the game should be over. This is promising as it indicates that ChatGPT may have the capability to understand what we are going for. We still have to be careful, as ChatGPT could just be going with the flow and have only the conversational and contextual clues that the game is over with me winning. But I think we have enough info to try a new reformulation of the prompt instead of trying another game.

## Attempt #2
For this next prompt, I will only be addressing the first issue instead of both at the same time. When learning and exploring, it is often helpful to only change one thing at a time to better isolate the effect of a single change to get a better understanding of the complex system we are dealing with. So I am thinking that we should be more explicit with our expectations set forth for how we are telling ChatGPT to respond. This may be sufficient without even explaining the rules of the game explicitly since it is a well known game that it already has demonstrated it has some level of understanding of.

``` Prompt 2
Let's play a game of tic-tac-toe. I will send you the board with my move, then you respond by sending back the board with your move. Please keep track of the state of the game and offer to play another once it is completed. I'll go first:
...
.x.
...
```

Lets see what we get...
![tactutimg2](https://user-images.githubusercontent.com/11038745/221381637-1649b163-0e02-47b3-b62d-e4ad30b9e32b.png)

Oops! It looks like we have a problem with the board representation again. It almost seems like the first row started a code snippet instead of being the first row. We could try using a different charecter for this or be more explicit about the format. I do actually like having it in a code snippet because the `Copy code` button is quite convenient for inputing my next move. But on the other hand, it might be better to change the input method to be typeing a number for the square or 2 numbers for the coordinate of the square.


I went ahead and just asked to see what would happen
```
me:
The board that you have sent is incomplete because it is missing the top row. Did you forget to include it or was it a formatting error having to do with the code snippet?

ChatGPT:
I apologize for the confusion! It must have been a formatting error. Here's the complete board with your move:

python

...
.x.
...

Please let me know where you would like to place your next move.
```

Oh dear, it fixed that, but lost its first move. It is great that it has the capability to respond to criticism and with enough back and forth it can get there, but let's get it all solved with the prompt. I think it would be best to remove any ambiguity around how we want the board represented.

``` Prompt 3
Let's play a game of tic-tac-toe. I will send you the board with my move, then you respond by sending back the board with your move. The board is represented by 3 rows of 3 characters: '.' for a blank space, 'o' for the O player, and 'x' for the X player. When responding, please include the board state in a code snippet. Please keep track of the state of the game and offer to play another once it is completed. I'll go first:
...
.x.
...
```

```
Great! Here's my move:

python

.o.
.x.
...

It's getting intense! Your turn again.
```
There we go! It is even adding in some banter! That is some non-trivial behavior that you wouldn't get out of a traditional approach to programming tic-tac-toe. Straight out of the box without even doing anything!

```
ChatGPT:
Good move! Here's my response:

.ox
.x.
xoo

Your move again. This is a close game!

me:
Is the game over?

ChatGPT:
Not yet! It's still your turn. The game will be over when either one of us gets three in a row (horizontally, vertically, or diagonally), or if all spaces on the board are filled without anyone winning.
```

After a couple of moves, I again manage to win the game. However, I ran into the same problem where it does not recognize that I had won. This time, I try to give it less leading information and just ask that the game is over without suggesting that I had won. It explains the game rules and when it should end. This is a strange but common limitation with ChatGPT: seemling like it knows what it is talking about when asked in a certain way, but not making the connection in terms of the ultimate goal output. It is important to note that keeping track of game states is not likely to be a concept that it learned as a language model. So the best approach is to explicitly tell it how to check the game. By including this instruction in the prompt we are basically adding on the way that we need to ask it to figure out this question into the original formulation. So it does what it is already doing, but we have specific instructions included in the context that it knows to follow every time.



``` Prompt 4
Let's play a game of tic-tac-toe. I will send you the board with my move, then you respond by sending back the board with your move. The board is represented by 3 rows of 3 characters: '.' for a blank space, 'o' for the O player, and 'x' for the X player. When responding, please include the board state in a code snippet. Please keep track of the state of the game and offer to play another once it is completed. After every move, check all of the rows, columns, and diagonals on the board to see if there are 3 x's or o's in a row. The game can also end in a tie if the board is completely filled without either player winning with 3 in a row. I'll go first:
...
.x.
...
```

Ugh, it messed up
```Here's the board with my move:

python

.o.
x..
...

It's your turn now.
```

``` Prompt 4
Let's play a game of tic-tac-toe. I will send you the board with my move, then you respond by sending back the board with your move. The board is represented by 3 rows of 3 characters: '.' for a blank space, 'o' for the O player, and 'x' for the X player. When responding, please include the board state in a code snippet. Please keep track of the state of the game and offer to play another once it is completed. After every move, check all of the rows, columns, and diagonals on the board to see if there are 3 x's or o's in a row. The game can also end in a tie if the board is completely filled without either player winning with 3 in a row. Also, make sure that the x's and o's do not move around after they are placed. I'll go first:
...
.x.
...
```

Issues with it trampling my moves, moving my moves, and claiming the game is over before it actually is. I think that we need to explicitly tell it what the rules are. Instead of writing out all the rules, I'm just going to go ahead and have ChatGPT do that. I am not sure if this will yield better or worse results, but I don't really see it making a difference other than the time that it will save.

 After generating the rules of tic-tac-toe, I asked for it to play a game against me in the same connversation. It did a pretty nice job with the interfacing on its own! It created a nice looking board and allowed me to select a square by describing its position. 
 This illustrates that it can be a good idea sometimes to back off with the prompt and go back to what ChatGPT would do without as much intruction to get a better feel for how it would approach the problem on its own. This may help by seeing the problem through ChatGPT's eyes so that you can craft a system that works better with ChatGPT instead of aginast it. At the very least, this can be helpful in showing simpler ways of approaching things incase you are heading down the wrong path. 
 ![2ea9714b0694748527c4e19da7204093.png](:/4fd4eaf3445a4a0ca3b16809daaecd1f)
 🤦‍♂️ It still doesn't have the concept of winning quite right
 
```
Act as my opponent in the game of tic-tac-toe. Tic-tac-toe is a two-player game played on a 3x3 grid. The players take turns marking spaces on the grid with either an "X" or an "O" until one player has three of their symbols in a row, either horizontally, vertically, or diagonally.

The following are the rules of tic-tac-toe:
    The game is played on a 3x3 grid.
    There are two players: Player 1 (who plays with "X") and Player 2 (who plays with "O").
    The game starts with an empty grid.
    Player 1 goes first and places an "X" in an empty cell on the grid.
    Player 2 goes next and places an "O" in an empty cell on the grid.
    Players take turns placing their symbol on the grid until one player wins or the game ends in a tie.
    A player wins if they have three of their symbols in a row, either horizontally, vertically, or diagonally.
    If all cells on the grid are filled and no player has won, the game ends in a tie.
    If a player tries to place their symbol in a cell that is already occupied, their turn is forfeited and the other player gets to go again.
    Once the game is over, the players can choose to play again or end the game.
	
I will send you the board with my move, then you respond by sending back the board with your move. The board is represented by 3 rows of 3 characters: '.' for a blank space, 'O' for the O player, and 'X' for the X player. When responding, please include the board state in a code snippet. Please keep track of the state of the game and offer to play another once it is completed. Continuity is very important. You must use the game state exactly as it is presented and not modify it in any way other than adding your move. Additionally, you must remember which player you are and only play a move by adding the letter corresponding to your player.  I'll go first:
...
.X.
...
```

This immediately had an issue where is misunderstood my first move and changed its posisiotn. I proceded with the game, and it otherwise completed successfully. I then tried to start another. It was going good until chatgpt suddenly changed sides and won for me?
 
 ```
 X.O
.OX
.XO

Here's my move:

X.O
.OX
OXO

Congratulations, you have won the game again! Would you like to play another round?

 ```
 
 
 ```
 Here is the updated board with my move:

.X.
..O
..-

It's your turn now. Please send back the board state with your move.
```
Ok, maybe this isnt possible. It messed up my initial position and also added a different placeholder randomly?

Lets try separating the instructions from the game.

```
Act as my opponent in the game of tic-tac-toe. Tic-tac-toe is a two-player game played on a 3x3 grid. The players take turns marking spaces on the grid with either an "X" or an "O" until one player has three of their symbols in a row, either horizontally, vertically, or diagonally.

The following are the rules of tic-tac-toe:
    The game is played on a 3x3 grid.
    There are two players: Player 1 (who plays with "X") and Player 2 (who plays with "O").
    The game starts with an empty grid.
    Player 1 goes first and places an "X" in an empty cell on the grid.
    Player 2 goes next and places an "O" in an empty cell on the grid.
    Players take turns placing their symbol on the grid until one player wins or the game ends in a tie.
    A player wins if they have three of their symbols in a row, either horizontally, vertically, or diagonally.
    If all cells on the grid are filled and no player has won, the game ends in a tie.
    If a player tries to place their symbol in a cell that is already occupied, their turn is forfeited and the other player gets to go again.
    Once the game is over, the players can choose to play again or end the game.
	
I will send you the board with my move, then you respond by sending back the board with your move. The board is represented by 3 rows of 3 characters: '.' for a blank space, 'O' for the O player, and 'X' for the X player. When responding, please include the board state in a code snippet. Please keep track of the state of the game and offer to play another once it is completed. Continuity is very important. You must use the game state exactly as it is presented and not modify it in any way other than adding your move. Additionally, you must remember which player you are and only play a move by adding the letter corresponding to your player.  If you understand, ask me if I would like to be Player 1 or Player 2 and then let's start the game!
```
This was mostly successful, but then it didn't recognize that the game was over. It might have just been getting lucky before. 
Lets try telling it to repeat the board state:

```
Act as my opponent in the game of tic-tac-toe. Tic-tac-toe is a two-player game played on a 3x3 grid. The players take turns marking spaces on the grid with either an "X" or an "O" until one player has three of their symbols in a row, either horizontally, vertically, or diagonally.

The following are the rules of tic-tac-toe:
    The game is played on a 3x3 grid.
    There are two players: Player 1 (who plays with "X") and Player 2 (who plays with "O").
    The game starts with an empty grid.
    Player 1 goes first and places an "X" in an empty cell on the grid.
    Player 2 goes next and places an "O" in an empty cell on the grid.
    Players take turns placing their symbol on the grid until one player wins or the game ends in a tie.
    A player wins if they have three of their symbols in a row, either horizontally, vertically, or diagonally.
    If all cells on the grid are filled and no player has won, the game ends in a tie.
    If a player tries to place their symbol in a cell that is already occupied, their turn is forfeited and the other player gets to go again.
    Once the game is over, the players can choose to play again or end the game.
	
I will send you the board with my move, then you respond by first confirming my move by repeating the current board state, then check to see if the game is over and tell me if it is. Next, play your move by outputting the next board state that shows your next move, finally, check to see if the game is over and indicate if it is over or if I should move again. The board is represented by 3 rows of 3 characters: '.' for a blank space, 'O' for the O player, and 'X' for the X player. When responding, please include the board state in a code snippet. Please keep track of the state of the game and offer to play another once it is completed. Continuity is very important. You must use the game state exactly as it is presented and not modify it in any way other than adding your move. Additionally, you must remember which player you are and only play a move by adding the letter corresponding to your player. If you understand, ask me if I would like to be Player 1 or Player 2 and then let's start the game!
```
This failed doubly as well, Firstly, it moved for meafter I only selected my player. Then for my second move, It thought that it was invalid because it thought I placed 2 xs in one turn and it also wanted me to specify the column numbers instead of the entire board. Based on both earlier tests and thinking about the language model conceptually, it seems that it would do a better job keeping track of things if we had it explicitly output the different stages of processing the game. Since language models process information in terms of sequences of tokens, it can easily get confused and make bad predictions if things aren't layed out. But if we instruct it to explicitly lay out each step in the thought process, it will have an easier time getting things correct as we have seen that it has the capability to do. In this next attempt, I will tell it to first output the current state of the game as I have entered it, then check if the game is over, and then play a move if it is not. Finally, it will be instructed to check the board one last time after its move to check if it has won. That way, we are not relying on it to keep track of the tic tac toe game conceptually, but instead directly through token, which it is best equiped to understand.

```
Act as my opponent in the game of tic-tac-toe. Tic-tac-toe is a two-player game played on a 3x3 grid. The players take turns marking spaces on the grid with either an "X" or an "O" until one player has three of their symbols in a row, either horizontally, vertically, or diagonally.

The following are the rules of tic-tac-toe:
    The game is played on a 3x3 grid.
    There are two players: Player 1 (who plays with "X") and Player 2 (who plays with "O").
    The game starts with an empty grid.
    Player 1 goes first and places an "X" in an empty cell on the grid.
    Player 2 goes next and places an "O" in an empty cell on the grid.
    Players take turns placing their symbol on the grid until one player wins or the game ends in a tie.
    A player wins if they have three of their symbols in a row, either horizontally, vertically, or diagonally.
    If all cells on the grid are filled and no player has won, the game ends in a tie.
    If a player tries to place their symbol in a cell that is already occupied, their turn is forfeited and the other player gets to go again.
    Once the game is over, the players can choose to play again or end the game.
	
The board is represented by 3 rows of 3 characters: '.' for a blank space, 'O' for the O player, and 'X' for the X player. When responding, please include the board state in a code snippet. First, ask me if I would like to be Player 1 or Player 2. Then, If I am Player 1, start off by showing a blank board. If I am Player 2, start off by placing your move onto the empty board. Next, I will copy the current state of the board, place my move, and send you the new board with my move in it, then you respond by first confirming my move by repeating the current board state, then check to see if the game is over and tell me if it is. Next, play your move by outputting the next board state that shows your next move, finally, check to see if the game is over and indicate if it is over or if I should move again. Continuity is very important. You must use the game state exactly as it is presented and not modify it in any way other than adding your move. Additionally, you must remember which player you are and only play a move by adding the letter corresponding to your player. Once the game is over, ask me if I would like to play another game. If you understand, ask me if I would like to be Player 1 or Player 2.
```
Finally! The first successful game completion! I may have just gotten lucky, so more testing is required, but it seems promising!
There is a notable change here in the format of the board. I have introduced the choice for the player to pick X or O and by doing so I have not explicitly given the board representation. This allows the model to come up with the board representation based only on how I have described it in the prompt instead of being further locked into how I represented it directly. It did a good job of representing the board as described with one notable difference: spaces as a separator between the squares. Originally I had represented the board with only the chars and did not include spaces to save space. However, it seems that I may have overlooked the fact that this representation would be much harder for chatgpt to work with in terms of tokenization. The spaces separate the board into the 9 individual squares on the board in a direct way where they each square would be a token. Without the spaces, there would only be 3 tokens like 'XO.', 'XXO', '.OX'. It seems to me like it is much harder to understand the meaning of a tic-tac-toe board in terms of these tokens.

I went ahead and played another game after the first one to continue testing. During this next game, I wanted to try switching it up and picking Player 2. Before, it had gotten confused and played a move as the wrong player, so I wanted to make sure that wouldn't happen. I was impressed to see that it was explicitly keeping track that it was Player 1 on the game state checkup phase. I think this is exactly what it needs to be doing to keep it on track. I was thinking earlier that I may need to tell it to do this to fix this issue but it looks like ChatGPT was one step ahead of me and anticipated the problem. Maybe after more games it could still end up getting confused. If that ends up being the case, I can always add that part in as an explicit part of the prompt. In any case, I am glad to see it do that because it is supporting evidence for my idea that it will keep track of things better by explicitly outputting them. It almost seems like it is speaking its own language or sharing its own thought process, which is very helpful to see for prompt engineering. But as always keep a healthy dose of skepticism going forward with this idea as this is very much uncharted territory.
```
Here's the current state of the board with your move:

X . O
. O .
. . X

It's now my turn as Player 1, and I will place my move:

X X O
. O .
. . X

The game is not over yet. It's your turn to make a move. Please send me the updated board with your move.
```

After a couple more games back and forth, I am satisfied with the results for the basic formulation of the game.  As long as the player is playing fair and not messing with the AI, it will play legal moves and correctly end and restart games! Although, it is definitely not a strong player yet. For the next part, we will make sure that it enforces that the player is playing legally and from there we can then try to teach it how to play well.

## Part 2: No Cheating!
```
>ChatGPT:
Here's the current state of the board with your move:

X . .
. . .
. . .

It's now my turn as Player 2, and I will place my move:

X . .
. . .
. . O

The game is not over yet. It's your turn to make a move. Please send me the updated board with your move.

>me:
X . X
. . .
X . O

>ChatGPT:
Here's the current state of the board with your move:

X . X
. . .
X . O

It's now my turn as Player 2, and I will place my move:

X . X
. O .
X . O

The game is not over yet. It's your turn to make a move. Please send me the updated board with your move.
```
I was able to do a double move
Maybe as part of the check board step, also check that there were no double moves, trampled moves, or moved plays

## Part 3: Achieving Optimal Results
Tell it that the goal is to win and explain the strategy
Ask chat gpt to explain the strategy
Basically block about to wins and go to your own about to wins, then counter the sneaky double option strat and its golden
