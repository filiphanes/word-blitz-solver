const results = new Set();

let Trie = function () {
}

Trie.prototype.add = function (word) {
    let node = this;
    for (let c of word) {
        if (!node.hasOwnProperty(c)) node[c] = {};
        node = node[c];
    }
    node[0] = true;
}

Trie.prototype.has_node = function (word) {
    let has = {value: false, subtrie: false}
    let node = this;
    for (let c of word) {
        if (!node[c]) return has;
        node = node[c];
    }
    if (node[0]) {
        has.value = true;
        if (Object.keys(node).length > 1)
            has.subtrie = true;
    } else if (Object.keys(node).length > 0)
        has.subtrie = true;

    return has;
}

function next_character(word, board, row, col) {
    word += board[row * 4 + col];
    const has = dictionary.has_node(word);
    if (has.value && word.length >= 4)
        results.add(word);

    // Don't continue if there are no words with this prefix
    if (!has.subtrie)
        return;

    // Remove visited letter
    board = board.slice();
    board[row * 4 + col] = false;

    const prev_row = row - 1;
    const next_row = row + 1;
    const prev_col = col - 1;
    const next_col = col + 1;

    if (next_row < 4) {
        if (board[next_row * 4 + col]){
            next_character(word, board, next_row, col);
        }
        if (next_col < 4 && board[next_row * 4 + next_col]){
            next_character(word, board, next_row, next_col);
        }
    }
    if (next_col < 4) {
        if (board[row * 4 + next_col]){
            next_character(word, board, row, next_col);
        }
        if (prev_row >= 0 && board[prev_row * 4 + next_col]){
            next_character(word, board, prev_row, next_col);
        }
    }
    if (prev_row >= 0) {
        if (board[prev_row * 4 + col]){
            next_character(word, board, prev_row, col);
        }
        if (prev_col >= 0 && board[prev_row * 4 + prev_col]){
            next_character(word, board, prev_row, prev_col);
        }
    }
    if (prev_col >= 0) {
        if (board[row * 4 + prev_col]){
            next_character(word, board, row, prev_col);
        }
        if (next_row < 4 && board[next_row * 4 + prev_col]){
            next_character(word, board, next_row, prev_col);
        }
    }
}

function solve(board) {
    let bonus;
    results.clear();
    board = [];
    for (let elem of document.getElementsByClassName('core-letter-cell')) {
        let cell = {
            letter: elem.querySelector('.letter').innerHTML.toUpperCase(),
            points: +elem.querySelector('.points').innerHTML,
        }
        bonus = elem.querySelector('.bonus .circle').innerHTML;
        if (bonus[1] == 'P') {
            cell.P = +bonus[0];
        } else if (bonus[1] == 'S') {
            cell.P = +bonus[0];
        }
        board.push(cell);
    }

    let letters = board.map(cell => cell.letter).join('');
    console.log('Solving', letters, board);
    console.log(JSON.stringify(board));
    /*
    console.log(board.map(cell => cell.points).join('') + '\n';
          + board.map(cell => cell.P || 1).join('') + '\n';
          + board.map(cell => cell.S || 1).join('') + '\n';
          + letters + '\n');
    */

    // Send to server
    let http = new XMLHttpRequest();
    http.open("POST", "http://localhost:7777/solve", true);
    http.send(JSON.stringify(board));

    for (let row = 0; row < 4; row++)
        for (let col = 0; col < 4; col++)
            next_character("", board, row, col);

    // sort by length
    let words = [...results];
    words.sort(function (a, b) { return b.length - a.length });
    for (let word of words)
        console.log(word);
}

function addWords() {
    let words = new Set();
    for (let w of document.getElementsByClassName('word')) {
        let word = w.innerHTML.toUpperCase();
        words.add(word);
        // dictionary.add(word);
    }
    console.log([...words].join('\n'));
    let http = new XMLHttpRequest();
    http.open("POST", "http://localhost:7777/addwords", true);
    http.send([...words].join('\n'));
}

let dictionary = new Trie()
for (let word of `ABO`.split('\n')
) {
    dictionary.add(word);
}

/*
letter
.points
.bonus .circle
*/