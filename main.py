from pathlib import Path
import json
from openai import OpenAI
import pygame

# Initialize the OpenAI client (Make sure to set your API key in the environment variables)
client = OpenAI()


def load_narration_instructions(filename):
    """
    Load narration instructions from the given filename using JSON format.
    
    Parameters:
    filename (str): The name of the file to load.
    
    Returns:
    dict: The loaded narration instructions.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def narrate_text_from_file(instructions_file):
    """
    A function to narrate text from a file using the provided narration instructions file.

    :param instructions_file: The file containing the narration instructions
    :type instructions_file: str

    :return: A list of file paths for the narrated segments
    :rtype: list
    """
    instructions = load_narration_instructions(instructions_file)

    files_output = []
    for i, instruction in enumerate(instructions, start=1):
        voice = instruction.get("voice")
        text = instruction.get("text")

        speech_file_path = Path(__file__).parent / f"speech_segment_{i}.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        response.stream_to_file(str(speech_file_path))
        print(
            f"Segment {i} narrated with voice {voice} and saved to {speech_file_path}")
        files_output.append(speech_file_path)
    return files_output


def play_audio_files(file_paths):
    """
    Play the audio files specified by the given file paths using the pygame library.

    Parameters:
    file_paths (list): A list of file paths for the audio files to be played.

    Returns:
    None
    """

    pygame.mixer.init()

    for file_path in file_paths:
        # Load the audio file
        pygame.mixer.music.load(file_path)

        # Play the audio file
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# Example usage with your generated audio files


# Example usage
narration_file = "podcast.json"  # Make sure this path is correct
files = narrate_text_from_file(narration_file)
play_audio_files(files)
