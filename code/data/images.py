from code.utils.utils import *

def load_images():
    images = {
        'weapons' : import_folders_of_folder_dict(get_assets_dir() + 'graphics/weapons'),

        # magic
        'flame': import_folder(get_assets_dir() + 'graphics/particles/flame/frames'),
        'aura': import_folder(get_assets_dir() + 'graphics/particles/aura'),
        'heal': import_folder(get_assets_dir() + 'graphics/particles/heal/frames'),

        # attacks
        'claw': import_folder(get_assets_dir() + 'graphics/particles/claw'),
        'slash': import_folder(get_assets_dir() + 'graphics/particles/slash'),
        'sparkle': import_folder(get_assets_dir() + 'graphics/particles/sparkle'),
        'leaf_attack': import_folder(get_assets_dir() + 'graphics/particles/leaf_attack'),
        'thunder': import_folder(get_assets_dir() + 'graphics/particles/thunder'),

        # monster deaths
        'squid': import_folder(get_assets_dir() + 'graphics/particles/smoke_orange'),
        'raccoon': import_folder(get_assets_dir() + 'graphics/particles/raccoon'),
        'spirit': import_folder(get_assets_dir() + 'graphics/particles/nova'),
        'bamboo': import_folder(get_assets_dir() + 'graphics/particles/bamboo'),

        # leafs
        'leaf': (
            import_folder(get_assets_dir() + 'graphics/particles/leaf1'),
            import_folder(get_assets_dir() + 'graphics/particles/leaf2'),
            import_folder(get_assets_dir() + 'graphics/particles/leaf3'),
            import_folder(get_assets_dir() + 'graphics/particles/leaf4'),
            import_folder(get_assets_dir() + 'graphics/particles/leaf5'),
            import_folder(get_assets_dir() + 'graphics/particles/leaf6'),
            reflect_images(import_folder(get_assets_dir() + 'graphics/particles/leaf1')),
            reflect_images(import_folder(get_assets_dir() + 'graphics/particles/leaf2')),
            reflect_images(import_folder(get_assets_dir() + 'graphics/particles/leaf3')),
            reflect_images(import_folder(get_assets_dir() + 'graphics/particles/leaf4')),
            reflect_images(import_folder(get_assets_dir() + 'graphics/particles/leaf5')),
            reflect_images(import_folder(get_assets_dir() + 'graphics/particles/leaf6'))
        )
    }

    return images
