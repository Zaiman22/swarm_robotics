import audio_utils as audio_utils
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation



if __name__ == "__main__":
    data, sample_rate, duration = audio_utils.get_audio('audio/KISINAN 2 - MASDDDHO (OFFICIAL MUSIC VIDEO).wav')
    # audio_utils.plot_audio_in_time(data,sample_rate,duration, 'KISINAN 2 - MASDDDHO')


    data = audio_utils.normalize_samples(data)
    # yf, xf = audio_utils.get_fft_transform(normalized_audio, sample_rate, duration)
    # audio_utils.plot_audio_in_frequency(xf, yf)


    # # create plot
    fig, ax = plt.subplots()
    ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
    ax.legend()

    def update(frame):
        # for each frame, update the data stored on each artist.
        ax.clear()
        amplitude = data[frame*2048:(frame+1)*2048,0]
        yf, xf = audio_utils.get_fft_transform(amplitude, sample_rate, 2048/sample_rate)
        max_amplitude = np.max(np.abs(yf))
        yf = yf / max_amplitude * 100  # normalize for better visualization
        plt.xlim((0,16000))
        plt.grid(True)
        plt.title(f'Fourier/Frequency Domain')
        plt.xlabel(f'Frequency (Hz)')
        plt.ylabel(f'Magnitude')
        plt.plot(np.abs(xf), np.abs(yf))
        return ax
    

    ani = animation.FuncAnimation(fig=fig, func=update, frames=data.shape[0]//2048, interval=30)
    plt.show()
