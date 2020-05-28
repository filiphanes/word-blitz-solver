#!/usr/bin/env python3

from pygtrie import CharTrie
import copy
import pyautogui
import json
from collections import namedtuple
import http.server

x0 = 71
y0 = 417

Cell = namedtuple('Cell', ['letter', 'points', 'P', 'S'])

class Solver:
    def __init__(self, cells, dictionary=None):
        self.cells = [Cell(
            c['letter'],
            c.get('points', 1),
            c.get('P', 1),
            c.get('S', 1),
            ) for c in cells]
        self.letters = [c['letter'] for c in cells]
        self.candidates = {}  # word => (positions, value)
        self.dictionary = dictionary
        if not dictionary:
            self.dictionary = CharTrie()
            print('Loading custom words ... ', end="")
            with open('SK-custom.txt') as f:
                self.dictionary.update((w, True) for w in f.read().splitlines())
                print(len(self.dictionary))

    def word_value(self, visited):
        val = 0
        S = 1
        for pos in visited:
            cell = self.cells[pos]
            val += cell.points * cell.P
            S *= cell.S
        return val * S

    def next_char(self, visited, pos):
        visited = visited + (pos,)
        word = ''.join((self.letters[p] for p in visited))
        has = self.dictionary.has_node(word)
        if has & CharTrie.HAS_VALUE:
            newval = self.word_value(visited)
            if self.candidates.get(word, (None, 0))[1] < newval:
                self.candidates[word] = (visited, newval)
            # print(word)

        # Don't continue if thera are no words with this prefix
        if not has & CharTrie.HAS_SUBTRIE:
            return

        row = pos // 4
        col = pos % 4
        prev_row = row - 1
        next_row = row + 1
        prev_col = col - 1
        next_col = col + 1

        if next_row < 4:
            # Adds the charcter S the current pos
            pos = next_row * 4 + col
            if pos not in visited:
                self.next_char(visited, pos)
            #Adds the character SE the current pos
            pos = next_row * 4 + next_col
            if next_col < 4 and pos not in visited:
                self.next_char(visited, pos)

        if next_col < 4:
            # Adds the charcter E of the current pos
            pos = row * 4 + next_col
            if pos not in visited:
                self.next_char(visited, pos)
            #Adds the character NE the current pos
            pos = prev_row * 4 + next_col
            if prev_row >= 0 and pos not in visited:
                self.next_char(visited, pos)

        if prev_row >= 0:
            # Adds the charcter N the current pos
            pos = prev_row * 4 + col
            if pos not in visited:
                self.next_char(visited, pos)
            # Adds the charcter NW of the current pos
            pos = prev_row * 4 + prev_col
            if prev_col >= 0 and pos not in visited:
                self.next_char(visited, pos)

        if prev_col >= 0:
            # Adds the charcter W of the current pos
            pos = row * 4 + prev_col
            if pos not in visited:
                self.next_char(visited, pos)
            # Adds the charcter SW of the current pos
            pos = next_row * 4 + prev_col
            if next_row < 4 and pos not in visited:
                self.next_char(visited, pos)

    def solve_and_swipe(self):
        for pos in range(0, 16):
            self.next_char((), pos)

        # sort by length
        pyautogui.moveTo(x0, y0, duration=0.1)
        pyautogui.click(duration=0.1)
        for word, visited_val in self.candidates.items():
            print(word, visited_val[1])
            self.swipe(visited_val[0])

    def swipe(self, positions):
        grid = 94
        pos = positions[0]
        pyautogui.moveTo(x0 + (pos % 4) * grid, y0 + (pos // 4) * grid, duration=0.1)
        pyautogui.mouseDown(button='left', logScreenshot=False, _pause=False, duration=0.1)
        for pos in positions[1:]:
            pyautogui.moveTo(x0 + (pos % 4) * grid, y0 + (pos // 4) * grid, duration=0.1)
        pyautogui.mouseUp(button='left', logScreenshot=False, _pause=False, duration=0.1)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print('POST', self.path, body)

        if self.path == '/solve':
            cells = json.loads(body)
            solver = Solver(cells)
            solver.solve_and_swipe()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b'')

        elif self.path == '/addwords':
            with open('SK-custom.txt', 'ba') as f:
                f.write(body)
                f.write(b'\n')

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Request: %s" % self.path.encode())


if __name__ == "__main__":
    # input("Leave mouse in center of first letter and press enter\n")
    # x0, y0 = pyautogui.position()
    print('Mouse position', pyautogui.position())
    print('First cell at', (x0, y0))

    PORT = 7777
    with http.server.HTTPServer(('localhost', PORT), Handler) as httpd:
        print(f"Server started http://localhost:{PORT}")
        httpd.serve_forever()
    print("Server stopped.")

    while True:
        inp = input("type table:\n")
        if inp.strip().startswith('['):
            solver = Solver(json.loads(inp))
        else:
            inp = inp[:16]
            solver = Solver([Cell(letter, 1, 1, 1) for letter in inp])
        solver.solve_and_swipe()
