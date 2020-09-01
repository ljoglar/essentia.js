#include <emscripten/bind.h>
#include "custom_extractor.h"

// expose the extractor class to js using embind templates
EMSCRIPTEN_BINDINGS(Class_Extractor) {
class_<StartStopSilenceExtractor>("StartStopSilenceExtractor")
.constructor<int, int>()
.function("configure", &StartStopSilenceExtractor::configure)
.function("computeStartframe", &StartStopSilenceExtractor::computeStartframe)
.function("computeStopframe", &StartStopSilenceExtractor::computeStopframe)
.function("reset", &StartStopSilenceExtractor::reset)
.function("shutdown", &StartStopSilenceExtractor::shutdown)
;
// utility function to convert a Float32 JS typed array into std::vector<float>
function("arrayToVector", &float32ArrayToVector);
register_vector<float>("VectorFloat");
};
