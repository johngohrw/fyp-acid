# fyp-acid: Automatic Compound Image Detection
[Live Prototype Website](https://johngohrw.github.io/fyp-acid/) (requires web-server running on background)

[Git repository for front-end component](https://github.com/johngohrw/fyp-acid-fe)

## Dependencies
We recommend using `pip` to install the necessary Python modules.
Command for installing dependencies below are prefixed with `pip install`:
  * Flask 
  * imutils
  * matplotlib
  * opencv-python
  * Pillow
  * pytesseract
  * scikit-learn
  * scikit-image

The Optical Character Recognition (OCR) module of our project depends on the
Tesseract OCR engine v4.0 with LSTM. 
See their Github [wiki](https://github.com/tesseract-ocr/tesseract/wiki) 
for installation instructions.

## Starting the web app
Run the web server:
```
python app.py
```
or
```
python3 app.py
```
The front end can be accessed [here](https://johngohrw.github.io/fyp-acid/) after successfully running the web-server.
