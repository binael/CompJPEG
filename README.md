# CompJPEG - JPEG Image Compresser

A commandline program that uses discreet cosine transfrom (DCT) to implement lossy compression of JPEG images. This program only compresses JPEG images with RGB color channels. A command interpreter is created to manage objects for the CompJEG program

#### Goals of the Project: 
* Decompose each phase of JPEG image compression into simple programs with scarce use of libraries
* Create a simple command line tool that can compress images and store details of the compressed files
* Satisfy ALX Africa requirement as a software engineering student

#### Functionalities of the command line interpreter
* compress image(s) from stdin, json files, text files and directory
* show the details of the compressed image
* display the compressed image
* delete the compressed image

---

## Table of Content
* [Environment](#environment)
* [Getting Started](#getting-started)
* [Command Description](#command-description)
* [Example](#example)
* [Authors](#authors)
* [License](#license)

## Environment
This project was interpreted and tested on Ubuntu 20.04 using python3 (version 3.10)

## Getting Started
1. Clone the project repository
```
	https://github.com/binael/CompJPEG.git
```
2. Access the repository
```
	cd CompJPEG
```
3. This stage is where a python virtual environment for the project is created. Note that an virtual environment has already been created and if you want to use it, you can skip this step
```
	python3 -m venv .venv
```
4. Activate the python virtual environment. The below step will work if you use the already created virtual environment or created one with (step 3)
```
	source project_env.sh
```
If above did not create a virtual environment, run the below:
```
	source .venv/bin/activate
```
5. Install the requirements for the program
```
	./build.sh
```
6. Run setup to ensure all imports are functional
```
	pip install -e .
```
The environment is all set up
7. You can start run the program in either interactive or non-interactive mode
	- Interactive mode
	```
		./main.py
	```
	- Non-interactive mode
	```
		echo "<command>" | ./main.py
	```

## Command Description
#### Note that all inputs and options to any command must be a key value pair, else the command returns an error. Check usage of each command for more information

### 1 `show id=<image id> mode=<option>`
Opens a window to display the image file requested by the user
* _Parameters for show command_:
	- id [default='<last compressed image id>']: <image id>
	- mode [default='compressed']: 'compressed' or 'compare' or 'original'

`show id=<image id> mode=<option>` Displays the image having mode of the chosen image id

`show mode=<option>` Displays the mode of the last compressed image

`show id=<image id>` Displays only the compressed image with the given id
`show` Displays only the last compressed image

2. `delete` : Deletes the stored object detail for each image with option to delete the compressed image
#### Parameters for delete command
	id : <image id> or 'all'
	remove [default=true]: 'true' or 'false
#### USAGE1:
`delete id=<id> remove=<option>` Removes the given id or all id objects in database, and the compressed image files if remove is true
#### USAGE2:
`delete id=<id>` Removes the given id or all id objects in database with their compressed image files
#### USAGE3:
`delete` Removes the last compressed image object and its image file
#### USAGE3:
`delete remove=<option>` Removes
