# Lingua-Cosmica
AI video translation service created as a study project for "Practical Machine Learning and Deep Learning" course at Innopolis University

## Project Structure Overview (preliminary)

The project is organized into three main components:

##### Frontend:
1. **Design (low level):** Create an user interface for interacting with the service.

2. **Send request to Backend with video file:** Establish a communication channel with the backend to transmit video files for translation.

3. **Receive processed video:** Retrieve the translated video from the backend for user access.

##### Backend:
1. **Receive request (video file):** Accept incoming video files from the frontend.

2. **Transfer video to ML-pipeline:** Facilitate the handover of video data to the ML-pipeline for processing.

3. **Receive processed video from ML-pipeline:** Retrieve the translated video from the ML-pipeline after processing.

4. **Send back to Frontend:** Forward the processed video to the frontend for user access.

##### ML-pipeline:
1. **Receive video:** Accept the video file from the backend for translation.

2. **Extract audio:** Isolate the audio component from the video for subsequent translation.

3. **Translate audio:** Utilize AI-based translation models to translate audio content to the desired language.

4. **Overwrite original audio:** Replace the original audio with the translated version.

5. **Send processed video back to service:** Return the fully translated video to the backend for user retrieval.

## Project Stack (preliminary)

The preliminary project stack for the AI video translation service:

- **Backend Framework:** Flask
- **Programming Language (ML):** Python
- **Database:** SQLite (for simplicity, can be swapped with a more robust database in production)
- **Machine Learning Framework:** PyTorch (in conjunction with Hugging Face)
- **Audio Processing Library:** Whisper
- **Deep Learning Models:** Leveraging pre-trained models from Hugging Face's Model Hub for translation tasks

## Assumptions

Since we are restricted with time and resources our project has some assumptions:

- **Only upload [videos]**: For a start, we plan to do the most minimal design and limit to just uploading videos manually rather than trying to pull a file from a link.
- **Voice-only videos**: Some videos are accompanied by music. Since noise can affect the output of [our] model, we will work with videos that contain only voice for now.
