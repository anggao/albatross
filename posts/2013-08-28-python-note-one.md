title: "Python Note One"
date: 2013-03-23
tags: python

+ Hexaadecimals and Octals

    >>> 0XAF
    175
    >>> 010
    8

+ Complex number arithmetic
<pre>
>>>import cmath
>>>cmath.sqrt(-1)
1j
>>>(1+3j) * (9+4j)
-3+31j
</pre>

+ `#!/usr/bin/env python`

+ Container consists of sequences and mappings

+ Python has six built-in types of sequence: `lists`, `tuples`, `unicode strings`, `strings`, `buffer objects`, `xrange objects`

+ extracting elements from right to left:
<pre>
>>>numbers[8:3:-1]
[9,8,7,6,5]
</pre>

+ convert between list and string
<pre>
>>>list('Hello')
['H', 'e', 'l', 'l', 'o']
>>>''.join(['H', 'e', 'l', 'l', 'o'])
'Hello'
</pre>

+ `a.extend(b)` can be done by `a[len(a):] = b`

+ `numbers.insert(3, 'four')` can be done in `numbers[3:3]=['four']` 

+ `pop` remove an element (by default the last one) from the list and return it. `pop(0)` remove the first

+ `remove` remove the first occurrence of a value

+ `sorted(cmp, key=None, reverse=False)` 

+ Format specifier: 
    - `%`
    - Conversion flags
        * `-` left alignment
        * `+` a sign should precede the convered value.
        * ` ` a space should precede positive numbers
        * `0` zero padded
    - Minimum field width: if `*` the width will be read from the value tuple
    - `.` followed by precision
    - Conversion type:
        * eg `x` hexadecimal 
        * `'%x' % 42` => 2a

    - Examples:
        * `'%10f' % pi` => `  3.141593`
        * `'%10.2f' % pi` => `      3.14`
        * `'%.2f' %pi` => `3.14`
        * `'%.5s' % 'Ang Gao'` => `'Ang G'`
        * `'%.*s' % (5, 'Ang 'Gao')` => `'Ang G'`
        * `'%010.2f' % pi` => `0000003.14`
        * `'%-10.2f' % pi` => `3.14      `

+ String translate: only works with single character
<pre>
>>>from string import maketrans
>>>table = maketrans('cs', 'kz')
>>>len(table)
256
>>>str1.translate(table)
</pre>
optional second argument can be supplied to translate,
specifying letters that should be delete: `text.translate(table, 'ab')`


+ String translate in PY3
<pre>
>>>str1.translate({ord('t'):ord('x')})
</pre>

+ String formatting with dict: `'%('))le)s' % {'title':'Ang'}`

+ dict methods
    - copy(): shallow copy
    - deep copy: `from copy import deepcopy` `dc = deepcopy(dit)`
    - fromkeys: create new dict with the given keys
        * `{}.fromkeys(['name', 'age'])`
        * `dict.fromkeys(['name', 'age'])`
        * `dict.fromkeys(['name', 'age'], 'unknown')`
    - get: return None if key not exists or supply default value
        * `names.get('name', 'default')`
    - pop(key): get value, remove key-value pair
    - popitem(): pops off an arbitrary item (key, value)
    - setdefault: similar to get retrieve a value associate with a key, sets the value corresponding
        to the given key if it is not in dict

+ In PY3: `a,b,*rest = [1,2,3,4]`

+ `chr(ord('a')) = 'a'`

+ `name = raw_input('Name ') or 'unknown'` 

+ `assert expression [, msg]`

+ else clauses in loop:
<pre>
for x in range(10):
    if x == 5:
        break
else:
    print 'only called if loop completed without break'
</pre>

+ `exec` VS `eval`
<pre>
>>>scope = {}
>>> exec 'sqrt = 1' in scope
>>> scope.keys()
['__builtins__', 'sqrt']
</pre>

`eval(raw_input(...))` has same effect as `input(..)`

+ `callable(x)` in PY3 `hasattr(x, '__call__')`

+ scoping
    - vars()
        * without argument = `locals()`
        * with argument = `object.__dict__`
    - globals(): a dict with the global vars

+ change global var
<pre>
x = 1
def change_global():
    global x
    x = x + 1
</pre>

+ A function that stores its enclosing scope is called a **closure**. Normally cannot 
rebind var in outter scope, in PY3 the keyword **nonlocal** is introduced. It is used
in much the same way as **global**, and lets you assign vars in outter but none global scopes

+ `map`, `filter`, `reduce` moved to `functools` module
