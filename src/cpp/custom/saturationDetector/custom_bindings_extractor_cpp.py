[[[cog
import cog

extractors = {'SaturationDetectorExtractor': {'params': 'int, int',
                                              'outputs': ['starts', 'ends']
                                              }
             }

cog.outl('#include <emscripten/bind.h>')
cog.outl('#include "custom_extractor.h"')
cog.outl()

for extractor_key, extractor in extractors.items():
    cog.outl('// expose the extractor class to js using embind templates')
    cog.outl('EMSCRIPTEN_BINDINGS(Class_Extractor) {')

    cog.outl('class_<%s>("%s")' % (extractor_key, extractor_key))
    cog.outl('.constructor<%s>()' % extractor['params'])
    cog.outl('.function("configure", &%s::configure)' % extractor_key)
    for output in extractor['outputs']:
        cog.outl('.function("compute%s", &%s::compute%s)' % (output.capitalize(), extractor_key, output.capitalize()))
    cog.outl('.function("reset", &%s::reset)' % extractor_key)
    cog.outl('.function("shutdown", &%s::shutdown)' % extractor_key)
    cog.outl(';')

cog.outl('// utility function to convert a Float32 JS typed array into std::vector<float>')
cog.outl('function("arrayToVector", &float32ArrayToVector);')
cog.outl('register_vector<float>("VectorFloat");')
cog.outl('};')

]]]
[[[end]]]