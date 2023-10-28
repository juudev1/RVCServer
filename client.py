import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory

# Define la ruta del archivo de audio original
original_audio_file = 'C:/Users/admin/Downloads/Michael Jackson - Billie Jean Vocals Only.mp3'
payload = {
    "url": 'https://huggingface.co/juuxn/RVCModels/resolve/main/Spreen_(RVC_-_1000_Epochs).zip',
    "method": 'harvest'
}

server_urls = [
    "http://127.0.0.1:3000/convert",
    # "http://34.125.160.47:3000/convert",
    # "http://21.115.160.47:3000/convert"
]

output_audio_path = "converted_client"
if not os.path.exists(output_audio_path):
    os.mkdir(output_audio_path)

# Divide el archivo de audio en partes
def split_audio(audio_file, num_parts):
    temp_dir = TemporaryDirectory()
    file_parts = []
    file_size = os.path.getsize(audio_file)
    chunk_size = file_size // num_parts

    with open(audio_file, 'rb') as audio:
        for i in range(num_parts):
            part_path = os.path.join(temp_dir.name, f'part_{i}{os.path.splitext(audio_file)[-1]}')
            with open(part_path, 'wb') as part:
                part.write(audio.read(chunk_size))
            file_parts.append(part_path)

    return temp_dir, file_parts

# Función para enviar una parte del audio a un servidor
def send_audio_part(part_file, server_url):
    print(f"Enviando {part_file} a {server_url}")
    with open(part_file, 'rb') as part:
        files = {'audio': ('part' + os.path.splitext(part_file)[-1], part)}
        response = requests.post(server_url, files=files, params=payload)
        return response.content

# Función para unir las partes recibidas de los servidores en un solo archivo
def join_audio_parts(parts, output_file):
    with open(output_file, 'wb') as output:
        for part_data in parts:
            output.write(part_data)

# Dividir el archivo de audio en partes
temp_dir, audio_parts = split_audio(original_audio_file, len(server_urls))

# Lista para almacenar las respuestas de los servidores
responses = []

# Realizar solicitudes a los servidores en paralelo
with ThreadPoolExecutor(max_workers=len(server_urls)) as executor:
    futures = [executor.submit(send_audio_part, part, server_url) for part, server_url in zip(audio_parts, server_urls)]
    
    for future in futures:
        responses.append(future.result())

# Unir las partes después de recibir las respuestas
output_audio_file = output_audio_path + os.path.splitext(original_audio_file)[-1]
join_audio_parts(responses, output_audio_file)

# Limpiar el directorio temporal
temp_dir.cleanup()

print("Proceso de unión completado. El archivo resultante se guarda como", output_audio_file)
