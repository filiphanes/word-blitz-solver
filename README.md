# Word-blitz facebook game solver

1. When game is opened, open Developer tools for game iframe https://developer.mozilla.org/en-US/docs/tools/Working_with_iframes
2. paste to console script from file `solver.js`
3. start python solver server `python3 solver.py`
4. then for each game run in browser console `solve()`,
   you need to set exact mouse position of first letter field from game in file `solver.py`
5. if you want to alsa collect new words, after game click on All words and run in console `addWords()`, they will be used in next `solve()` command

Inspired by https://github.com/taixhi/wordblitz
- but improved performance using Trie data structure for dictionary
- and automating mouse movements

Happy winning.
