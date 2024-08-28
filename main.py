import json
from typing import Dict, Union, List, Set, Optional
from analyser import Analyser


config_file : str = "config.json"
output_file : str = "output.txt"





if __name__ == "__main__":

    analyser : Optional[Analyser] = None

    with open(config_file, "r") as file:
        data : Dict[str, Union[bool, str]] = json.load(file)

        analyser = Analyser(
            image_dir=str(data["image_dir"]),
            ignore_video = bool(data["ignore_video"]),
            find_duplicates = bool(data["find_duplicates"]),
            delete_duplicates=bool(data["delete_duplicates"]),
            create_new_subfolders_by_year=bool(data["create_new_subfolders_by_year"]),
            move_not_copy=bool(data["move_not_copy"]),
            output_file = output_file
        )

    analyser.run()

    



    
    


