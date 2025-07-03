import os
import subprocess

def convert_excels_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".xlsx") and not file.startswith("~$"):
            input_file = os.path.join(input_folder, file)
            try:
                subprocess.run([
                    "soffice",
                    "--headless",
                    "--convert-to", "pdf",
                    "--outdir", output_folder,
                    input_file
                ], check=True)
                print(f"✔ Converted: {file}")
            except subprocess.CalledProcessError as e:
                print(f"✘ Failed to convert {file}: {e}")

if __name__ == "__main__":
    input_folder = "pdfs_reformatted_a4"
    output_folder = "pdfs_op"
    convert_excels_to_pdf(input_folder, output_folder)
