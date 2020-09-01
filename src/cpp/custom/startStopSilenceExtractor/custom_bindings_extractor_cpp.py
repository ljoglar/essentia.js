[[[cog
import cog

extractors = {'StartStopSilenceExtractor': {'params': 'int, int'} }

cog.outl('#include <emscripten/bind.h>')
cog.outl('#include "custom_extractor.h"')
cog.outl()

cog.outl('// expose the extractor class to js using embind templates')
cog.outl('EMSCRIPTEN_BINDINGS(Class_Extractor) {')

cog.outl('class_<%s>("%s")' % (list(extractors.keys())[0], list(extractors.keys())[0]))
cog.outl('.constructor<%s>()' % extractors[list(extractors.keys())[0]]['params'])
cog.outl('.function("configure", &%s::configure)' % list(extractors.keys())[0])
cog.outl('.function("compute", &%s::compute)' % list(extractors.keys())[0])
cog.outl('.function("reset", &%s::reset)' % list(extractors.keys())[0])
cog.outl('.function("shutdown", &%s::shutdown)' % list(extractors.keys())[0])
cog.outl(';')

cog.outl('// utility function to convert a Float32 JS typed array into std::vector<float>')
cog.outl('function("arrayToVector", &float32ArrayToVector);')
cog.outl('register_vector<float>("VectorFloat");')
cog.outl('};')

]]]
[[[end]]]