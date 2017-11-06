# The BugSwarm Client

![The BugSwarm Mascot](https://cloud.githubusercontent.com/assets/8139148/24324903/1101b9a2-114c-11e7-9340-316022ef57d5.png)

A command line client to interface with the [BugSwarm](https://bugswarm.github.io) artifact collection.

## Getting Started

### Installation
> Requires Python 3.

> Installation will be a single command after after we register the tool on PyPI.
1. Clone this repository.
    ```
    $ git clone
    ```
1. `cd` into the root directory of this repository.
    ```
    $ cd client
    ```
1. Install the tool.
    ```
    $ sudo pip3 install --editable .
    ```

### Uninstallation
```
$ pip3 uninstall bugswarm
```

### Usage
- Download a Docker image and enter the Docker container associated with an artifact. Choose an image tag from the website (coming soon) or via the [REST API](https://github.com/BugSwarm/database#endpoints).
    ```
    $ bugswarm run --image-tag <image_tag>
    ```
- Show metadata for an artifact.
    ```
    $ bugswarm show --image-tag <image_tag>
    ```
- Show usage text.
    ```
    $ bugswarm --help
    ```
