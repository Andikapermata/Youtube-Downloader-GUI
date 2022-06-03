# Youtube-Downloader-GUI
Youtube Downloader using GUI Framework Tkinter

####  Requirement
- Python 3
    - pytube
    - pillow

## Fix Error on Pytube
Change at chiper.py on module pytube line 30
From
```python
var_regex = re.compile(r"^\w+\W")
```
To
```python
var_regex = re.compile(r"^\$*\w+\W")
```
