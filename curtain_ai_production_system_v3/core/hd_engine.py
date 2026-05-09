from pathlib import Path
import cv2


def enhance_hd(image_path: Path, output_path: Path) -> Path:
    img = cv2.imread(str(image_path))
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
    sharp = cv2.addWeighted(denoised, 1.2, cv2.GaussianBlur(denoised, (0, 0), 2), -0.2, 0)
    cv2.imwrite(str(output_path), sharp)
    return output_path
