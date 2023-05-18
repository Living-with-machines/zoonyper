# Setup:
# - put username and password separated with a space in a file called "auth"
# - make sure panoptes_client, tqdm and requests are installed packages

from pathlib import Path
from panoptes_client import Panoptes, Project, SubjectSet
from tqdm.notebook import tqdm
from zoonyper.utils import get_md5

import requests
import json
import pickle
import time
from yaml import load, Loader

# Set up settings file + settings dict
settings_file = Path(__file__).parent / "settings.yaml"

if not settings_file.exists():
    print("A settings.yaml file could not be found")
with open(settings_file) as f:
    settings = load(f, Loader=Loader)

# Set up project ID, auth file and cache locations as correct types
project_id = int(settings["project_id"])
auth_file = Path(settings["auth_file"])
cache = Path(settings["cache"])

if not auth_file.exists():
    raise RuntimeError(
        f"The auth file could not be found: {auth_file.resolve()}"
    )

if cache.exists() and not cache.is_dir():
    raise RuntimeError("The cache provided is not an existing directory.")

username, password = auth_file.read_text().split(" ")

# Connect to API
print("Connecting to API...")
Panoptes.connect(username=username, password=password)
print("--> connected.")

# Set up Project
project = Project(project_id)
print("--> project loaded.")

# Load subject sets + set up names
subject_set_ids = settings["subject_sets"]
subject_set_names = list(subject_set_ids.keys())

# Load in the done subject sets (so we don't double up)
done_subject_sets = (
    json.loads(Path("done_subject_sets.json").read_text())
    if Path("done_subject_sets.json").exists()
    else []
)

lst = [x for x in subject_set_names if x not in done_subject_sets]
# and x in PROCESS_KEYS

cache.mkdir(parents=True, exist_ok=True)
for subject_set_name in tqdm(lst):
    data_file = cache / f"{subject_set_name}"
    print(data_file)
    if data_file.exists():
        continue
    subject_set_id = subject_set_ids[subject_set_name]
    subject_set = SubjectSet(subject_set_id)
    subjects = []
    for subject in (pbar_ss := tqdm(subject_set.subjects, position=0)):
        pbar_ss.update()
        subjects.append(subject)

    data_file.write_bytes(pickle.dumps(subjects))

for subject_set_name in (pbar_ss := tqdm(lst, position=0)):
    pbar_ss.set_description(subject_set_name)
    subject_set_id = subject_set_ids[subject_set_name]
    subject_set = SubjectSet(subject_set_id)

    errors_occured = False

    for subject in (
        pbar := tqdm(
            subject_set.subjects,
            position=1,
            total=subject_set.set_member_subjects_count,
            desc=subject_set_name,
        )
    ):  # leave=False,
        if "!zooniverse_file_md5" in subject.metadata.keys():
            pbar.set_description(f"skipping {subject.id}")
            continue

        pbar.set_description(f"updating {subject.id}")
        urls = [url for x in subject.locations for url in x.values()]

        # Ensure we have only one URL
        if len(urls) > 1:
            raise NotImplementedError(
                "This script has no ability to process multi-URL subjects yet."
            )

        if len(urls) == 0:
            print(f"--> Warning: subject {subject.id} had not URL!")
            continue

        # because we will only process subjects with one URL (see above)
        url = urls[0]

        filename = url.split("/")[-1]
        filepath = Path(f"downloads/{filename}")

        if not filepath.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)

            try:
                r = requests.get(url, timeout=10)
            except:
                errors_occured = True
                time.sleep(50)
                continue

            if r.status_code != 200:
                raise RuntimeError(f"Failed with status {r.status_code}")

            filepath.write_bytes(r.content)

        md5 = get_md5(str(filepath))

        subject.metadata["!zooniverse_file_md5"] = md5
        subject.save()

    if not errors_occured:
        done_subject_sets.append(subject_set_name)
        Path("done_subject_sets.json").write_text(
            json.dumps(done_subject_sets)
        )
