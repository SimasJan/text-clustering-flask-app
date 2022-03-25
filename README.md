# Text Clustering Flask App

### About

A simple flask app to cluster unstructured (text) data that is uploaded by the user.


### Setup

1. Clone the repo

##### Local
2. Create a virtual-environment and activate it.
3. Install `requirements.txt` file.
4. Run `text_cluster_api.py` file with `python3`.
5. Open the URL and navigate to `/cluster` to upload your text data to cluster.

##### Docker
2. add execute permissions to `build.sh` file with the command: `chmod u+x build.sh`
3. Run `build.sh` file as follows: `./build.sh`. Docker image `text-clustering-app` will be built and container with the same name will start in a _detached_ mode on _port 5000_.
4. Open the localhost URL and navigate to `/cluster` to upload your text data to cluster.


##### OpenShift

Inside your project use the following command to create an application with a name 'text-cls-app' on port 5000 with a label 'text-cls-app'.

`oc new-app https://github.com/SimasJan/text-clustering-flask-app --name=text-cls-app -port=5000:5000 -l app=text-cls-app`

- Check status: `oc logs -f bc/text-cls-app`
- Get all info: `oc get all`

Expose service (app) to the outside WWW.

`oc expose service/text-cls-app`

#### Upload data format
A sample of data input can be found in the `data/` directory.

----
