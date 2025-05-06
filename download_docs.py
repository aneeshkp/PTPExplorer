import os
import requests

# Version to URL mapping
docs = {
    "4.13": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.13/pdf/networking/OpenShift_Container_Platform-4.15-Networking-en-US.pdf",
    "4.14": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.14/pdf/networking/OpenShift_Container_Platform-4.15-Networking-en-US.pdf",
    "4.15": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.15/pdf/networking/OpenShift_Container_Platform-4.15-Networking-en-US.pdf",
    "4.16": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/pdf/networking/OpenShift_Container_Platform-4.15-Networking-en-US.pdf",
    "4.17": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/pdf/networking/OpenShift_Container_Platform-4.15-Networking-en-US.pdf",
    "4.18": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/pdf/networking/OpenShift_Container_Platform-4.15-Networking-en-US.pdf",
}

base_dir = "openshift_docs"
os.makedirs(base_dir, exist_ok=True)

for version, url in docs.items():
    version_dir = os.path.join(base_dir, version)
    os.makedirs(version_dir, exist_ok=True)
    file_path = os.path.join(version_dir, "networking.pdf")
    
    print(f"Downloading OpenShift {version} networking guide...")
    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {file_path}")
