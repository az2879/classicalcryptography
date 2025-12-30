import os
import click

from utils.text_processing import clean_text
from ciphers.caesar import encrypt, decrypt, brute_force_attack, frequency_attack, ranked_candidates


@click.command()
@click.argument("input-file")
@click.option("--output-file", default="output.txt", help="Name of output file")
@click.option("--output-dir", default=os.getcwd(), help="Directory to save output file")
@click.option("--cipher", default="caesar", help="Cipher to use (default: caesar)")
@click.option("--shift", default=1, help="Shift value for Caesar cipher", type=int)
@click.option(
    "--attack",
    is_flag=True,
    help="Performs brute-force and frequency-analysis attacks",
)
def demo(input_file, output_file, output_dir, cipher, shift, attack):
    """
    Encrypt text from input file and optionally perform cryptanalysis attacks.
    """

    # -----------------------------
    # Read and clean input text
    # -----------------------------
    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read().strip()
    plaintext = clean_text(raw_text)

    # -----------------------------
    # Encryption
    # -----------------------------
    if cipher.lower() != "caesar":
        raise click.ClickException("Only Caesar cipher is currently supported.")

    ciphertext = encrypt(plaintext, shift)

    # -----------------------------
    # Prepare output
    # -----------------------------
    output_lines = []
    output_lines.append("=== ENCRYPTED MESSAGE ===")
    output_lines.append(ciphertext)
    output_lines.append("")

    # -----------------------------
    # Attacks
    # -----------------------------
    if attack:
        output_lines.append("=== BRUTE FORCE ATTACK RESULTS ===")
        for shift, guess in brute_force_attack(ciphertext):
            output_lines.append(f"Shift {shift:2d}: {guess}")
            output_lines.append("")

        output_lines.append("=== TOP 5 FREQUENCY ANALYSIS GUESSES ===")

        top_guesses = ranked_candidates(ciphertext, top_n=5)
        for shift_guess, text_guess, score in top_guesses:
            output_lines.append(
                f"Shift {shift_guess:2d} | Score {score:8.2f} | {text_guess}"
            )

    # -----------------------------
    # Write output file
    # -----------------------------
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    click.echo(f"Output saved to: {output_path}")


if __name__ == "__main__":
    demo()