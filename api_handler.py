import requests

def get_minecraft_versions():
    """Получение списка версий Minecraft из Mojang API"""
    url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    response = requests.get(url)
    data = response.json()
    versions = [version['id'] for version in data['versions']]
    return versions

def get_version_details(version):
    """Получение подробностей о версии Minecraft (ссылка для скачивания)"""
    version_manifest_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    version_info = requests.get(version_manifest_url).json()
    for ver in version_info['versions']:
        if ver['id'] == version:
            version_url = ver['url']
            break
    return requests.get(version_url).json()

