from sys import platform

import os
import subprocess

def homebrewCheck():
    print("Checking for Homebrew on your machine...", end="")
    newLineCount = -1

    try:
        with open('temp', 'w+') as out:
            subprocess.run(['brew', 'help'], stdout=out)
            out.seek(0, 0)
            newLineCount = out.read(500).count('\n')
    except:
        pass
    finally:
        if newLineCount < 10:
            print("Homebrew was not found on your machine. Download and "
                  + "install it before running setup.py.")
            exit(1)
        else:
            print("FOUND!")


def fsCheck(system: str):
    print("Checking for FluidSynth on your machine...", end="")

    try:
        with open('temp', 'w') as out:
            child = subprocess.Popen(args=["fluidsynth"], stdout=out)
            if child.poll() is None:
                child.terminate()
            else:
                print("MISSING!")
                installFS(system)
                return

            print("FOUND!")
    except:
        print("MISSING!")
        installFS(system)


def installFS(system: str):
    print("Installing FluidSynth on your machine...")

    try:
        if system == "MAC":
            subprocess.run(['brew', 'install', 'fluidsynth', 'pkg-config'])

            with open('temp', 'w+') as out:
                subprocess.run(['brew', 'list'], stdout=out)
                out.seek(0, 0)
                out.read(500).count('\n')
        else:  # WINDOWS
            print("Follow the instructions located in the fluidsynth folder to"
                  + "add fluidsynth to your PATH. After, rerun setup.py.")
    except:
        print("ERROR!\nAn error occurred while installing FluidSynth.")
        exit(1)

    print("SUCCESSFUL!\n")


def pipCheck():
    print("Checking for pip on your machine...", end="")
    newLineCount = -1

    try:
        with open('temp', 'w+') as out:
            subprocess.run(['pip', '--help'], stdout=out)
            out.seek(0, 0)
            newLineCount = out.read(500).count('\n')
    except:
        print("ERROR!\nAn error occurred while checking for pip.")
    finally:
        if newLineCount < 10:
            print("pip was not found on your machine. Download and "
                  + "install it before running setup.py.")
            exit(1)
        else:
            print("FOUND!")


def moduleCheck(system: str):
    try:
        with open("temp", "w+") as out:
            subprocess.run(['pip', 'list'], stdout=out)
            out.seek(0, 0)
            pipList = out.readlines()
    except:
        print("Error occurred while looking for pip list.")

    genModuleBank = ["Kivy", "mido", "numpy"]  # capital K needed for kivy
    windowsModules = ["Pillow"]

    if system == "MAC":
        moduleBank = genModuleBank
    else:
        moduleBank = genModuleBank + windowsModules

    print("Checking for the necessary python modules:")

    for mod in moduleBank:
        found = False
        print(f"{mod}...", end="")

        for installed in pipList:
            if mod in installed.split():
                print("FOUND!")
                found = True
                break

        if not found:
            print("MISSING!")

            try:
                subprocess.run(['pip', 'install', mod])
            except:
                print(f"An error occurred while installing {mod}.")
                exit(1)

            print(f"Module {mod} was successfully installed.\n")


def main():
    userOS = ""

    if platform.startswith("linux"):
        userOS = "LINUX"
    elif platform == 'darwin':
        userOS = "MAC"
    elif platform == 'win32' or platform == 'cygwin':
        userOS = "WINDOWS"
    else:
        print("Melodies currently does not support/cannot identify your "
              + "platform. Please view repository for more info.")
        print("\nSetup failed.")
        exit(1)

    print(f"Detected system platform...{userOS}")

    if userOS == "MAC":
        homebrewCheck()

    fsCheck(userOS)
    pipCheck()
    moduleCheck(userOS)

    if os.path.exists("temp"):
        os.remove("temp")

    print("Melodies was successfully setup on this machine and is now "
          + "available to use.")


if __name__ == '__main__':
    main()
