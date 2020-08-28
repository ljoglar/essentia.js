#include "custom_extractor.h"


// Util function to convert a Float32 JS typed array into std::vector<float>
// https://github.com/emscripten-core/emscripten/issues/5519#issuecomment-624775352
std::vector<float> float32ArrayToVector(const val &v) {
  std::vector<float> rv;
  const auto l = v["length"].as<unsigned>();
  rv.resize(l);
  emscripten::val memoryView{emscripten::typed_memory_view(l, rv.data())};
  memoryView.call<void>("set", v);
  return rv;
}

// class constructor to call the configure method
LogMelSpectrogramExtractor::LogMelSpectrogramExtractor(const int frameSize, const int hopSize, const int numBands, const std::string& windowType) {
  configure();
};

// method to configure algorithm settings used in your extractor
void LogMelSpectrogramExtractor::configure(const int frameSize, const int hopSize, const int numBands, const std::string& windowType){
  essentia::init();
  AlgorithmFactory& factory = standard::AlgorithmFactory::instance();

  _FrameCutter = factory.create("FrameCutter",
          "frameSize", frameSize,
          "hopSize", hopSize,
          "startFromZero", true
  );
  _Windowing = factory.create("Windowing",
          "type", windowType,
          "zeroPadding", frameSize
  );
  _Spectrum = factory.create("Spectrum",
          "size", frameSize
  );
  _MelBands = factory.create("MelBands",
          "numberBands", numBands,
          "type", "magnitude"
  );
  _UnaryOperator = factory.create("UnaryOperator",
          "type", "log"
  );
};

// compute method for your extractor
std::vector<float> LogMelSpectrogramExtractor::compute(const val& audioData) {

  // convert JS Float32 typed array into std::vector<float>
  // eg. getChannelData output from the Web Audio API AudioContext instance
  std::vector<float> audioSignal = float32ArrayToVector(audioData);

  _FrameCutter->input("signal").set(audioSignal);
  std::vector<Real> frameFrameCutter;
  _FrameCutter->output("frame").set(frameFrameCutter);
  _Windowing->input("frame").set(frameFrameCutter);
  std::vector<Real> frameWindowing;
  _Windowing->output("frame").set(frameWindowing);
  _Spectrum->input("frame").set(frameWindowing);
  std::vector<Real> spectrumSpectrum;
  _Spectrum->output("spectrum").set(spectrumSpectrum);
  _MelBands->input("spectrum").set(spectrumSpectrum);
  std::vector<Real> bandsMelBands;
  _MelBands->output("bands").set(bandsMelBands);
  _UnaryOperator->input("array").set(bandsMelBands);
  std::vector<Real> arrayUnaryOperator;
  _UnaryOperator->output("array").set(arrayUnaryOperator);

  while (true) {
      // compute a frame
      _FrameCutter->compute();
      // if it was the last one (ie: it was empty), then we are done.
      if (!frameFrameCutter.size()) {
          break;
      }
      // if the frame is silent, just drop it and go on processing
      if (isSilent(frameFrameCutter)) continue;
      _Windowing->compute();
      _Spectrum->compute();
      _MelBands->compute();
      _UnaryOperator->compute();
      }
      return arrayUnaryOperator;
};

// method for resetting the internal states used in the extractor
void LogMelSpectrogramExtractor::reset() {
  _FrameCutter->reset();
  _Windowing->reset();
  _Spectrum->reset();
  _MelBands->reset();
  _UnaryOperator->reset();
};

// method for deleting the algorithms used in the extractor
void LogMelSpectrogramExtractor::shutdown() {
  delete _FrameCutter;
  delete _Windowing;
  delete _Spectrum;
  delete _MelBands;
  delete _UnaryOperator;
  essentia::shutdown();
};
