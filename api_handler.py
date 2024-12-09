import requests

def get_minecraft_versions():
    """Получение списка версий Minecraft из Mojang API"""
    url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    response = requests.get(url)
    data = response.json()
    versions = [version['id'] for version in data['versions']]
    return versions

def download_server(version):
        """Скачиваем сервер Minecraft с прогрессом."""
        version_manifest_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
        version_info = requests.get(version_manifest_url).json()
        for ver in version_info['versions']:
            if ver['id'] == version:
                version_url = ver['url']
                break
        server_info = requests.get(version_url).json()
        server_url = server_info['downloads']['server']['url']

        # Запускаем скачивание
        response = requests.get(server_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        file_name = f'{version}.jar'
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                downloaded += len(chunk)
        return file_name