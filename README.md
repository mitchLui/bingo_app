# Mark Six

**This project was originally a commission but project was abandoned by client. Further development might take place but is unlikely.**

A Python app for playing a variation of the Mark Six game.

---

## Build from Source

Requirements are listed in requirements.txt

Prerequisites include python 3.8 or above.

```sh
cd bingo_app
pip install -r requirements.txt
pyinstaller build_app.spec
```

---

## Modules

```txt
.
├── app.py
├── app_backend.py
├── bingo_sheet.py
├── database.py
├── game.py
└── tickets.py
```
| Filename          | Description                                                 |
| ----------------- | ----------------------------------------------------------- |
|`app.py`           | Main application, built using [DearPyGui][1]                |
|`app_backend.py`   | Backend for application, handles interaction and callbacks  |
|`bingo_sheet.py`   | Handles data formatting before passing to `tickets.py`      |
|`database.py`      | Handles database functions                                  |
|`game.py`          | Actual game mechanism, probability generation etc           |
|`tickets.py`       | Creates tickets in the form of PDFs                         |

---

[1]:https://github.com/hoffstadt/DearPyGui
