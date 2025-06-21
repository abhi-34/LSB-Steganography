
# LSB Steganography Tool (Image Text Hider/Extractor)

## Project Description

This project implements a simple Least Significant Bit (LSB) steganography technique to hide secret text messages within digital images and extract them. LSB steganography works by manipulating the least significant bits of the pixel values, which are generally imperceptible to the human eye, thus embedding the secret message without visibly altering the image.

The tool provides an interactive interface for users to choose between two primary operations:
1.  **Hiding Text:** Embed a secret message into a selected cover image (PNG recommended).
2.  **Extracting Text:** Retrieve a hidden message from a stego-image.

The project is developed using Python and designed to be run conveniently within Google Colaboratory.

## Features

* **Hide Text:** Embeds any plain text message into a lossless image format (like PNG).
* **Extract Text:** Recovers the hidden message from a stego-image.
* **User-Friendly Interface:** Interactive command-line prompts within Google Colab for easy operation.
* **Google Colab Integration:** Utilizes `google.colab.files` for easy file upload/download within the Colab environment.
* **Lossless Embedding:** Employs LSB technique, which requires lossless image formats (e.g., PNG, BMP) to preserve hidden data integrity.

## How It Works (LSB Steganography)

The core principle involves modifying the last bit of each color channel (Red, Green, Blue) of selected pixels in the image. Since changing the least significant bit results in a very minor change (a value of 0 or 1), this modification is visually undetectable. A unique binary delimiter is appended to the secret message during embedding, allowing the extraction process to know precisely where the hidden message ends.

## Getting Started

### Prerequisites

* A Google Account (to use Google Colaboratory)
* Web browser

### Running the Notebook

1.  **Open in Google Colab:**
    * Click the "Open in Colab" badge above (if you add one), or go to [Google Colab](https://colab.research.google.com/) and upload the `lsb_steganography.ipynb` (or your notebook's name) file.
2.  **Run Initial Cells:**
    * Execute the first code cell containing the necessary `import` statements (`numpy`, `PIL`, `google.colab.files`).
    * Execute the second code cell containing all the function definitions (`text_to_binary`, `binary_to_text`, `hide_text`, `extract_text`).
3.  **Start Interactive Tool:**
    * Execute the final code cell that contains the `while True:` loop for the interactive menu.
    * Follow the on-screen prompts:
        * Choose '1' to hide text, '2' to extract, or '3' to exit.
        * When prompted, upload your cover image or stego-image using the provided file uploader. **Ensure images are in PNG format.**
        * Enter your secret message or the desired output filename.

## Sample Files

For quick testing and demonstration, this repository includes:
* `sample_images/cover_image.png`: A small PNG image that can be used as a cover image for hiding messages.
* `sample_images/stego_image.png`: A sample stego-image (generated from `cover_image.png` with a hidden message) that can be used for extraction testing.

**How to use them:** When prompted to upload an image in the Colab notebook, navigate to the `sample_images/` folder on your local machine to select these files.



## Important Notes

* **Image Format:** For successful steganography and retrieval, **always use lossless image formats like PNG (.png) or BMP (.bmp)**. Saving or converting the stego-image to a lossy format like JPEG (.jpg) will likely destroy the hidden data.
* **Capacity:** The amount of text you can hide depends on the size (dimensions) of your cover image. Larger images can hold more data. The tool includes a check to prevent embedding messages that are too large.
* **Security:** This LSB steganography implementation is primarily for demonstration and educational purposes. It is **not cryptographically secure** and is easily detectable by steganalysis tools. For real-world secure communication, stronger cryptographic methods and more advanced steganographic techniques would be required.

