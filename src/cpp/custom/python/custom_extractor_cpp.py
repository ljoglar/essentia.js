[[[cog
    import cog

    extractors = {'LogMelSpectrogramExtractor':
                        {'params': 'const int frameSize, const int hopSize, const int numBands, const std::string& windowType',
                        'algorithms':
                            {'FrameCutter':
                                {'params': ["frameSize", "frameSize", "hopSize", "hopSize", "startFromZero", "true"],
                                'inputs': {'signal': 'std::vector<float>'},
                                'outputs': {'frame': 'std::vector<Real>'} },
                            'Windowing':
                                {'params': ["type", "windowType", "zeroPadding", "frameSize"],
                                'inputs': {'frame':  'std::vector<Real>'},
                                'outputs': {'frame': 'std::vector<Real>'} },
                            'Spectrum':
                                {'params': ["size", "frameSize"],
                                 'inputs': {'frame': 'std::vector<Real>'} ,
                                 'outputs': {'spectrum': 'std::vector<Real>'} },
                            'MelBands':
                                 {'params': ["numberBands", "numBands", "type", '"magnitude"'],
                                  'inputs': {'spectrum': 'std::vector<Real>'},
                                  'outputs':{'bands': 'std::vector<Real>'} },
                            'UnaryOperator':
                                 {'params': ["type", '"log"'],
                                 'inputs': {'array': 'std::vector<Real>'},
                                 'outputs': {'array': 'std::vector<Real>'} }
                            }
                        }
    }


    cog.outl('#include "custom_extractor.h"')
    cog.outl()
    cog.outl()

    cog.outl('// Util function to convert a Float32 JS typed array into std::vector<float>')
    cog.outl('// https://github.com/emscripten-core/emscripten/issues/5519#issuecomment-624775352')
    cog.outl('std::vector<float> float32ArrayToVector(const val &v) {')
    cog.outl('  std::vector<float> rv;')
    cog.outl('  const auto l = v["length"].as<unsigned>();')
    cog.outl('  rv.resize(l);')
    cog.outl('  emscripten::val memoryView{emscripten::typed_memory_view(l, rv.data())};')
    cog.outl('  memoryView.call<void>("set", v);')
    cog.outl('  return rv;')
    cog.outl('}')
    cog.outl()


    for extractor_key, extractor in extractors.items():
        cog.outl('// class constructor to call the configure method')
        cog.outl('%s::%s(%s) {' % (extractor_key, extractor_key, extractor['params']))
        paramsArray = extractor['params'].split(" ")
        params = []
        for param in paramsArray:
            if param.find('=') > 0:
                params.append(param.split('=')[0])
        cog.outl('  configure(%s);' % ', '.join(params))
        cog.outl('};')
        cog.outl()
        cog.outl('// method to configure algorithm settings used in your extractor')
        cog.outl('void %s::configure(%s){' % (extractor_key, extractor['params']))
        cog.outl('  essentia::init();')
        cog.outl('  AlgorithmFactory& factory = standard::AlgorithmFactory::instance();')
        cog.outl()
        for algorithm_name in extractor['algorithms']:

            cog.outl('  _%s = factory.create("%s",' % (algorithm_name, algorithm_name))
            for i in range(int(len(extractor['algorithms'][algorithm_name]['params'])/2)):
                if i == int(len(extractor['algorithms'][algorithm_name]['params'])/2) - 1:
                    cog.outl('          "%s", %s' % (extractor['algorithms'][algorithm_name]['params'][i*2], extractor['algorithms'][algorithm_name]['params'][i*2+1]))
                else:
                    cog.outl('          "%s", %s,' % (extractor['algorithms'][algorithm_name]['params'][i*2], extractor['algorithms'][algorithm_name]['params'][i*2+1]))
            cog.outl('  );')
        cog.outl('};')
        cog.outl()

        cog.outl('// compute method for your extractor')
        cog.outl('std::vector<float> %s::compute(const val& audioData) {' % extractor_key)
        cog.outl()
        cog.outl('  // convert JS Float32 typed array into std::vector<float>')
        cog.outl('  // eg. getChannelData output from the Web Audio API AudioContext instance')
        cog.outl('  std::vector<float> audioSignal = float32ArrayToVector(audioData);')
        variablesChain = 'audioSignal'
        variableFrame = ''
        cog.outl()
        for algorithm_name in extractor['algorithms']:
            for input_name in extractor['algorithms'][algorithm_name]['inputs']:
                cog.outl('  _%s->input("%s").set(%s);' % (algorithm_name, input_name, variablesChain))

            for output_name in extractor['algorithms'][algorithm_name]['outputs']:
                if (algorithm_name == 'FrameCutter'):
                    variableFrame = output_name + algorithm_name
                cog.outl('  %s %s%s;' % (extractor['algorithms'][algorithm_name]['outputs'][output_name], output_name, algorithm_name))
                variablesChain = output_name + algorithm_name
                cog.outl('  _%s->output("%s").set(%s);' % (algorithm_name, output_name, variablesChain))

        cog.outl()
        cog.outl('  while (true) {')
        cog.outl('      // compute a frame')
        cog.outl('      _%s->compute();' % list(extractor['algorithms'].keys())[0])
        cog.outl('      // if it was the last one (ie: it was empty), then we are done.')
        cog.outl('      if (!%s.size()) {' % variableFrame)
        cog.outl('          break;')
        cog.outl('      }')

        cog.outl('      // if the frame is silent, just drop it and go on processing')
        cog.outl('      if (isSilent(%s)) continue;' % variableFrame)
        for i in range(1, len(list(extractor['algorithms'].keys())) ):
            cog.outl('      _%s->compute();' % list(extractor['algorithms'].keys())[i])

        cog.outl('      }')
        cog.outl('      return %s;' % variablesChain)
        cog.outl('};')

        cog.outl()

        cog.outl('// method for resetting the internal states used in the extractor')
        cog.outl('void %s::reset() {' % extractor_key)
        for algorithm_name in extractor['algorithms']:
            cog.outl('  _%s->reset();' % (algorithm_name))
        cog.outl('};')

        cog.outl()

        cog.outl('// method for deleting the algorithms used in the extractor')
        cog.outl('void %s::shutdown() {' % extractor_key)
        for algorithm_name in extractor['algorithms']:
            cog.outl('  delete _%s;' % (algorithm_name))
        cog.outl('  essentia::shutdown();')
        cog.outl('};')

]]]
[[[end]]]