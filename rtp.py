import pyshark
import wave
import struct

def extract_rtp_audio(pcap_file, output_audio_file):
    # Open the pcap file using pyshark with a filter for RTP packets
    cap = pyshark.FileCapture(pcap_file, display_filter="rtp")
    
    # Create a byte array to store the audio data
    audio_data = bytearray()
    
    print("Extracting RTP payloads from the capture file...")
    
    try:
        for packet in cap:
            # Ensure the packet contains RTP payload
            if hasattr(packet, 'rtp') and hasattr(packet.rtp, 'payload'):
                # Extract RTP payload as a hexadecimal string
                payload_hex = packet.rtp.payload.replace(':', '')
                # Convert the hexadecimal string to raw bytes
                payload_bytes = bytes.fromhex(payload_hex)
                audio_data.extend(payload_bytes)
    except Exception as e:
        print(f"An error occurred during packet analysis: {e}")
    finally:
        cap.close()
    
    print(f"Extracted {len(audio_data)} bytes of audio data.")
    
    # Save the extracted audio data as a WAV file
    try:
        with wave.open(output_audio_file, 'wb') as wav_file:
            # Define the WAV file parameters (e.g., 8000 Hz, mono, 16-bit PCM)
            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(2)  # 2 bytes (16 bits) per sample
            wav_file.setframerate(8000)  # 8000 samples per second
            # Convert the byte array to PCM frames
            pcm_frames = struct.pack(f'<{len(audio_data)//2}h', *struct.unpack(f'>{len(audio_data)//2}h', audio_data))
            wav_file.writeframes(pcm_frames)
        
        print(f"Audio successfully saved to {output_audio_file}")
    except Exception as e:
        print(f"An error occurred while saving audio: {e}")

# Example usage
if __name__ == "__main__":
    pcap_file = "cn.pcapng"  # Use the correct file name
    output_audio_file = "output_audio.wav"  # Replace with your desired output file name
    
    extract_rtp_audio(pcap_file, output_audio_file)
