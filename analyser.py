from os import listdir, remove , path, makedirs
from typing import Dict, Union, List, Set, Any
from PIL import Image
#from videohash import VideoHash
import hashlib
from tqdm import tqdm
from datetime import datetime
import shutil

class Analyser:
    def __init__(self, 
                image_dir : str,
                ignore_video : bool,
                find_duplicates : bool,
                delete_duplicates : bool,
                create_new_subfolders_by_year : bool,
                move_not_copy : bool,
                output_file : str) -> None:
        self._image_dir: str = image_dir
        self._ignore_video : bool = ignore_video
        self._find_duplicates = find_duplicates
        self._delete_duplicates : bool = delete_duplicates
        self._create_new_subfolders_by_year : bool = create_new_subfolders_by_year
        self._move_not_copy : bool = move_not_copy
        self._output_file : str = output_file

    
    def getMedia(self,parent_dir : str,child_dir : str) -> List[str]:
        _path : str = parent_dir + "/" + child_dir
        images : List[str] = [f for f in listdir(_path) if path.isfile(path.join(_path, f))]
        for dir in set(listdir(_path)).difference(set(images)):
            images += self.getMedia(parent_dir+"/"+child_dir, dir)

        def image_bool(file_name : str) -> bool:
            return (
                str(file_name).endswith("JPEG") or 
                str(file_name).endswith("JPG") or 
                str(file_name).endswith("jepg") or 
                str(file_name).endswith("jpg") or
                str(file_name).endswith("png") )
        
        def video_bool(file_name : str) -> bool:
            return (
                str(file_name).endswith("mp4") or 
                str(file_name).endswith("avi") or 
                str(file_name).endswith("mov") or 
                str(file_name).endswith("wmv") or
                str(file_name).endswith("mkv") or 
                str(file_name).endswith("mpeg"))

        return [child_dir +"/" + f for f in images if 
                image_bool(f) or video_bool(f)]
    
    def _clear_output(self) -> None :
        with open(self._output_file , "w") as file:
            pass

    def _hash_media_without_metadata(self, whole_image_path : str) -> str:
        #Image typing does not work
        im = Image.open(whole_image_path)
        return hashlib.sha512(im.tobytes()).hexdigest()
    
        #hash = VideoHash(path = whole_image_path)

    def _analyse_media(self) -> None:
        hahes : Set = set()
        self._duplicates : List = []
        for image_path in tqdm(self._path_of_images):
            image_hash : str= self._hash_media_without_metadata(self._image_dir +  "/" + image_path)
            if image_hash in hahes: #sets are faster
                with open(self._output_file , "a") as file:
                    file.write(image_path+ "\n")
                    self._duplicates.append(image_path)
            hahes.add(image_hash)
    
    def _delete_all_duplicates(self) -> None:
        for duplicate in tqdm(self._duplicates):
            try: 
                remove(duplicate)
            except FileNotFoundError:
                print(duplicate, " does not exists")
            except PermissionError:
                print("Premission denaied to delete file")
            except Exception as e:
                print(e)

    def _sort_by_year(self) ->None:
        for image_path in tqdm(self._path_of_images):
            creation_time: Any = path.getmtime(self._image_dir + "/" + image_path)
            directory : str = self._image_dir + "/" + str(datetime.utcfromtimestamp(creation_time).year)
            if not path.exists(directory):
                try:
                    makedirs(directory)
                except Exception as e:
                    print(e)
            source : str = self._image_dir + "/" + image_path
            destination : str = directory + "/" + str(image_path.split("/")[-1])
            if (self._move_not_copy):
                shutil.move(source, destination)
            else:
                shutil.copy(source, destination)
    
    def run(self) -> None:
        self._path_of_images : List[str] = self.getMedia(self._image_dir, "")
        self._clear_output()
        if (self._find_duplicates):
            print("finding duplicates...")
            self._analyse_media()
            if (self._delete_duplicates):
                print("deleting duplicates...")
                self._delete_all_duplicates()
        if (self._create_new_subfolders_by_year):
            print("sorting by year...")
            self._sort_by_year()