import sys, argparse
import numpy as np
import matplotlib.pyplot as plt

'''
  Objectives:
    A viff or xv file is from Khoros/VisiQuest packages which has a header of
    1024 bytes and is BSQ formated raw raster file. We can parse the header
    information based upon the C struct definition provided in the source 
    section. All of these elements are accessable in the class structure.
   
  Source: Quote from http://www.fileformat.info/format/viff/egff.htm
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
'''

class viffFile():
  def __init__(self, filename=None, data=None):
    self.filename = filename
    if data is not None:
      self.data = data
      self.write(self.filename)
    else:
      self.read()
    return
  
  def read(self):
    f = open(self.filename,'rb')
    self.FileId   = f.read(1)
    self.FileType = f.read(1)
    self.Release  = f.read(1)
    self.Version  = f.read(1)
    assert (self.FileId  == b'\xab') and (self.FileType == b'\x01') and \
           (self.Release == b'\x01'), \
           'viffFile: '+self.filename+' is not a viff or xv file format'
    self.MachineDep = f.read(1)
    if   self.MachineDep == b'\x08':
      self.endianness = 'little'
    elif self.MachineDep == b'\x02':
      self.endianness = 'big'
    else:
      assert True, \
             'viffFile: '+self.filename+' is not a viff or xv file format'
    self.Padding = f.read(3)
    assert (self.Padding == b'\x00\x00\x00'), \
           'viffFile: '+self.filename+' is not a viff or xv file format'
    self.Comment = f.read(512).decode('ASCII','ignore')
    self.NumberOfRows = int.from_bytes(f.read(4),byteorder='little')
    self.NumberOfColumns = int.from_bytes(f.read(4),byteorder='little')
    self.LengthOfSubrow = int.from_bytes(f.read(4),byteorder='little')
    self.StartX = f.read(4)
    self.StartY = f.read(4)
    assert (self.StartX == b'\xff\xff\xff\xff') and (self.StartY == b'\xff\xff\xff\xff'),\
           'viffFile: Unkown values in StartX | StartY'
    self.XPixelSize = f.read(4)
    self.YPixelSize = f.read(4)
    self.LocationType = f.read(4)
    self.LocationDim = f.read(4)
    self.NumberOfImages = int.from_bytes(f.read(4),byteorder='little')
    self.NumberOfBands = int.from_bytes(f.read(4),byteorder='little')
    self.DataStorageType = int.from_bytes(f.read(4),byteorder='little')
    if   self.DataStorageType == 0: # bit
      assert True, 'viffFile: '+self.filename+' unsuported bit format'
    elif self.DataStorageType == 1: # uint8
      self.dt = np.dtype(np.uint8)
    elif self.DataStorageType == 2: # uint16
      self.dt = np.dtype(np.uint16)
    elif self.DataStorageType == 4: # uint32
      self.dt = np.dtype(np.uint32)
    elif self.DataStorageType == 5: # int
      self.dt = np.dtype(np.single)
    elif self.DataStorageType == 6: # uint
      self.dt = np.dtype(np.csingle)
    elif self.DataStorageType == 9: # complex
      self.dt = np.dtype(np.double)
    elif self.DataStorageType == 10:# double complex
      self.dt = np.dtype(np.cdouble)
    else:
      assert True, 'viffFile: '+self.filename+' unkown type format: '+self.DataStorageType
    if self.endianness == 'little':
      self.dt.newbyteorder('L')
    elif self.endianness == 'big':
      self.dt.newbyteorder('B')
    self.DataEncodingScheme = f.read(4)
    self.MapScheme = f.read(4)
    self.MapStorageType = f.read(4)
    self.MapRowSize = f.read(4)
    self.MapColumnSize = f.read(4)
    self.MapSubrowSize = f.read(4)
    self.MapEnable = f.read(4)
    self.MapsPerCycle = f.read(4)
    self.ColorSpaceModel = f.read(4)
    self.ISpare1 = f.read(4)
    self.ISpare2 = f.read(4)
    self.FSpare1 = f.read(4)
    self.FSpare2 = f.read(4)
    self.Reserve = f.read(404)
    buffer = f.read()
    self.data = np.reshape(np.frombuffer(buffer,dtype=self.dt),
                          (self.NumberOfImages,self.NumberOfBands,self.NumberOfColumns,self.NumberOfRows))
    f.close()
    return
  
  def write(self,filename):
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
      print('viffFile: unkown endianness')
    f.write(b'\x00\x00\x00')               # Padding
    f.write(b'\x00'*512)                   # Comment
    f.write(np.uint32(self.data.shape[3])) # NumberOfRows
    f.write(np.uint32(self.data.shape[2])) # NumberOfColumns
    f.write(np.uint32(0.0))                # LengthOfSubrow
    f.write(b'\xff\xff\xff\xff')           # StartX
    f.write(b'\xff\xff\xff\xff')           # StartY
    f.write(b'\x00\x00\x80\x3f')           # XPixelSize
    f.write(b'\x00\x00\x80\x3f')           # YPixelSize
    f.write(b'\x01\x00\x00\x00')           # LocationType
    f.write(b'\x00\x00\x00\x00')           # LocationDim
    f.write(np.uint32(self.data.shape[0])) # NumberOfImages
    f.write(np.uint32(self.data.shape[1])) # NumberOfBands
    # TODO finish DataStorageType
    if   self.data.dtype == 'byte':        # DataStorageType
      f.write(np.uint32(1)) 
    elif self.data.dtype == 'ubyte':
      f.write(np.uint32(1))
    elif self.data.dtype == 'float32':
      f.write(np.uint32(5))
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
    f.write(self.data)
    f.close()
    return
  

''' demonstration of deployment '''
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='viffFile reader example')
  parser.add_argument('--file', type=str, help='filename (default=None)')
  args = parser.parse_args()

  test = viffFile(args.file)

  plt.imshow(test.data[0,0,:,:])
  plt.show()
