import sys
import numpy as np

__author__ = "Patrick C O\'Driscoll"
__copyright__ = "2020 Patrick C O\'Driscoll"
__credits__ = ["Patrick C O\'Driscoll"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Patrick C O\'Driscoll"
__email__ = "patrick.c.odriscoll@gmail.com"

""" Viff File reader and writer
  A viff or xv file is from Khoros/VisiQuest packages which has a header of
  1024 bytes and is BSQ formated raw raster file. The file is parsed based upon 
  the C struct definition provided in the source section.

  Parameters:
  filename  (str): filename to read from or write to
  data (np.array): data to be saved or resulting from reading the file
              [NumberOfImages,NumberOfBands,NumberOfColumns,NumberOfRows]

  Functions:
    read: Read the desired file and return the data payload.

    write: Writes the data in a viff formated file.
  
  Sources and Stucture: 
  Quote from http://www.fileformat.info/format/viff/egff.htm
    typedef struct _ViffHeader
    { CHAR  FileId;            /* Khoros file ID value (always ABh)*/
      CHAR  FileType;          /* VIFF file ID value (always 01h) */
      CHAR  Release;           /* Release number (1) */
      CHAR  Version;           /* Version number (0) */
      CHAR  MachineDep;        /* Machine dependencies indicator */
      CHAR  Padding[3];        /* Structure alignment padding (always 00h)*/
      CHAR  Comment[512];      /* Image comment text */
      DWORD NumberOfRows;      /* Length of image rows in pixels */
      DWORD NumberOfColumns;   /* Length of image columns in pixels */
      DWORD LengthOfSubrow;    /* Size of any sub-rows in the image */
      LONG  StartX;            /* Left-most display starting position */
      LONG  StartY;            /* Upper-most display starting position */
      FLOAT XPixelSize;        /* Width of pixels in meters */
      FLOAT YPixelSize;        /* Height of pixels in meters */
      DWORD LocationType;      /* Type of pixel addressing used */
      DWORD LocationDim;       /* Number of location dimensions */
      DWORD NumberOfImages;    /* Number of images in the file */
      DWORD NumberOfBands;     /* Number of bands (color channels) */
      DWORD DataStorageType;   /* Pixel data type */
      DWORD DataEncodingScheme;/* Type of data compression used */
      DWORD MapScheme;         /* How map is to be interpreted */
      DWORD MapStorageType;    /* Map element data type */
      DWORD MapRowSize;        /* Length of map rows in pixels */
      DWORD MapColumnSize;     /* Length of map columns in pixels */
      DWORD MapSubrowSize;     /* Size of any subrows in the map */
      DWORD MapEnable;         /* Map is optional or required */
      DWORD MapsPerCycle;      /* Number of different   maps present */
      DWORD ColorSpaceModel;   /* Color model used to represent image */
      DWORD ISpare1;           /* User-defined field */
      DWORD ISpare2;           /* User-defined field */
      FLOAT FSpare1;           /* User-defined field */
      FLOAT FSpare2;           /* User-defined field */
      CHAR  Reserve[404];      /* Padding */
      } VIFFHEADER;
"""

def read(filename):
  ''' read the filename '''
  f = open(filename,'rb')
  FileId   = f.read(1)
  FileType = f.read(1)
  Release  = f.read(1)
  Version  = f.read(1)
  assert (FileId  == b'\xab') and (FileType == b'\x01') and \
          (Release == b'\x01'), \
          'viff: '+filename+' is not a viff or xv file format'
  MachineDep = f.read(1)
  if   MachineDep == b'\x08':
    endianness = 'little'
  elif MachineDep == b'\x02':
    endianness = 'big'
  else:
    assert True, \
            'viff: '+filename+' unsupported endianness'
  Padding = f.read(3)
  assert (Padding == b'\x00\x00\x00'), \
          'viff: '+filename+' is not a viff or xv file format'
  Comment = f.read(512).decode('ASCII','ignore')
  NumberOfRows = int.from_bytes(f.read(4),byteorder='little')
  NumberOfColumns = int.from_bytes(f.read(4),byteorder='little')
  LengthOfSubrow = int.from_bytes(f.read(4),byteorder='little')
  StartX = f.read(4)
  StartY = f.read(4)
  assert (StartX == b'\xff\xff\xff\xff') and (StartY == b'\xff\xff\xff\xff'),\
          'viff: Unkown values in StartX | StartY'
  XPixelSize = f.read(4)
  YPixelSize = f.read(4)
  LocationType = f.read(4)
  LocationDim = f.read(4)
  NumberOfImages = int.from_bytes(f.read(4),byteorder='little')
  NumberOfBands = int.from_bytes(f.read(4),byteorder='little')
  DataStorageType = int.from_bytes(f.read(4),byteorder='little')
  if   DataStorageType == 0: # bit
    assert True, 'viff: '+filename+' unsuported bit format'
  elif DataStorageType == 1: # uint8
    dt = np.dtype(np.uint8)
  elif DataStorageType == 2: # uint16
    dt = np.dtype(np.uint16)
  elif DataStorageType == 4: # uint32
    dt = np.dtype(np.uint32)
  elif DataStorageType == 5: # float
    dt = np.dtype(np.single)
  elif DataStorageType == 6: # complex
    dt = np.dtype(np.csingle)
  elif DataStorageType == 9: # double
    dt = np.dtype(np.double)
  elif DataStorageType == 10:# double complex
    dt = np.dtype(np.cdouble)
  else:
    assert True, 'viff: '+filename+' unkown type format: '+DataStorageType
  if endianness == 'little':
    dt.newbyteorder('L')
  elif endianness == 'big':
    dt.newbyteorder('B')
  DataEncodingScheme = f.read(4)
  if DataEncodingScheme != b'\x00\x00\x00\x00':
    assert True, 'viff: '+filename+' unsupported DataEncodingScheme'
  MapScheme = f.read(4)
  MapStorageType = f.read(4)
  MapRowSize = f.read(4)
  MapColumnSize = f.read(4)
  MapSubrowSize = f.read(4)
  MapEnable = f.read(4)
  MapsPerCycle = f.read(4)
  ColorSpaceModel = f.read(4)
  ISpare1 = f.read(4)
  ISpare2 = f.read(4)
  FSpare1 = f.read(4)
  FSpare2 = f.read(4)
  Reserve = f.read(404)
  buffer = f.read()
  data = np.reshape(np.frombuffer(buffer,dtype=dt),
                        (NumberOfImages,NumberOfBands,NumberOfColumns,NumberOfRows))
  f.close()
  return data

def write(filename,data):
  ''' write the data to the target file '''
  f = open(filename,'wb')
  f.write(b'\xab')                       # FileId
  f.write(b'\x01')                       # FileType
  f.write(b'\x01')                       # Release
  f.write(b'\x00')                       # Version
  if sys.byteorder == 'little':          # MachineDep
    f.write(b'\x08')
  elif sys.byteorder == 'big':
    f.write(b'\x02')
  else:
    assert True, 'viff: unkown endianness'
  f.write(b'\x00\x00\x00')               # Padding
  f.write(b'\x00'*512)                   # Comment
  f.write(np.uint32(data.shape[3])) # NumberOfRows
  f.write(np.uint32(data.shape[2])) # NumberOfColumns
  f.write(np.uint32(0.0))                # LengthOfSubrow
  f.write(b'\xff\xff\xff\xff')           # StartX
  f.write(b'\xff\xff\xff\xff')           # StartY
  f.write(b'\x00\x00\x80\x3f')           # XPixelSize
  f.write(b'\x00\x00\x80\x3f')           # YPixelSize
  f.write(b'\x01\x00\x00\x00')           # LocationType
  f.write(b'\x00\x00\x00\x00')           # LocationDim
  f.write(np.uint32(data.shape[0])) # NumberOfImages
  f.write(np.uint32(data.shape[1])) # NumberOfBands
  if   data.dtype == 'int8':        # DataStorageType
    f.write(np.uint32(1)) 
  elif data.dtype == 'int16':
    f.write(np.uint32(2))
  elif data.dtype == 'int32':
    f.write(np.uint32(4))
  elif data.dtype == 'float32':
    f.write(np.uint32(5))
  elif data.dtype == 'complex64':
    f.write(np.uint32(6))
  elif data.dtype == 'flaot64':
    f.write(np.uint32(9))
  elif data.dtype == 'complex128':
    f.write(np.uint32(10))
  else:
    assert True, 'viff: warning unkown data type: ' + data.dtype
  f.write(np.uint32(0))                  # DataEncodingScheme
  f.write(np.uint32(0))                  # MapScheme
  f.write(np.uint32(1))                  # MapStorageType
  f.write(np.uint32(0))                  # MapRowSize
  f.write(np.uint32(0))                  # MapColumnSize
  f.write(np.uint32(0))                  # MapSubrowSize
  f.write(np.uint32(0))                  # MapEnable
  f.write(np.uint32(0))                  # MapsPerCycle
  f.write(np.uint32(0))                  # ColorSpaceModel
  f.write(np.uint32(0))                  # ISpare1
  f.write(np.uint32(0))                  # ISpare2
  f.write(np.uint32(0))                  # FSpare1
  f.write(np.uint32(0))                  # FSpare2
  f.write(b'\x00'*404)                   # Reserve
  f.write(data)
  f.close()
  return
  

if __name__ == "__main__":
  import matplotlib.pyplot as plt
  import argparse
  """ Demonstration """
  parser = argparse.ArgumentParser(description='viff reader example')
  parser.add_argument('--file', type=str, help='filename (default=None)')
  args = parser.parse_args()

  """ Read a file """
  data = read(args.file)

  plt.imshow(data[0,0,:,:])
  plt.show()

  """ Write a new file """
  write('testing.xv',data)
