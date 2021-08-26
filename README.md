# Melodies
Made by: Austin Ng, John Mocettini, Kelechi Igwe, Yvan Gonzales

## About
Melodies is a software application that allows a user to generate melodies using Python. Melodies is a musical collaboration between human and computer, as the user works with AI to generate new and innovative melodies!

Melodies is a senior project for Austin, John, Kelechi, and Yvan, who are seniors at California Polytechnic State University, San Luis Obispo (Austin, John, and Yvan are Computer Science majors, Kelechi is a Computer Engineering major). The advisor for this project is Dr. John Clements, a Computer Science professor at Cal Poly.

## Installation Instructions
1. Install Python 3.x (newest version recommended)
2. (For Mac users only) Install Homebrew
3. Download the MuseScore Soundfont2 file and place it in the following folder in this project's directory calling it melodies.sf2: /support-files/req/melodies.sf2 (Download from here: https://drive.google.com/file/d/1Ap53QQcdl_WKtbZ_9SlcE-7LYi014w6E/view?usp=sharing)
4. Run setup.py (located in the setup folder) and make sure that at the end it says "Melodies was successfully setup on this machine and is now available to use". If not follow the error messages to make sure all supporting modules and programs are installed.
5. Run the Melodies executable (located in bin folder) to start Melodies (or run genalgo.py in the src folder).

## How To Use
### Main Tab
When you open Melodies, you will first see an array of options describing how you want your melodies to be created. From the key to the instrument used, there are a variety of optional characteristics that a user can choose to modify which melodies are made. When ready, you can select 'Generate Melodies' to create 10 random melodies.

For each of the 10 melodies generated, you will have the option to either replay the melody, save the melody into the saved folder, add the melody to the Melody Stack (see next section), or rate the melody. Saving a melody saves it as a MIDI file (.mid) and a WAV file (.wav) for listening compatibility on all platforms. Rating a melody helps the program to generate better melodies by using an internal genetic algorithm.

(EXPERIMENTAL) The 'Autoplay' button allows you to let Melodies generate and improve melodies based on your previous decisions. Your previous ratings are stored in support-files/opt/taste.mel and are only read by Melodies if you run the program with the '-t' or '-tr' argument. For Autoplay to work, there must be at least one melody in taste.mel for each note, including "R" for rest. To store new melodies that you rate into taste.mel, run the program with the '-t' or '-tw' argument.

### Melody Stack
Clicking the 'melody stack' tab on the top left of Melodies takes you to the Melody Stack feature of Melodies. The Melody Stack provides a melody player that allows up to 10 melodies to be played at the same time. Clicking 'play' on each individual spot only plays the melody stored on that spot. However, clicking 'play' at the bottom (next to Full Stack) plays all the melodies stored in the stack. (Note: A green 'play' indicates that there is a melody in that spot while a red 'play' indicates there is not a melody)
  
## Demo
No demo has been made for this product. Please download the repo and install using the above instructions to view Melodies.
