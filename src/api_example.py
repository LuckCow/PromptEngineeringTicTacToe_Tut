"""
GPTicTacToe Game Loop Code
Use this code to manage the prompts in order to play tictactoe against ChatGPT
CLIPBOARD_MODE = True will copy the prompt to your clipboard so you can paste it into the OpenAI Playground,
CLIPBOARD_MODE = False will use the OpenAI API to execute the prompt automatically
"""

import re

CLIPBOARD_MODE = True
# COMPLETIONS_MODEL = "text-davinci-003"
COMPLETIONS_MODEL = "gpt-3.5-turbo"
# COMPLETIONS_MODEL = "gpt-4"

if CLIPBOARD_MODE:
    import pyperclip
else:
    import openai
    openai.api_key = 'your-key-here'  # make sure you don't commit this to git


prompt_dimension = '''I want you to act as a tic-tac-toe game board analyzer. The tic-tac-toe board is represented by a 3 by 3 grid of characters. Each cell is represented by either ' X' for Player 1's moves, ' O' for Player 2's moves, and ' _' for a blank cell. 

I want you to output the contents of each dimension (meaning row, column, and diagonal). 
The row numbers go from top to bottom. Within each row, the order should be from left to right. The columns numbers go from left to right. Within the column, the letter order goes from top to bottom. Diagonal 1 goes from the top left to the bottom right. This means that it has the top left, middle, and bottom right cells. Diagonal 2 goes from the bottom left to the top right. This means that it has the bottom left, middle, and top right cells. It is important not to mix up the order of the letters within the dimension.

In order to show the contents of the dimensions follow this transformation scheme outlined below. Each cell within the tic-tac-toe board is numbered from 1 to 9 going left to right and top to bottom. Each dimension always contains the letter from the same set of 3 cells shown below. For example, when showing the contents of Diagonal 2, always copy the letters from cell numbers 7, 5, and 3.
Cell Numbers:
 1 2 3
 4 5 6
 7 8 9

These are all of the dimensions and which cell numbers make up each dimension
Row 1: " 1 2 3"
Row 2: " 4 5 6"
Row 3: " 7 8 9"
Column 1: " 1 4 7"
Column 2: " 2 5 8"
Column 3: " 3 6 9"
Diagonal 1: " 1 5 9"
Diagonal 2: " 7 5 3"

For example, given this board to analyze: 
"""
 _ _ _
 X O X
 _ O X
"""

You should copy the cell from each number and fill them in to the corresponding number in the dimension break downs like this:
"""
Dimensions:
Row 1: " _ _ _"
Row 2: " X O X"
Row 3: " _ O X"
Column 1: " _ X _"
Column 2: " _ O O"
Column 3: " _ X X"
Diagonal 1: " _ O X"
Diagonal 2: " _ O _"
"""

Board to analyze:
"""
%s
"""
'''

prompt_count_class = 'Act as an instance counter and classifier. Given a list of dimensions, ' \
                     'count how many time each letter occurs and then classify the dimension based on the counts.' \
                     'Each dimension will have 3 letters outputted from step 1, ' \
                     'and I need you to count how many times each character occurs in that sequence. ' \
                     'There are only 3 characters that are possible in the sequence: " X", " O", and " _". ' \
                     'For example: given the sequence " X X _", the counts should be "X: 2 O: 0 _:1"' \
                     'The classification of this dimension corresponding to these counts: ' \
                     'The four possible classifications are "possible O", "possible X", "open", and "closed".' \
                     ' The "possible O" category means that there are two O\'s and an empty cell and no X\'s. ' \
                     'This means that if the counts are "X:0 O:2 _:1", it will always be in the category "possible O".' \
                     ' The "possible X" for when there are two X\'s and an empty cell and no O\'s. ' \
                     'This means that if the counts are "X:2 O:0 _:1", it will always be in the category "possible O".' \
                     ' The "open" category means that there are one or less X or O within the dimension. ' \
                     'This means that if the counts are of the blank cells are greater than or equal to 2, ' \
                     'it will always be in the category "open". The "closed" category means that there is ' \
                     'at least one X and at least one O. This means that if the counts of both X and O are ' \
                     'greater than or equal to 1, it will always be the "closed" category.\n' \
                     'For example, given these dimensions, you should output the following:\n' \
                     '"""\n' \
                     'Dimensions:\n' \
                     'Row 1: " _ _ _" Counts "X:0 O:0 _:3" Classification: "open"\n' \
                     'Row 2: " X O X" Counts "X:2 O:1 _:0" Classification: "closed"\n' \
                     'Row 3: " _ O X" Counts "X:1 O:1 _:1" Classification: "closed"\n' \
                     'Column 1: " _ X _" Counts "X:1 O:0 _:2" Classification: "open"\n' \
                     'Column 2: " _ O O" Counts "X:0 O:2 _:1" Classification: "possible O"\n' \
                     'Column 3: " _ X X" Counts "X:2 O:0 _:1" Classification: "possible X"\n' \
                     'Diagonal 1: " _ O X" Counts "X:1 O:1 _:1" Classification: "closed"\n' \
                     'Diagonal 2: " _ O _" Counts "X:0 O:1 _:2" Classification: "open"\n' \
                     '"""' \
                     'Output:\n' \
                     '"""\n' \
                     'Dimensions:\n' \
                     'Row 1: " _ _ _" Counts "X:0 O:0 _:3" Classification: "open"\n' \
                     'Row 2: " X O X" Counts "X:2 O:1 _:0" Classification: "closed"\n' \
                     'Row 3: " _ O X" Counts "X:1 O:1 _:1" Classification: "closed"\n' \
                     'Column 1: " _ X _" Counts "X:1 O:0 _:2" Classification: "open"\n' \
                     'Column 2: " _ O O" Counts "X:0 O:2 _:1" Classification: "possible O"\n' \
                     'Column 3: " _ X X" Counts "X:2 O:0 _:1" Classification: "possible X"\n' \
                     'Diagonal 1: " _ O X" Counts "X:1 O:1 _:1" Classification: "closed"\n' \
                     'Diagonal 2: " _ O _" Counts "X:0 O:1 _:2" Classification: "open"\n' \
                     '"""' \
                     'Now give the counts and classifications for these dimensions:\n' \
                     '"""\n' \
                     '%s\n' \
                     '"""'

prompt_pick_move = 'Act as a decision maker for tic-tac-toe game. ' \
                   'Given a the player whose turn it is and a breakdown of each dimension on the tic-tac-toe' \
                   ' board and its classification, pick the best dimension to make a move in based on ' \
                   'this priority system using the classification. The best dimension is determined by ' \
                   'following this simple priority system. First, check if there is a "possible" win in for ' \
                   'the player from the prompt. This means if the player being asked about is "X", "possible X" is' \
                   ' the priority over "possible O" for the number one priority. Conversely, if the prompt is for ' \
                   'Player O, then "possible O" is the priority over "possible X" for the number one priority. ' \
                   'If there is, make a move in the blank cell in this dimension to win the game. ' \
                   'Next, check if there is a "possible" win for the other player. If there is, then make a move in' \
                   ' this column in order to block the other player from winning (but only if you cannot win yourself).' \
                   ' If there are none of these categories, then move in the first available "open" dimension. ' \
                   'Finally, if no other options are available, ' \
                   'make a move in the first empty cell within a "closed" dimension.' \
                   ' Once you have selected the single best dimension to move in, you must select the number of the' \
                   ' blank cell in that dimension that the move will be in. Output that information in the ' \
                   'format after replacing the square bracket placeholders with the actual information: ' \
                   '"Best Move for Player [X or O]: Category: [selected category], Dimension: [best dimension], ' \
                   'Cell: #[1, 2, or 3], Coordinate: ([row], [column])."' \
                   '\n\n' \
                   'The next step is to reconstruct the board based on the dimensions. Just copy the contents of ' \
                   'Row 1, Row 2, and Row 3. Only copy the contents part of the board which is the part in quotes ("). ' \
                   ' Then, place the best move you selected by replacing the blank cell ' \
                   'at the coordinates specified with the letter corresponding to the player whose turn it is. ' \
                   '\n' \
                   'Now pick the best move for Player %s with these dimensions:\n' \
                   '%s'

prompts = [prompt_dimension, prompt_count_class, prompt_pick_move]


def make_move(board, player):
    """ Send a series of prompts back and forth to chatgpt to select the next move to run """
    print('Player %s' % player)
    print(board)
    # first, break board into dimensions
    dimensions = ask_gpt(prompt_dimension % board)
    print(dimensions)

    # then, count letter occurrences and classify each dimension
    classifications = ask_gpt(prompt_count_class % dimensions)
    print(classifications)

    # finally, select the best move and output the resulting board
    result = ask_gpt(prompt_pick_move % (player, classifications))
    print(result)

    # parse board from results
    # TODO: better error checking incase it gives a wonky format
    board = '\n'.join(m.group(2) for m in re.finditer(r'(Row \d: )?"?( [_OoXx] [_OoXx] [_OoXx])"?', result))
    print(board)
    return board


def ask_gpt(prompt):
    if not CLIPBOARD_MODE:
        # Run through API
        # possible roles: system, user, assistant
        conversation = [{'role': 'user', 'content': prompt}]

        resp = openai.ChatCompletion.create(
            # prompt=prompt,
            messages=conversation,
            temperature=0,
            max_tokens=2048,
            # presence_penalty=-1.0,
            # frequency_penalty=1.0,
            model=COMPLETIONS_MODEL
        )

        # print(resp["choices"][0]["text"].strip(" \n"))
        return resp.choices[0].message.content

    else:
        # Prompt mode: use clipboard and external website instead of direct to API

        print(prompt)

        # Copy prompt into clipboard
        pyperclip.copy(prompt)

        _ = input('The prompt is copied to your clipboard. Please paste it into ChatGPT and then copy its response '
                  'and then type anything to continue to the next step: ')

        # Copy ChatGPT's response
        res = pyperclip.paste()

        return res


if __name__ == '__main__':
    make_move(""" _ O _
     _ O X
     _ X X""", 'O')

    make_move(""" _ O _
     _ X _
     X _ _""", 'O')

    make_move(""" _ O _
     _ X _
     X _ _""", 'O')

    make_move(""" _ O O
     _ X _
     X _ X""", 'O')

    make_move(""" _ O O
     _ X _
     X O X""", 'X')

    make_move(""" _ O O
     _ _ _
     X _ X""", 'X')

# Test results: --------------------------
test_inputs = [""" _ O _
 _ O X
 X X _
 """,
               'Dimensions:\n' \
               'Row 1: " _ O _"\n' \
               'Row 2: " _ O X"\n' \
               'Row 3: " X X _"\n' \
               'Column 1: " _ _ X"\n' \
               'Column 2: " O O X"\n' \
               'Column 3: " _ X _"\n' \
               'Diagonal 1: " _ O _"\n' \
               'Diagonal 2: " X O _"\n',
               'Counts and Classifications:\n' \
               'Row 1: " _ O _" Counts "X:0 O:1 _:2" Classification: "open"\n' \
               'Row 2: " _ O X" Counts "X:1 O:1 _:1" Classification: "closed"\n' \
               'Row 3: " X X _" Counts "X:2 O:0 _:1" Classification: "possible X"\n' \
               'Column 1: " _ _ X" Counts "X:1 O:0 _:2" Classification: "open"\n' \
               'Column 2: " O O X" Counts "X:1 O:2 _:0" Classification: "closed"\n' \
               'Column 3: " _ X _" Counts "X:1 O:0 _:2" Classification: "open"\n' \
               'Diagonal 1: " _ O _" Counts "X:0 O:1 _:2" Classification: "open"\n' \
               'Diagonal 2: " X O _" Counts "X:1 O:1 _:1" Classification: "closed"\n',
               """Best Move for Player O: Category: possible X, Dimension: Row 3, Cell: #3, Coordinate: [(3, 3)].
           
           Reconstructed Board:
           Row 1: " _ O _"
           Row 2: " _ O X"
           Row 3: " X X O"
           """
               ]

# test #1
"""
Player O
 X X _
 _ O O
 _ X _
"""
"""
Dimensions:
Row 1: " X X _" Counts "X:2 O:0 _:1" Classification: 'possible X'
Row 2: " _ O O" Counts "X:0 O:2 _:1" Classification: 'possible O'
Row 3: " _ X _" Counts "X:1 O:0 _:2" Classification: 'open'
Column 1: " X _ _" Counts "X:1 O:0 _:2" Classification: 'open'
Column 2: " X O O" Counts "X:1 O:2 _:0" Classification: 'closed'
Column 3: " _ X _" Counts "X:1 O:0 _:2" Classification: 'open'
Diagonal 1: " X O _" Counts "X:1 O:1 _:1" Classification: 'closed'
Diagonal 2: " _ O X" Counts "X:1 O:1 _:1" Classification: 'closed'

Best Move for Player O: 
(2, 3) Because Columns 2 is classified as 'possible O'

Resulting Board:
 X X O
 _ O O
 _ X O
"""

# test #2
"""
Dimensions:
Row 1: " X X _" Counts "X:2 O:0 _:1" Classification: 'possible X'
Row 2: " _ O O" Counts "X:0 O:2 _:1" Classification: 'possible O'
Row 3: " _ X _" Counts "X:1 O:0 _:2" Classification: 'open'
Column 1: " X _ _" Counts "X:1 O:0 _:2" Classification: 'open'
Column 2: " X O O" Counts "X:1 O:2 _:0" Classification: 'closed'
Column 3: " _ X _" Counts "X:1 O:0 _:2" Classification: 'open'
Diagonal 1: " X O _" Counts "X:1 O:1 _:1" Classification: 'closed'
Diagonal 2: " _ O X" Counts "X:1 O:1 _:1" Classification: 'closed'

Best Move for Player O: 
(2, 1) Because Row 2 is classified as 'possible O'

Resulting Board:
 X X _
 O O O
 _ X _
 """

# davinci
"""

Dimensions:
Row 1: " _ O _"
Row 2: " _ O X"
Row 3: " X X _"
Column 1: " _ _ X"
Column 2: " O O X"
Column 3: " _ X _"
Diagonal 1: " _ O _"
Diagonal 2: " X O X"
"""

# Turbo
"""Dimensions:
Row 1: " _ O _"
Row 2: " _ O X"
Row 3: " X X _"
Column 1: " _ _ X"
Column 2: " O O X"
Column 3: " _ X _"
Diagonal 1: " _ O _"
Diagonal 2: " X O _" 
"""