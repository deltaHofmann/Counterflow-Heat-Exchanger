class PlaybackController:
    def __init__(self):
        self.playback_speed = 1.0
        self.frame_accumulator = 0.0
        self.current_frame = 0
        self.playing = False

    def play(self):
        # Wenn bereits abgespielt wird:
        # Geschwindigkeit auf 1x zurücksetzen
        if self.playing:
            self.playback_speed = 1.0
            print("Playback speed reset to 1.0x")
        else:
            self.playing = True

    def pause(self):
        self.playing = False

    def slower(self):
        self.playback_speed = max(
            0.25,
            self.playback_speed / 2
        )
        print(f"Playback speed: {self.playback_speed:.2f}x")

    def faster(self):
        self.playback_speed = min(
            8.0,
            self.playback_speed * 2
        )
        print(f"Playback speed: {self.playback_speed:.2f}x")

    def get_next_frame(self, number_of_frames):
        """
        Determines the next frame based on the current
        playback speed.

        Returns
        -------
        int
            Index of the next frame.
        """

        if not self.playing:
            return self.current_frame

        self.frame_accumulator += self.playback_speed

        frame_step = int(self.frame_accumulator)
        self.frame_accumulator -= frame_step

        if frame_step == 0:
            return self.current_frame

        next_frame = self.current_frame + frame_step

        # Loop back to the beginning
        if next_frame >= number_of_frames:
            next_frame = 0

        self.current_frame = next_frame

        return self.current_frame