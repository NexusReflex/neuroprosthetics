import time
from Neuroprosthetics.filter_banks import *
from Neuroprosthetics.vocoder import *
from scipy.io import wavfile
from exercise_7 import plot_spectogram


def single_sided_spectrum(signal, dt):
    n = signal.size
    spectrum = np.abs(np.fft.rfft(signal) / n)
    frequencies = np.fft.rfftfreq(n, dt)
    spectrum[1:] = spectrum[1:] * 2
    return frequencies, spectrum


def plot_filtered(signal, time, name, idx=False, save=False):
    set_plot_params([13, 8], fontsize=11)
    fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    ax = ax.ravel()

    for i, channel in enumerate(signal):
        set_plot_params([10, 8], fontsize=11, spines=True)
        channel /= np.max(channel)
        plt.ylim(-1, 1)
        if idx:
            indices = (time > 1) & (time < 1.04)
            timeslot = time[indices]
            noise = channel[indices]
            ax[i].plot(timeslot, noise)
        else:
            ax[i].plot(time, channel)

        ax[i].set_title('Channel {}'.format(i))
        if i > 7:
            ax[i].set_xlabel('Time (s)')

    if save:
        plt.savefig('../latex/tex_8/imgs/' + name + '.eps',
                    format='eps')



def plot_envelope(env, time_array, name, save=False):
    set_plot_params([13, 8], fontsize=11)
    fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    ax = ax.ravel()

    for i, envel in enumerate(env):
        set_plot_params([10, 8], fontsize=11, spines=True)
        plt.ylim(-1, 1)
        ax[i].plot(time_array, envel, color='orange')
        ax[i].set_title('Channel {}'.format(i))
        if i > 7:
            ax[i].set_xlabel('Time (s)')

    if save:
        plt.savefig('../latex/tex_8/imgs/' + name + '.eps',
                    format='eps')


def show_vocoder_result(channels, time_array, summed_signal, fs, name, save=False):
    plot_filtered(channels, time_array, 'vocoder_channels')
    print('Vocoder signal')
    play_back_sound(summed_signal, fs)
    f, s = single_sided_spectrum(summed_signal, fs)
    plt.figure()
    plt.loglog()
    plt.plot(f, s)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')

    if save:
        plt.savefig('../latex/tex_8/imgs/' + name + '.eps',
                    format='eps')

    plot_spectogram(summed_signal, sample_rate, exercise_num=8, save=save)



if __name__=='__main__':

    audio_file_name = "sorekara"
    play_back = False
    num_channels = 12
    save_img=True

    filtered_channels, sample_rate = filter_wav_file(audio_file_name, num_channels,
                                                     play_back=play_back, show_plot=False, order=4)

    filtered_channels = np.array(filtered_channels)
    t_max = filtered_channels.shape[1]/sample_rate
    t = np.arange(0, t_max, 1/sample_rate)

    noise_f = noise_generator(num_channels, signal_duration=t_max, fs=sample_rate, order=4)
    t = t[:noise_f.shape[1]]
    plot_filtered(noise_f, t, 'noise_filtered_timeslot', idx=True, save=save_img)

    envelopes = extract_envelopes(filtered_channels, fs=sample_rate)

    plot_filtered(filtered_channels, t, 'filtered_audio', save=save_img)
    plot_envelope(envelopes, t, 'envelopes', save=save_img)

    for lower_clip in [0.4, 0.5, 0.6, 0.7]: # best is 0.6
        env_compressed = compress_envelopes(envelopes, lower_clip=lower_clip)
        audio_file_path = '../data/exercise_7/{}.wav'.format(audio_file_name)
        _, audio_data = wavfile.read(audio_file_path)
        vocoder_channels, summed_channels = vocoder(env_compressed, noise_f, audio_data)

        print('result for lower clip: {}'.format(lower_clip))
        show_vocoder_result(vocoder_channels, t, summed_channels, sample_rate, 'vocoder_lower_clip_{}'.format(lower_clip), save=save_img)
        time.sleep(2)



    plt.show()
