# https://www.kaggle.com/datasets/balraj98/cvcclinicdb
import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "CVC-ClinicDB"
    images_path = "/mnt/d/datasetninja-raw/cvc-clinic-db/CVC-ClinicDB/PNG/Original"
    masks_path = "/mnt/d/datasetninja-raw/cvc-clinic-db/CVC-ClinicDB/PNG/Ground Truth"
    batch_size = 30
    ds_name = "ds"

    def create_ann(image_path):
        labels = []

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        # img_height = image_np.shape[0]
        # img_wight = image_np.shape[1]

        mask_path = os.path.join(masks_path, get_file_name_with_ext(image_path))

        mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
        img_height = mask_np.shape[0]
        img_wight = mask_np.shape[1]
        obj_mask = mask_np == 255
        curr_bitmap = sly.Bitmap(obj_mask)
        curr_label = sly.Label(curr_bitmap, obj_class)
        labels.append(curr_label)

        frame_number = int(get_file_name(image_path))
        for sequence, (start, end) in enumerate(frame_ranges, start=1):
            if start <= frame_number <= end:
                tag_name = sequence

        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name]
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("polyp", sly.Bitmap)

    tag_names = ["sequence"]
    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    frame_ranges = [
        (1, 25),
        (26, 50),
        (51, 67),
        (68, 78),
        (79, 103),
        (104, 126),
        (127, 151),
        (152, 177),
        (178, 199),
        (200, 205),
        (206, 227),
        (228, 252),
        (253, 277),
        (278, 297),
        (298, 317),
        (318, 342),
        (343, 363),
        (364, 383),
        (384, 408),
        (409, 428),
        (429, 447),
        (448, 466),
        (467, 478),
        (479, 503),
        (504, 528),
        (529, 546),
        (547, 571),
        (572, 591),
        (592, 612),
    ]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_names = os.listdir(images_path)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        images_pathes_batch = [
            os.path.join(images_path, image_name) for image_name in img_names_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
        api.annotation.upload_anns(img_ids, anns_batch)

        progress.iters_done_report(len(img_names_batch))
    return project
