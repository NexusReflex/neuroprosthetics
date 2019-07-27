import time
from Neuroprosthetics.filter_banks import *
from Neuroprosthetics.vocoder import *
from scipy.io import wavfile
from exercise_7 import plot_spectogram


def plot_filtered(sig, t_array, name, idx=False, save=False):
    set_plot_params([13, 8], fontsize=18)
    fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')
    fig.subplots_adjust(hspace=0.3, wspace=0.2)
    ax = ax.ravel()

    for i, channel in enumerate(sig):
        set_plot_params(fontsize=15, spines=True)
        ax[i].set_ylim(-1, 1)
        plt.yticks(np.arange(-1, 1.00001, step=0.5), fontsize=18)
        channel /= np.max(channel)
        if idx:
            indices = (t_array > 1.04) & (t_array < 1.08)
            timeslot = t_array[indices]
            noise = channel[indices]
            ax[i].plot(timeslot, noise)
        else:
            ax[i].plot(t_array, channel)

        ax[i].set_title('Channel {}'.format(i), fontdict={'fontsize': 18, 'fontweight': 'medium'})
        if i > 7:
            ax[i].set_xlabel('Time (s)')


    if save:
        plt.savefig('../latex/tex_8/imgs/' + name + '.eps',
                    format='eps')


def plot_envelope(original_sig, env, time_array, name, save=False):

    set_plot_params([13, 8], fontsize=18)
    fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    ax = ax.ravel()

    for i, (envel, sig) in enumerate(zip(env, original_sig)):
        set_plot_params([10, 8], fontsize=18, spines=True)
        plt.ylim(-1, 1)
        ax[i].plot(time_array, sig)
        ax[i].plot(time_array, envel, color='orange')
        ax[i].set_title('Channel {}'.format(i), fontdict={'fontsize': 18, 'fontweight': 'medium'})
        if i > 7:
            ax[i].set_xlabel('Time (s)')

    if save:
        plt.savefig('../latex/tex_8/imgs/' + name + '.eps',
                    format='eps')


def show_vocoder_result(channels, time_array, summed_signal, fs, name, save, play_audio=False):
    def single_sided_spectrum(sig, dt):
        n = sig.size
        spectrum = np.abs(np.fft.rfft(sig) / n)
        frequencies = np.fft.rfftfreq(n, dt)
        spectrum[1:] = spectrum[1:] * 2
        return frequencies, spectrum

    plot_filtered(channels, time_array, 'vocoder_channels')
    print('Vocoder signal')

    if play_audio:
        play_back_sound(summed_signal, fs)
        time.sleep(2)

    f, s = single_sided_spectrum(summed_signal, fs)
    set_plot_params([10, 8], fontsize=15, spines=True)
    plt.figure()
    plt.loglog()
    plt.plot(f, s)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')

    if save:
        plt.savefig('../latex/tex_8/imgs/' + name + '.eps',
                    format='eps')

    plot_spectogram(summed_signal, sample_rate, name=name, exercise_num=8, save=save)


if __name__=='__main__':

    audio_file_name = "sorekara"
    play_back = True
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
    plot_envelope(filtered_channels, envelopes, t, 'envelopes', save=save_img)

    for lower_clip in [0.4, 0.5, 0.6, 0.7]: # best is 0.6
        env_compressed = compress_envelopes(envelopes, lower_clip=lower_clip)
        audio_file_path = '../data/exercise_7/{}.wav'.format(audio_file_name)
        _, audio_data = wavfile.read(audio_file_path)
        vocoder_channels, summed_channels = vocoder(env_compressed, noise_f, audio_data)

        print('result for lower clip: {}'.format(lower_clip))
        show_vocoder_result(vocoder_channels, t, summed_channels, sample_rate, 'vocoder_lower_clip_{}'.format(lower_clip), save_img, play_audio=play_back)

    plt.show()
