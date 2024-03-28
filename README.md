# גְלֶבָּה

מחלקות עזר לפי-גיים

![גיף מוזר](https://github.com/Rotlug/Gleba/blob/master/weird.gif?raw=true)
## איך משתמשים???
כל אובייקט בגלבה הוא "חוליה" (Node)

כדי להתחיל:
```python
from gleba import *

window = Window(
    size=Point(600, 800),
    fps=30
)

window.run()
```
עכשיו יש חלון :)

גם החלון עצמו הוא חוליה: חוליה היא עצם עם רשימה של ילדים

אפשר להוסיף לחלון ילד, לדוגמה מלבן
```python
rect = Rect(
    size=Point(64, 64),
    position=Point(0, 0),
    color=(255, 0, 0)
)

window.add_child(rect)
```
## כותבים

- [DJ רותם](https://www.github.com/rotlug)

