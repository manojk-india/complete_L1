import io
from tempfile import NamedTemporaryFile
import chainlit as cl
import speech_recognition as sr
from dataclasses import dataclass
import os
from entry import entrypoint
import wave, time
import pandas as pd
import asyncio
import numpy as np


# This is where the frontend chainlit part starts............
os.environ["CHAINLIT_AUTH_SECRET"]="my_secret_key"

@dataclass
class UIConfig:
    """Configuration for the Chainlit UI"""
    app_name: str = "JANVI - JIRA AI Assistant"
    theme_color: str = "#1E88E5"  
    support_audio: bool = True
    max_input_length: int = 500
    default_placeholder: str = "Enter your JIRA query here... 💡"


@cl.on_chat_start
async def start():
    """Initialize the chat interface"""
   
    welcome_message="Please enter your prompt! "
    await cl.Message(
        content=welcome_message,
        author="Assistant"
    ).send() 


     
@cl.step(type="tool")
async def processing(message):
    await entrypoint(message)
    return "Process1 completed successfully"

@cl.step(type="tool")
async def speech_to_text(audio_file):
    """Enhanced speech to text processing using Google's speech recognition"""
    # Create a temporary file with a unique name
    temp_file_path = None
    try:
        # Create a temp file that won't be auto-deleted when closed
        with NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(audio_file[1])
            # Make sure file is written and closed properly
            temp_file.flush()
            os.fsync(temp_file.fileno())
        
        # Initialize the recognizer
        recognizer = sr.Recognizer()
        
        # Now open the fully written file with SpeechRecognition
        with sr.AudioFile(temp_file_path) as source:
            audio_data = recognizer.record(source)
            
            try:
                # Use Google's speech recognition
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return f"Error processing audio: {str(e)}"
    finally:
        # Clean up the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass  # If we can't delete it now, it will be cleaned up later

@cl.on_audio_start
async def on_audio_start():
    """Initialize audio session variable"""
    
    cl.user_session.set("audio_chunks", [])
    return True

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.InputAudioChunk):
    """Process incoming audio chunks"""
    audio_chunks = cl.user_session.get("audio_chunks")

    if audio_chunks is not None:
        audio_chunk = np.frombuffer(chunk.data, dtype=np.int16)
        audio_chunks.append(audio_chunk)
        cl.user_session.set("audio_chunks", audio_chunks)

@cl.on_audio_end
async def on_audio_end():
    """Process the audio chunk when the audio ends"""
    await process_audio()
        
async def process_audio():
    try:
        # Get the audio buffer from the session
        if audio_chunks := cl.user_session.get("audio_chunks"):
            # Concatenate all chunks
            concatenated = np.concatenate(list(audio_chunks))

            # Create an in-memory binary stream
            wav_buffer = io.BytesIO()

            # Create WAV file with proper parameters
            with wave.open(wav_buffer, "wb") as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
                wav_file.setframerate(24000)  # sample rate (24kHz PCM)
                wav_file.writeframes(concatenated.tobytes())

            # Reset buffer position
            wav_buffer.seek(0)

            cl.user_session.set("audio_chunks", [])

            audio_buffer = wav_buffer.getvalue()

            input_audio_el = cl.Audio(content=audio_buffer, mime="audio/wav")

            input = ("audio.wav", audio_buffer, "audio/wav")
            transcription = await speech_to_text(input)

            # Store the conversation
            message_history = cl.user_session.get("message_history")
            if not message_history:
                message_history = []
            message_history.append({"role": "user", "content": transcription})
            cl.user_session.set("message_history", message_history)

            # Send the transcribed text
            message = await cl.Message(
                author="You",
                type="user_message",
                content=transcription,
                elements=[input_audio_el],
            ).send()

            res = await cl.AskActionMessage(
                content='''Is our transcription accurate? ✅ If not, feel free to cancel it. ❌ Did you know that reducing unnecessary API calls helps save energy ⚡and lower carbon emissions 🌍? Let's contribute to a greener environment together! 🍃''',
                actions=[
                    cl.Action(name="continue", payload={"value": "continue"}, label="✅ Continue"),
                    cl.Action(name="cancel", payload={"value": "cancel"}, label="❌ Cancel"),
                ],
            ).send()

            if res and res.get("payload").get("value") == "continue":
                await process_message(message)
            else:
                await cl.Message(content="❌ Cancelled. Thank you. Lets create a sustainable environment 🌍 for our future generations").send()
            
    except Exception as e:
        # Handle any exceptions that might occur during processing
        await cl.Message(content=f"Error processing audio: {str(e)}").send()




@cl.on_message
async def process_message(message):
    """Main message processing handler"""
    
    await processing(message.content)

    await asyncio.sleep(3)

    with open("outputs/output.txt", "r") as f:
        content = f.read()

     # Create an empty message
    msg = cl.Message(content="")
    await msg.send()

    # Stream character by character
    for char in content:
        msg.content += char
        await msg.update()
        await asyncio.sleep(0.01)  # Adjust typing speed here
    
    df= pd.read_csv("generated_files/current.csv") 

    await cl.Message(
            content="Here's the list of relevant issues :",
            elements=[
                cl.Dataframe(
                    data=df, 
                    display="inline",
                    name="JIRA Data",
                )
            ]
            ).send()
    
    await asyncio.sleep(1)
    
    image1= cl.Image(path='outputs/jira_hygiene_dashboard.png', name="JIRA Hygiene", display="inline")

    await asyncio.sleep(1)

    await cl.Message(
        content="Jira Hygiene Dashboard",
        elements=[image1],
    ).send()

    try:
        df2= pd.read_csv("generated_files/poor_acceptance.csv") 

        await cl.Message(
            content="Here's the list of Low quality acceptance crieterias",
            elements=[
                cl.Dataframe(
                    data=df2, 
                    display="inline",
                    name="JIRA Data",
                )
            ]
            ).send()
        
        output_file = "outputs/acceptance_crieteria_report.pdf"
        if output_file and os.path.exists(output_file):
                        await cl.Message(
                            content="Download report here!.",
                            elements=[cl.File(name=os.path.basename(output_file), path=output_file)]
                        ).send()
    except:
        pass



    


    
def configure_chainlit_app():
    """Configure Chainlit application settings"""
    cl.App.config(
        name=UIConfig().app_name,
        theme=cl.Theme(
            primary_color=UIConfig().theme_color,
            font_family="Inter, sans-serif"
        ),
        enable_audio=True
    )
if __name__ == "__main__":
    # Make sure the generated_files directory exists
    configure_chainlit_app()






