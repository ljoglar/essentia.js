#include <emscripten/bind.h>
#include "custom_extractor.h"

// expose the extractor class to js using embind templates
EMSCRIPTEN_BINDINGS(Class_Extractor) {
    class_<LogMelSpectrogramExtractor>("LogMelSpectrogramExtractor")
        .constructor<int, int, int, std::string>()
        .function("configure", &LogMelSpectrogramExtractor::configure)
        .function("compute", &LogMelSpectrogramExtractor::compute)
        .function("reset", &LogMelSpectrogramExtractor::reset)
        .function("shutdown", &LogMelSpectrogramExtractor::shutdown)
    ;
    // utility function to convert a Float32 JS typed array into std::vector<float>
    function("arrayToVector", &float32ArrayToVector);
    register_vector<float>("VectorFloat");
};
