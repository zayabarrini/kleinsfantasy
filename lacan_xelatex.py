import matplotlib.pyplot as plt
import os
import subprocess
import shutil


# Check if XeLaTeX is available
def check_xelatex_installation():
    """Check if XeLaTeX is properly installed"""
    if shutil.which("xelatex") is None:
        print("❌ XeLaTeX is not installed or not in PATH")
        print("Please install XeLaTeX:")
        print("Ubuntu/Debian: sudo apt-get install texlive-xetex")
        print("Mac: Install MacTeX from https://www.tug.org/mactex/")
        print("Windows: Install MiKTeX from https://miktex.org/")
        return False
    return True


# Create output directory
os.makedirs("lacanian_equations", exist_ok=True)


def save_equation_xelatex(equation_text, filename, fontsize=16):
    """Save a single equation as SVG using XeLaTeX"""
    try:
        # Create a temporary LaTeX file
        latex_content = (
            r"""\documentclass[preview]{standalone}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{mathrsfs}
\usepackage{wasysym}
\usepackage{xunicode-symbols}
\usepackage{fontspec}
\setmainfont{DejaVu Serif}

% Define custom commands for the symbols you need
\newcommand{\textstrokea}{Ⱥ}  % LATIN CAPITAL LETTER A WITH STROKE
\newcommand{\strokegamma}{Ɣ}  % LATIN CAPITAL LETTER GAMMA

\begin{document}
\large
"""
            + equation_text
            + r"""
\end{document}"""
        )

        # Write temporary files
        with open("temp_equation.tex", "w") as f:
            f.write(latex_content)

        # Compile with XeLaTeX to PDF
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "temp_equation.tex"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        if result.returncode != 0:
            print(f"XeLaTeX compilation failed for {filename}:")
            print(result.stderr)
            return False

        # Convert PDF to SVG (you might need to install pdf2svg)
        # Alternatively, use another conversion method
        svg_result = subprocess.run(
            ["pdf2svg", "temp_equation.pdf", f"lacanian_equations/{filename}.svg"],
            capture_output=True,
            text=True,
        )

        if svg_result.returncode != 0:
            # Fallback: use matplotlib with different approach
            return save_equation_fallback(equation_text, filename, fontsize)

        # Clean up temporary files
        for ext in [".tex", ".pdf", ".aux", ".log"]:
            if os.path.exists(f"temp_equation{ext}"):
                os.remove(f"temp_equation{ext}")

        print(f"✅ Generated: {filename}.svg")
        return True

    except Exception as e:
        print(f"❌ Failed to generate {filename}.svg: {str(e)}")
        return save_equation_fallback(equation_text, filename, fontsize)


def save_equation_fallback(equation_text, filename, fontsize=16):
    """Fallback method using matplotlib with simplified symbols"""
    try:
        plt.figure(figsize=(12, 3))
        plt.axis("off")

        # Replace problematic symbols with alternatives
        safe_equation = equation_text.replace(r"\textstrokea", r"A\!\!/")
        safe_equation = safe_equation.replace(r"\strokegamma", r"\Gamma")
        safe_equation = safe_equation.replace(r"\m{G}", r"G")

        plt.text(
            0.5,
            0.5,
            safe_equation,
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
        print(f"✅ Generated (fallback): {filename}.svg")
        return True
    except Exception as e:
        print(f"❌ Failed to generate {filename}.svg even with fallback: {str(e)}")
        plt.close()
        return False


# Configure matplotlib for better LaTeX support
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
        
        % Define fallback commands
        \newcommand{\textstrokea}{A\!\!/}
        \newcommand{\strokegamma}{\Gamma}
    """,
    }
)

if not check_xelatex_installation():
    print("Please install XeLaTeX first and then run the script again.")
    exit(1)

print("Generating Lacanian equations...")

# Updated equations with multiple approaches
equations_to_generate = [
    # Original equations
    (
        r"$\text{Abuse}_{\phi} = (\text{As jouissance acting on } \mathfrak{H}) \Rightarrow a$",
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
    (r"$\mathrm{\AA}: \mathrm{Otro\ en\ falta\ o\ barrado}$", "A_barred"),
    (r"$-\phi: \mathrm{Castration\ Anxiety}$", "castration_anxiety"),
    (r"$\mathfrak{H}: \mathrm{Hilflosigkeit}$", "Hilflosigkeit_Abandonment"),
    (
        r"$\subset K: \mathrm{Sujeto\ como\ botella\ de\ Klein}$",
        "klein_bottle_subject_symbol",
    ),
    (r"$\$ \to a$", "subject_to_object"),
    # Using custom commands
    (r"$S(\textstrokea) \to \mathcal{J}$", "signifier_of_lack"),
    (r"$R \to S \to I$", "RSI_borromean"),
    (r"$\mathcal{J}_{\phi} = \Phi \cdot S(\textstrokea)$", "phallic_jouissance"),
    (r"$\mathcal{J}_O = \infty \cdot \varnothing$", "other_jouissance"),
    (r"$\$ = \frac{\text{Signifier}}{\text{Signifier}}$", "barred_subject"),
    (r"$a = f(\mathcal{J}, \varnothing)$", "object_cause"),
    (r"$s(O) \to \$ \to d$", "graph_of_desire"),
    (r"$\triangle \text{Che vuoi?} \to a$", "che_vuoi"),
    # Gamma symbol variations
    (r"$\strokegamma: \mathrm{Jouissance}$", "will_to_enjoy"),
    (r"$\Gamma: \mathrm{Jouissance}$", "will_to_enjoy_gamma"),
    (r"$(\$ \ \diamond \ D): \mathrm{Pulsion}$", "drive_structure"),
    (r"$(\$ \ \diamond \ a): \mathrm{Fantasma}$", "fantasy_structure"),
    # Paternal metaphor
    (
        r"$\mathrm{Nombre\text{-}del\text{-}padre} \times \mathrm{Deseo\ de\ la\ madre} \to \mathrm{Nombre\text{-}del\text{-}padre} (A)$",
        "paternal_metaphor",
    ),
    # Desire of the mother structure
    (
        r"$\mathrm{Deseo\ de\ la\ madre} \longrightarrow \mathrm{significado\ al\ sujeto} \longrightarrow \mathrm{Falo}$",
        "desire_mother_structure",
    ),
    # Conjunctive metaphor
    (
        r"$\mathrm{UNNO\text{-}del\text{-}A} \times \mathrm{Deseo\ de\ uno} \to \mathrm{unno\text{-}del\text{-}\AA}$",
        "conjunctive_metaphor",
    ),
    # Logical impossibility
    (r"$\sqrt{-1}: \mathrm{Sujeto\ como\ imposible\ logico}$", "subject_impossible"),
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
        r"$S \longrightarrow a \longrightarrow a' \longrightarrow S'$",
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

print("🔧 Installing pdf2svg if needed...")
# Check if pdf2svg is installed
if shutil.which("pdf2svg") is None:
    print("📦 pdf2svg not found. Please install it:")
    print("Ubuntu/Debian: sudo apt-get install pdf2svg")
    print("Using fallback method...")
    use_fallback = True
else:
    use_fallback = False

for eq_text, filename in all_equations:
    if use_fallback:
        success = save_equation_fallback(eq_text, filename)
    else:
        success = save_equation_xelatex(eq_text, filename)

    if success:
        successful += 1
    else:
        failed.append(filename)

print(f"\n📊 Generation Summary:")
print(f"✅ Successful: {successful}")
print(f"❌ Failed: {len(failed)}")
if failed:
    print(f"Failed equations: {failed}")

# Create HTML preview
html_content = (
    """<!DOCTYPE html>
<html>
<head>
    <title>Lacanian Equations</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .equation { margin: 25px 0; padding: 25px; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        img { max-width: 100%; height: auto; display: block; margin: 10px auto; }
        h1 { color: #2c3e50; text-align: center; }
        h3 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
        .success { color: #27ae60; }
        .error { color: #e74c3c; }
    </style>
</head>
<body>
    <h1>🧠 Lacanian Equations</h1>
    <div class="success">✅ Successful: """
    + str(successful)
    + """</div>
    <div class="error">❌ Failed: """
    + str(len(failed))
    + """</div>
"""
)

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

# Installation instructions
print("\n📦 For best results, install:")
print("   sudo apt-get install texlive-xetex texlive-fonts-recommended pdf2svg")
print("\n🎨 To use in Canva:")
print("1. Go to Canva → Uploads → Upload media")
print("2. Select all SVG files from the 'lacanian_equations' folder")
print("3. Drag and drop into your design")
