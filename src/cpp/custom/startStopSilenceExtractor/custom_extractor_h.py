[[[cog
   import cog

   extractors = {'StartStopSilenceExtractor':{'params': 'const int frameSize=512, const int hopSize=256' ,
                                                'algorithms': ['FrameCutter', 'StartStopSilence'],
                                                'compute_return': 'int'
                                                }
                 }

   cog.outl("#ifndef __EXTRACTOR_EXAMPLE_H__ ")
   cog.outl("#define __EXTRACTOR_EXAMPLE_H__")
   cog.outl()
   cog.outl("#include <vector>")
   cog.outl("#include <essentia/algorithmfactory.h>")
   cog.outl("#include <essentia/essentiamath.h>")
   cog.outl("#include <emscripten/bind.h>")
   cog.outl()
   cog.outl("using namespace essentia;")
   cog.outl("using namespace essentia::standard;")
   cog.outl("using namespace emscripten;")
   cog.outl()
   cog.outl()

   for extractor_key, extractor in extractors.items():
      cog.outl("class %s {" % extractor_key)
      cog.outl()
      cog.outl("  public:")
      cog.outl("    std::string essentiaVersion = essentia::version;")
      cog.outl()
      cog.outl("    %s(%s);" % (extractor_key, extractor['params']))
      cog.outl()
      cog.outl("    ~%s() {};" % extractor_key)
      cog.outl()
      cog.outl("    void configure(%s);" % extractor['params'])
      cog.outl()
      cog.outl("    %s compute(const val& audioData);" %extractor['compute_return'])
      cog.outl()
      cog.outl("    void reset();")
      cog.outl()
      cog.outl("    void shutdown();")
      cog.outl()

      cog.outl("  private:")
      for algorithm in extractor['algorithms']:
         cog.outl("    Algorithm* _%s;" % algorithm)
      cog.outl()
      cog.outl("};")
      cog.outl()

   cog.outl('// convert a Float32 JS typed array into std::vector<float>')
   cog.outl('// https://github.com/emscripten-core/emscripten/issues/5519#issuecomment-589702756')
   cog.outl('std::vector<float> float32ArrayToVector(const val &v);')
   cog.outl()
   cog.outl('#endif // __EXTRACTOR_EXAMPLE_H__')

]]]
[[[end]]]