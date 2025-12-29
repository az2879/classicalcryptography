import click
import os

@click.command()
@click.argument('input-file')
@click.option('--output-file', help='Output file name', default='processed_output.txt')
@click.option('--output-dir', help='Directory to save the output file to', default=os.getcwd())

def process_text_file(input_file, output_file, output_dir):
    """
    Reads a text file, processes its content by converting to uppercase,
    and removing non-alphanumeric characters. Outputs the processed content 
    to a new file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        processed_content = ''.join(c.upper() if c.isalnum() or c.isspace() else "" for c in content)
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)
        print(f"Processed file saved to: {output_path}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == '__main__':
    process_text_file()