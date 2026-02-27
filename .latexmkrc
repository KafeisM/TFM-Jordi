# Configure latexmk so all generated artifacts land inside build/
$aux_dir = 'build';
$out_dir = 'build';

# Ensure the directory exists before compilation starts
mkdir 'build', 0755 unless -d 'build';
