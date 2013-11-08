from cffi import FFI

# Create position independent code
#cc_src = "g++ -O3 -fPIC -c -o {in}.cc {in}.h {out.o}"
#cc_lib = "g++ -shared -o libCSim.o {out}.so"

#-------------------------------------------------------------------------
# gen_cppsim
#-------------------------------------------------------------------------
def gen_cppsim( clib, cdef ):
  ffi = FFI()
  ffi.cdef( cdef )
  cmodule = ffi.dlopen( clib )
  return cmodule
  #return wrap( cmodule )

#-------------------------------------------------------------------------
# translate
#-------------------------------------------------------------------------
# Create the string passed into ffi.cdef
def gen_cdef( top_ports ):
  str_    = '\n'
  str_   += 'void cycle(void);\n'
  str_   += 'void flop(void);\n'
  str_   += 'int  ncycles;\n'
  for name, cname, type_ in top_ports:
    str_ += '{} {}; // {}\n'.format( type_, cname, name )
  return str_

#-------------------------------------------------------------------------
# gen_cheader
#-------------------------------------------------------------------------
# Create the header for the simulator
def gen_cheader( top_ports ):
  str_    = '\n'
  #str_   += '#ifndef CSIM_H\n'
  #str_   += '#define CSIM_H\n'
  str_   += 'extern "C" {\n'
  str_   += '  extern void cycle( void );\n'
  str_   += '  extern void flop( void );\n'
  str_   += '  extern int ncycles;\n'
  for name, cname, type_ in top_ports:
    str_ += '  extern {} {}; // {}\n'.format( type_, cname, name )
  str_   += '}\n'
  #str_   += '#endif\n'
  return str_

#-------------------------------------------------------------------------
# gen_pywrapper
#-------------------------------------------------------------------------
# Create the header for the simulator
def gen_pywrapper( top_ports ):

  # Inner class to create unique classes
  class CSimWrapper( object ):
    def __init__( self, cmodule ):
      self.cmodule = cmodule
    def cycle( self ):
      self.cmodule.cycle()
      self.cmodule.flop()
    @property
    def ncycles( self ):
      return self.cmodule.ncycles

  # Accessor closure, needed to create unique accessors
  def make_accessor( closed_name, closed_cname ):
    setattr( CSimWrapper, closed_name, property(
      lambda self:        getattr( self.cmodule, closed_cname ),
      lambda self, value: setattr( self.cmodule, closed_cname, value )
    ))

  # Create the properties for each port
  for name, cname, type_ in top_ports:
    name = name[4:]  # remove the 'top_' prefix
    make_accessor( name, cname )

  return CSimWrapper


#-------------------------------------------------------------------------
# gen_csim
#-------------------------------------------------------------------------
# TODO: not implemented, only works if generated code is pure C
def gen_csim( cstring, cdef ):
  raise Exception("Doesn't currently work!")
  ffi = FFI()
  ffi.cdef( cdef )
  clib = ffi.verify( cstring )
  return clib
