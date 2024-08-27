# @Author: Matthew Ragan
# @Date: 01.28.2023
# @Email: matthew@sudomagic.com

'''
This script acts as an automated means of generating a link list to be used
in TouchDesigner curriculum pages. The automation here is intended to automate
the process of generating links to reduce errors when copying and pasting.

curriculum_links is a file generated for faster integration with the
learn.derivative site

url_manifests is a file that can be used to download all files from
an example set for a local store.
'''

import os
import datetime
import shutil

# NOTE - repo variables
repo_owner = "TouchDesigner"
repo_name = "CurriculumExamples"
branch_name = "main"

# NOTE - download_link_structs
link_struct = "https://github.com/{repo_owner}/{repo_name}/raw/{branch_name}/{asset_path}"
navigator_link_struct = "?actionable=1&action=load_tox&remotePath={url}"

# NOTE - directories that will be used to generate manifest and download lists
new_release_paths = [
    'toxExamples/sweet16',
    'toxExamples/TouchDesignerFundamentals/100',
    'toxExamples/TouchDesignerFundamentals/200',
]

archive_dir = 'toxExamples/_zipped'

print("- "*10, '\n', "-> Starting automated file generation\n", "- "*10)

# NOTE - creates download manifest
# create download manifest
for each_release_path in new_release_paths:
    manifest = f"{each_release_path}/manifest.txt"
    curriculum_links = f"{each_release_path}/curriculum_links.txt"
    url_manifests = [manifest, curriculum_links]

    # delete manifest and curriculum if they exist
    for each_manifest in url_manifests:
        if os.path.isfile(each_manifest):
            os.remove(each_manifest)
            print(f"--> Removing file {each_manifest}")

    # generate tox download manifest
    print(f"---> Creating manifest {manifest}")
    with open(manifest, 'w') as manifest_file:
        header_line = f"TOX Download Manifest | Last Modified {datetime.datetime.now()}\n \n"
        manifest_file.write(header_line)
        for root, dirs, files in os.walk(each_release_path):
            for each_file in files:
                if each_file.endswith(".tox"):
                    tox_path = f'{root}/{each_file}'
                    tox_url = link_struct.format(
                        repo_owner=repo_owner,
                        repo_name=repo_name,
                        branch_name=branch_name,
                        asset_path=tox_path)
                    manifest_file.write(f'{tox_url}\n')

    # generate curriculum links
    print(f"---> Creating curriculum links {curriculum_links}")
    with open(curriculum_links, 'w') as curriculum_links_file:
        header_line = f"Curriculum links Manifest | Last Modified {datetime.datetime.now()}\n \n"
        curriculum_links_file.write(header_line)
        for root, dirs, files in os.walk(each_release_path):
            for each_file in files:
                if each_file.endswith(".tox"):
                    tox_path = f'{root}/{each_file}'
                    tox_url = link_struct.format(
                        repo_owner=repo_owner,
                        repo_name=repo_name,
                        branch_name=branch_name,
                        asset_path=tox_path)
                    nav_link = navigator_link_struct.format(url=tox_url)
                    curriculum_links_file.write(f'TOX | {each_file}\n')
                    curriculum_links_file.write(f'{nav_link}\n')
                    curriculum_links_file.write(f'{tox_url}\n')
                    curriculum_links_file.write('\n')

print("- "*10, '\n', "-> Automated file generation completed\n", "- "*10)

# NOTE creates zips of TOX directories

# ensure archive directory exists
if os.path.exists(archive_dir):
    pass
else:
    os.mkdir(archive_dir)

# generate new zipped archive
for each in new_release_paths:
    path_parts = each.split('/')[1:]
    output_path = f'{archive_dir}/{"".join(path_parts)}Examples'
    new_archive = shutil.make_archive(output_path, 'zip', each)

    if os.path.exists(new_archive):
        print(f'-> {new_archive} created')
    else:
        print(f'-> {new_archive} Archive Generation failed')
