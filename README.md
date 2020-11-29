# viff-xv
A viff or xv file is from Khoros/VisiQuest packages which has a header of 1024 bytes and is BSQ formated raw raster file. The file is parsed based upon the C struct definition provided in the source section.

## Requirements
* Python 3.7
* numpy

## Features and I/O
### Read
```
data = viff.read(filename: str)
```
### Write
```
viff.write(filename: str, data: np.array)
```
### Variable Description
* filenames (str) - Path to the input file to read
* data (np.array) - data to save formated as np.array with dimensions [NumberOfImages,NumberOfBands,NumberOfColumns,NumberOfRows]

## Code Example
### Read and Display File
Read and display the first image and band of the read in file.
```
import viff
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='viff reader example')
parser.add_argument('--file', type=str, help='filename (default=None)')
parser.add_argument('--save', action='store_true', help='save a copy as testing.xv')
args = parser.parse_args()

""" Read a file """
data = viff.read(args.file)

plt.imshow(data[0,0,:,:])
plt.show()
```
### Write a new file
```
if args.save:
  """ Write a new file """
  viff.write('testing.xv',data)
```
### Command line usage
```
$ python viff.py --file <filename> --save
```
This generates a plot and a new file 'testing.xv'.

## Sources:
### File Format
http://www.fileformat.info/format/viff/egff.htm
