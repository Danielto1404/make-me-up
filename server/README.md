## Run server
```shell
$ pip install requirements.txt
$ python main.py
```

## Download pretrained models:
All models will be added to Google Drive.


## GPU
For running torch modules on GPU change device type to `cuda` in [config.yaml](config.yaml) file, like so:

```yaml
models:
    device: cuda
    ...
```