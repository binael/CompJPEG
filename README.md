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
* [Examples](#examples)
* [Authors](#authors)
* [License](#license)

## Environment
This project was interpreted and tested on Ubuntu 20.04 using python3 (version 3.10)

## Getting Started
1. Clone the project repository
```
	git clone https://github.com/binael/CompJPEG.git
```
2. Access the repository
```
	cd CompJPEG
```
3. This stage is where a python virtual environment for the project is created. Note that a virtual environment has already been created and if you want to use it, you can skip this step
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
	- Interactive mode: `./main.py`
	- Non-interactive mode:  `echo "<command>" | ./main.py`

## Command Description
#### Note that all inputs and options to any command must be a key value pair, else the command returns an error. Check usage of each command for more information
### 1. `show id=<image id> mode=<option>`
Opens a window to display the image file requested by the user
* _Parameters for show command_:
	- `id [default=<last compressed image id>] : <image id>`
	- `mode [default='compressed'] : 'compressed' or 'compare' or 'original'`
* _Usages for show command_:
	- `show id=<image id> mode=<option>` Displays the image having mode of the chosen image id
	- `show mode=<option>` Displays the mode of the last compressed image
	- `show id=<image id>` Displays only the compressed image with the given id
	- `show` Displays only the last compressed image

### 2. `delete id=<id> remove=<option>`
Deletes the stored object detail for each image with option to delete the compressed image
* _Parameters for delete command_:
	- `id [default=<'last compressed image id'>]: <image id> or 'all'`
	- `remove [default=True]: True or False`
* _Usages for delete command_:
	- `delete id=<id> remove=<option>` Removes the given id or all id objects in database, and the compressed image files if remove is true
	- `delete id=<id>` Removes the given id or all id objects in database with their compressed image files
	- `delete` Removes the last compressed image object and its image file
	- `delete remove=<option>` Removes the last compressed image object and the compressed image file if option is True

### 3. `detail id=<id>`
Shows the details (like size, resolution, id, compression time etc) of the compressed image file(s)
* _Parameters for detail command_:
	- `id [default=<'last compressed image id'>]: <image id> or 'all'`
* _Usages for detail command_:
	- `detail id=<image id>` Shows the detail of the object with the given image id
	- `detail id=all` Shows the details of all compressed objects in the database
	- `detail` Shows the detail of the last compressed file object

### 4. `compress "path=<image path1> quality=<int>" "path=<"image path2> quality=<int> ...`
Takes up input details from standard input (stdin) and compresses the image file(s) with the desired quality
* _Parameters for compress command_:
	- `path : <image path name>`
	- `quality : <int>`
* _Usages for compress command_:
	- `compress "path=<image path1> quality=<int>" "path=<"image path2> quality=<int> ...` Note that each detail of files to compress must be in quote to separate from the next detail

### 5. `compressFiles type=<option> path=<file path>`
Takes input details from files or directories and compresses the image file(s) with the quality. Note that directory paths have default quality of 50
* _Parameters for compressFiles command_:
	- `type : 'json' or 'text' or 'directory'`
	- `path : <image path>`
* _Usages for compressFiles command_:
	- `compressFiles type=<option> path=<file path>` Compresses all the image files found in the given directory or the file
* _Example for accepted format for json and text file details_:
	- [`Text File Example`](./example/example_text.txt)
	- [`Json File Example`](./example/example_json.json)

### 6. `help <command>`
Shows the list of valid commands or the detail of the chosen commands
* _Usages for help command_:
	- `help` Shows the list of all valid command for the program
	- `help <command>` command options: 'show' or 'compress' or 'compressFiles' or 'detail' or 'delete'

## Examples
```
(.venv) root@root:~/CompJPEG$ ./main.py
(CompJPEG) help

Documented commands (type help <topic>):
========================================
EOF  compress  compressFiles  delete  detail  help  quit  show

(CompJPEG) detail
ERROR: No image id found
(CompJPEG) compressFiles type=text path=./example/example_text.txt
(CompJPEG) detail
         Image ID: mountain-e56cf50f.jpeg
         Resolution: 320 X 180
         Time Taken: 0m:0s
         Quality: 55
         | ORIGINAL   | COMPRESSED
----------------------------------------------
    Name | mountain.jpeg | mountain-e56cf50f.jpeg
----------------------------------------------
    Size | 16.4KB     | 10.2KB
----------------------------------------------

(CompJPEG) detail id=landscape-881b0212.jpg
         Image ID: landscape-881b0212.jpg
         Resolution: 612 X 408
         Time Taken: 0m:1s
         Quality: 60
         | ORIGINAL   | COMPRESSED
----------------------------------------------
    Name | landscape.jpg | landscape-881b0212.jpg
----------------------------------------------
    Size | 49.2KB     | 43.8KB
----------------------------------------------

(CompJPEG) delete id=landscape-881b0212.jpg remove=True
(CompJPEG) detail id=landscape-881b0212.jpg
ERROR: Could not found object with id:	landscape-881b0212.jpg
(CompJPEG) help show

        Pulls out a window showing the image file requested
        by the user

        USAGE: show id=image_id mode=[ compressed | original | compare ]
        USAGE: show mode=[ compressed | original | compare ]
        USAGE: show id=image_id
        USAGE: show

        Arguments
        ---------
        id : [default=last_object]
            The id of the image that was compressed
        mode : [default=compressed]
            Must be a key-value pair that shows the image to
            display
            compressed:
                displays the compressed image of the given image_id
            compare:
                displays the compressed and original side by side
            original:
                displays the input image file of the image_id
(CompJPEG) quit
(.venv) root@root:~/CompJPEG$
(.venv) root@root:~/CompJPEG$ echo "detail id=car-key-710fc093.jpg" | ./main.py
(CompJPEG)       Image ID: car-key-710fc093.jpg
         Resolution: 612 X 408
         Time Taken: 0m:1s
         Quality: 85
         | ORIGINAL   | COMPRESSED
----------------------------------------------
    Name | car-key.jpg | car-key-710fc093.jpg
----------------------------------------------
    Size | 66.4KB     | 56.1KB
----------------------------------------------

(CompJPEG) (.venv) root@root:~/CompJPEG$
(.venv) root@root:~/CompJPEG$ deactivate
root@root:~/CompJPEG$
```

## Authors
Binael Nchekwube -[Github](https://github.com/binael) | [Twitter](https://twitter.com/binaelnchekwube) | [LinkedIn]()

## License
Public Domain. No copy write protection.
