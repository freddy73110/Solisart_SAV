import pandas as pd
import numpy as np
import sys


class convertjson:
    def jsontocsv(
        installation_SN=None, installation_name=None, path=None, dicttoconvert=None
    ):
        from django.templatetags.static import static
        import os, json

        pathtocsvdefault = os.path.join(
            os.path.abspath(os.getcwd()),
            "sav",
            "static",
            "sav",
            "fichier",
            "config_default.csv",
        )
        df = pd.read_csv(pathtocsvdefault, skiprows=1, sep=";", header=None)
        df.columns = ["idx", "key", "value"]
        if installation_SN:
            df.value[df.key == "serial"] = installation_SN
        if installation_name:
            df.value[df.key == "srv_id"] = installation_name
        if not dicttoconvert:
            with open(
                os.path.join(
                    os.path.abspath(os.getcwd()),
                    "sav",
                    "static",
                    "sav",
                    "fichier",
                    "json.json",
                ),
                encoding="utf-8",
            ) as json_file:
                data = json.load(json_file)
        with open(
            os.path.join(
                os.path.abspath(os.getcwd()),
                "sav",
                "static",
                "sav",
                "fichier",
                "json_to_csv.json",
            ),
            encoding="utf-8",
        ) as json_file:
            convertjson = json.load(json_file)
            # convertjsonlower={}
            # for k, v in convertjson.items():
            #     convertjsonlower[k]={"translation":{}}
            #     for key, value in v["translation"].items():                    
            #         convertjsonlower[k]["translation"].update({key.lower():value})
            # with open(os.path.join(
            #     os.path.abspath(os.getcwd()),
            #     "sav",
            #     "static",
            #     "sav",
            #     "fichier",
            #     "json_to_csvlower.json",
            # ), "w") as outfile: 
            #     json.dump(convertjsonlower, outfile)
        if "formulaire" in dicttoconvert:
            dicttoconvert = dicttoconvert["formulaire"]
        for k, v in dicttoconvert.items():
            if k in convertjson:
                try:
                    if("typeAppoint" in str(k)):
                        if (
                            dicttoconvert["appoint" + k.replace("typeAppoint", "")]
                            != "autre"
                        ):
                            pass
                    for key, value in convertjson[k]["translation"][v.lower()].items():
                        df.value[df.key == key] = value
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(ex)
                    print("error", k)
                    pass
        from django.utils import timezone

        df.columns = [
            timezone.now().strftime("%d/%m/%Y"),
            timezone.now().strftime("%H:%M:%S"),
            "Configuration du " + timezone.now().strftime("%d/%m/%Y à %H:%M"),
        ]
        if path:
            df.to_csv(path, sep=";", header=True, index=False, columns=None)
        else:
            from django.http import HttpResponse

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=config.csv"
            df.to_csv(
                path_or_buf=response, index=False, encoding="utf-8"
            )  # with other applicable parameters
            return response
