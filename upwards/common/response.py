from rest_framework.response import Response


class MetaDataResponse(Response):
    meta_data_dict = {
        "meta": "",
        "data": {}
    }

    def __init__(self, *args, **kwargs):
        if args:
            MetaDataResponse.meta_data_dict["data"] = args[0]
            modified_args = list(args)
            modified_args[0] = MetaDataResponse.meta_data_dict
        super(MetaDataResponse, self).__init__(*tuple(modified_args), **kwargs)
