from .Neuroprosthetics.signalGeneration import plotSignal, signalGenerator, calcSingleSidedAmplitudeSpectrum
# 1.0 Get signal
frequencies = [100, 600, 9000]
amplitudes = [1, 1.5, 2]
offset = 3
duration = 1
sampleRate = 100000

signalArray, timeArray = signalGenerator(amplitudes, frequencies, offset,
                                         duration, sampleRate)

# 1.1 Plot the first 100 ms
plotSignal(timeArray[:10000], signalArray[:10000], 0, 0.1, -2, 8,
           name='signalDataPlot')

# 2.0 Calculate FFT single sided spectrum for three different sample rates and
# plot the results
sampleRates = [10000, 20000, 100000]

for fs in sampleRates:
    signalArray, timeArray = signalGenerator(amplitudes, frequencies, offset,
                                             duration, fs)
    calcSingleSidedAmplitudeSpectrum(signalArray, fs)