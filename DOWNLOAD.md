Dataset **CVC-ClinicDB** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/e/n/yx/yldqfiuIPbNtvP1dxKxLT9o2rodD5t39rauvjhMHKewgJH6qsO7fSwm7Kg3T11cW8TA1xSnjsLNEgi4vvXRyeSxTRLUGbB6nRBQKz9S4a2PU0erQyt8iSWUA8e81.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CVC-ClinicDB', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://polyp.grand-challenge.org/CVCClinicDB/).