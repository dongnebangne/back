import os
import torch
from django.conf import settings
import numpy as np
from .sam_segment import predict_masks_with_sam
from .lama_inpaint import inpaint_img_with_lama
from .stable_diffusion_inpaint import fill_img_with_sd
#from .utils import dilate_mask, save_array_to_img, show_mask, show_points
from .utils import dilate_mask, save_array_to_img, show_mask, show_points, load_img_to_array
from pathlib import Path
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

def generate_masks_with_sam(img, point_coords, point_labels, dilate_kernel_size, sam_model_type, sam_ckpt, device="cuda"):
    # SAM을 통해 마스크 생성
    masks, _, _ = predict_masks_with_sam(
        img,
        [point_coords],
        point_labels,
        model_type=sam_model_type,
        ckpt_p=sam_ckpt,
        device=device,
    )
    masks = masks.astype(np.uint8) * 255

    # 마스크 확장 (선택 사항)
    if dilate_kernel_size is not None:
        masks = [dilate_mask(mask, dilate_kernel_size) for mask in masks]

    # 생성된 마스크 시각화 및 저장
    output_dir = Path('media/results')
    output_dir.mkdir(parents=True, exist_ok=True)

    mask_file_paths = []
    for idx, mask in enumerate(masks):
        mask_path = output_dir / f"mask_{idx}.png"
        mask_image_path = output_dir / f"masked_image_{idx}.png"
        save_array_to_img(mask, mask_path)

        # 마스크가 적용된 이미지를 시각적으로 저장 (포인트 표시 포함)
        dpi = plt.rcParams['figure.dpi']
        height, width = img.shape[:2]
        plt.figure(figsize=(width/dpi/0.77, height/dpi/0.77))
        plt.imshow(img)
        plt.axis('off')
        show_points(plt.gca(), [point_coords], point_labels, size=(width*0.04)**2)
        show_mask(plt.gca(), mask, random_color=False)
        plt.savefig(mask_image_path, bbox_inches='tight', pad_inches=0)
        plt.close()

        mask_file_paths.append((mask_path, mask_image_path))

    return mask_file_paths


# def inpaint_image_with_selected_mask(img, selected_mask_idx, text_prompt, lama_config, lama_ckpt, device="cuda"):
#     try:
#         output_dir = Path('media/results')
#         mask_path = output_dir / f"mask_{selected_mask_idx}.png"
#         mask = load_img_to_array(mask_path)
#
#         if not text_prompt:
#             img_inpainted = inpaint_img_with_lama(img, mask, lama_config, lama_ckpt, device=device)
#         else:
#             img_inpainted = fill_img_with_sd(img, mask, text_prompt, device=device)
#
#         inpainted_image_path = output_dir / 'inpainted_image.png'
#         save_array_to_img(img_inpainted, inpainted_image_path)
#
#         return inpainted_image_path
#     except Exception as e:
#         logger.error(f"Error during image inpainting: {e}")
#         raise

def inpaint_image_with_selected_mask(img, selected_mask_idx, text_prompt, lama_config, lama_ckpt, device="cuda"):
    try:
        output_dir = Path('media/results')
        mask_path = output_dir / f"mask_{selected_mask_idx}.png"
        mask = load_img_to_array(mask_path)

        # Stable Diffusion을 사용하여 이미지 처리
        img_inpainted = fill_img_with_sd(img, mask, text_prompt, device=device)

        inpainted_image_path = output_dir / 'inpainted_image.png'
        save_array_to_img(img_inpainted, inpainted_image_path)

        return inpainted_image_path
    except Exception as e:
        logger.error(f"Error during image inpainting with Stable Diffusion: {e}")
        raise

def remove_object_with_lama(img, selected_mask_idx, lama_config, lama_ckpt, device="cuda"):
    try:
        output_dir = Path('media/results')
        mask_path = output_dir / f"mask_{selected_mask_idx}.png"
        mask = load_img_to_array(mask_path)

        # LAMA를 사용하여 개체 지우기
        img_inpainted = inpaint_img_with_lama(img, mask, lama_config, lama_ckpt, device=device)

        # 결과 저장
        removed_image_path = output_dir / 'removed_image.png'
        save_array_to_img(img_inpainted, removed_image_path)

        return removed_image_path
    except Exception as e:
        logger.error(f"Error during object removal with Lama: {e}")
        raise