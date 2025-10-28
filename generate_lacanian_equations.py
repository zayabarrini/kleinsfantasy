import matplotlib.pyplot as plt
import os
import subprocess
import shutil


# Check if LaTeX is available
def check_latex_installation():
    """Check if LaTeX is properly installed"""
    if shutil.which("latex") is None:
        print("❌ LaTeX is not installed or not in PATH")
        print("Please install LaTeX:")
        print(
            "Ubuntu/Debian: sudo apt-get install texlive-latex-extra texlive-fonts-recommended"
        )
        print("Mac: Install MacTeX from https://www.tug.org/mactex/")
        print("Windows: Install MiKTeX from https://miktex.org/")
        return False
    return True


# Create output directory
os.makedirs("lacanian_equations", exist_ok=True)


def save_equation(equation_text, filename, fontsize=16):
    """Save a single equation as SVG"""
    try:
        plt.figure(figsize=(12, 3))
        plt.axis("off")

        # Use raw strings and proper LaTeX formatting
        plt.text(
            0.5,
            0.5,
            equation_text,
            fontsize=fontsize,
            ha="center",
            va="center",
            usetex=True,
        )

        plt.savefig(
            f"lacanian_equations/{filename}.svg",
            format="svg",
            bbox_inches="tight",
            transparent=True,
            dpi=300,
        )
        plt.close()
        print(f"✅ Generated: {filename}.svg")
        return True
    except Exception as e:
        print(f"❌ Failed to generate {filename}.svg: {str(e)}")
        plt.close()
        return False


# Configure matplotlib for LaTeX
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern"],
        "font.size": 16,
        "text.latex.preamble": r"""
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{amsfonts}
        \usepackage{mathrsfs}
        \usepackage{wasysym}
    """,
    }
)

if not check_latex_installation():
    print("Please install LaTeX first and then run the script again.")
    exit(1)

print("Generating Lacanian equations...")

# Your original equations (fixed escape sequences)
equations_to_generate = [
    # Original equations
    (
        r"$\text{Abuse}_{\phi} = (\text{A"
        "s jouissance acting on } \mathfrak{H}) \Rightarrow a$",
        "abuse_definition",
    ),
    (r"$\langle \$ \; \Diamond \; a(\mathfrak{H}) \rangle$", "fantasy_of_abuse"),
    (
        r"$\forall x \in (\text{Subjects}), \; x = f(\mathfrak{H}, A, S, R)$",
        "universal_structure",
    ),
    (
        r"$\mathfrak{H} \xrightarrow{S} (\text{Trauma, Guilt, Art, Gender, Desire})$",
        "resymbolization",
    ),
    (
        r"$\subset K(\$) = (S \cup I) / \Delta \;+\; R(\mathfrak{H})$",
        "klein_bottle_subject",
    ),
    # Additional Lacanian equations
    (r"$\$ \to a$", "subject_to_object"),
    (r"$S(/A) \to \mathscr{J}$", "signifier_of_lack"),
    (r"$R \to S \to I$", "RSI_borromean"),
    (r"$\mathscr{J}_{\phi} = \Phi \cdot S(/A)$", "phallic_jouissance"),
    (r"$\mathscr{J}_O = \infty \cdot \varnothing$", "other_jouissance"),
    (r"$\$ = \frac{\text{Signifier}}{\text{Signifier}}$", "barred_subject"),
    (r"$a = f(\mathscr{J}, \varnothing)$", "object_cause"),
    (r"$s(O) \to \$ \to d$", "graph_of_desire"),
    (r"$\triangle \text{Che vuoi?} \to a$", "che_vuoi"),
]

# Four Discourse formulas
discourses = [
    (r"$\frac{S_1}{S_2} \to \frac{\$}{a}$", "discourse_master"),
    (r"$\frac{S_2}{a} \to \frac{S_1}{\$}$", "discourse_university"),
    (r"$\frac{\$}{S_1} \to \frac{a}{S_2}$", "discourse_hysteric"),
    (r"$\frac{a}{\$} \to \frac{S_2}{S_1}$", "discourse_analyst"),
]

# L-Scheme equations
l_schemes = [
    (
        r"$S \longrightarrow a \longrightarrow a" " \longrightarrow S" "$",
        "l_scheme_basic",
    ),
    (
        r"$\text{Ego} \leftrightarrow \text{Other} \ \bot \ \text{Subject} \leftrightarrow \text{Unconscious}$",
        "l_scheme_full",
    ),
]

# Combine all equations
all_equations = equations_to_generate + discourses + l_schemes

# Generate equations one by one
successful = 0
failed = []

for eq_text, filename in all_equations:
    if save_equation(eq_text, filename):
        successful += 1
    else:
        failed.append(filename)

print(f"\n📊 Generation Summary:")
print(f"✅ Successful: {successful}")
print(f"❌ Failed: {len(failed)}")
if failed:
    print(f"Failed equations: {failed}")

# Create a simple HTML preview
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Lacanian Equations Preview</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .equation { margin: 30px 0; padding: 20px; border-bottom: 1px solid #ccc; }
        img { max-width: 100%; height: auto; background: white; padding: 10px; }
    </style>
</head>
<body>
    <h1>Lacanian Equations Preview</h1>
"""

for _, filename in all_equations:
    if filename not in failed:
        html_content += f"""
    <div class="equation">
        <h3>{filename}</h3>
        <img src="{filename}.svg" alt="{filename}">
    </div>
        """

html_content += """
</body>
</html>
"""

with open("lacanian_equations/preview.html", "w") as f:
    f.write(html_content)

print(f"\n📁 All files saved in 'lacanian_equations' folder")
print("🌐 Open 'lacanian_equations/preview.html' to view all equations")
print("\n🎨 To use in Canva:")
print("1. Go to Canva → Uploads → Upload media")
print("2. Select all SVG files from the 'lacanian_equations' folder")
print("3. Drag and drop into your design")
