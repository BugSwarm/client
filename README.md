# The BugSwarm Client

![The BugSwarm Mascot](https://cloud.githubusercontent.com/assets/8139148/24324903/1101b9a2-114c-11e7-9340-316022ef57d5.png)

The official command line client for the [BugSwarm](https://bugswarm.org) artifact dataset

## Installation
> Requires Python 3.
```
$ pip3 install bugswarm-client
```

## Usage
- Download a Docker image and enter the Docker container associated with an artifact. At this time, we cannot make our website live. Until then, the best way to acquire image tags is to contact us.<!--Choose an image tag from the [website](http://bugswarm.org/artifact-browser) or via the [REST API](https://github.com/BugSwarm/database#api-endpoints).-->
    ```
    $ bugswarm run --image-tag <image_tag>
    ```
- Show metadata for an artifact.
    ```
    $ bugswarm show --image-tag <image_tag>
    ```
- Show the version.
    ```
    $ bugswarm --version
    ```
- Show usage text for the entire tool or for a specific sub-command.
    ```
    $ bugswarm --help
    $ bugswarm <sub-command> --help
    ```

## Development
Execute the following commands to install the tool in ["editable" mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).
1. Clone this repository.
    ```
    $ git clone https://github.com/BugSwarm/client.git
    ```
1. `cd` into the root directory of this repository.
    ```
    $ cd client
    ```
1. Install the tool.
    ```
    $ pip3 install --upgrade --force-reinstall --process-dependency-links -e .
    ```
