# Import Libraries
import os
import sys
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet


def get_size_format(b, factor=1024, suffix="B"):
    # Scale bytes to its proper byte format
    # 1253656 => 1.20MB
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_file(input_file: str, output_file: str):
    # Initialize PDFNet Key
    PDFNet.Initialize("demo:1719395537700:7fb0be6c030000000023d9cbd1534551b9cb85a094666bdfdbfa540941")

    # Compress PDF file
    if not output_file:
        output_file = input_file 
    initial_size = os.path.getsize(input_file)
    
    try:
        # Initialize the library
        PDFNet.Initialize()
        doc = PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and compressing data streams
        Optimizer.Optimize(doc)
        # Save and close the document
        doc.Save(output_file, SDFDoc.e_linearized)
        doc.Close()
    except Exception as e:
        print("Error compress_file=", e)
        doc.Close()
        return False
    
    # Calculate the ratio of the compression
    compressed_size = os.path.getsize(output_file)
    ratio = 1 - (compressed_size / initial_size)

    # Printing Summary
    summary = {
        "Input File": input_file, "Initial Size": get_size_format(initial_size),
        "Output File": output_file, f"Compressed Size": get_size_format(compressed_size),
        "Compression Ratio": "{0:.3%}.".format(ratio)
    }
    print("-------------------------------------------------------------------")
    print("Summary")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("-------------------------------------------------------------------")
    return True


if __name__ == "__main__":
    # Parsing command line arguments entered by user
    # python pdf_compressor.py input_file.pdf output_file.pdf
    # The last argument is optional. If there is none, the code will automatically output the compressed file as input_file_compressed.pdf 
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        input_file_split = input_file.rsplit('.', 1)
        output_file = input_file_split[0] + "_compressed." + input_file_split[1]
    compress_file(input_file, output_file)


# Notes for future update: If there is no argument after "input_file.pdf", create "output_file.pdf" automatically
# Make output_file.pdf == input_file_compressed.pdf essentially
# Done :3

# It would be cool if the whole system was automated and the code looped through every pdf file and added compression versions separately
# Only pdf files though... Other types can be compressed normally in winRAR
