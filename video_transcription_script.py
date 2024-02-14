import moviepy.editor as mp
import speech_recognition as sr

def transcribe_video(video_path, duration_minutes, output_file):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio

    # Set up the recognizer
    recognizer = sr.Recognizer()

    total_duration = min(video_clip.duration, duration_minutes * 60)
    start_time = 0
    transcriptions = []

    while start_time < total_duration:
        # Extract a chunk of audio for transcription
        chunk_duration = min(60, total_duration - start_time)  # Process audio in 60-second chunks
        end_time = start_time + chunk_duration
        audio_chunk = audio_clip.subclip(start_time, end_time)

        # Save chunk to a temporary file
        audio_chunk_path = "temp_audio.wav"
        audio_chunk.write_audiofile(audio_chunk_path)

        # Transcribe the chunk
        with sr.AudioFile(audio_chunk_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                transcriptions.append(text)
            except sr.UnknownValueError:
                transcriptions.append("Could not understand audio")
            except sr.RequestError as e:
                transcriptions.append(f"Could not request results; {e}")

        # Move to the next chunk
        start_time = end_time

    # Save transcriptions to a text file
    with open(output_file, "w") as f:
        for i, transcription in enumerate(transcriptions, start=1):
            f.write(f"Transcription {i}: {transcription}\n")

    # Clean up temporary files
    audio_clip.close()
    video_clip.close()

# Example usage
video_path = r"C:\Users\KIIT\Videos\Captures\Meet - nem-fdiy-ftu - Google Chrome 2022-05-24 20-34-32.mp4"
duration_minutes = 1
output_file = "transcriptions.txt"
transcribe_video(video_path, duration_minutes, output_file)
print("Transcriptions saved to", output_file)
