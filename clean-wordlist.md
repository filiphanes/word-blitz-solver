```python
import re
s = set()
with open('prim-9.0-public-all-word_frequency.txt') as f:
    s = f.read().lower()

for m in re.finditer(r'^([a-záäčďéíľľňóôŕšťúýž]+){2,12}\s', s):
    s.add(m.group(1))

for w in sorted(m.group(1) for m in re.all(r'^([a-záäčďéíľľňóôŕšťúýž]{2,12})\s', s)):
    print(w)
```

```sh
time head -n 200000 prim-9.0-public-all-word_frequency.txt | ack "^([a-záäčďéíľľňóôŕšťúýž]{2,12})\s" - --output '$1' | PERLIO=:utf8 perl -pe '$_=uc' > SK.txt
```

Get words from word-blitz iframe
```js
words = new Set();
for (let w of document.getElementsByClassName('word')) {
	words.add(w.innerHTML.toUpperCase());
}
[...words].join('\n');


letters = '';
for (let l of document.getElementsByClassName('letter')) {
	letters += l.innerHTML.toUpperCase()
}
// letters
```

