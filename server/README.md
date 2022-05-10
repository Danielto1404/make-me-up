## Run server
```shell
$ pip install requirements.txt
$ python main.py
```

## Pretrained models:

Download models weights from [here](https://drive.google.com/drive/folders/1SkxAHTa9XMiK328J1G_ejjEbFpPS4nWX?usp=sharing) and then put them into [models](models) folder.

```yaml
    server:
        models:
            - PARSING.pth
            - SG3.pth
            - SSAT.pth
            - W_STDS.pt
        ... 
```


## GPU
For running torch modules on GPU change device type to `cuda` in [config.yaml](config.yaml) file, like so:

```yaml
models:
    device: cuda
    ...
```


### Project structure:

[api](src/api/) – defines a FastAPI routes for handling HTTP requests

[clip](src/clip) – module which wraps an OpenAI clip implementation

[clip_trainer](src/clip_trainer/) – module which is responsible for optimizing text to image score and finding best latent vector in StyleGAN3 spac which fits to given text prompt

[face_detector](src/face_detector/) –
module which is validates source face for correctness

[face_parsing](src/face_parsing/) – module which is parses a given source face into 18 sematic regions (e.i lips, eyes). Parsing result helps to transfer make from target face to source face

[ssat](src/ssat/) – module which is responsible for transferring makeup from target face to source face (Symantic Simmetric Aware Transformer)

[stylegan](src/stylegan/) – axiluary files which is required by StyleGAN3 model