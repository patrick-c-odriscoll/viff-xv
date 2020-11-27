# viff-xv
Read and write old Khoros/VisiQuest viff and xv formats.

## Requirements
* Python 3.7
* numpy

## Features and I/O
### Read

### Write

## Code Example
### Read and Display File
Read and create an image showing the 0th band of the image.
```
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description='viff reader example')
parser.add_argument('--file', type=str, help='filename (default=None)')
parser.add_argument('--save', action='store_true', help='save a copy as testing.xv')
args = parser.parse_args()

""" Read a file by initializing the class """
test1 = viff(args.file)

plt.imshow(test1.data[0,0,:,:])
plt.show()
```
### Write a new file
```
if args.save:
  """ Write a new file recycling the test1 class """
  test1.write('testing.xv')
  """ Write a new file by class initialization """
  test2 = viff('testing.xv',test1.data)
```
### Command line usage
```
$ python viff.py --file <filename> --save
```
This generates a plot and a new file 'testing.xv' two times. This can be read in 
## Sources:
### File Format
http://www.fileformat.info/format/viff/egff.htm
### Image Used in this Readme is from
O'Driscoll, Patrick. "Self-Organizing Maps for Segmentation of fMRI: Understanding the Genesis of Willed Movement Through A Multiple Subject Study." (2018) Diss., Rice University. https://hdl.handle.net/1911/105789.
