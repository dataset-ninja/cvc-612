Dataset **CVC-ClinicDB** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMwMTdfQ1ZDLUNsaW5pY0RCL2N2Yy1jbGluaWNkYi1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJEcXY3YUZkc2g4OUE1NGNQM01HUXdmQmhBMFltd2ozclZkY3lxK0dUMDNVPSJ9)

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