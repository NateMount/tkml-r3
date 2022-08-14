# TKML
***

### Quick Navigation
  - [Overview]()
  - [Usage]()
  - [Syntax]()
  - [Widgets]()
  - [Packages]()
  - [Projects]()
  - [Programmers]()
 
### Overview
TKML is a language desinged for rapid graphical interface prototyping, with a focus on compatability and modularity.

### Usage
TKML command line usage
```sh
tkml [command] [args(s)]
```

TKML has four (4) command usage modes. 
1. **Run**
    The run usage mode is meant to be used during program development to live build and run a TKML program.

2. **Compile**
    The compile usage mode is used to convert your finished program into a single executable file that can be run on supported hardware.

3. **Render**
    The render usage mode will convert your TKML application into another graphical format. Exaples include Webstack (HTML / JS / CSS), ncurses, and RUI. 

4. ***Debug***
    The debug usage mode will check the program for errors and will then run the program with a `--debug` flag passed to all programs in your project or main file

### Syntax
All code must be placed within the tkml tag braces to be run all external code will be considered module dependent and not used until it is called upon
```html
<tkml>
    ... code ...
</tkml>
```

##### Frames
Frames are containers for grouped widgets, code, and variables. Frames can be called upon to be included by themselves, or as components of other frames.
In TKML, by default, there are multiple reserved frames that can be interacted with but not overwritten.

```html
<frame>
    ... data ...
</frame>
```

**pre-proc**
The pre-proc frame is dedicated to defining other files to be used in the current file and defining macros.
These macros are simple find and replace statements

**init**
The init frame is the first frame rendered when an application is run

**pre-def**
This frame sets the standards for all widgets prior to style being applied

##### Functions
Functions in TKML can be utilized through a single brace 
```html
<funct param1=val1 param2="value 2">
```
Or through brace delimeters
```html
<funct>
    param1=val1
    param2="value 2"
</funct>
```
| Function Name | Syntax | Description |
|:------:| ------------ | ------ |
| Use           | `<use module>` | This function includes code from a given module |
| Define        | `<define key=value>` | This function sets the program to replace all instances of `key` with `value`|
| Set | `<set global=value>` | This function sets a global variable equal to `value`. If the global does not exist then it is created and initialized |
| Assign | `<assign global=value>` | This function assigns a global variable a value. If the gloabal variable does not exist then nothing will happen |
| Load Frame | `<loadframe frame>` | This function will load a provided frame and destroy the pre-existing frame |
